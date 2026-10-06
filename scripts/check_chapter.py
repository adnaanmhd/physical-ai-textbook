#!/usr/bin/env python3
"""Validate a chapter against the style contract, the claim ledger and the bibliography.

Usage:
  python3 scripts/check_chapter.py NN [--stage draft|final] [--only CAT[,CAT...]] [--stats]
  python3 scripts/check_chapter.py --all [--stage final]

Categories: template, sections, citations, claims, facts, quotes, spelling, todos, banned, crossrefs
Exit code 1 if any ERROR is reported. WARN lines are advisory.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys

from common import (CROSSREF_PREFIXES, STUB_MARKER, WRITTEN_STATUSES, banned_domains, bib_source_ids,
                    chapter_file, find_chapter, is_banned, iter_chapters, ledger_index, load_progress,
                    norm_ch, parse_bib, read_lines, root_from, source_id, strip_code_and_math)

CATEGORIES = ["template", "sections", "citations", "claims", "facts", "quotes", "spelling",
              "todos", "banned", "crossrefs"]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*(\{[^{}]*\})?\s*$")
HOW_RE = re.compile(r"\*\*How it(?:'|’)s actually done\.?\*\*")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
CITE_KEY_RE = re.compile(r"(?<![\w@.\\/])-?@([A-Za-z0-9_][A-Za-z0-9_:\-.]*[A-Za-z0-9_])")
INCLUDE_TMPL = r"\{\{<\s*include\s+_sources/chNN\.qmd\s*>\}\}"
TODO_RE = re.compile(r"<!--\s*TODO", re.I)
FIG_MARKER_RE = re.compile(r"<!--\s*FIG:", re.I)
CLAIM_TOKEN_RE = re.compile(r"<!--\s*C:(\d{2})\.(\d{2})-(\d{3})\s*-->")
LABEL_DEF_RE = re.compile(r"\{#((?:sec|fig|tbl|eq)-[A-Za-z0-9_\-:.]*[A-Za-z0-9_])")
CELL_LABEL_RE = re.compile(r"^\s*(?:#|%%)\|\s*label:\s*((?:fig|tbl)-[A-Za-z0-9_\-]+)", re.M)
XREF_USE_RE = re.compile(r"(?<![\w@.\\/])@((?:sec|fig|tbl|eq)-[A-Za-z0-9_\-:.]*[A-Za-z0-9_])")
UNITS = (r"%|percent|per cent|[kMG]?Hz|kg|mg|mm|cm|km|ms|µs|μs|min|hours?|hrs?|days?|weeks?|months?|years?"
         r"|[kMG]?W|[kM]?Wh|[kM]?V|mA|N·m|Nm|N|°C|°|dB|fps|DoF|[KMGTP]B|TOPS|T?FLOPS"
         r"|thousand|million|billion|trillion|bn|[kMBT]\b|×|x\b|times|USD|EUR|INR|GBP|CNY"
         r"|m\b|s\b|h\b|g\b|A\b|V\b|K\b")
COUNT_NOUNS = (r"parameters|params|tokens|units|robots|humanoids|people|workers|operators|customers|homes"
               r"|households|sites|factories|warehouses|countries|trials|episodes|demonstrations|demos|tasks"
               r"|skills|steps|hours|objects|scenes|environments|vehicles|parts|cars|joints|degrees|actuators"
               r"|motors|cameras|sensors|fingers|GPUs|chips|frames|images|videos|clips|trajectories|samples"
               r"|datasets|languages")
# Numbers that make a sentence a quantitative claim: units, magnitudes, money, years, and counts
# (a count noun may have one describing word in between: "30 unfamiliar homes", "2,048 Nvidia GPUs").
QUANT_RE = re.compile(
    r"\d[\d,.]*\s?(?:" + UNITS + r")s?(?![A-Za-z])"
    r"|\d[\d,.]*\s(?:[A-Za-z][\w-]*\s)?(?:" + COUNT_NOUNS + r")\b"
    r"|[$€£₹¥]\s?\d|\b(?:19|20)\d{2}\b"
)
# Product and model names that contain digits (π0.5, GR00T N1.5, G1, H1, V3) and 2D/3D/4D.
NAME_RE = re.compile(r"\b[^\W\d_]+\d+(?:\.\d+)*[^\W\d_]*\b|\b\d+D\b")
TAG_START_RE = re.compile(r"<!--\s*C:")
NOFACT_START_RE = re.compile(r"<!--\s*nofact")
LIST_MARK_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
SKIP_CALLOUT_TITLES = ("ELI5", "Running example", "Try it", "Before you start", "In preparation")
# Abbreviations whose full stop must not end a sentence when splitting.
ABBREV_RE = re.compile(r"\b(et al|e\.g|i\.e|cf|vs|approx|ca|Fig|Figs|Eq|Eqs|Ref|Refs|No|Nos|Vol|pp"
                       r"|Dr|Prof|Mr|Ms|Mrs|Inc|Ltd|Co|Corp|Jr|Sr|St|U\.S|U\.K|Jan|Feb|Mar|Apr|Jun|Jul"
                       r"|Aug|Sep|Sept|Oct|Nov|Dec)\.")
NOFACT_RE = re.compile(r"<!--\s*nofact\s*-->")
BADGE_RE = re.compile(r"^(?:\[[^\[\]]*\]\{\.ev\}\s*)+")

US_TO_UK = {
    "color": "colour", "colors": "colours", "colored": "coloured",
    "behavior": "behaviour", "behaviors": "behaviours", "behavioral": "behavioural",
    "modeling": "modelling", "modeled": "modelled", "labeled": "labelled", "labeling": "labelling",
    "center": "centre", "centers": "centres", "centered": "centred",
    "analyze": "analyse", "analyzed": "analysed", "analyzing": "analysing",
    "fiber": "fibre", "fibers": "fibres", "gray": "grey", "defense": "defence",
    "catalog": "catalogue", "traveled": "travelled", "traveling": "travelling",
    "signaling": "signalling", "fueled": "fuelled", "aluminum": "aluminium",
    "favor": "favour", "favorable": "favourable", "neighbor": "neighbour", "labor": "labour",
    "vapor": "vapour", "flavor": "flavour", "artifact": "artefact", "artifacts": "artefacts",
    "toward": "towards", "centimeters": "centimetres", "millimeters": "millimetres",
}
IZE_RE = re.compile(r"\b([a-z]+iz(?:e|es|ed|ing|ation|ations|er|ers))\b")
IZE_ALLOW = {"size", "sizes", "sized", "sizing", "resize", "resized", "resizing", "oversize",
             "oversized", "downsize", "downsized", "prize", "prizes", "seize", "seized", "seizes",
             "seizing", "capsize", "capsized", "maize", "baize"}


class Report:
    def __init__(self, label, only):
        self.label, self.only = label, only
        self.errors = []
        self.warnings = []

    def on(self, cat):
        return not self.only or cat in self.only

    def error(self, cat, msg):
        if self.on(cat):
            self.errors.append(f"ERROR [{cat}] {msg}")

    def warn(self, cat, msg):
        if self.on(cat):
            self.warnings.append(f"WARN  [{cat}] {msg}")

    def by_stage(self, stage, cat, msg):
        (self.error if stage == "final" else self.warn)(cat, msg)


def headings(lines):
    out = []
    for i, ln in enumerate(lines):
        m = HEADING_RE.match(ln)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip(), m.group(3) or ""))
    return out


def section_range(heads, lines, idx):
    i, level = heads[idx][0], heads[idx][1]
    end = len(lines)
    for j in range(idx + 1, len(heads)):
        if heads[j][1] <= level:
            end = heads[j][0]
            break
    return i, end


def find_h2(heads, lines, name):
    for k, (i, level, title, _a) in enumerate(heads):
        if level == 2 and title.lower().startswith(name.lower()):
            return section_range(heads, lines, k)
    return None


def callout_title_re(title):
    return re.compile(r"^\s*:::+\s*\{[^}]*title\s*=\s*[\"']" + re.escape(title) + r"[\"'][^}]*\}")


def clean_for_keys(text):
    text = COMMENT_RE.sub(" ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)          # attribute blocks like {#sec-x .concept}
    text = re.sub(r"\]\([^)]*\)", "] ", text)        # markdown link targets
    text = re.sub(r"https?://\S+", " ", text)         # bare URLs (e.g. x.com/@handle)
    text = re.sub(r"`[^`\n]*`", " ", text)            # inline code (never across lines or fences)
    return text.replace("\\@", " ")


def cite_keys(text):
    keys = []
    for m in CITE_KEY_RE.finditer(clean_for_keys(text)):
        key = m.group(1)
        if not key.startswith(CROSSREF_PREFIXES):
            keys.append(key)
    return keys


def paragraphs(lines):
    """Yield (first_line_index, joined_text) for blocks separated by blank lines."""
    block, start = [], 0
    for i, ln in enumerate(lines + [""]):
        if ln.strip():
            if not block:
                start = i
            block.append(ln.strip())
        elif block:
            yield start, " ".join(block)
            block = []


def check_template(rep, lines, heads):
    concepts = [k for k, h in enumerate(heads) if ".concept" in h[3]]
    if not concepts:
        rep.error("template", "no headings carry the .concept class")
        return 0
    endings = ("key takeaways", "people, tools and costs", "research prompts", "sources for this chapter")
    in_ending = False
    for i, level, title, attrs in heads:
        if level == 2:
            in_ending = title.lower().startswith(endings)
        elif level == 3 and not in_ending and ".concept" not in attrs and ".aside" not in attrs:
            rep.warn("template", f'heading "{title}" (line {i + 1}) has neither .concept nor .aside: add '
                                 ".concept if it teaches a concept (it then needs all five layers), or .aside if not")
    patterns = {
        "ELI5": callout_title_re("ELI5"),
        "First principles": callout_title_re("First principles"),
        "How it's actually done": HOW_RE,
        "Deployment lens": callout_title_re("Deployment lens"),
    }
    for k in concepts:
        start, end = section_range(heads, lines, k)
        title = heads[k][2]
        block = lines[start + 1:end]
        pos = {}
        for j, ln in enumerate(block):
            for name, pat in patterns.items():
                if name not in pos and pat.search(ln):
                    pos[name] = j
        missing = [n for n in patterns if n not in pos]
        where = f'concept "{title}" (line {start + 1})'
        if missing:
            rep.error("template", f"{where}: missing {', '.join(missing)}")
        else:
            order = [pos[n] for n in patterns]
            if order != sorted(order):
                rep.error("template", f"{where}: layers out of order (ELI5 → First principles → "
                                      f"How it's actually done → Deployment lens)")
        if not cite_keys("\n".join(block)):
            rep.error("template", f"{where}: no citation anywhere in the concept")
    return len(concepts)


def check_sections(rep, nn, lines, heads, lifecycle, stage):
    h1 = [h for h in heads if h[1] == 1]
    if not h1 or f"#sec-ch{nn}" not in h1[0][3]:
        rep.error("sections", f"first-level heading must carry {{#sec-ch{nn}}}")
    else:
        first_h2 = next((h[0] for h in heads if h[1] == 2), len(lines))
        opener = COMMENT_RE.sub(" ", " ".join(lines[h1[0][0] + 1:first_h2]))
        if len(opener.split()) < 40:
            rep.warn("sections", "opener before the first section is under 40 words")
    required = ["Key takeaways", "Research prompts", "Sources for this chapter"]
    if lifecycle:
        required.insert(1, "People, tools and costs")
    for name in required:
        rng = find_h2(heads, lines, name)
        if not rng:
            rep.error("sections", f'missing "## {name}" section')
            continue
        body = lines[rng[0] + 1:rng[1]]
        if name == "Key takeaways":
            bullets = sum(1 for ln in body if re.match(r"^\s*[-*]\s+\S", ln))
            if not 5 <= bullets <= 9:
                rep.by_stage(stage, "sections", f"Key takeaways has {bullets} bullets (need 5–9)")
        if name == "Research prompts":
            n = sum(1 for ln in body if re.match(r"^\s*\d+\.\s+\S", ln))
            if stage == "final" and not 5 <= n <= 8:
                rep.error("sections", f"Research prompts has {n} numbered prompts (need 5–8)")
            elif stage == "draft" and n == 0:
                rep.warn("sections", "Research prompts is empty (the prompt-designer fills it later)")
        if name == "Sources for this chapter":
            if not re.search(INCLUDE_TMPL.replace("NN", nn), "\n".join(body)):
                rep.error("sections", f"Sources section must contain {{{{< include _sources/ch{nn}.qmd >}}}}")


def check_sources_include(rep, root, nn, keys, bib, stage):
    path = root / "book" / "chapters" / "_sources" / f"ch{nn}.qmd"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    table_keys = cite_keys(text)
    if keys and not table_keys:
        rep.by_stage(stage, "citations", f"sources table is empty: run python3 scripts/sources_table.py {nn}")
    for k in sorted(set(table_keys)):
        if k not in bib:
            rep.by_stage(stage, "citations", f"sources table cites @{k}, which is not in book/references.bib")
    if "(entry missing from references.bib)" in text:
        rep.by_stage(stage, "citations", "sources table has entries missing from references.bib")


def check_claims(rep, root, nn, raw, stage, require_tags=True, bib=None):
    own = ledger_index(root, nn) if nn.isdigit() else {}
    mismatched = set()
    everything = None
    counts = collections.Counter()
    tags = []
    prev_end, prev_keys = None, set()
    for m in CLAIM_TOKEN_RE.finditer(raw):
        cid = f"C{m.group(1)}.{m.group(2)}-{m.group(3)}"
        tags.append(cid)
        # Citation keys in the sentence this tag closes: from the previous tag (or paragraph start).
        if prev_end is not None and raw[prev_end:m.start()].strip() == "":
            keys = prev_keys
        else:
            para_start = raw.rfind("\n\n", 0, m.start())
            start = max(prev_end or 0, para_start if para_start >= 0 else 0)
            keys = set(cite_keys(raw[start:m.start()]))
        prev_end, prev_keys = m.end(), keys
        obj = own.get(cid)
        if obj is None:
            if everything is None:
                everything = ledger_index(root)
            obj = everything.get(cid)
        if obj is None:
            rep.error("claims", f"{cid} is not in the ledger")
            continue
        status = obj.get("status")
        counts[obj.get("evidence", "?")] += 1
        if status in ("failed", "superseded"):
            rep.error("claims", f"{cid} has status '{status}' and must not be used")
        elif stage == "final" and status != "verified":
            rep.error("claims", f"{cid} has status '{status}' (final stage needs 'verified')")
        elif status == "flagged":
            rep.warn("claims", f"{cid} is flagged: {str(obj.get('note', ''))[:80]}")
        src = obj.get("source_key")
        if src and src not in keys:
            shown = ", ".join("@" + k for k in sorted(keys)) or "no citation"
            rep.by_stage(stage, "claims", f"{cid} comes from @{src}, but the sentence it tags cites {shown}")
        entry = (bib or {}).get(src)
        if entry and cid not in mismatched:
            ids = bib_source_ids(entry)
            if ids and source_id(obj.get("url", "")) not in ids:
                mismatched.add(cid)
                rep.by_stage(stage, "claims", f"{cid} was taken from {obj.get('url')}, but @{src} in references.bib "
                                              f"points elsewhere ({entry.get('url') or entry.get('doi') or entry.get('eprint')}): "
                                              "one key must mean one source")
    if not tags and require_tags:
        rep.error("claims", "no claim tags found (every factual sentence needs <!--C:NN.SS-XXX-->)")
    return tags, counts


def skip_mask(lines):
    """True for lines whose numbers are illustrative or not prose: the Research prompts and Sources
    sections, and ELI5, Running example, Try it, Before you start and In preparation callouts."""
    mask = []
    skip_section = skip_callout = False
    for ln in lines:
        s = ln.strip()
        h2 = re.match(r"^##\s+(.*)", s)
        if h2:
            skip_section = h2.group(1).lower().startswith(("research prompts", "sources for this chapter"))
        if s.startswith(":::"):
            if "{" in s:
                skip_callout = any(f'title="{t}' in s or f"title='{t}" in s for t in SKIP_CALLOUT_TITLES)
            else:
                skip_callout = False
            mask.append(True)
            continue
        mask.append(skip_section or skip_callout)
    return mask


def fact_blocks(lines):
    """Yield (line_index, text) for prose blocks eligible for the untagged-fact check. Each list
    item and each image caption is its own block; headings, tables and skipped regions are excluded."""
    mask = skip_mask(lines)
    block, start = [], 0
    for i, ln in enumerate(lines + [""]):
        s = ln.strip()
        caption = re.match(r"!\[(.*)\]\(", s) if i < len(lines) and not mask[i] else None
        excluded = (i >= len(lines) or mask[i] or not s
                    or s.startswith(("#", "|", "{{<", "![", "%%|", ":")))
        is_item = bool(LIST_MARK_RE.match(ln))
        if excluded or is_item:
            if block:
                yield start, " ".join(block)
                block = []
            if caption:
                yield i, caption.group(1)
            if excluded:
                continue
            s = LIST_MARK_RE.sub("", s)
        if not block:
            start = i
        block.append(s)


def check_facts(rep, lines, stage, show_all=False):
    """Sentences with numbers but no claim tag or <!--nofact--> marker.

    Quantitative sentences (units, percentages, money, years) are errors at the final stage. So is a
    sentence with a number that cites a source but carries no claim tag: the number never reached
    the ledger, so nobody has verified it. Cited sentences without numbers or tags get one summary
    warning, because pointers ("for a survey, see …") are legitimate."""
    shown = hidden = 0
    pointers = []
    for start, text in fact_blocks(lines):
        text = ABBREV_RE.sub(lambda m: m.group(1).replace(".", "\u00b7"), text)
        parts = re.split(r"(?<=[.!?])\s+|(?<=[.!?][”\"’')\]])\s+", text)
        for i, part in enumerate(parts):
            s = re.sub(r"^\s*(?:<!--\s*(?:C:[^>]*|nofact[^>]*)-->\s*)+", "", part)
            if not s.strip():
                continue
            nxt = BADGE_RE.sub("", parts[i + 1].lstrip()) if i + 1 < len(parts) else ""
            if (TAG_START_RE.search(s) or NOFACT_START_RE.search(s)
                    or TAG_START_RE.match(nxt) or NOFACT_START_RE.match(nxt)):
                continue
            cited = "[@" in s
            probe = COMMENT_RE.sub(" ", s)
            probe = re.sub(r"\[[^\[\]]*@[^\[\]]*\]", " ", probe)
            probe = re.sub(r"\{[^{}]*\}", " ", probe)
            probe = re.sub(r"@[\w:.\-]+", " ", probe)
            probe = re.sub(r"\$[^$]*\$", " ", probe)
            probe = re.sub(r"`[^`\n]*`", " ", probe)
            probe = re.sub(r"\b(?:[Cc]hapters?|ch|Parts?|P|[Aa]ppendi(?:x|ces)|[Ss]ections?|[Ff]igures?"
                           r"|[Tt]ables?|[Ee]quations?|[Ss]teps?|[Ss]tages?|[Gg]ates?|G)\s?[\dA-Z]+(?:\.\d+)*\b", " ", probe)
            probe = LIST_MARK_RE.sub(" ", probe)
            probe = re.sub(r"\s+", " ", NAME_RE.sub(" ", probe))
            snippet = probe.strip()[:90]
            if not re.search(r"\d", probe):
                if cited:
                    pointers.append(start + 1)
                continue
            quant = bool(QUANT_RE.search(probe))
            if cited:
                only_year = not re.search(r"\d", re.sub(r"\b(?:19|20)\d{2}\b", " ", probe))
                if only_year and re.search(r"\bsee\b", s, re.I):
                    pointers.append(start + 1)        # "For a 2025 survey, see [@key]."
                else:
                    rep.by_stage(stage, "facts", f"line {start + 1}: sentence with numbers cites a source "
                                                 f"but has no claim tag: \"{snippet}\"")
                continue
            msg = (f"line {start + 1}: {'quantitative claim' if quant else 'number'} without citation "
                   f"or claim tag: \"{snippet}\"")
            if quant and stage == "final":
                rep.error("facts", msg + " (tag it, or mark illustrative numbers with <!--nofact-->)")
            elif quant or show_all or shown < 25:
                rep.warn("facts", msg)
                shown += 0 if quant else 1
            else:
                hidden += 1
    if hidden:
        rep.warn("facts", f"{hidden} more sentence(s) with numbers but no claim tag; list them all with --only facts")
    if pointers:
        where = ", ".join(str(n) for n in pointers[:8]) + (" …" if len(pointers) > 8 else "")
        rep.warn("facts", f"{len(pointers)} cited sentence(s) without a claim tag (lines {where}): fine for "
                          "pointers such as 'for a survey, see …'; a factual sentence needs its claim tag")


def check_mermaid_captions(rep, raw, stage):
    """A Mermaid caption that states a number needs a claim tag on the line after the closing fence."""
    for m in re.finditer(r"```\{mermaid\}(.*?)\n[ \t]*```[ \t]*\n([^\n]*)", raw, re.S):
        cap = re.search(r"^\s*%%\|\s*fig-cap:\s*(.*)$", m.group(1), re.M)
        if not cap:
            continue
        probe = re.sub(r"\[[^\[\]]*@[^\[\]]*\]", " ", cap.group(1))
        probe = NAME_RE.sub(" ", COMMENT_RE.sub(" ", probe))
        if re.search(r"\d", probe) and not (TAG_START_RE.match(m.group(2).strip())
                                            or NOFACT_START_RE.search(cap.group(1))):
            line = raw.count("\n", 0, m.start()) + 1
            rep.by_stage(stage, "facts", f"line {line}: Mermaid caption with numbers needs its claim tag on "
                                         f"the line right after the closing fence: \"{cap.group(1).strip()[:80]}\"")


def table_blocks(lines):
    """Yield (first_line_index, [(line_index, row), ...]) for each pipe table."""
    i, n = 0, len(lines)
    while i < n:
        if lines[i].lstrip().startswith("|"):
            start, rows = i, []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append((i, lines[i]))
                i += 1
            yield start, rows
        else:
            i += 1


def check_tables(rep, lines, stage):
    """Every table row that states numbers needs a claim tag (or the table an exemption:
    <!--nofact--> on the line just above it, for illustrative tables)."""
    mask = skip_mask(lines)
    for start, rows in table_blocks(lines):
        if mask[start]:
            continue
        j = start - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        if j >= 0 and NOFACT_RE.fullmatch(lines[j].strip()):
            continue
        for k, row in rows[1:]:
            if re.fullmatch(r"\s*\|[\s:|\-]+\|?\s*", row):
                continue                      # the separator line
            if TAG_START_RE.search(row) or NOFACT_START_RE.search(row):
                continue
            probe = COMMENT_RE.sub(" ", row)
            probe = re.sub(r"\[[^\[\]]*@[^\[\]]*\]", " ", probe)
            probe = re.sub(r"\$[^$]*\$", " ", probe)
            if not re.search(r"\d", probe):
                continue
            what = "cites a source but has no claim tag" if "[@" in row else "has no citation or claim tag"
            rep.by_stage(stage, "facts", f"line {k + 1}: table row with numbers {what}: "
                                         f"\"{probe.strip()[:80]}\"")


def check_quotes(rep, lines):
    count = 0
    keep = [l for l in lines if not l.strip().startswith((":::", "%%|", "#|"))]
    for _start, text in paragraphs(keep):
        text = COMMENT_RE.sub(" ", text)
        text = re.sub(r"\{[^{}]*\}", " ", text)
        spans = re.findall(r"“([^”]{1,800})”", text)
        spans += re.findall(r'(?<![\w=])"([^"]{1,800})"', text)
        spans += re.findall(r"(?:(?<=\s)|^)‘([^‘’]{1,800})’(?=[\s.,;:!?)]|$)", text)
        spans += re.findall(r"(?:(?<=\s)|^)'([^'\n]{40,800}?)'(?=[\s.,;:!?)]|$)", text)
        count += len(spans)
        for s in spans:
            n = len(s.split())
            if n > 15:
                rep.error("quotes", f"quotation over 15 words ({n}): \"{s[:80]}…\"")
    if count > 12:
        rep.warn("quotes", f"{count} quoted passages; prefer paraphrase (one quote per source per chapter)")


def check_spelling(rep, lines, allow):
    text = clean_for_keys("\n".join(lines))
    text = re.sub(r"\[@[^\]]*\]|@[\w:.\-]+", " ", text)
    text = re.sub(r"\$[^$]*\$", " ", text)
    found = collections.Counter()
    for m in re.finditer(r"\b[A-Za-z]+\b", text):
        w = m.group(0)
        if w != w.lower() or w in allow:     # capitalised words are usually names: leave them
            continue
        if w in US_TO_UK:
            found[(w, US_TO_UK[w])] += 1
    for m in IZE_RE.finditer(text):
        w = m.group(1)
        if w in allow or w in IZE_ALLOW:
            continue
        found[(w, re.sub(r"iz", "is", w, count=1))] += 1
    for (w, uk), n in sorted(found.items()):
        rep.warn("spelling", f"'{w}' ×{n} → '{uk}' (never change proper names; add them to scripts/spelling_allow.txt)")


def check_todos(rep, raw, stage):
    todos = len(TODO_RE.findall(raw))
    figs = len(FIG_MARKER_RE.findall(raw))
    if todos:
        rep.by_stage(stage, "todos", f"{todos} TODO marker(s) remain")
    if figs:
        rep.by_stage(stage, "todos", f"{figs} FIG marker(s) not yet replaced by figures")


def check_banned(rep, root, keys, bib, tags):
    banned = banned_domains(root)
    if not banned:
        return
    for k in sorted(set(keys)):
        url = bib.get(k, {}).get("url", "")
        if url and is_banned(url, banned):
            rep.error("banned", f"@{k} cites a banned domain: {url}")
    idx = ledger_index(root)
    for cid in sorted(set(tags)):
        url = idx.get(cid, {}).get("url", "")
        if url and is_banned(url, banned):
            rep.error("banned", f"{cid} comes from a banned domain: {url}")


def defined_labels(root):
    labels = set()
    for path in (root / "book").rglob("*.qmd"):
        if "_book" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        labels.update(LABEL_DEF_RE.findall(text))
        labels.update(CELL_LABEL_RE.findall(text))
    return labels


def check_crossrefs(rep, root, stripped, stage):
    used = set(XREF_USE_RE.findall(clean_for_keys(stripped).replace("{", " ")))
    if not used:
        return
    labels = defined_labels(root)
    for ref in sorted(used - labels):
        rep.by_stage(stage, "crossrefs", f"@{ref} does not resolve (forward references may point only to chapter labels like @sec-chNN)")


def stats(nn, raw, lines, keys, tags, ev_counts, n_concepts, heads):
    prose = COMMENT_RE.sub(" ", "\n".join(lines))
    prose = re.sub(r"\{[^{}]*\}", " ", prose)
    words = len(re.findall(r"[A-Za-z0-9’']+", prose))
    rng = find_h2(heads, lines, "Research prompts")
    prompts = sum(1 for ln in lines[rng[0] + 1:rng[1]] if re.match(r"^\s*\d+\.\s+\S", ln)) if rng else 0
    print(f"words: {words:,} · concepts: {n_concepts} · equations: {raw.count('{#eq-')} · "
          f"figures: {raw.count('{#fig-') + raw.count('label: fig-')} · tables: {raw.count('{#tbl-')}")
    evidence = ", ".join(f"{k}: {v}" for k, v in sorted(ev_counts.items()))
    print(f"sources cited: {len(set(keys))} · claim tags: {len(tags)} ({evidence}) · research prompts: {prompts}"
          f" · nofact markers: {len(NOFACT_RE.findall(raw))}")
    by_sec = collections.Counter(t[4:6] if t[1:3] == nn else "other" for t in tags)
    if by_sec:
        print("claim tags by section: " + " · ".join(
            f"s{k} {v}" if k != "other" else f"other chapters {v}" for k, v in sorted(by_sec.items())))


def check_one(root, ch_id, stage, only, want_stats=False):
    nn = norm_ch(ch_id)
    progress = load_progress(root)
    part, ch = find_chapter(progress, nn)
    if ch is None:
        print(f"Unknown chapter {ch_id}")
        return 1
    is_appendix = bool(part.get("appendix"))
    if is_appendix:
        path = root / "book" / "appendices" / f"{nn.lower()}-{ch['slug']}.qmd"
    else:
        path = chapter_file(root, nn)
    label = f"{'Appendix ' + nn if is_appendix else 'ch' + nn} · {ch['title']} · stage={stage}"
    if not path or not path.exists():
        print(f"{label}\nERROR [sections] chapter file not found")
        return 1
    raw = path.read_text(encoding="utf-8")
    if STUB_MARKER in raw:
        if ch["status"] in WRITTEN_STATUSES:
            print(f"{label}\nERROR [sections] file is still a stub but status is '{ch['status']}'")
            return 1
        print(f"{label}\nstub (status {ch['status']}): skipped")
        return 0
    rep = Report(label, set(only) if only else set())
    stripped = strip_code_and_math(raw)
    lines = stripped.splitlines()
    heads = headings(lines)
    allow = set(read_lines(root / "scripts" / "spelling_allow.txt"))
    n_concepts = 0
    if not is_appendix and rep.on("template"):
        n_concepts = check_template(rep, lines, heads)
    if not is_appendix and rep.on("sections"):
        check_sections(rep, nn, lines, heads, bool(ch.get("lifecycle")), stage)
    keys = cite_keys(stripped)
    bib = parse_bib(root)
    if rep.on("citations"):
        for k in sorted({k for k in keys if k not in bib}):
            rep.by_stage(stage, "citations", f"@{k} is not in book/references.bib")
        if not is_appendix:
            check_sources_include(rep, root, nn, keys, bib, stage)
    claim_rep = rep if rep.on("claims") else Report(label, {"__silent__"})
    tags, ev_counts = check_claims(claim_rep, root, nn, raw, stage, require_tags=not is_appendix, bib=bib)
    if rep.on("facts"):
        check_facts(rep, lines, stage, show_all=bool(only))
        check_tables(rep, lines, stage)
        check_mermaid_captions(rep, raw, stage)
    if rep.on("quotes"):
        check_quotes(rep, lines)
    if rep.on("spelling"):
        check_spelling(rep, lines, allow)
    if rep.on("todos"):
        check_todos(rep, raw, stage)
    if rep.on("banned"):
        check_banned(rep, root, keys, bib, tags)
    if rep.on("crossrefs"):
        check_crossrefs(rep, root, stripped, stage)
    print(label)
    for w in rep.warnings:
        print(w)
    for e in rep.errors:
        print(e)
    if want_stats:
        if not n_concepts and not is_appendix:
            n_concepts = sum(1 for h in heads if ".concept" in h[3])
        stats(nn, raw, lines, keys, tags, ev_counts, n_concepts, heads)
    print(f"Summary: {len(rep.errors)} errors, {len(rep.warnings)} warnings")
    return 1 if rep.errors else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chapter", nargs="?")
    ap.add_argument("--root")
    ap.add_argument("--stage", choices=["draft", "final"], default="final")
    ap.add_argument("--only", help="comma-separated categories: " + ",".join(CATEGORIES))
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--all", action="store_true", help="check every chapter whose status is drafted or later")
    args = ap.parse_args()
    root = root_from(args.root)
    only = [c.strip() for c in args.only.split(",")] if args.only else []
    bad = [c for c in only if c not in CATEGORIES]
    if bad:
        sys.exit(f"Unknown categories: {bad}")
    if args.all:
        progress = load_progress(root)
        code = 0
        for _part, ch in iter_chapters(progress):
            if ch["status"] in WRITTEN_STATUSES:
                code |= check_one(root, ch["id"], args.stage, only, args.stats)
                print()
        sys.exit(code)
    if not args.chapter:
        sys.exit("Give a chapter number or --all")
    sys.exit(check_one(root, args.chapter, args.stage, only, args.stats))


if __name__ == "__main__":
    main()
