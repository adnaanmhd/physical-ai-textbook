#!/usr/bin/env python3
"""Helpers for the scouting stage.

Usage:
  python3 scripts/research_tool.py summary NN [--expect N]   # sources per section vs. the exit criteria
  python3 scripts/research_tool.py sources NN SS             # every source serving one section
  python3 scripts/research_tool.py merge-bans NN             # fold BAN lines into scripts/banned_domains.txt
  python3 scripts/research_tool.py pending NN                # evidence still needed (exit 1 if any)

Scouts write research/chNN/sSS-sources.json (a JSON list) and research/chNN/sSS-rejected.md (one
line per rejected candidate, with the reason). A rejection line of the form

  BAN: example.com — reason

proposes banning the whole domain. Scouts never edit scripts/banned_domains.txt themselves; the
main session runs merge-bans once the scouts have finished, and logs new bans in PROGRESS.md for
the human to review. Platforms that host both good and bad material (video sites, social networks,
blog platforms), scholarly infrastructure, standards bodies, the labs the book covers and the
named trade and general press can never be banned this way: reject the individual page instead.

summary exits 1 if a section misses the exit criteria (at least 5 usable sources, at least 2 of
them priority 1) or a sources file is malformed.

pending lists the evidence a chapter still needs before revision: <!--TODO--> markers in the text,
unticked "- [ ]" requests in checks/chNN-requests.md, and entries in research/chNN/extra-sources.json
(the skeptic's counter-evidence) that a researcher has not yet marked "done". Exit 1 if any.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from common import atomic_write, banned_domains, chapter_file, file_lock, is_banned, norm_ch, root_from

MIN_SOURCES, MIN_P1 = 5, 2
BAN_RE = re.compile(r"^\s*[-*]?\s*BAN:\s*(\S+)\s*(?:[—–:-]+\s*)?(.*)$")
DOMAIN_RE = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$")
PROTECTED = {
    # platforms and scholarly infrastructure
    "arxiv.org", "doi.org", "github.com", "github.io", "huggingface.co", "openreview.net", "ieee.org",
    "acm.org", "springer.com", "nature.com", "science.org", "sciencedirect.com", "wiley.com",
    "roboticsproceedings.org", "mlr.press", "neurips.cc", "thecvf.com", "aaai.org",
    "youtube.com", "youtu.be", "vimeo.com", "x.com", "twitter.com", "linkedin.com", "medium.com",
    "substack.com", "blogspot.com", "wordpress.com", "google.com",
    # standards bodies and regulators
    "iso.org", "iec.ch", "ansi.org", "ul.com", "automate.org", "nist.gov", "osha.gov", "europa.eu",
    "gov.uk", "gov",
    # labs and companies the book covers (docs/BRIEF.md)
    "figure.ai", "neura-robotics.com", "dyna.co", "skild.ai", "physicalintelligence.company",
    "deepmind.google", "deepmind.com", "nvidia.com", "tesla.com", "1x.tech", "agilityrobotics.com",
    "bostondynamics.com", "tri.global", "apptronik.com", "generalistai.com", "openai.com", "meta.com",
    "unitree.com", "agibot.com", "galbot.com", "ubtrobot.com",
    # named trade and general press (docs/SOURCES.md)
    "therobotreport.com", "reuters.com", "bloomberg.com", "ft.com", "techcrunch.com", "wired.com",
    "technologyreview.com",
}
SOURCE_FIELDS = ["key", "title", "url", "published", "source_type", "evidence", "priority", "access"]


def chapter_arg(value) -> str:
    nn = norm_ch(value)
    if not nn.isdigit():
        sys.exit(f"'{value}' is not a chapter number")
    return nn


def clean_domain(raw: str) -> str:
    d = raw.strip().lower()
    d = re.sub(r"^[a-z]+://", "", d).split("/")[0].split(":")[0]
    if d.startswith("www."):
        d = d[4:]
    return d.strip(".")


def protected(domain: str) -> bool:
    return any(domain == p or domain.endswith("." + p) for p in PROTECTED)


def cmd_merge_bans(root, args):
    nn = chapter_arg(args.chapter)
    folder = root / "research" / f"ch{nn}"
    proposals = []
    for path in sorted(folder.glob("*rejected.md")):
        for ln in path.read_text(encoding="utf-8").splitlines():
            m = BAN_RE.match(ln)
            if m:
                proposals.append((clean_domain(m.group(1)), (m.group(2) or "no reason given").strip(),
                                  path.name.split("-")[0]))
    target = root / "scripts" / "banned_domains.txt"
    added, refused, known = [], [], []
    with file_lock(target):
        current = set(banned_domains(root))
        text = target.read_text(encoding="utf-8") if target.exists() else ""
        if text and not text.endswith("\n"):
            text += "\n"
        for domain, reason, sec in proposals:
            if not DOMAIN_RE.match(domain):
                refused.append(f"{domain} (not a domain name)")
            elif protected(domain):
                refused.append(f"{domain} (platform or scholarly domain: reject single pages instead)")
            elif domain in current:
                known.append(domain)
            else:
                text += f"# ch{nn} {sec}: {reason[:120]}\n{domain}\n"
                current.add(domain)
                added.append(domain)
        if added:
            atomic_write(target, text)
    print(f"ch{nn}: {len(proposals)} BAN proposals · added {len(added)}: {', '.join(added) or '-'}")
    if added:
        print("Log the new bans in PROGRESS.md so the human can review them.")
    if known:
        print(f"already banned: {', '.join(sorted(set(known)))}")
    for r in refused:
        print(f"refused: {r}")


def load_sources(path):
    """Return (list, errors) for one sSS-sources.json file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], [f"{path.name}: invalid JSON ({exc.msg})"]
    if not isinstance(data, list):
        return [], [f"{path.name}: must be a JSON list"]
    errors = []
    for i, s in enumerate(data, start=1):
        if not isinstance(s, dict):
            errors.append(f"{path.name} item {i}: not an object")
            continue
        missing = [f for f in SOURCE_FIELDS if s.get(f) in (None, "")]
        if missing:
            errors.append(f"{path.name} item {i} ({s.get('key', '?')}): missing {', '.join(missing)}")
    return [s for s in data if isinstance(s, dict)], errors


def section_sources(root, nn, sec):
    """Every source serving section `sec`: its own file plus sources cross-listed from other sections."""
    out = {}
    for path in sorted((root / "research" / f"ch{nn}").glob("s[0-9][0-9]-sources.json")):
        own = path.name[1:3]
        items, _errs = load_sources(path)
        for s in items:
            serves = {own, *[str(x).zfill(2) for x in s.get("sections", []) or []]}
            if sec in serves:
                out.setdefault(s.get("url") or s.get("key"), dict(s, listed_in=f"s{own}"))
    return list(out.values())


def cmd_sources(root, args):
    nn = chapter_arg(args.chapter)
    sec = str(args.section).lstrip("sS").zfill(2)
    banned = banned_domains(root)
    items = [s for s in section_sources(root, nn, sec) if not is_banned(s.get("url", ""), banned)]
    items.sort(key=lambda s: (str(s.get("priority", 9)), str(s.get("key"))))
    print(json.dumps(items, indent=1, ensure_ascii=False))
    print(f"{len(items)} sources for ch{nn} s{sec}", file=sys.stderr)


def cmd_summary(root, args):
    nn = chapter_arg(args.chapter)
    folder = root / "research" / f"ch{nn}"
    files = sorted(folder.glob("s[0-9][0-9]-sources.json"))
    banned = banned_domains(root)
    by_sec, errors = {}, []
    for path in files:
        sec = path.name[1:3]
        items, errs = load_sources(path)
        errors += errs
        for s in items:
            for target in {sec, *[str(x).zfill(2) for x in s.get("sections", []) or []]}:
                by_sec.setdefault(target, {})[s.get("url") or s.get("key")] = s
    expected = [f"{i:02d}" for i in range(1, args.expect + 1)] if args.expect else sorted(by_sec)
    thin = 0
    print(f"ch{nn} scouting summary (exit: at least {MIN_SOURCES} usable sources, {MIN_P1} at priority 1)")
    for sec in expected:
        items = list(by_sec.get(sec, {}).values())
        usable = [s for s in items if not is_banned(s.get("url", ""), banned)]
        p1 = sum(1 for s in usable if str(s.get("priority")) == "1")
        dates = sorted(str(s.get("published", "")) for s in usable if s.get("published"))
        flag = "OK" if len(usable) >= MIN_SOURCES and p1 >= MIN_P1 else ("MISSING" if not items else "THIN")
        thin += flag != "OK"
        newest = dates[-1] if dates else "-"
        dropped = len(items) - len(usable)
        extra = f" · {dropped} on banned domains" if dropped else ""
        print(f"  s{sec}  {len(usable):>2} sources · {p1} priority-1 · newest {newest} · {flag}{extra}")
    bans = sum(1 for p in folder.glob("*rejected.md")
               for ln in p.read_text(encoding="utf-8").splitlines() if BAN_RE.match(ln))
    if bans:
        print(f"BAN proposals in rejection files: {bans} (run merge-bans {nn})")
    for e in errors:
        print(f"ERROR {e}")
    sys.exit(1 if thin or errors else 0)


def cmd_pending(root, args):
    nn = chapter_arg(args.chapter)
    items = []
    path = chapter_file(root, nn)
    if path and path.exists():
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"<!--\s*TODO:?\s*(.*?)-->", text, re.S):
            line = text.count("\n", 0, m.start()) + 1
            items.append(f"TODO (line {line}): {' '.join(m.group(1).split())[:100]}")
    req = root / "checks" / f"ch{nn}-requests.md"
    if req.exists():
        for ln in req.read_text(encoding="utf-8").splitlines():
            if re.match(r"^\s*[-*]\s*\[ \]", ln):
                items.append("request: " + re.sub(r"^\s*[-*]\s*\[ \]\s*", "", ln)[:100])
    extra = root / "research" / f"ch{nn}" / "extra-sources.json"
    if extra.exists():
        try:
            data = json.loads(extra.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            items.append(f"research/ch{nn}/extra-sources.json is invalid JSON ({exc.msg})")
            data = []
        for src in data if isinstance(data, list) else []:
            if isinstance(src, dict) and not src.get("done"):
                items.append(f"counter-evidence: {src.get('key') or src.get('url')} "
                             f"(for: {str(src.get('for', ''))[:60]})")
    for it in items:
        print(it)
    print(f"{len(items)} pending evidence items for ch{nn}")
    sys.exit(1 if items else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="project root (default: repo root)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("summary"); s.add_argument("chapter"); s.add_argument("--expect", type=int, default=0)
    s = sub.add_parser("sources"); s.add_argument("chapter"); s.add_argument("section")
    s = sub.add_parser("merge-bans"); s.add_argument("chapter")
    s = sub.add_parser("pending"); s.add_argument("chapter")
    for sp in sub.choices.values():
        sp.add_argument("--root", default=argparse.SUPPRESS)
    args = ap.parse_args()
    root = root_from(args.root)
    {"summary": cmd_summary, "sources": cmd_sources, "merge-bans": cmd_merge_bans,
     "pending": cmd_pending}[args.cmd](root, args)


if __name__ == "__main__":
    main()
