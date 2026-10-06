#!/usr/bin/env python3
"""Self-test for the production scripts. Builds a throwaway project in a temp folder, runs every
script against it, and checks that good input passes and bad input fails. Needs no network.

Usage:
  python3 scripts/selftest.py
"""
from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))

CHAPTER = """# The sim-to-real gap {#sec-ch29}

Robots increasingly learn their skills in simulation before they touch real hardware. This
chapter explains why those skills stumble when they meet the real world, how engineers measure
the stumble, and the main ways to close the gap. It matters for deployment because every skill
learned in simulation must survive real floors, real objects and real sensors.

## Closing the gap {#sec-ch29-closing}

### Domain randomisation {#sec-ch29-domain-randomisation .concept}

::: {.callout-tip title="ELI5"}
Practise catching in wind, rain and glare, and a stormy day feels like one more variation.
:::

::: {.callout-note title="First principles"}
A simulator is never an exact copy of reality, so a policy trained on one setting exploits its
quirks. If the simulated box always weighs 2 kg, a real 3 kg box surprises the policy. <!--nofact-->
Randomising the uncertain quantities forces behaviour that works across the whole range.
:::

**How it's actually done.** The idea was popularised for vision by randomising textures,
lighting and camera poses, so that a detector trained only on rendered images worked on real
images [@tobin2017domain]. <!--C:29.03-001--> In 2017, Tobin et al. showed this with rendered
images alone [@tobin2017domain]. <!--C:29.03-001--> Later work widened the ranges automatically as
the policy improved [@openai2019rubiks]. <!--C:29.03-002--> Chapter 52 returns to the idea (@sec-ch52).

::: {.callout-important title="Deployment lens"}
What breaks: conditions outside the randomised ranges. What to measure: success as parameters
approach the edges of their ranges. How it improves: widen the ranges that field logs show were
too narrow, then retrain.
:::

## Key takeaways {#sec-ch29-takeaways}

::: {.callout-tip title="Key takeaways"}
- Simulators are always wrong in small ways.
- Randomisation trades peak performance for robustness.
- Field logs show which ranges were too narrow.
- Automatic randomisation widens the ranges as the policy improves.
- Transfer has to be measured on the real robot, never assumed.
:::

## People, tools and costs {#sec-ch29-ptc}

Simulation engineers and controls engineers share this work.

## Research prompts {#sec-ch29-prompts}

1. Find a recent paper that measures sim-to-real transfer for a humanoid. *A strong answer names the metric.*
2. Compare two randomisation schemes. *A strong answer states the trade-off.*
3. Design an acceptance test for a transferred skill. *A strong answer defines success.*
4. Critique a public claim of zero-shot transfer. *A strong answer checks the conditions.*
5. Apply randomisation to the greenhouse example. *A strong answer lists the parameters.*

## Sources for this chapter {#sec-ch29-sources}

{{< include _sources/ch29.qmd >}}
"""

def _ch(cid, slug, title, lifecycle=False):
    return {"id": cid, "slug": slug, "title": title, "lifecycle": lifecycle, "status": "planned", "notes": ""}


# A frozen chapter list, so legitimate outline changes after gate G1 cannot break the self-test.
PROGRESS = {
    "book": {"title": "Test Book", "subtitle": "Fixture", "current_as_of": None, "pilot": "29", "last": "01"},
    "parts": [
        {"id": "P0", "title": "Orientation", "chapters": [_ch("01", "lifecycle-on-one-page", "The lifecycle on one page")]},
        {"id": "P1", "title": "The body", "chapters": [_ch("04", "anatomy", "Anatomy")]},
        {"id": "P5", "title": "Simulation", "chapters": [
            _ch("27", "simulators", "Simulators"), _ch("28", "training-in-simulation", "Training in simulation", True),
            _ch("29", "sim-to-real-gap", "The sim-to-real gap", True)]},
        {"id": "P12", "title": "Landscape", "chapters": [_ch("52", "open-problems", "Open problems")]},
        {"id": "APP", "title": "Appendices", "appendix": True, "chapters": [
            _ch("A", "data-dictionary", "Data dictionary"), _ch("E", "glossary", "Glossary")]},
    ],
}

TAKEAWAYS = """# What the reader knows so far

## ch28 · Training in simulation
- Simulation makes practice cheap.

## ch52 · Open problems
- A later chapter that must never count as known before ch29.
"""

BIB = """@misc{smith2025survey,
  title = {A Fixture Survey},
  author = {Smith, Ann},
  year = {2025},
  url = {https://example.org/survey},
  note = {evidence: preprint}
}

@inproceedings{tobin2017domain,
  title = {Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World},
  author = {Tobin, Josh and Fong, Rachel and Ray, Alex and Schneider, Jonas and Zaremba, Wojciech and Abbeel, Pieter},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year = {2017},
  url = {https://arxiv.org/abs/1703.06907},
  note = {evidence: peer-reviewed}
}

@misc{openai2019rubiks,
  title = {Solving Rubik's Cube with a Robot Hand},
  author = {{OpenAI}},
  year = {2019},
  eprint = {1910.07113},
  archivePrefix = {arXiv},
  url = {https://arxiv.org/abs/1910.07113},
  note = {evidence: preprint}
}
"""

HTML = """<!doctype html><html><head><title>Test page</title><style>.x { color: red }</style></head>
<body><p>The robot’s grasp succeeded in 56 % of trials—across thirty   homes.</p>
<script>var secret = "hidden words never shown";</script>
<p>A second para-
graph about grippers.</p></body></html>
"""

GOOD_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><title>Test</title>'
            '<rect x="1" y="1" width="98" height="48" fill="none" stroke="currentColor"/></svg>')
BAD_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><title>Copied</title>'
           '<image href="https://example.com/figure3.png" width="100" height="50"/></svg>')


def claim(n, key, url, evidence, published, status="verified"):
    return {
        "id": f"C29.03-{n:03d}", "chapter": "29", "section": "03",
        "claim": f"Test claim number {n}, paraphrased in the researcher's own words.",
        "type": "result", "source_key": key, "url": url,
        "source_type": "peer-reviewed" if evidence == "peer-reviewed" else "preprint",
        "evidence": evidence, "published": published, "accessed": "2026-01-15", "access": "full",
        "support": "short verbatim passage for verification", "volatile": n == 2, "status": status,
    }


NEW_CLAIM = {
    "claim": "Automatic domain randomisation widened the randomisation ranges during training.",
    "type": "mechanism", "source_key": "openai2019rubiks", "url": "https://arxiv.org/abs/1910.07113",
    "source_type": "preprint", "evidence": "preprint", "published": "2019-10", "access": "full",
    "support": "short verbatim passage", "volatile": False,
}


def source(key, priority):
    return {"key": key, "title": f"Title of {key}", "authors_or_org": "Someone", "published": "2026-05",
            "url": f"https://arxiv.org/abs/{key}", "source_type": "preprint", "evidence": "preprint",
            "sections": [], "why": "test", "priority": priority, "access": "full"}


def run(root, *args, stdin=None):
    proc = subprocess.run([sys.executable, *map(str, args), "--root", str(root)],
                          capture_output=True, text=True, input=stdin)
    return proc.returncode, proc.stdout + proc.stderr


def run_plain(*args):
    proc = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


FAILS = []


def expect(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        FAILS.append(name)
        if detail:
            print("      " + detail.strip().replace("\n", "\n      ")[:1500])


def main():
    tmp = Path(tempfile.mkdtemp(prefix="booktest-"))
    S = HERE
    try:
        # ------------------------------------------------------------ project fixture
        (tmp / "state").mkdir()
        (tmp / "state" / "progress.json").write_text(json.dumps(PROGRESS, indent=2), encoding="utf-8")
        (tmp / "state" / "takeaways.md").write_text(TAKEAWAYS, encoding="utf-8")
        (tmp / "scripts").mkdir()
        for name in ("banned_domains.txt", "spelling_allow.txt"):
            if (HERE / name).exists():
                shutil.copy(HERE / name, tmp / "scripts" / name)
        (tmp / "book" / "chapters").mkdir(parents=True)
        chap = tmp / "book" / "chapters" / "ch29-sim-to-real-gap.qmd"
        chap.write_text(CHAPTER, encoding="utf-8")
        (tmp / "book" / "references.bib").write_text(BIB, encoding="utf-8")
        led = tmp / "ledger" / "ch29"
        led.mkdir(parents=True)
        rows = [claim(1, "tobin2017domain", "https://arxiv.org/abs/1703.06907", "peer-reviewed", "2017-03"),
                claim(2, "openai2019rubiks", "https://arxiv.org/abs/1910.07113", "preprint", "2019-10")]
        (led / "s03.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")

        # ------------------------------------------------------------ sync_quarto
        code, out = run(tmp, S / "sync_quarto.py")
        yml = (tmp / "book" / "_quarto.yml").read_text(encoding="utf-8")
        expect("sync_quarto writes _quarto.yml with every chapter",
               code == 0 and "chapters/ch29-sim-to-real-gap.qmd" in yml and "chapters/ch52-" in yml
               and "appendices/e-glossary.qmd" in yml and "ev-badges.lua" in yml
               and (tmp / "book" / "ev-badges.lua").exists(), out)
        expect("sync_quarto keeps the existing chapter file", "Domain randomisation" in chap.read_text())
        expect("sync_quarto creates stubs",
               "<!-- STUB -->" in (tmp / "book/chapters/ch04-anatomy.qmd").read_text())

        # ------------------------------------------------------------ ledger basics
        code, out = run(tmp, S / "ledger_tool.py", "validate", "29")
        expect("ledger validate passes on a good ledger", code == 0, out)
        code, out = run(tmp, S / "ledger_tool.py", "next-id", "29", "3")
        expect("ledger next-id", out.strip() == "C29.03-003", out)
        code, out = run(tmp, S / "ledger_tool.py", "volatile", "--older-than", "0")
        expect("ledger volatile lists volatile claims", "C29.03-002" in out and "C29.03-001" not in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "validate", "C")
        expect("ledger rejects appendix ids", code != 0 and "not a chapter number" in out, out)

        # ------------------------------------------------------------ chapter check (good chapter)
        code, out = run(tmp, S / "check_chapter.py", "29", "--stage", "final")
        expect("check_chapter asks for the sources table when it is empty",
               code != 0 and "sources table is empty" in out, out)
        code, out = run(tmp, S / "sources_table.py", "29")
        table = (tmp / "book/chapters/_sources/ch29.qmd").read_text()
        expect("sources_table lists sources in order with evidence",
               code == 0 and table.index("tobin2017domain") < table.index("openai2019rubiks")
               and "peer-reviewed" in table and "preprint" in table, out + table)
        code, out = run(tmp, S / "check_chapter.py", "29", "--stage", "final", "--stats")
        expect("check_chapter passes a good chapter (final), incl. nofact and 'et al.'", code == 0, out)
        expect("check_chapter --stats reports counts",
               "concepts: 1" in out and "claim tags: 3" in out and "nofact markers: 1" in out, out)

        def mutate(name, old, new, stage="final", should_fail=True, needle=None, absent=None):
            assert old in CHAPTER, old
            chap.write_text(CHAPTER.replace(old, new, 1), encoding="utf-8")
            code, out = run(tmp, S / "check_chapter.py", "29", "--stage", stage)
            ok = (code != 0) if should_fail else (code == 0)
            if needle:
                ok = ok and needle in out
            if absent:
                ok = ok and absent not in out
            expect(name, ok, out)
            chap.write_text(CHAPTER, encoding="utf-8")

        how = "Later work widened"
        mutate("missing Deployment lens is an error",
               '::: {.callout-important title="Deployment lens"}', "::: {.callout-important}", needle="Deployment lens")
        mutate("long quotation is an error", how,
               '"one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen" ' + how,
               needle="[quotes]")
        mutate("unknown claim tag is an error", "C:29.03-002", "C:29.03-099", needle="C29.03-099")
        mutate("claim tag whose source the sentence does not cite is an error",
               "[@openai2019rubiks]. <!--C:29.03-002-->", "[@tobin2017domain]. <!--C:29.03-002-->",
               needle="comes from @openai2019rubiks")
        mutate("TODO marker fails at final", "## Key takeaways", "<!--TODO: need claim for X-->\n\n## Key takeaways",
               needle="[todos]")
        mutate("TODO marker allowed at draft", "## Key takeaways", "<!--TODO: need claim for X-->\n\n## Key takeaways",
               stage="draft", should_fail=False)
        mutate("too few research prompts fails at final", "5. Apply randomisation", "Apply randomisation",
               needle="Research prompts")
        mutate("too few key takeaways fails at final", "- Transfer has to be measured", "Transfer has to be measured",
               needle="Key takeaways has 4")
        mutate("missing citation key fails at final", "[@openai2019rubiks]", "[@nosuchkey2026]", needle="nosuchkey2026")
        mutate("American spelling is a warning, not an error", "Randomisation trades", "Randomization trades optimized behavior",
               should_fail=False)
        mutate("unresolved cross-reference fails at final", how, "See @sec-ch29-no-such-section. " + how,
               needle="[crossrefs]")
        mutate("untagged quantitative sentence fails at final", how, "A humanoid weighs about 60 kg. " + how,
               needle="[facts]")
        mutate("untagged quantitative sentence is only a warning at draft", how,
               "A humanoid weighs about 60 kg. " + how, stage="draft", should_fail=False)
        mutate("<!--nofact--> exempts an illustrative number", how,
               "Suppose a humanoid weighs 60 kg. <!--nofact--> " + how, should_fail=False)
        mutate("cited but untagged quantitative sentence fails at final", how,
               "The study used 100 test images [@tobin2017domain]. " + how, needle="cites a source but has no claim tag")
        mutate("cited sentence without numbers or tag is only a warning", how,
               "Domain randomisation is widely used [@tobin2017domain]. " + how, should_fail=False)
        mutate("table row with numbers but no claim tag fails at final", "## Key takeaways",
               "| Robot | Mass |\n|---|---|\n| Example | 60 kg |\n\n## Key takeaways", needle="table row")
        mutate("<!--nofact--> above a table exempts it", "## Key takeaways",
               "<!--nofact-->\n\n| Robot | Mass |\n|---|---|\n| Example | 60 kg |\n\n## Key takeaways",
               should_fail=False)
        mutate("untagged degrees of freedom fail at final", how, "The robot has 23 degrees of freedom. " + how,
               needle="[facts]")
        mutate("untagged 'billion parameters' fails at final", how, "The model has 2 billion parameters. " + how,
               needle="[facts]")
        mutate("a model name does not split a quantity from its unit", how, "Training used 2,048 H100 GPUs. " + how,
               needle="[facts]")
        mutate("a count with a describing word is a quantity", how, "It was tested in 30 unfamiliar homes. " + how,
               needle="[facts]")
        mutate("model names with digits are not numbers", how, "Both π0.5 and GR00T N1.5 use 3D inputs. " + how,
               should_fail=False, absent="[facts]")
        mutate("claim tags written with spaces are accepted", "images [@tobin2017domain]. <!--C:29.03-001--> In",
               "images [@tobin2017domain]. <!-- C:29.03-001 --> In", should_fail=False, absent="[facts]")
        mutate("a sentence after a closing quotation mark is still checked", how,
               "Engineers call it \u201cthe gap.\u201d It ran 300 trials per day. " + how, needle="300 trials")
        mutate("a 'see' pointer whose only number is a year is allowed", how,
               "For a 2025 survey, see [@smith2025survey]. " + how, should_fail=False)
        mutate("numbered steps in prose are not reported as numbers", "## Key takeaways",
               "1. Collect demonstrations.\n2. Train the policy.\n\n## Key takeaways", should_fail=False,
               absent="[facts]")
        mutate("an image caption with an untagged number fails at final", "## Key takeaways",
               "![Success fell to 40% in field tests [@tobin2017domain].](../figures/ch29/x.svg){#fig-ch29-x "
               "fig-alt=\"A chart.\"}\n\n## Key takeaways", needle="has no claim tag")
        mutate("a claim tag inside the image caption passes", "## Key takeaways",
               "![Success fell to 40% in field tests [@tobin2017domain]. <!--C:29.03-001-->](../figures/ch29/x.svg)"
               "{#fig-ch29-x fig-alt=\"A chart.\"}\n\n## Key takeaways", should_fail=False)
        mermaid = ("```{mermaid}\n%%| label: fig-ch29-loop\n%%| fig-cap: \"Ranges widened 3 times [@openai2019rubiks].\"\n"
                   "flowchart LR\n  A --> B\n```\n")
        mutate("a Mermaid caption with a number needs a tag after the fence", "## Key takeaways",
               mermaid + "\n## Key takeaways", needle="Mermaid caption")
        mutate("a tag right after the Mermaid fence passes", "## Key takeaways",
               mermaid + "<!--C:29.03-002-->\n\n## Key takeaways", should_fail=False)
        mutate("a ### heading without .concept or .aside is a warning only", "## Key takeaways",
               "### A plain heading\n\nSome words.\n\n## Key takeaways", should_fail=False,
               needle="neither .concept nor .aside")

        # Unverified claims: fail at final, pass at draft.
        (led / "s03.jsonl").write_text("\n".join(json.dumps(r) for r in
                                                 [rows[0], dict(rows[1], status="extracted")]) + "\n")
        code, out = run(tmp, S / "check_chapter.py", "29", "--stage", "final")
        expect("unverified claim fails at final", code != 0 and "C29.03-002" in out, out)
        code, out = run(tmp, S / "check_chapter.py", "29", "--stage", "draft")
        expect("unverified claim allowed at draft", code == 0, out)
        code, out = run(tmp, S / "ledger_tool.py", "mark", "C29.03-002", "verified", "--note", "ok")
        code2, out2 = run(tmp, S / "ledger_tool.py", "get", "C29.03-002")
        expect("ledger mark updates status", code == 0 and '"verified"' in out2 and '"checked_by"' in out2, out + out2)

        bib_path = tmp / "book" / "references.bib"
        bib_path.write_text(BIB.replace("url = {https://arxiv.org/abs/1703.06907}", "url = {https://example.org/other}"),
                            encoding="utf-8")
        code, out = run(tmp, S / "check_chapter.py", "29", "--stage", "final")
        expect("a citation key whose bib entry is a different source fails", code != 0 and "points elsewhere" in out, out)
        bib_path.write_text(BIB, encoding="utf-8")

        # ------------------------------------------------------------ ledger add / update / rekey
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "3", "--json", json.dumps(NEW_CLAIM))
        expect("ledger add assigns the next id", code == 0 and "C29.03-003  added" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "3", stdin=json.dumps([NEW_CLAIM]))
        expect("ledger add skips duplicates (stdin input)", code == 0 and "duplicate of C29.03-003" in out
               and "0 added" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "3",
                        "--json", json.dumps(dict(NEW_CLAIM, claim="Another claim.", status="verified")))
        expect("ledger add refuses a pre-verified claim", code != 0 and "Nothing written" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "3", "--json",
                        json.dumps(dict(NEW_CLAIM, claim="A post claim.", source_type="social", evidence="peer-reviewed")))
        expect("ledger add enforces evidence for social sources", code != 0 and "cannot carry evidence" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "3", "--json",
                        json.dumps(dict(NEW_CLAIM, claim="A future claim.", published="2099-01")))
        expect("ledger add rejects future dates", code != 0 and "in the future" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "B", "1", "--json", json.dumps(NEW_CLAIM))
        expect("ledger add rejects appendix ids", code != 0 and "not a chapter number" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "stats", "29")
        expect("ledger stats shows per-section counts", code == 0 and "s03" in out and "3 claims" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "4", "--json",
                        json.dumps(dict(NEW_CLAIM, claim="Same key, other paper.", url="https://example.org/another")))
        expect("ledger add rejects one key for two sources", code != 0 and "already names another source" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "4", "--json",
                        json.dumps(dict(NEW_CLAIM, claim="Same paper, PDF link.", url="https://arxiv.org/pdf/1910.07113v2",
                                        volatile=True)))
        expect("ledger add accepts another link to the same paper", code == 0 and "C29.04-001  added" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "4", "--json", json.dumps(
            dict(NEW_CLAIM, claim="Same paper via arXiv's own DOI.", url="https://doi.org/10.48550/arXiv.1910.07113")))
        expect("ledger add treats arXiv's own DOI as the same paper", code == 0 and "C29.04-002  added" in out, out)
        videos = [dict(NEW_CLAIM, claim=f"A claim from video {v}.", source_key="examplelab2026demo",
                       url=f"https://www.youtube.com/watch?v={v}", source_type="social", evidence="demo",
                       autonomy="unspecified") for v in ("AAA", "BBB")]
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "6", "--json", json.dumps(videos))
        expect("ledger add tells two YouTube videos apart", code != 0 and "already names another source" in out, out)
        post = [dict(NEW_CLAIM, claim=f"Claim {c} from a company post.", source_key="examplelab2026post",
                     url="https://example.org/post-old", source_type="company-blog", evidence="company-claim")
                for c in ("A", "B")]
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "6", "--json", json.dumps(post))
        run(tmp, S / "ledger_tool.py", "mark", "C29.06-001", "verified")
        code, out = run(tmp, S / "ledger_tool.py", "update", "C29.06-001", "--set", "url=https://example.org/post-new")
        expect("ledger update of a URL shared by other claims points to repoint", code != 0 and "repoint" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "repoint", "examplelab2026post", "https://example.org/post-new")
        code2, out2 = run(tmp, S / "ledger_tool.py", "get", "C29.06-001")
        expect("ledger repoint moves every claim of a key and sends them back for checking",
               code == 0 and "2 claims now point" in out and '"status": "extracted"' in out2 and "post-new" in out2,
               out + out2)
        code, out = run(tmp, S / "ledger_tool.py", "rekey", "examplelab2026post", "openai2019rubiks")
        expect("ledger rekey refuses to merge different documents", code != 0 and "different documents" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "validate", "--all")
        expect("ledger validate --all stays clean after repoint", code == 0, out)
        code, out = run(tmp, S / "ledger_tool.py", "usages", "C29.03-001", "C29.04-001")
        expect("ledger usages finds where claims are tagged",
               "book/chapters/ch29-sim-to-real-gap.qmd:" in out and "not used in the book" in out, out)
        code, out = run(tmp, S / "ledger_tool.py", "volatile", "--older-than", "0", "--used")
        expect("ledger volatile --used skips claims the book never tags",
               "C29.03-002" in out and "C29.04-001" not in out, out)

        code, out = run(tmp, S / "ledger_tool.py", "update", "C29.03-001", "--set", "claim=A sharper paraphrase.")
        code2, out2 = run(tmp, S / "ledger_tool.py", "get", "C29.03-001")
        expect("ledger update of substance resets a verified claim",
               code == 0 and "status reset" in out and '"status": "extracted"' in out2, out + out2)
        code, out = run(tmp, S / "ledger_tool.py", "update", "C29.03-001", "--set", "status=verified")
        expect("ledger update cannot change status", code != 0, out)
        run(tmp, S / "ledger_tool.py", "mark", "C29.03-001", "verified")

        code, out = run(tmp, S / "ledger_tool.py", "rekey", "openai2019rubiks", "openai2019solving")
        text = chap.read_text()
        ledger_text = (led / "s03.jsonl").read_text()
        expect("ledger rekey updates ledger and chapters",
               code == 0 and "@openai2019solving" in text and "@openai2019rubiks" not in text
               and "openai2019rubiks" not in ledger_text and "4 ledger claims" in out, out)
        run(tmp, S / "ledger_tool.py", "rekey", "openai2019solving", "openai2019rubiks")
        chap.write_text(CHAPTER, encoding="utf-8")

        # ------------------------------------------------------------ research_tool
        res = tmp / "research" / "ch29"
        res.mkdir(parents=True)
        (res / "s01-sources.json").write_text(json.dumps(
            [source(f"a{i}", 1 if i < 2 else 2) for i in range(5)]), encoding="utf-8")
        (res / "s02-sources.json").write_text(json.dumps([source("b0", 1), dict(source("b1", 3), sections=["01"])]),
                                              encoding="utf-8")
        (res / "s01-rejected.md").write_text(
            "- https://spamfarm.example/top-10-humanoids — listicle without primary links\n"
            "BAN: spamfarm.example — SEO listicle farm\n"
            "BAN: youtube.com — one poor video\n"
            "BAN: figure.ai — a lab the book covers\n", encoding="utf-8")
        code, out = run(tmp, S / "research_tool.py", "summary", "29", "--expect", "3")
        expect("research summary flags thin and missing sections",
               code != 0 and "s01" in out and "OK" in out and "THIN" in out and "MISSING" in out, out)
        code, out = run(tmp, S / "research_tool.py", "merge-bans", "29")
        banned = (tmp / "scripts" / "banned_domains.txt").read_text()
        expect("merge-bans adds new domains and refuses platforms",
               code == 0 and "spamfarm.example" in banned and "youtube.com" not in banned
               and "refused: youtube.com" in out, out + banned)
        code, out = run(tmp, S / "research_tool.py", "merge-bans", "29")
        expect("merge-bans is idempotent and refuses lab domains",
               "already banned: spamfarm.example" in out and "refused: figure.ai" in out, out)
        code, out = run(tmp, S / "research_tool.py", "sources", "29", "1")
        expect("research sources includes cross-listed sources", code == 0 and '"b1"' in out and '"s02"' in out, out)
        code, out = run(tmp, S / "research_tool.py", "pending", "29")
        expect("research pending is empty for a clean chapter", code == 0 and "0 pending" in out, out)
        (res / "extra-sources.json").write_text(json.dumps([dict(source("c0", 1), **{"for": "C29.03-001"})]),
                                                encoding="utf-8")
        (tmp / "checks").mkdir(exist_ok=True)
        (tmp / "checks" / "ch29-requests.md").write_text("- [ ] s03: a number for X\n- [x] s03: done → C29.03-003\n",
                                                         encoding="utf-8")
        code, out = run(tmp, S / "research_tool.py", "pending", "29")
        expect("research pending lists open requests and unprocessed counter-evidence",
               code == 1 and "a number for X" in out and "counter-evidence: c0" in out and "2 pending" in out, out)
        (res / "extra-sources.json").write_text(json.dumps([dict(source("c0", 1), **{"for": "C29.03-001",
                                                                                   "done": "C29.03-003"})]),
                                                encoding="utf-8")
        (tmp / "checks" / "ch29-requests.md").write_text("- [x] s03: a number for X → C29.03-003\n", encoding="utf-8")
        code, out = run(tmp, S / "research_tool.py", "pending", "29")
        expect("research pending clears once items are done", code == 0, out)
        code, out = run(tmp, S / "ledger_tool.py", "add", "29", "3", "--json",
                        json.dumps(dict(NEW_CLAIM, claim="From a farm.", url="https://www.spamfarm.example/x")))
        expect("ledger add rejects banned domains", code != 0 and "banned domain" in out, out)

        # ------------------------------------------------------------ fetch_text (local, no network)
        page = tmp / "page.html"
        page.write_text(HTML, encoding="utf-8")
        code, out = run_plain(S / "fetch_text.py", page,
                              "--find", "the robot's grasp succeeded in 56 % of trials-across thirty homes",
                              "--find", "a second paragraph about grippers")
        expect("fetch_text finds phrases across quote, dash, space and hyphenation differences",
               code == 0 and "Test page" in out and out.count("FOUND (1×)") == 2 and "»" in out, out)
        code, out = run_plain(S / "fetch_text.py", page, "--find", "hidden words never shown")
        expect("fetch_text ignores scripts and exits 1 when a phrase is missing",
               code == 1 and "NOT FOUND" in out, out)
        code, out = run_plain(S / "fetch_text.py", page, "--find", "grasp succeeded in 75 % of trials across thirty homes")
        expect("fetch_text reports the closest match", code == 1 and "closest match" in out, out)

        wall = tmp / "wall.html"
        wall.write_text("<html><head><title>Just a moment...</title></head><body>Checking your browser.</body></html>",
                        encoding="utf-8")
        code, out = run_plain(S / "fetch_text.py", wall, "--find", "anything at all here")
        expect("fetch_text treats a bot-check page as a failed fetch, not a missing phrase",
               code == 2 and "bot check" in out, out)

        import fetch_text
        fetch_text.CACHE_DIR = tmp / "fetch-cache"

        class FakeResp:
            def __init__(self, body):
                self.body, self.headers = body, {"Content-Type": "text/plain"}

            def read(self, n=-1):
                return self.body

            def geturl(self):
                return "https://example.org/page"

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        def fake_urlopen(req, timeout=None):
            url = req.full_url if hasattr(req, "full_url") else str(req)
            if url.endswith("/robots.txt"):
                return FakeResp(b"User-agent: *\nDisallow: /private\n")
            if "busy" in url:
                raise urllib.error.HTTPError(url, 429, "Too Many Requests", {"Retry-After": "0"}, io.BytesIO(b""))
            raise urllib.error.HTTPError(url, 403, "Forbidden", {}, io.BytesIO(b""))

        real = fetch_text.urllib.request.urlopen
        fetch_text.urllib.request.urlopen = fake_urlopen
        old_err, sys.stderr = sys.stderr, io.StringIO()
        try:
            robots_ok = (fetch_text.robots_allows("https://example.org/public/page")
                         and not fetch_text.robots_allows("https://example.org/private/page"))
            try:
                fetch_text.fetch_url("https://example.org/public/page")
                refused = None
            except SystemExit as exc:
                refused = exc.code
            try:
                fetch_text.fetch_url("https://example.org/busy/page")
                limited = None
            except SystemExit as exc:
                limited = exc.code
            import hashlib
            import time
            marker = fetch_text.CACHE_DIR / f"host-{hashlib.sha1(b'queue.example').hexdigest()}"
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text(str(time.time() + 200))
            try:
                fetch_text.polite_wait("queue.example", 15.0)
                queued = None
            except SystemExit as exc:
                queued = exc.code
        finally:
            fetch_text.urllib.request.urlopen = real
            sys.stderr = old_err
        expect("fetch_text obeys robots.txt", robots_ok)
        expect("fetch_text stops on HTTP 403 with exit code 3", refused == 3, f"exit code {refused}")
        expect("fetch_text retries a 429 once, then reports rate-limiting as exit 2 (not a refusal)",
               limited == 2, f"exit code {limited}")
        expect("fetch_text reports a long Crawl-delay queue as busy (exit 2) instead of waiting",
               queued == 2, f"exit code {queued}")

        chap.write_text(CHAPTER.replace(how, "As @smith2025survey notes, transfer is hard. " + how, 1), encoding="utf-8")
        code, out = run(tmp, S / "sources_table.py", "29")
        table = (tmp / "book/chapters/_sources/ch29.qmd").read_text()
        expect("sources_table includes narrative citations", "smith2025survey" in table, out + table)
        chap.write_text(CHAPTER, encoding="utf-8")
        run(tmp, S / "sources_table.py", "29")

        # ------------------------------------------------------------ check_svg
        code, out = run(tmp, S / "check_svg.py", "--ch", "29")
        expect("check_svg --ch passes a chapter without SVG figures", code == 0 and "nothing to check" in out, out)
        (tmp / "good.svg").write_text(GOOD_SVG, encoding="utf-8")
        (tmp / "bad.svg").write_text(BAD_SVG, encoding="utf-8")
        code, out = run_plain(S / "check_svg.py", tmp / "good.svg")
        expect("check_svg accepts an original drawing", code == 0, out)
        code, out = run_plain(S / "check_svg.py", tmp / "bad.svg")
        expect("check_svg rejects embedded images", code != 0 and "<image>" in out, out)

        # ------------------------------------------------------------ ledger validation of broken lines
        (led / "s05.jsonl").write_text(json.dumps({"id": "C29.05-001", "chapter": "29", "section": "05",
                                                   "claim": "x"}) + "\n{not json\n", encoding="utf-8")
        code, out = run(tmp, S / "ledger_tool.py", "validate", "29")
        expect("ledger validate catches missing fields and bad JSON",
               code != 0 and "missing required field" in out and "invalid JSON" in out, out)
        (led / "s05.jsonl").unlink()

        # ------------------------------------------------------------ progress
        code, out = run(tmp, S / "progress.py", "next")
        expect("progress next starts with the pilot", out.strip() == "29", out)
        code, out = run(tmp, S / "progress.py", "set", "29", "done", "--note", "test")
        code2, out2 = run(tmp, S / "progress.py", "show", "29")
        expect("progress set/show", code == 0 and "status: done" in out2, out + out2)
        code, out = run(tmp, S / "progress.py", "part", "P5")
        expect("progress part lists chapters", out.strip() == "27 28 29", out)
        code, out = run(tmp, S / "progress.py", "next")
        expect("progress next follows production order after the pilot", out.strip() == "04", out)
        for cid in ("04", "27", "28", "52"):
            run(tmp, S / "progress.py", "set", cid, "done")
        code, out = run(tmp, S / "progress.py", "next")
        expect("progress next keeps the 'last' chapter (ch01) until everything else is done", out.strip() == "01", out)
        code, out = run(tmp, S / "progress.py", "known", "29")
        expect("progress known counts only earlier chapters",
               "Simulation makes practice cheap" in out and "must never count" not in out
               and "takeaways are missing" in out and "- ch27 · Simulators" not in out, out)
        run(tmp, S / "progress.py", "set", "27", "drafted")
        code, out = run(tmp, S / "progress.py", "known", "29")
        expect("progress known lists earlier chapters not yet written", "- ch27 · Simulators" in out, out)
        run(tmp, S / "progress.py", "set", "27", "blocked", "--note", "test block")
        code, out = run(tmp, S / "progress.py", "show", "27")
        expect("progress show tells where a blocked chapter resumes", "resume from: drafted" in out, out)
        code, out = run(tmp, S / "progress.py", "current-as-of", "2026-10-06")
        expect("progress current-as-of writes _variables.yml",
               code == 0 and "6 October 2026" in (tmp / "book/_variables.yml").read_text(), out)
        leftovers = [p.name for p in tmp.rglob("*.tmp")]
        expect("no temp files left behind", not leftovers, ", ".join(leftovers))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    if FAILS:
        print(f"{len(FAILS)} TEST(S) FAILED")
        sys.exit(1)
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
