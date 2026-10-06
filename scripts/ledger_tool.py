#!/usr/bin/env python3
"""Claim-ledger utilities (see docs/LEDGER-SCHEMA.md).

Never edit ledger files by hand. add, mark, update and rekey lock the file, validate the result and
write it atomically, so parallel agents cannot corrupt it.

Usage:
  python3 scripts/ledger_tool.py add NN SS --file claims.json     # or --json '{...}', or JSON on stdin
  python3 scripts/ledger_tool.py validate NN | --all
  python3 scripts/ledger_tool.py stats [NN]
  python3 scripts/ledger_tool.py get CLAIM_ID
  python3 scripts/ledger_tool.py mark CLAIM_ID STATUS [--note "..."] [--by fact-checker] [--superseded-by ID]
  python3 scripts/ledger_tool.py update CLAIM_ID --set field=value [--set ...] [--unset field] [--note "..."]
  python3 scripts/ledger_tool.py rekey OLD_KEY NEW_KEY
  python3 scripts/ledger_tool.py repoint KEY URL
  python3 scripts/ledger_tool.py usages CLAIM_ID [...] | --status failed,flagged,superseded
  python3 scripts/ledger_tool.py volatile --older-than DAYS [--ch NN] [--used]
  python3 scripts/ledger_tool.py next-id NN SS

add: the input is one JSON object, a JSON list of objects, or JSON Lines. The tool assigns id,
chapter and section; status starts as "extracted" and accessed defaults to today. A claim whose
text and source_key match an existing claim in the same section is skipped as a duplicate. If any
claim fails validation, nothing is written.

update: changing the substance of a checked claim (its text, value, conditions, source, date or
support) sends it back to "extracted", so the fact-checker must verify it again.

One source_key means one document: add, update and validate --all reject a key used for two
different documents. Versions of one arXiv paper, and arXiv's own DOI for it, count as one
document; the published version of a paper has its own DOI, so it is a different document with its
own key. repoint moves every claim of a key to a corrected URL (they go back to "extracted"); rekey
merges two keys only when they name the same document.

usages: where claims are tagged in the book. With --status, every tagged claim whose status is in
the list, and the chapters that use it (to route regressions after a fact-check or refresh).
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path

from common import (CLAIM_ID_RE, CLAIM_TAG_RE, atomic_write, banned_domains, file_lock, is_banned,
                    ledger_index, load_ledger, norm_ch, norm_sec, root_from, source_id)

TYPES = {"definition", "mechanism", "number", "date", "result", "limitation",
         "comparison", "forecast", "opinion", "spec"}
SOURCE_TYPES = {"peer-reviewed", "preprint", "tech-report", "company-blog", "press-release",
                "press", "standard", "regulator", "talk", "social", "dataset", "code", "docs"}
EVIDENCE = {"peer-reviewed", "preprint", "tech-report", "company-claim", "demo", "standard", "press"}
# Evidence tags a source type may carry. Types not listed here may carry any tag.
EVIDENCE_FOR_SOURCE = {
    "social": {"company-claim", "demo"},
    "press-release": {"company-claim", "demo"},
    "company-blog": {"company-claim", "demo", "tech-report"},
    "press": {"press", "company-claim", "demo"},
    "peer-reviewed": {"peer-reviewed"},
    "standard": {"standard"},
    "regulator": {"standard"},
}
ACCESS = {"full", "abstract"}
STATUS = {"extracted", "verified", "failed", "flagged", "superseded"}
AUTONOMY = {"autonomous", "teleoperated", "unspecified"}
REQUIRED = ["id", "chapter", "section", "claim", "type", "source_key", "url", "source_type",
            "evidence", "published", "accessed", "access", "support", "volatile", "status"]
SUBSTANCE = {"claim", "type", "value", "conditions", "source_key", "url", "source_type", "evidence",
             "autonomy", "published", "support", "locator", "access"}
PROTECTED = {"id", "chapter", "section", "status", "checked_by", "checked_at"}
BOOL_FIELDS = {"volatile"}
LIST_FIELDS = {"conflict_with"}
DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_:\-.]*[A-Za-z0-9_]$")


def words(s) -> int:
    return len(str(s).split())


def chapter_arg(value) -> str:
    nn = norm_ch(value)
    if not nn.isdigit():
        sys.exit(f"'{value}' is not a chapter number. Appendices have no ledger of their own: "
                 "they reuse the claims of the chapters they summarise.")
    return nn


def section_arg(value) -> str:
    try:
        return norm_sec(value)
    except ValueError:
        sys.exit(f"'{value}' is not a section number (expected e.g. 03)")


def section_path(root: Path, nn: str, ss: str) -> Path:
    return root / "ledger" / f"ch{nn}" / f"s{ss}.jsonl"


def _date_ok(value, today) -> bool:
    """False if a YYYY[-MM[-DD]] date lies in the future (one day of slack for time zones)."""
    try:
        parts = [int(x) for x in str(value).split("-")]
        y, m, d = parts[0], (parts[1] if len(parts) > 1 else 1), (parts[2] if len(parts) > 2 else 1)
        return dt.date(y, m, d) <= today + dt.timedelta(days=1)
    except (ValueError, IndexError):
        return False


def key_sources(rows, skip_id=None):
    """Map source_key -> {source identities} over ledger rows (optionally ignoring one claim id)."""
    out = collections.defaultdict(set)
    for _p, _l, obj, _e in rows:
        if isinstance(obj, dict) and obj.get("id") != skip_id and obj.get("source_key") and obj.get("url"):
            out[obj["source_key"]].add(source_id(obj["url"]))
    return out


def validate_rows(rows, banned=(), known_keys=None):
    """rows: (path, line_no, obj_or_None, error_or_None). Returns (errors, warnings).
    known_keys: source_key -> identities already in the ledger, for the one-key-one-source rule."""
    errors, warnings = [], []
    seen = {}
    today = dt.date.today()
    keys = collections.defaultdict(set)
    for k, v in (known_keys or {}).items():
        keys[k] |= set(v)
    for path, line, obj, err in rows:
        where = f"{path.parent.name}/{path.name}:{line}"
        if err:
            errors.append(f"{where}: {err}")
            continue
        if not isinstance(obj, dict):
            errors.append(f"{where}: line is not a JSON object")
            continue
        for field in REQUIRED:
            if field not in obj or obj[field] in (None, ""):
                errors.append(f"{where}: missing required field '{field}'")
        cid = obj.get("id", "")
        m = CLAIM_ID_RE.match(str(cid))
        if not m:
            errors.append(f"{where}: bad id '{cid}' (expected like C29.03-014)")
        else:
            ch, sec = m.group(1), m.group(2)
            if path.parent.name != f"ch{ch}" or path.stem != f"s{sec}":
                errors.append(f"{where}: id {cid} does not match file ledger/ch{ch}/s{sec}.jsonl")
            if str(obj.get("chapter")) != ch or str(obj.get("section")) != sec:
                errors.append(f"{where}: chapter/section fields disagree with id {cid}")
            if cid in seen:
                errors.append(f"{where}: duplicate id {cid} (first at {seen[cid]})")
            seen[cid] = where

        def enum(field, allowed, required=True):
            val = obj.get(field)
            if val is None and not required:
                return
            if val not in allowed:
                errors.append(f"{where}: {field}='{val}' not in {sorted(allowed)}")
        enum("type", TYPES)
        enum("source_type", SOURCE_TYPES)
        enum("evidence", EVIDENCE)
        enum("access", ACCESS)
        enum("status", STATUS)
        enum("autonomy", AUTONOMY, required=False)
        allowed_ev = EVIDENCE_FOR_SOURCE.get(obj.get("source_type"))
        if allowed_ev and obj.get("evidence") in EVIDENCE and obj.get("evidence") not in allowed_ev:
            errors.append(f"{where}: a '{obj.get('source_type')}' source cannot carry evidence "
                          f"'{obj.get('evidence')}' (allowed: {', '.join(sorted(allowed_ev))})")
        if obj.get("evidence") == "demo" and "autonomy" not in obj:
            errors.append(f"{where}: demo claims need 'autonomy'")
        if obj.get("published"):
            if not DATE_RE.match(str(obj["published"])):
                errors.append(f"{where}: published must be YYYY, YYYY-MM or YYYY-MM-DD")
            elif not _date_ok(obj["published"], today):
                errors.append(f"{where}: published date {obj['published']} is in the future or invalid")
        for f in ("accessed", "checked_at"):
            if obj.get(f):
                if not DAY_RE.match(str(obj[f])):
                    errors.append(f"{where}: {f} must be YYYY-MM-DD")
                elif not _date_ok(obj[f], today):
                    errors.append(f"{where}: {f} date {obj[f]} is in the future or invalid")
        if not isinstance(obj.get("volatile"), bool):
            errors.append(f"{where}: volatile must be true or false")
        if words(obj.get("support", "")) > 50:
            errors.append(f"{where}: support is {words(obj['support'])} words (max 50)")
        if words(obj.get("claim", "")) > 60:
            warnings.append(f"{where}: claim is {words(obj['claim'])} words (aim for 60 or fewer)")
        if obj.get("status") == "superseded" and not obj.get("superseded_by"):
            errors.append(f"{where}: superseded claims need 'superseded_by'")
        sb = obj.get("superseded_by")
        if sb and not CLAIM_ID_RE.match(str(sb)):
            errors.append(f"{where}: superseded_by must be a claim id")
        if obj.get("type") in ("number", "spec") and not obj.get("value"):
            warnings.append(f"{where}: {obj.get('type')} claim without 'value'")
        url = obj.get("url")
        if url and not str(url).startswith(("http://", "https://")):
            errors.append(f"{where}: url must start with http(s)://")
        elif url and banned and is_banned(url, banned):
            errors.append(f"{where}: url is on a banned domain ({url}); find the primary source")
        if obj.get("source_key") and not KEY_RE.match(str(obj["source_key"])):
            errors.append(f"{where}: bad source_key '{obj['source_key']}'")
        cw = obj.get("conflict_with")
        if cw is not None and (not isinstance(cw, list) or not all(CLAIM_ID_RE.match(str(x)) for x in cw)):
            errors.append(f"{where}: conflict_with must be a list of claim ids")
        key = obj.get("source_key")
        if key and url:
            sid = source_id(url)
            if keys[key] and sid not in keys[key]:
                errors.append(f"{where}: source_key '{key}' already names another source "
                              f"({', '.join(sorted(keys[key]))}); give this source ({sid}) its own key")
            keys[key].add(sid)
    return errors, warnings


def read_section(path: Path):
    """Return (non-empty lines, parsed objects). Exits if a line is not valid JSON."""
    if not path.exists():
        return [], []
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    objs = []
    for i, ln in enumerate(lines, start=1):
        try:
            objs.append(json.loads(ln))
        except json.JSONDecodeError as exc:
            sys.exit(f"{path}:{i}: invalid JSON ({exc.msg}). Run validate and repair this line first.")
    return lines, objs


def write_section(path: Path, objs) -> None:
    atomic_write(path, "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs))


def report(errors, warnings, footer=None) -> None:
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if footer:
        print(footer)


# ---------------------------------------------------------------- commands

def cmd_validate(root, args):
    if args.all:
        rows = load_ledger(root)
    elif args.chapter:
        rows = load_ledger(root, chapter_arg(args.chapter))
    else:
        sys.exit("Give a chapter number or --all")
    errors, warnings = validate_rows(rows, banned_domains(root))
    n = sum(1 for r in rows if r[2] is not None)
    report(errors, warnings, f"{n} claims checked · {len(errors)} errors · {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


def _norm_claim(text) -> str:
    return re.sub(r"\s+", " ", str(text)).strip().rstrip(".").casefold()


def _parse_input(args):
    if args.json:
        text = args.json
    elif args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        sys.exit("Give --file, --json, or pipe JSON on stdin")
    text = text.strip()
    if not text:
        sys.exit("No claims given")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = []
        for i, line in enumerate(text.splitlines(), start=1):
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    sys.exit(f"Input line {i}: invalid JSON ({exc.msg})")
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
        sys.exit("Input must be a JSON object, a list of objects, or JSON Lines")
    return data


def cmd_add(root, args):
    nn, ss = chapter_arg(args.chapter), section_arg(args.section)
    path = section_path(root, nn, ss)
    incoming = _parse_input(args)
    today = dt.date.today().isoformat()
    with file_lock(path):
        _lines, existing = read_section(path)
        highest = 0
        for o in existing:
            m = CLAIM_ID_RE.match(str(o.get("id", "")))
            if m:
                highest = max(highest, int(m.group(3)))
        seen = {(_norm_claim(o.get("claim", "")), o.get("source_key")): o.get("id") for o in existing}
        new, dupes, problems = [], [], []
        for n, obj in enumerate(incoming, start=1):
            status = obj.get("status", "extracted")
            if status != "extracted":
                problems.append(f"input claim {n}: new claims start as 'extracted' (got '{status}'); "
                                "only the fact-checker changes status, with mark")
                continue
            key = (_norm_claim(obj.get("claim", "")), obj.get("source_key"))
            if key in seen:
                dupes.append((seen[key], obj))
                continue
            highest += 1
            cid = f"C{nn}.{ss}-{highest:03d}"
            row = {"id": cid, "chapter": nn, "section": ss}
            row.update({k: v for k, v in obj.items() if k not in ("id", "chapter", "section")})
            row["status"] = "extracted"
            row.setdefault("accessed", today)
            seen[key] = cid
            new.append(row)
        start = len(existing) + 1
        errors, warnings = validate_rows([(path, start + i, r, None) for i, r in enumerate(new)],
                                         banned_domains(root), key_sources(load_ledger(root)))
        errors = problems + errors
        if errors:
            report(errors, warnings, "Nothing written: fix the input and run add again.")
            sys.exit(1)
        if new:
            write_section(path, existing + new)
    report([], warnings)
    for r in new:
        print(f"{r['id']}  added  {str(r.get('claim', ''))[:70]}")
    for cid, obj in dupes:
        print(f"skipped: duplicate of {cid}  {str(obj.get('claim', ''))[:60]}")
    print(f"{len(new)} added · {len(dupes)} duplicates skipped · {len(warnings)} warnings")


def cmd_next_id(root, args):
    nn, ss = chapter_arg(args.chapter), section_arg(args.section)
    _lines, objs = read_section(section_path(root, nn, ss))
    highest = 0
    for o in objs:
        m = CLAIM_ID_RE.match(str(o.get("id", "")))
        if m:
            highest = max(highest, int(m.group(3)))
    print(f"C{nn}.{ss}-{highest + 1:03d}")


def _counts(objs, field):
    c = collections.Counter(str(o.get(field)) for o in objs)
    return ", ".join(f"{k}: {v}" for k, v in sorted(c.items()))


def cmd_stats(root, args):
    nn = chapter_arg(args.chapter) if args.chapter else None
    objs = [r[2] for r in load_ledger(root, nn) if isinstance(r[2], dict)]
    print(f"claims: {len(objs)} · distinct sources: {len({o.get('source_key') for o in objs})}")
    print("by status:   " + _counts(objs, "status"))
    print("by evidence: " + _counts(objs, "evidence"))
    if nn:
        by_sec = collections.defaultdict(list)
        for o in objs:
            by_sec[str(o.get("section"))].append(o)
        print("by section:")
        for sec in sorted(by_sec):
            group = by_sec[sec]
            srcs = len({o.get("source_key") for o in group})
            print(f"  s{sec}  {len(group):>3} claims · {srcs:>2} sources · {_counts(group, 'status')}")
    else:
        print("by chapter:  " + ", ".join(f"ch{k}: {v}" for k, v in sorted(
            collections.Counter(str(o.get("chapter")) for o in objs).items())))


def _locate(root, claim_id):
    m = CLAIM_ID_RE.match(str(claim_id))
    if not m:
        sys.exit(f"Bad claim id {claim_id} (expected like C29.03-014)")
    return section_path(root, m.group(1), m.group(2))


def _find(objs, claim_id, path):
    for i, o in enumerate(objs):
        if o.get("id") == claim_id:
            return i
    sys.exit(f"Claim {claim_id} not found in {path}")


def cmd_get(root, args):
    path = _locate(root, args.claim_id)
    _lines, objs = read_section(path)
    print(json.dumps(objs[_find(objs, args.claim_id, path)], indent=2, ensure_ascii=False))


def _save_one(root, path, objs, i, check_keys=True):
    known = key_sources(load_ledger(root), skip_id=objs[i].get("id")) if check_keys else None
    errors, warnings = validate_rows([(path, i + 1, objs[i], None)], banned_domains(root), known)
    if errors:
        report(errors, warnings, "Nothing written.")
        sys.exit(1)
    write_section(path, objs)
    report([], warnings)


def cmd_mark(root, args):
    if args.status not in STATUS:
        sys.exit(f"Status must be one of {sorted(STATUS)}")
    path = _locate(root, args.claim_id)
    with file_lock(path):
        _lines, objs = read_section(path)
        i = _find(objs, args.claim_id, path)
        obj = objs[i]
        old = obj.get("status")
        obj["status"] = args.status
        obj["checked_by"] = args.by
        obj["checked_at"] = dt.date.today().isoformat()
        if args.note:
            obj["note"] = args.note
        if args.superseded_by:
            obj["superseded_by"] = args.superseded_by
        _save_one(root, path, objs, i, check_keys=False)
    print(f"{args.claim_id}: {old} -> {args.status}")


def _parse_value(field, raw):
    if field in BOOL_FIELDS:
        if raw.lower() in ("true", "false"):
            return raw.lower() == "true"
        sys.exit(f"{field} must be true or false")
    if field in LIST_FIELDS:
        try:
            val = json.loads(raw)
        except json.JSONDecodeError:
            val = [x.strip() for x in raw.split(",") if x.strip()]
        if not isinstance(val, list):
            sys.exit(f"{field} must be a list")
        return val
    return raw


def cmd_update(root, args):
    if not args.set and not args.unset:
        sys.exit("Nothing to update: give --set field=value or --unset field")
    path = _locate(root, args.claim_id)
    with file_lock(path):
        _lines, objs = read_section(path)
        i = _find(objs, args.claim_id, path)
        obj = objs[i]
        changed = set()
        for item in args.set or []:
            if "=" not in item:
                sys.exit(f"--set needs field=value (got '{item}')")
            field, raw = item.split("=", 1)
            field = field.strip()
            if field in PROTECTED:
                sys.exit(f"'{field}' cannot be changed with update (use mark for status)")
            val = _parse_value(field, raw)
            if obj.get(field) != val:
                obj[field] = val
                changed.add(field)
        for field in args.unset or []:
            if field in PROTECTED or field in REQUIRED:
                sys.exit(f"'{field}' cannot be removed")
            if field in obj:
                del obj[field]
                changed.add(field)
        reset = bool(changed & SUBSTANCE) and obj.get("status") not in ("extracted", "superseded")
        if reset:
            obj["status"] = "extracted"
            obj["note"] = "changed after check; needs re-verification"
        if args.note:
            obj["note"] = args.note
        if "url" in changed and "source_key" not in changed:
            others = key_sources(load_ledger(root), skip_id=obj.get("id")).get(obj.get("source_key"), set())
            if others and source_id(obj["url"]) not in others:
                sys.exit(f"Other claims use @{obj.get('source_key')} with the old URL. To move them all to the "
                         f"corrected URL, run: python3 scripts/ledger_tool.py repoint {obj.get('source_key')} "
                         f"{obj['url']}. If this one claim came from a different document, give it its own key: "
                         f"update {obj.get('id')} --set source_key=NEWKEY --set url=URL")
        _save_one(root, path, objs, i, check_keys=bool({"url", "source_key"} & changed))
    print(f"{args.claim_id}: updated {', '.join(sorted(changed)) or 'nothing'}"
          + (" · status reset to extracted" if reset else ""))


def cmd_rekey(root, args):
    old, new = args.old, args.new
    if not KEY_RE.match(new):
        sys.exit(f"Bad key '{new}'")
    if old == new:
        sys.exit("Old and new keys are the same")
    ids = key_sources(load_ledger(root))
    if ids.get(old) and ids.get(new) and ids[old] != ids[new]:
        sys.exit(f"@{old} ({', '.join(sorted(ids[old]))}) and @{new} ({', '.join(sorted(ids[new]))}) name different "
                 "documents, so they keep separate keys (a preprint and its published version are different "
                 f"documents). If they really are one document, first run: repoint {old} <the URL of @{new}>")
    n_claims = 0
    for path in sorted((root / "ledger").glob("ch*/*.jsonl")):
        with file_lock(path):
            _lines, objs = read_section(path)
            hits = [o for o in objs if o.get("source_key") == old]
            if hits:
                for o in hits:
                    o["source_key"] = new
                write_section(path, objs)
                n_claims += len(hits)
    pat = re.compile(r"(?<![\w@.\\/])@" + re.escape(old) + r"(?![A-Za-z0-9_]|[:.\-][A-Za-z0-9_])")
    files = []
    for path in sorted((root / "book").rglob("*.qmd")):
        if "_book" in path.parts or ".quarto" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = pat.subn("@" + new, text)
        if n:
            atomic_write(path, new_text)
            files.append(f"{path.relative_to(root)} ({n})")
    print(f"@{old} -> @{new}: {n_claims} ledger claims; book files: {', '.join(files) or 'none'}")
    print(f"Now delete the @{old} entry from book/references.bib (keep @{new}).")


def cmd_repoint(root, args):
    key, url = args.key, args.url.strip()
    if not url.startswith(("http://", "https://")):
        sys.exit("The URL must start with http(s)://")
    if is_banned(url, banned_domains(root)):
        sys.exit(f"{url} is on a banned domain")
    moved = 0
    for path in sorted((root / "ledger").glob("ch*/*.jsonl")):
        with file_lock(path):
            _lines, objs = read_section(path)
            hits = [o for o in objs if o.get("source_key") == key and o.get("url") != url]
            if not hits:
                continue
            for o in hits:
                o["url"] = url
                if o.get("status") not in ("extracted", "superseded"):
                    o["status"] = "extracted"
                    o["note"] = "source URL corrected with repoint; needs re-verification"
            write_section(path, objs)
            moved += len(hits)
    if not moved:
        print(f"No claims of @{key} needed moving")
        return
    print(f"@{key}: {moved} claims now point to {url}; they are back to 'extracted' and need re-verification.")
    print("Update the url (and doi or eprint) of its entry in book/references.bib to match.")


def tag_usages(root):
    """Map claim id -> ['book/...qmd:LINE', ...] for every claim tag in the book's source files."""
    out = collections.defaultdict(list)
    for path in sorted((root / "book").rglob("*.qmd")):
        if "_book" in path.parts or ".quarto" in path.parts:
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for m in CLAIM_TAG_RE.finditer(line):
                out[f"C{m.group(1)}.{m.group(2)}-{m.group(3)}"].append(f"{path.relative_to(root)}:{n}")
    return out


def cmd_usages(root, args):
    uses = tag_usages(root)
    index = ledger_index(root)
    if args.status:
        wanted = {x.strip() for x in args.status.split(",") if x.strip()}
        ids = sorted(cid for cid in uses if index.get(cid, {}).get("status") in wanted)
    elif args.claim_ids:
        ids = args.claim_ids
    else:
        sys.exit("Give claim ids, or --status")
    files = set()
    for cid in ids:
        where = uses.get(cid, [])
        files.update(w.rsplit(":", 1)[0] for w in where)
        status = index.get(cid, {}).get("status", "not in ledger")
        print(f"{cid} [{status}]: {', '.join(where) or 'not used in the book'}")
    print(f"{len(ids)} claims · book files affected: {', '.join(sorted(files)) or 'none'}")


def cmd_volatile(root, args):
    today = dt.date.today()
    nn = chapter_arg(args.ch) if args.ch else None
    used = tag_usages(root) if args.used else None
    stale = []
    for _p, _l, obj, _e in load_ledger(root, nn):
        if not isinstance(obj, dict) or not obj.get("volatile") or obj.get("status") == "superseded":
            continue
        if used is not None and obj.get("id") not in used:
            continue
        last = obj.get("checked_at") or obj.get("accessed")
        try:
            age = (today - dt.date.fromisoformat(str(last))).days
        except (TypeError, ValueError):
            age = 10_000
        if age >= args.older_than:
            stale.append((str(obj.get("chapter")), obj.get("id", "?"), age, str(obj.get("claim", ""))[:90]))
    for ch, cid, age, text in sorted(stale):
        print(f"ch{ch}  {cid}  {age:>4} days  {text}")
    print(f"{len(stale)} volatile claims{' used in the book' if args.used else ''} older than {args.older_than} days")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="project root (default: repo root)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add"); s.add_argument("chapter"); s.add_argument("section")
    s.add_argument("--file"); s.add_argument("--json")
    s = sub.add_parser("validate"); s.add_argument("chapter", nargs="?"); s.add_argument("--all", action="store_true")
    s = sub.add_parser("next-id"); s.add_argument("chapter"); s.add_argument("section")
    s = sub.add_parser("stats"); s.add_argument("chapter", nargs="?")
    s = sub.add_parser("get"); s.add_argument("claim_id")
    s = sub.add_parser("mark"); s.add_argument("claim_id"); s.add_argument("status")
    s.add_argument("--note"); s.add_argument("--by", default="fact-checker"); s.add_argument("--superseded-by")
    s = sub.add_parser("update"); s.add_argument("claim_id")
    s.add_argument("--set", action="append", metavar="FIELD=VALUE")
    s.add_argument("--unset", action="append", metavar="FIELD"); s.add_argument("--note")
    s = sub.add_parser("rekey"); s.add_argument("old"); s.add_argument("new")
    s = sub.add_parser("repoint"); s.add_argument("key"); s.add_argument("url")
    s = sub.add_parser("usages"); s.add_argument("claim_ids", nargs="*"); s.add_argument("--status")
    s = sub.add_parser("volatile"); s.add_argument("--older-than", type=int, default=60); s.add_argument("--ch")
    s.add_argument("--used", action="store_true", help="only claims tagged in the book")
    for sp in sub.choices.values():
        sp.add_argument("--root", default=argparse.SUPPRESS)
    args = ap.parse_args()
    root = root_from(args.root)
    {"add": cmd_add, "validate": cmd_validate, "next-id": cmd_next_id, "stats": cmd_stats,
     "get": cmd_get, "mark": cmd_mark, "update": cmd_update, "rekey": cmd_rekey, "repoint": cmd_repoint,
     "usages": cmd_usages, "volatile": cmd_volatile}[args.cmd](root, args)


if __name__ == "__main__":
    main()
