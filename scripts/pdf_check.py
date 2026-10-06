#!/usr/bin/env python3
"""Check the PDF toolchain before it matters: TinyTeX, the book's PDF fonts (which must keep Greek
letters such as π0 and τ0 and symbols such as ≤ ≈ →), Mermaid diagrams (Chrome Headless Shell) and
SVG figures (rsvg-convert). Renders a one-page sample in a temporary folder, outside the book.

Usage:
  python3 scripts/pdf_check.py
Exit code 0 when the sample renders and every test glyph survives.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from common import root_from

GLYPHS = ["π0.5", "τ0", "≤", "≥", "≈", "→", "×", "µs", "±"]
SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 40"><title>Test</title>'
       '<rect x="2" y="2" width="116" height="36" fill="none" stroke="black"/>'
       '<text x="60" y="25" text-anchor="middle" font-size="12">SVG ok</text></svg>')


def pdf_fonts(root: Path) -> list:
    """The font lines from the pdf section of book/_quarto.yml."""
    path = root / "book" / "_quarto.yml"
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    return [ln.strip() for ln in lines if re.match(r"^\s+(main|sans|mono)font:", ln)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    args = ap.parse_args()
    root = root_from(args.root)
    quarto = shutil.which("quarto")
    if not quarto:
        sys.exit("FAIL quarto is not installed: brew install --cask quarto")
    fonts = pdf_fonts(root)
    tmp = Path(tempfile.mkdtemp(prefix="pdfcheck-"))
    try:
        (tmp / "figure.svg").write_text(SVG, encoding="utf-8")
        if fonts:
            header = ["---", 'title: "PDF check"', "format:", "  pdf:"] + ["    " + f for f in fonts] + ["---", ""]
        else:
            header = ["---", 'title: "PDF check"', "format: pdf", "---", ""]
        body = [f"Glyphs: {' '.join(GLYPHS)}", "",
                "```{mermaid}", "flowchart LR", "  A[Mermaid] --> B[ok]", "```", "",
                "![An SVG figure.](figure.svg)", ""]
        (tmp / "check.qmd").write_text("\n".join(header + body), encoding="utf-8")
        proc = subprocess.run([quarto, "render", "check.qmd", "--to", "pdf"], cwd=tmp,
                              capture_output=True, text=True, timeout=900)
        log = proc.stdout + proc.stderr
        pdf = tmp / "check.pdf"
        if proc.returncode != 0 or not pdf.exists():
            lines = log.strip().splitlines()
            key = [ln for ln in lines if re.search(r"FATAL|ERROR|^!|not found|cannot be found", ln)]
            print("FAIL the sample PDF did not render:")
            print("\n".join("  " + ln.strip() for ln in (key[:8] or lines[-12:])))
            hints = []
            if re.search(r"tinytex|no tex installation|pdflatex|lualatex.*not found", log, re.I):
                hints.append("quarto install tinytex")
            if re.search(r"font .* (not found|cannot be found)|fontspec", log, re.I):
                hints.append("brew install --cask font-dejavu   (the book's PDF fonts)")
            if re.search(r"chrom|puppeteer|browser", log, re.I):
                hints.append("quarto install chrome-headless-shell   (Mermaid diagrams)")
            if re.search(r"rsvg|svg", log, re.I):
                hints.append("brew install librsvg   (SVG figures)")
            for h in hints:
                print(f"  fix: {h}")
            sys.exit(1)
        exe = shutil.which("pdftotext")
        if not exe:
            sys.exit("FAIL pdftotext is missing, so the glyphs cannot be checked: brew install poppler")
        text = subprocess.run([exe, str(pdf), "-"], capture_output=True, text=True).stdout
        lost = [g for g in GLYPHS if g not in text]
        if lost:
            print(f"FAIL the PDF dropped these characters: {' '.join(lost)}")
            print("  fix: brew install --cask font-dejavu, and keep the mainfont/sansfont/monofont lines in "
                  "scripts/sync_quarto.py")
            sys.exit(1)
        print(f"PASS the PDF toolchain works and keeps {' '.join(GLYPHS)} (fonts: {', '.join(fonts) or 'default'})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
