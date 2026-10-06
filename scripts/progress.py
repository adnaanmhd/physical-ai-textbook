#!/usr/bin/env python3
"""Read and update chapter status in state/progress.json.

Usage:
  python3 scripts/progress.py show [NN]
  python3 scripts/progress.py set NN STATUS [--note "text"]
  python3 scripts/progress.py part PID            # chapter ids in a Part, space-separated
  python3 scripts/progress.py next [--part PID]   # next chapter that is not done, in production order
  python3 scripts/progress.py known NN [--out checks/chNN-known.md]   # what the reader knows before NN
  python3 scripts/progress.py current-as-of YYYY-MM-DD

next: the pilot comes first; the chapter named book.last (ch01, which summarises the whole book)
comes after every other chapter.
known: the Key takeaways (state/takeaways.md) of finished chapters numbered below NN, plus the
titles of earlier chapters not yet written. Later chapters never count, even when finished.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import io
import re
import sys
from pathlib import Path

from common import (PRODUCTION_ORDER, STATUSES, atomic_write, file_lock, find_chapter, iter_chapters,
                    load_progress, norm_ch, root_from, save_progress)


def cmd_show(root, args):
    progress = load_progress(root)
    if args.chapter:
        part, ch = find_chapter(progress, args.chapter)
        if not ch:
            sys.exit(f"Unknown chapter {args.chapter}")
        print(f"ch{ch['id']} · {ch['title']}")
        print(f"  part: {part['id']} ({part['title']})")
        print(f"  status: {ch['status']}")
        if ch["status"] == "blocked" and ch.get("blocked_from"):
            print(f"  resume from: {ch['blocked_from']} (the last completed stage; set it back to this to resume)")
        print(f"  lifecycle: {'yes' if ch.get('lifecycle') else 'no'}")
        print(f"  slug: {ch['slug']}")
        if ch.get("notes"):
            print(f"  notes: {ch['notes']}")
        for h in ch.get("history", [])[-5:]:
            print(f"  · {h}")
        return
    counts = {s: 0 for s in STATUSES}
    for part in progress["parts"]:
        print(f"\n{part['id']} · {part['title']}")
        for ch in part["chapters"]:
            counts[ch["status"]] = counts.get(ch["status"], 0) + 1
            note = f"  ({ch['notes']})" if ch.get("notes") and ch["status"] == "blocked" else ""
            print(f"  {ch['id']:>3}  {ch['status']:<12} {ch['title']}{note}")
    total = sum(counts.values())
    summary = ", ".join(f"{k}: {v}" for k, v in counts.items() if v)
    print(f"\n{total} items · {summary}")
    asof = progress.get("book", {}).get("current_as_of")
    print(f"current as of: {asof or 'not yet set'}")


def cmd_set(root, args):
    if args.status not in STATUSES:
        sys.exit(f"Status must be one of: {', '.join(STATUSES)}")
    with file_lock(root / "state" / "progress.json"):
        progress = load_progress(root)
        part, ch = find_chapter(progress, args.chapter)
        if not ch:
            sys.exit(f"Unknown chapter {args.chapter}")
        old = ch["status"]
        ch["status"] = args.status
        if args.status == "blocked":
            if old != "blocked":
                ch["blocked_from"] = old
        else:
            ch.pop("blocked_from", None)
        if args.note is not None:
            ch["notes"] = args.note
        stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        ch.setdefault("history", []).append(f"{stamp} {old} -> {args.status}" + (f": {args.note}" if args.note else ""))
        save_progress(root, progress)
    print(f"ch{ch['id']}: {old} -> {args.status}")


def cmd_part(root, args):
    progress = load_progress(root)
    for part in progress["parts"]:
        if part["id"].upper() == args.part.upper():
            print(" ".join(ch["id"] for ch in part["chapters"]))
            return
    sys.exit(f"Unknown part {args.part}")


def cmd_next(root, args):
    progress = load_progress(root)
    by_id = {p["id"]: p for p in progress["parts"]}
    order = [args.part.upper()] if args.part else PRODUCTION_ORDER
    book = progress.get("book", {})
    pilot, last = book.get("pilot"), norm_ch(book["last"]) if book.get("last") else None
    open_ = lambda c: c["status"] not in ("done", "blocked")
    if pilot and not args.part:
        _p, ch = find_chapter(progress, pilot)
        if ch and open_(ch):
            print(ch["id"])
            return
    others_open = any(open_(c) for p, c in iter_chapters(progress) if not p.get("appendix") and c["id"] != last)
    for pid in order:
        part = by_id.get(pid)
        if not part:
            continue
        for ch in part["chapters"]:
            if ch["id"] == last and others_open:
                continue
            if open_(ch):
                print(ch["id"])
                return
    if last and not args.part:
        _p, ch = find_chapter(progress, last)
        if ch and open_(ch):
            print(ch["id"])
            return
    print("none")


def takeaway_blocks(root):
    """{chapter id: block} from state/takeaways.md, whose blocks start with '## chNN · Title'."""
    path = root / "state" / "takeaways.md"
    blocks, cur, buf = {}, None, []
    if not path.exists():
        return blocks
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+ch(\d{2})\b", line)
        if m:
            if cur:
                blocks[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1), [line]
        elif cur:
            buf.append(line)
    if cur:
        blocks[cur] = "\n".join(buf).strip()
    return blocks


def cmd_known(root, args):
    if args.out:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _known(root, args)
        atomic_write(root / args.out if not args.out.startswith("/") else Path(args.out), buf.getvalue())
        print(f"wrote {args.out}")
    else:
        _known(root, args)


def _known(root, args):
    progress = load_progress(root)
    part, ch = find_chapter(progress, args.chapter)
    if not ch:
        sys.exit(f"Unknown chapter {args.chapter}")
    appendix = bool(part.get("appendix"))
    chapters = [c for p, c in iter_chapters(progress) if not p.get("appendix")]
    earlier = chapters if appendix else [c for c in chapters if c["id"] < ch["id"]]
    blocks = takeaway_blocks(root)
    label = f"Appendix {ch['id']}" if appendix else f"ch{ch['id']}"
    print(f"# What the reader knows before {label} · {ch['title']}")
    if not earlier:
        print("\nNothing yet: this chapter teaches everything from zero, and points forward to later "
              "chapters with @sec-chNN references.")
        return
    print("Only earlier chapters count, in book order, even when later chapters are already finished.\n")
    missing = []
    for c in earlier:
        if c["status"] != "done":
            missing.append(c)
        elif c["id"] in blocks:
            print(blocks[c["id"]] + "\n")
        else:
            print(f"## ch{c['id']} · {c['title']}\n(Finished, but its takeaways are missing from "
                  "state/takeaways.md: read the chapter's Key takeaways section.)\n")
    if missing:
        print("## Earlier chapters not yet written")
        print("The reader will have read these first. Read their entries in docs/OUTLINE-DETAILED.md (or "
              "docs/OUTLINE.md), assume what they teach, and give a one-sentence recap with @sec-chNN.\n")
        for c in missing:
            print(f"- ch{c['id']} · {c['title']}")


def cmd_asof(root, args):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        sys.exit("Date must be YYYY-MM-DD")
    with file_lock(root / "state" / "progress.json"):
        progress = load_progress(root)
        progress.setdefault("book", {})["current_as_of"] = args.date
        save_progress(root, progress)
    pretty = dt.date.fromisoformat(args.date).strftime("%-d %B %Y")
    (root / "book" / "_variables.yml").write_text(f'current_as_of: "{pretty}"\n', encoding="utf-8")
    print(f"current as of: {pretty}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="project root (default: repo root)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("show"); s.add_argument("chapter", nargs="?")
    s = sub.add_parser("set"); s.add_argument("chapter"); s.add_argument("status"); s.add_argument("--note")
    s = sub.add_parser("part"); s.add_argument("part")
    s = sub.add_parser("next"); s.add_argument("--part")
    s = sub.add_parser("known"); s.add_argument("chapter"); s.add_argument("--out")
    s = sub.add_parser("current-as-of"); s.add_argument("date")
    for sp in sub.choices.values():
        sp.add_argument("--root", default=argparse.SUPPRESS)
    args = ap.parse_args()
    root = root_from(args.root)
    {"show": cmd_show, "set": cmd_set, "part": cmd_part, "next": cmd_next, "known": cmd_known,
     "current-as-of": cmd_asof}[args.cmd](root, args)


if __name__ == "__main__":
    main()
