#!/usr/bin/env python3
"""Fetch the plain text of a web page or PDF, so verbatim passages can be captured and checked
exactly. WebFetch returns a model's summary of a page: fine for reading, not for verbatim checks.

Rules (docs/SOURCES.md):
- Use it only on a URL that WebFetch has already read in this task. If WebFetch declined a site,
  do not fetch that site any other way.
- It obeys robots.txt (including Crawl-delay, shared across parallel agents) and stops on HTTP 401,
  402, 403 and 451. A refusal only rules out verbatim capture: keep WebFetch's reading and note
  "not exact-matched". Never work around it.
- Never save full texts in the repository. Extracted text is cached for three days in the system
  temp folder, so checking many claims from one source fetches it once.

Usage:
  python3 scripts/fetch_text.py URL_OR_FILE                          # print the text (paged)
  python3 scripts/fetch_text.py URL_OR_FILE --offset 20000           # next page
  python3 scripts/fetch_text.py URL_OR_FILE --find "exact phrase" [--find "another"] [--context 300]

Batch every phrase for one URL into a single call. --find matching ignores case, whitespace,
curly-vs-straight quotes, dash types, ligatures and soft hyphens, then prints the passage exactly as
the source has it. arXiv abstract pages are read from the paper's PDF.

Exit codes: 0 ok · 1 a --find phrase was not found in the document · 2 fetch failed, rate-limited,
or a bot-check page instead of the document (nothing can be concluded about the claim) · 3 refused
(robots.txt or HTTP 401/402/403/451) · 4 the document is a PDF and pdftotext is missing
(brew install poppler)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path

from common import file_lock

UA = "HumanoidTextbookFactCheck/1.0 (non-commercial research; respects robots.txt)"
TIMEOUT = 30
MAX_BYTES = 30 * 1024 * 1024
REFUSED = {401, 402, 403, 451}
TRY_LATER = {429, 503}
CACHE_DIR = Path(tempfile.gettempdir()) / "humanoid-textbook-fetch"
CACHE_TTL = 3 * 24 * 3600
MAX_WAIT = 30                       # seconds: the longest we sleep for Retry-After or Crawl-delay
MAX_QUEUE = 75                      # seconds: the longest we queue behind other agents for one host
CHALLENGE_RE = re.compile(r"verifying (?:you are human|your browser)|client challenge|just a moment|"
                          r"attention required|access denied|are you a robot|captcha|security check|"
                          r"enable javascript and cookies|checking your browser", re.I)
SKIP_TAGS = {"script", "style", "noscript", "svg", "template"}
BLOCK_TAGS = {"p", "div", "br", "li", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "section",
              "article", "header", "footer", "blockquote", "pre", "table", "ul", "ol", "dd", "dt",
              "figcaption", "main", "aside", "nav", "hr"}
CHAR_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'", "`": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"', "«": '"', "»": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "―": "-", "−": "-",
    "­": "", "​": "", "‌": "", "‍": "", "﻿": "",
}


def die(code: int, msg: str):
    print(msg, file=sys.stderr)
    sys.exit(code)


def refuse(why: str):
    die(3, f"REFUSED: {why}. fetch_text will not read this page, and nothing may work around that. "
           "If WebFetch could read it, keep WebFetch's reading and note 'not exact-matched'; otherwise "
           "use another source, or the abstract only (access: \"abstract\").")


def cache_path(kind: str, key: str) -> Path:
    return CACHE_DIR / f"{kind}-{hashlib.sha1(key.encode('utf-8')).hexdigest()}.json"


def cache_get(kind: str, key: str, ttl: int):
    path = cache_path(kind, key)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - data.get("time", 0) < ttl:
            return data
    except (OSError, ValueError):
        pass
    return None


def cache_put(kind: str, key: str, data: dict) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        data = dict(data, time=time.time())
        tmp = cache_path(kind, key).with_suffix(".tmp%d" % id(data))
        tmp.write_text(json.dumps(data), encoding="utf-8")
        tmp.replace(cache_path(kind, key))
    except OSError:
        pass                                   # the cache is an optimisation only


def polite_wait(host: str, delay: float) -> None:
    """Space requests to one host across all parallel agents by at least `delay` seconds.
    Each call reserves the next free slot under a short lock, then sleeps without holding it. A
    slot more than MAX_QUEUE seconds away means the host is busy: exit 2 and let the agent retry."""
    delay = min(max(delay, 1.0), MAX_WAIT)
    marker = CACHE_DIR / f"host-{hashlib.sha1(host.encode('utf-8')).hexdigest()}"
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with file_lock(marker):
            try:
                last = float(marker.read_text() or 0)
            except (OSError, ValueError):
                last = 0.0
            now = time.time()
            slot = max(now, last + delay)
            if slot - now > MAX_QUEUE:
                die(2, f"FAILED: {host} is busy (other agents are queued behind its Crawl-delay of {delay:.0f} s). "
                       "Not a refusal: retry in a minute, or check another source first.")
            marker.write_text(str(slot))
    except OSError:
        return
    if slot > now:
        print(f"waiting {slot - now:.0f} s for {host} (Crawl-delay)", file=sys.stderr)
        time.sleep(slot - now)


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.title, self.in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        elif tag == "title":
            self.in_title = True
        elif tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        if tag in ("br", "hr"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
        elif tag == "title":
            self.in_title = False
        elif tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif not self.skip:
            self.parts.append(data)

    def text(self) -> str:
        t = "".join(self.parts)
        t = re.sub(r"[ \t\r\f\v ]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        return re.sub(r"\n{3,}", "\n\n", t).strip()


def robots_info(url: str):
    """Return (allowed, crawl_delay_seconds) for this URL under the site's robots.txt."""
    parts = urllib.parse.urlsplit(url)
    robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
    cached = cache_get("robots", robots_url, 24 * 3600)
    if cached is not None:
        body, code = cached.get("body", ""), cached.get("code", 200)
    else:
        req = urllib.request.Request(robots_url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                body, code = resp.read(512 * 1024).decode("utf-8", errors="replace"), 200
        except urllib.error.HTTPError as exc:
            body, code = "", exc.code
        except (urllib.error.URLError, OSError, ValueError):
            body, code = "", 0                 # no reachable robots.txt
        cache_put("robots", robots_url, {"body": body, "code": code})
    if code in (401, 403):
        return False, 0.0                      # as urllib.robotparser does: 401/403 means "disallow all"
    if code != 200:
        return True, 0.0
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.splitlines())
    delay = rp.crawl_delay(UA) or 0
    return rp.can_fetch(UA, url), float(delay)


def robots_allows(url: str) -> bool:
    return robots_info(url)[0]


def fetch_url(url: str):
    allowed, delay = robots_info(url)
    host = urllib.parse.urlsplit(url).netloc
    if not allowed:
        refuse(f"robots.txt of {host} disallows this page")
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,text/plain;q=0.8,*/*;q=0.5"})
    for attempt in (1, 2):
        polite_wait(host, delay)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = resp.read(MAX_BYTES + 1)
                ctype = resp.headers.get("Content-Type", "") or ""
                final = resp.geturl()
            break
        except urllib.error.HTTPError as exc:
            if exc.code in REFUSED:
                refuse(f"HTTP {exc.code} from {url}")
            if exc.code in TRY_LATER and attempt == 1:
                try:
                    wait = float(exc.headers.get("Retry-After", "") or 10) if exc.headers else 10.0
                except ValueError:
                    wait = 10.0
                time.sleep(min(max(wait, delay, 1.0), MAX_WAIT))
                continue
            if exc.code in TRY_LATER:
                die(2, f"FAILED: {host} is rate-limiting (HTTP {exc.code}). Not a refusal: try again later, "
                       "and batch all phrases for one URL into a single call.")
            die(2, f"FAILED: HTTP {exc.code} {exc.reason} for {url}")
        except urllib.error.URLError as exc:
            reason = str(exc.reason)
            if "CERTIFICATE_VERIFY_FAILED" in reason:
                die(2, "FAILED: certificate verification failed. If your Python came from python.org, run "
                       "'Install Certificates.command' in its Applications folder. Never disable verification.")
            die(2, f"FAILED: could not reach {url}: {reason}")
        except (OSError, ValueError) as exc:
            die(2, f"FAILED: {url}: {exc}")
    if len(data) > MAX_BYTES:
        die(2, f"FAILED: {url} is larger than {MAX_BYTES // (1024 * 1024)} MB")
    if urllib.parse.urlsplit(final).netloc != urllib.parse.urlsplit(url).netloc and not robots_allows(final):
        refuse(f"redirected to {final}, which robots.txt disallows")
    return data, ctype, final


def pdf_to_text(data: bytes) -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        die(4, "This is a PDF and pdftotext is not installed. Install it with: brew install poppler")
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "doc.pdf"
        pdf.write_bytes(data)
        proc = subprocess.run([exe, "-enc", "UTF-8", str(pdf), "-"], capture_output=True, timeout=180)
    if proc.returncode != 0:
        die(2, f"FAILED: pdftotext could not read this PDF: {proc.stderr.decode(errors='replace')[:200]}")
    return proc.stdout.decode("utf-8", errors="replace")


def decode(data: bytes, ctype: str) -> str:
    enc = None
    m = re.search(r"charset=([\w.:-]+)", ctype, re.I)
    if m:
        enc = m.group(1)
    else:
        m = re.search(rb"<meta[^>]+charset=[\"']?([\w.:-]+)", data[:4096], re.I)
        if m:
            enc = m.group(1).decode("ascii", errors="ignore")
    try:
        return data.decode(enc or "utf-8", errors="replace")
    except LookupError:
        return data.decode("utf-8", errors="replace")


def to_text(data: bytes, ctype: str, name: str):
    """Return (title, text)."""
    if data[:5] == b"%PDF-" or "pdf" in ctype.lower() or name.lower().endswith(".pdf"):
        return "", pdf_to_text(data)
    raw = decode(data, ctype)
    head = raw[:2000].lower()
    if "html" in ctype.lower() or name.lower().endswith((".html", ".htm")) or "<html" in head or "<!doctype html" in head:
        parser = TextExtractor()
        parser.feed(raw)
        parser.close()
        return re.sub(r"\s+", " ", parser.title).strip(), parser.text()
    return "", raw.strip()


def normalise(text: str, dehyphenate: bool = False):
    """Return (normalised text, index map back into the original text)."""
    out, idx = [], []
    n = len(text)
    i = 0
    space = True
    while i < n:
        ch = text[i]
        if dehyphenate and ch in "-­‐" and i + 1 < n and text[i + 1] == "\n":
            j = i + 1
            while j < n and text[j].isspace():
                j += 1
            if j < n and text[j].islower():
                i = j
                continue
        ch = CHAR_MAP.get(ch, ch)
        for c in unicodedata.normalize("NFKC", ch).casefold() if ch else "":
            c = CHAR_MAP.get(c, c)
            if not c:
                continue
            if c.isspace():
                if space:
                    continue
                c, space = " ", True
            else:
                space = False
            out.append(c)
            idx.append(i)
        i += 1
    return "".join(out), idx


class Matcher:
    """Finds phrases in a text, caching the normalised forms of the text."""

    def __init__(self, text: str):
        self.text = text
        self._cache = {}

    def norm(self, dehyphenate: bool):
        if dehyphenate not in self._cache:
            self._cache[dehyphenate] = normalise(self.text, dehyphenate)
        return self._cache[dehyphenate]

    def excerpt(self, idx, pos, length, context):
        text = self.text
        a, b = idx[pos], idx[pos + length - 1] + 1
        lo, hi = max(0, a - context), min(len(text), b + context)
        out = ("…" if lo else "") + text[lo:a] + "»" + text[a:b] + "«" + text[b:hi] + ("…" if hi < len(text) else "")
        return re.sub(r"\s+", " ", out)

    def loose(self):
        """The normalised text with punctuation turned into spaces, for the closest-match search."""
        if "loose" not in self._cache:
            norm, idx = self.norm(True)
            out, lidx, space = [], [], True
            for c, i in zip(norm, idx):
                if not (c.isalnum() or c == "%"):
                    if space:
                        continue
                    c, space = " ", True
                else:
                    space = False
                out.append(c)
                lidx.append(i)
            self._cache["loose"] = ("".join(out), lidx)
        return self._cache["loose"]

    def find(self, phrase: str, context: int):
        """Return (count, excerpt) for the first match, or (0, diagnostic)."""
        target = normalise(phrase)[0].strip()
        if not target:
            return 0, "empty phrase"
        for dehyph in (False, True):
            norm, idx = self.norm(dehyph)
            pos = norm.find(target)
            if pos >= 0:
                return norm.count(target), self.excerpt(idx, pos, len(target), context)
        # Not found: report the longest run of the phrase's words that does occur, ignoring punctuation.
        norm, idx = self.loose()
        words = re.sub(r"[^\w%]+", " ", target).split()
        for size in range(len(words) - 1, 3, -1):
            for start in range(0, len(words) - size + 1):
                chunk = " ".join(words[start:start + size])
                pos = norm.find(chunk)
                if pos >= 0:
                    return 0, (f"closest match ({size} of {len(words)} words): "
                               + self.excerpt(idx, pos, len(chunk), context))
        return 0, "no run of 4 or more of its words occurs in the source"


def interstitial(final: str, title: str, text: str) -> bool:
    """True when the fetched page is a bot check or JavaScript wall, not the document."""
    path = urllib.parse.urlsplit(final).path.lower()
    return ("challenge" in path or "captcha" in path or bool(CHALLENGE_RE.search(title or ""))
            or (len(text) < 1500 and bool(CHALLENGE_RE.search(text))))


def get_text(source: str, use_cache: bool = True):
    """Return (final_url, title, text, is_pdf) for a URL or a local file."""
    if not re.match(r"^https?://", source, re.I):
        path = Path(source).expanduser()
        if not path.is_file():
            die(2, f"FAILED: no such file: {path}")
        data = path.read_bytes()
        title, text = to_text(data, "", path.name)
        return str(path), title, text, data[:5] == b"%PDF-"
    url = source
    m = re.match(r"^https?://(?:www\.)?arxiv\.org/abs/(\S+?)/?$", url, re.I)
    if m:
        url = f"https://arxiv.org/pdf/{m.group(1)}"
        print(f"note: arXiv abstract page, so reading the paper's PDF: {url}")
    if use_cache:
        hit = cache_get("text", url, CACHE_TTL)
        if hit:
            return hit["final"], hit["title"], hit["text"], hit.get("pdf", False)
    data, ctype, final = fetch_url(url)
    title, text = to_text(data, ctype, urllib.parse.urlsplit(final).path)
    is_pdf = data[:5] == b"%PDF-"
    if text.strip() and not interstitial(final, title, text):
        cache_put("text", url, {"final": final, "title": title, "text": text, "pdf": is_pdf})
    return final, title, text, is_pdf


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="http(s) URL, or a local file path")
    ap.add_argument("--find", action="append", default=[], metavar="PHRASE")
    ap.add_argument("--context", type=int, default=250, help="characters of context around a match")
    ap.add_argument("--max-chars", type=int, default=20000)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--no-cache", action="store_true", help="fetch again even if a cached copy exists")
    args = ap.parse_args()

    final, title, text, is_pdf = get_text(args.source, use_cache=not args.no_cache)
    if not text.strip():
        die(2, "FAILED: no text could be extracted (the page may need JavaScript, or the PDF may be scanned "
               "images). Nothing can be concluded about the claim: keep WebFetch's reading and note "
               "'not exact-matched'.")
    if not is_pdf and interstitial(final, title, text):
        die(2, f"FAILED: {final} returned a bot check or JavaScript page (\"{title or text[:60]}\"), not the "
               "document. Nothing can be concluded about the claim: keep WebFetch's reading and note "
               "'not exact-matched'.")

    print(f"source: {final}")
    if title:
        print(f"title: {title}")
    print(f"characters: {len(text):,}")
    if len(text) < 1500 and not is_pdf:
        print("WARNING: very short page. Check that it is the document itself (not a cookie wall, a "
              "script-rendered page or an abstract) before concluding that a phrase is missing.")
    if args.find:
        missing = 0
        matcher = Matcher(text)
        for phrase in args.find:
            count, excerpt = matcher.find(phrase, args.context)
            if count:
                print(f"\nFOUND ({count}×): {phrase[:80]}\n  {excerpt}")
            else:
                missing += 1
                print(f"\nNOT FOUND: {phrase[:80]}\n  {excerpt}")
        sys.exit(1 if missing else 0)
    chunk = text[args.offset:args.offset + args.max_chars]
    print("-" * 60)
    print(chunk)
    rest = len(text) - (args.offset + len(chunk))
    if rest > 0:
        print("-" * 60)
        print(f"[{rest:,} more characters: rerun with --offset {args.offset + len(chunk)}]")


if __name__ == "__main__":
    main()
