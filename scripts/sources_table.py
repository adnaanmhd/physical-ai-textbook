#!/usr/bin/env python3
"""Generate book/chapters/_sources/chNN.qmd: the table of sources cited in a chapter,
in order of first appearance, with publication dates and evidence tags.

Usage:
  python3 scripts/sources_table.py NN
"""
from __future__ import annotations

import argparse
import re
import sys

from check_chapter import CITE_KEY_RE
from common import CLAIM_TAG_RE, CROSSREF_PREFIXES, chapter_file, ledger_index, norm_ch, parse_bib, root_from

EVIDENCE_LABEL = {
    "peer-reviewed": "peer-reviewed", "preprint": "preprint", "tech-report": "technical report",
    "company-claim": "company claim", "demo": "demo", "standard": "standard", "press": "press",
}
# Weakest first: if one source supports claims with several tags, show the weakest.
WEAKEST_FIRST = ["demo", "company-claim", "press", "preprint", "tech-report", "standard", "peer-reviewed"]


def esc(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def blank(m) -> str:
    return re.sub(r"[^\n]", " ", m.group(0))


def prepare(raw: str) -> str:
    """Blank out code (keeping figure-caption option lines), display maths, HTML comments other
    than claim tags, attribute blocks, link targets, URLs and inline code, without moving text."""
    out, fence, math = [], False, False
    for line in raw.split("\n"):
        st = line.strip()
        if st.startswith(("```", "~~~")):
            fence = not fence
            out.append(" " * len(line))
        elif fence:
            out.append(line if re.match(r"^\s*(?:%%|#)\|\s*fig-cap:", line) else " " * len(line))
        elif st.startswith("$$"):
            if not (st.count("$$") >= 2 and len(st) > 2):
                math = not math
            out.append(" " * len(line))
        else:
            out.append(" " * len(line) if math else line)
    text = "\n".join(out)
    text = re.sub(r"<!--(?!\s*C:).*?-->", blank, text, flags=re.S)
    text = re.sub(r"\{[^{}]*\}", blank, text)
    text = re.sub(r"\]\([^)]*\)", lambda m: "]" + " " * (len(m.group(0)) - 1), text)
    text = re.sub(r"https?://\S+", blank, text)
    text = re.sub(r"`[^`\n]*`", blank, text)
    return text.replace("\\@", "  ")


def ordered_tokens(raw: str):
    """(position, kind, value) for claim tags and citation keys (bracketed or narrative), in order."""
    text = prepare(raw)
    tokens = [(m.start(), "tag", f"C{m.group(1)}.{m.group(2)}-{m.group(3)}") for m in CLAIM_TAG_RE.finditer(text)]
    no_tags = CLAIM_TAG_RE.sub(blank, text)
    for m in CITE_KEY_RE.finditer(no_tags):
        if not m.group(1).startswith(CROSSREF_PREFIXES):
            tokens.append((m.start(), "key", m.group(1)))
    return sorted(tokens)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chapter")
    ap.add_argument("--root")
    args = ap.parse_args()
    root = root_from(args.root)
    nn = norm_ch(args.chapter)
    path = chapter_file(root, nn)
    if not path:
        sys.exit(f"No chapter file for ch{nn}")
    raw = path.read_text(encoding="utf-8")
    index = ledger_index(root)
    bib = parse_bib(root)

    # Order of first appearance: walk the text and interleave citation keys and claim tags.
    order: list[str] = []
    evidence: dict[str, set] = {}
    published: dict[str, str] = {}
    urls: dict[str, str] = {}
    for _pos, kind, value in ordered_tokens(raw):
        if kind == "tag":
            obj = index.get(value)
            if not obj:
                continue
            key = obj.get("source_key")
            evidence.setdefault(key, set()).add(obj.get("evidence"))
            published.setdefault(key, obj.get("published", ""))
            urls.setdefault(key, obj.get("url", ""))
        else:
            key = value
        if key and key not in order:
            order.append(key)

    rows = []
    for key in order:
        entry = bib.get(key, {})
        title = entry.get("title") or "(entry missing from references.bib)"
        date = published.get(key) or "-".join(x for x in (entry.get("year", ""), entry.get("month", "")) if x)
        tags = evidence.get(key) or set()
        if not tags and "note" in entry:
            m = re.search(r"evidence:\s*([\w-]+)", entry["note"])
            if m:
                tags = {m.group(1)}
        weakest = next((t for t in WEAKEST_FIRST if t in tags), None)
        label = EVIDENCE_LABEL.get(weakest, "—") if weakest else "—"
        url = urls.get(key) or entry.get("url", "")
        title_cell = f"[{esc(title)}]({url})" if url else esc(title)
        rows.append(f"| [@{key}] | {title_cell} | {esc(date) or '—'} | {label} |")

    out_dir = root / "book" / "chapters" / "_sources"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"ch{nn}.qmd"
    if rows:
        body = ("| Ref | Source | Published | Evidence |\n|---|---|---|---|\n" + "\n".join(rows) +
                f"\n\n: Sources cited in this chapter, in order of first appearance. Evidence tags are explained in the preface. {{#tbl-ch{nn}-sources}}\n")
    else:
        body = "*No sources cited yet.*\n"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out.relative_to(root)} ({len(rows)} sources)")


if __name__ == "__main__":
    main()
