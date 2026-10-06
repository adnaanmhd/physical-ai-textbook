#!/usr/bin/env python3
"""Validate original SVG figures: well-formed XML with an <svg> root, a viewBox and a <title>; no
scripts or event handlers; no external references; no embedded raster images (figures are drawn,
never pasted in from a source).

Usage:
  python3 scripts/check_svg.py book/figures/chNN/name.svg [more.svg ...]
  python3 scripts/check_svg.py --ch NN          # every SVG in book/figures/chNN/
"""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import norm_ch, root_from


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def check(path: Path):
    errors, warnings = [], []
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"not well-formed XML: {exc}"], []
    root = tree.getroot()
    if local(root.tag) != "svg":
        errors.append(f"root element is <{local(root.tag)}>, not <svg>")
    if "viewBox" not in root.attrib:
        warnings.append("no viewBox, so the figure will not scale cleanly")
    if not any(local(el.tag) == "title" for el in root):
        warnings.append("no <title> child of <svg> (needed for accessibility)")
    for el in root.iter():
        name = local(el.tag)
        if name in ("script", "foreignObject"):
            errors.append(f"<{name}> is not allowed")
        if name == "image":
            errors.append("<image> embeds a picture: draw the figure instead")
        for attr, val in el.attrib.items():
            a = local(attr)
            if a.lower().startswith("on"):
                errors.append(f"event handler {a} on <{name}>")
            if a == "href" and not str(val).startswith("#"):
                errors.append(f"external reference {str(val)[:60]} on <{name}>")
            if "url(" in str(val) and "url(#" not in str(val).replace(" ", ""):
                errors.append(f"external url() in {a} on <{name}>")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--ch")
    ap.add_argument("--root")
    args = ap.parse_args()
    files = [Path(f) for f in args.files]
    if args.ch:
        folder = root_from(args.root) / "book" / "figures" / f"ch{norm_ch(args.ch)}"
        found = sorted(folder.glob("*.svg"))
        if not found and not files:
            print(f"no SVG figures in {folder}: nothing to check")
            return
        files += found
    if not files:
        sys.exit("No SVG files given")
    bad = 0
    for f in files:
        errors, warnings = check(f)
        for w in warnings:
            print(f"WARN  {f}: {w}")
        for e in errors:
            print(f"ERROR {f}: {e}")
        if errors:
            bad += 1
        else:
            print(f"ok    {f}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
