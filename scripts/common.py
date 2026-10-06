"""Shared helpers for the production scripts. Standard library only (Python 3.9+)."""
from __future__ import annotations

import contextlib
import json
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

try:
    import fcntl
except ImportError:  # not POSIX: locking becomes a no-op
    fcntl = None

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

STATUSES = [
    "planned", "scouted", "researched", "blueprinted", "drafted",
    "checked", "revised", "edited", "done", "blocked",
]
# Statuses at which a chapter file is expected to contain real prose.
WRITTEN_STATUSES = {"drafted", "checked", "revised", "edited", "done"}

PRODUCTION_ORDER = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8",
                    "P9", "P10", "P11", "P12", "P0", "APP"]

CLAIM_TAG_RE = re.compile(r"<!--\s*C:(\d{2})\.(\d{2})-(\d{3})\s*-->")
CLAIM_ID_RE = re.compile(r"^C(\d{2})\.(\d{2})-(\d{3})$")
CROSSREF_PREFIXES = ("sec-", "fig-", "tbl-", "eq-", "lst-", "thm-", "lem-",
                     "cor-", "prp-", "cnj-", "def-", "exm-", "exr-")
STUB_MARKER = "<!-- STUB -->"


def root_from(arg: str | None) -> Path:
    return Path(arg).resolve() if arg else DEFAULT_ROOT


def norm_ch(value: str) -> str:
    """Normalise '7', 'ch7', 'ch07', '07' -> '07'. Appendix letters pass through upper-cased."""
    v = str(value).strip().lower()
    if v.startswith("ch"):
        v = v[2:]
    if v.isdigit():
        return f"{int(v):02d}"
    return v.upper()


def norm_sec(value: str) -> str:
    v = str(value).strip().lower().lstrip("s")
    return f"{int(v):02d}"


def load_progress(root: Path) -> dict:
    path = root / "state" / "progress.json"
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_progress(root: Path, data: dict) -> None:
    atomic_write(root / "state" / "progress.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")


@contextlib.contextmanager
def file_lock(path: Path):
    """Exclusive lock on <path>.lock, so parallel agents never interleave read-modify-write cycles."""
    lock_path = path.with_name(path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+") as fh:
        if fcntl:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def atomic_write(path: Path, text: str) -> None:
    """Write through a uniquely named temp file in the same folder, then rename over the target."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix="." + path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


def iter_chapters(progress: dict):
    """Yield (part, chapter) pairs in book order."""
    for part in progress["parts"]:
        for ch in part["chapters"]:
            yield part, ch


def find_chapter(progress: dict, ch_id: str):
    ch_id = norm_ch(ch_id)
    for part, ch in iter_chapters(progress):
        if ch["id"] == ch_id:
            return part, ch
    return None, None


def chapter_relpath(part: dict, ch: dict) -> str:
    """Path relative to book/ for a chapter or appendix."""
    if part.get("appendix"):
        return f"appendices/{ch['id'].lower()}-{ch['slug']}.qmd"
    return f"chapters/ch{ch['id']}-{ch['slug']}.qmd"


def chapter_file(root: Path, ch_id: str) -> Path | None:
    ch_id = norm_ch(ch_id)
    progress = load_progress(root)
    part, ch = find_chapter(progress, ch_id)
    if ch is not None:
        p = root / "book" / chapter_relpath(part, ch)
        if p.exists():
            return p
    # Fall back to a glob, in case the slug changed.
    matches = sorted((root / "book" / "chapters").glob(f"ch{ch_id}-*.qmd"))
    return matches[0] if matches else None


def load_ledger(root: Path, ch_id: str | None = None):
    """Return a list of (path, line_no, obj_or_None, error_or_None)."""
    base = root / "ledger"
    if ch_id is None:
        files = sorted(base.glob("ch*/*.jsonl"))
    else:
        files = sorted((base / f"ch{norm_ch(ch_id)}").glob("*.jsonl"))
    rows = []
    for f in files:
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                rows.append((f, i, json.loads(line), None))
            except json.JSONDecodeError as exc:
                rows.append((f, i, None, f"invalid JSON: {exc.msg}"))
    return rows


def ledger_index(root: Path, ch_id: str | None = None) -> dict:
    """Map claim id -> claim object, later lines winning (they should not repeat ids)."""
    index = {}
    for _f, _i, obj, err in load_ledger(root, ch_id):
        if obj and not err and isinstance(obj.get("id"), str):
            index[obj["id"]] = obj
    return index


BIB_ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,")


def parse_bib(root: Path) -> dict:
    """Very small BibTeX reader: key -> {'type':..., field: value}. Good enough for checks."""
    path = root / "book" / "references.bib"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    entries = {}
    positions = [(m.start(), m.group(1).lower(), m.group(2)) for m in BIB_ENTRY_RE.finditer(text)]
    for idx, (start, etype, key) in enumerate(positions):
        end = positions[idx + 1][0] if idx + 1 < len(positions) else len(text)
        body = text[start:end]
        fields = {"type": etype}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            name = fm.group(1).lower()
            j = fm.end()
            if j >= len(body):
                continue
            if body[j] == "{":
                depth, k = 0, j
                while k < len(body):
                    if body[k] == "{":
                        depth += 1
                    elif body[k] == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    k += 1
                value = body[j + 1:k]
            elif body[j] == '"':
                k = body.find('"', j + 1)
                value = body[j + 1:k if k != -1 else len(body)]
            else:
                m2 = re.match(r"[^,\n}]+", body[j:])
                value = m2.group(0) if m2 else ""
            fields.setdefault(name, re.sub(r"\s+", " ", value.replace("{", "").replace("}", "")).strip())
        entries[key] = fields
    return entries


def strip_code_and_math(text: str) -> str:
    """Blank fenced code (except figure-caption option lines) and display maths, keeping line numbers."""
    out_lines = []
    in_fence = False
    in_math = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out_lines.append("")
            continue
        if in_fence:
            # Keep figure-caption option lines: captions are prose and may cite sources.
            out_lines.append(line if re.match(r"^\s*(?:%%|#)\|\s*fig-cap:", line) else "")
            continue
        if stripped.startswith("$$"):
            # A single-line $$...$$ block, or the start/end of a multi-line one.
            if stripped.count("$$") >= 2 and len(stripped) > 2 and not in_math:
                out_lines.append("")
                continue
            in_math = not in_math
            out_lines.append("")
            continue
        if in_math:
            out_lines.append("")
            continue
        out_lines.append(line)
    return "\n".join(out_lines)


def read_lines(path: Path) -> list[str]:
    """Non-empty lines, with comments (# to end of line) removed."""
    if not path.exists():
        return []
    out = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.split("#", 1)[0].strip()
        if ln:
            out.append(ln)
    return out


def banned_domains(root: Path) -> list[str]:
    return [d.lower().lstrip(".") for d in read_lines(root / "scripts" / "banned_domains.txt")]


TRACKING_PARAMS = re.compile(r"^(?:utm_\w+|fbclid|gclid|dclid|msclkid|mc_cid|mc_eid|_hsenc|_hsmi|igshid|si"
                             r"|ref|ref_src|ref_url|feature|share)$", re.I)


def source_id(url: str) -> str:
    """A normalised identity for a source document.

    - arXiv papers by id, whatever the version, page type or arXiv DOI (10.48550/arXiv.X).
    - Other DOIs by DOI. A published version has its own DOI, so it is a different document
      from its arXiv preprint and needs its own key.
    - YouTube videos by video id; X/Twitter posts by path.
    - Other pages by host, path and identifying query parameters (?v=, ?id=, ?uri=, ?arnumber=),
      ignoring www., fragments, trailing slashes and tracking parameters."""
    u = str(url or "").strip()
    m = re.search(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/[0-9]{7})", u, re.I)
    if m:
        return "arxiv:" + m.group(1).lower()
    m = re.search(r"(?:doi\.org/|doi:\s*)(10\.\d{4,9}/[^\s?#]+)", u, re.I)
    if m:
        doi = m.group(1).lower().rstrip(".")
        ax = re.match(r"10\.48550/arxiv\.(.+?)(?:v\d+)?$", doi)
        return "arxiv:" + ax.group(1) if ax else "doi:" + doi
    p = urlparse(u if "://" in u else "https://" + u)
    host = (p.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    for prefix in ("m.", "mobile."):
        if host.startswith(prefix) and host[len(prefix):] in ("youtube.com", "twitter.com", "x.com"):
            host = host[len(prefix):]
    path = re.sub(r"/+$", "", p.path or "")
    params = [(k, v) for k, v in parse_qsl(p.query) if not TRACKING_PARAMS.match(k)]
    if host == "youtu.be":
        return "youtube.com/watch?v=" + path.strip("/")
    if host == "youtube.com":
        vid = dict(params).get("v") or (path.split("/")[2] if path.startswith(("/shorts/", "/live/", "/embed/")) else "")
        return "youtube.com/watch?v=" + vid if vid else host + path
    if host in ("twitter.com", "x.com"):
        return "x.com" + path
    query = "&".join(f"{k}={v}" for k, v in sorted(params))
    return host + path + ("?" + query if query else "")


def bib_source_ids(entry: dict) -> set:
    """Every identity a references.bib entry can be matched on: its url, doi and arXiv eprint."""
    ids = set()
    if entry.get("url"):
        ids.add(source_id(entry["url"]))
    if entry.get("doi"):
        ids.add(source_id("https://doi.org/" + entry["doi"].strip()))
    if entry.get("eprint"):
        ids.add("arxiv:" + re.sub(r"v\d+$", "", entry["eprint"].strip().lower()))
    return ids


def is_banned(url: str, banned) -> bool:
    host = (urlparse(str(url)).hostname or "").lower()
    return bool(host) and any(host == d or host.endswith("." + d) for d in banned)
