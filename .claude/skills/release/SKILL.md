---
description: Finish and publish the book. With no argument, writes the back matter (appendices A–F and the preface) and stops for the human's final read. With "build", checks freshness and the toolchain, stamps the "current as of" date, renders HTML, PDF and EPUB, and tags the release.
argument-hint: "[build [tag]]  (empty = back matter and final read; 'build v1.0' = publish)"
disable-model-invocation: true
allowed-tools:
  - Bash(python3 scripts/*)
  - Bash(quarto render *)
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(git tag *)
---
**Arguments:** $ARGUMENTS

## If the arguments do not start with `build`: back matter, then the final read
1. **Check readiness.** Every chapter 01–52 must be `done` (`python3 scripts/progress.py show`), and `python3 scripts/check_chapter.py --all --stage final` must pass. If not, stop and list what remains.
2. **Appendices**, in the order of the Back matter table in `docs/PIPELINE.md`, skipping any already `done`. For each appendix X:
   - write what it may assume: `python3 scripts/progress.py known X --out checks/X-known.md`;
   - spawn the `synthesizer` to plan it from the finished chapters, their blueprints and the ledger;
   - spawn the `writer` to draft it. Appendices add no new facts: every number reuses the claim tag and citation of the chapter that established it;
   - for appendices that state facts (A, B, C, D), spawn the `fact-checker` in appendix mode. It reports problems and never changes claim statuses; route claim problems to the owning chapters as in `build-chapter` step 5;
   - if the fact-check or the checker finds problems, spawn the `writer` (revise mode) and re-check, at most two rounds; then `blocked`;
   - spawn the `editor`; `python3 scripts/check_chapter.py X --stage final` must exit 0;
   - set the status to `done` and commit.

   For the glossary (E), the editor deduplicates and alphabetises the entries and checks that each points to the chapter that teaches it.
3. **Preface.** Spawn the `writer` to revise `book/index.qmd` so it describes the finished book, keeping its sections (the five layers, the evidence tags, the running examples, the research prompts and the "current as of" line). Then spawn the `editor`.
4. **Final read (gate).** Render with `quarto render book --to html`, commit, and tell the human:
   "Final read: preview with `quarto preview book`. Add notes to `FEEDBACK.md` and run `/apply-feedback`, or run `/release build v1.0` to publish."
   Stop here.

## If the arguments start with `build`: publish
The tag is the second word of the arguments (default `v1.0`). Record `Final read approved YYYY-MM-DD` in `PROGRESS.md`.
1. **Gate checks**, each of which must pass:
   - `python3 scripts/ledger_tool.py validate --all`
   - `python3 scripts/check_chapter.py --all --stage final`
   - no open items in `FEEDBACK.md`;
   - **freshness:** `python3 scripts/ledger_tool.py volatile --older-than 60 --used` lists nothing. If it lists claims, stop and ask the human to run `/refresh` first: the "current as of" date must be true of every fast-moving fact in the book.
   - **toolchain:** `python3 scripts/pdf_check.py` passes.
2. **Stamp the date:** `python3 scripts/progress.py current-as-of YYYY-MM-DD`, using today's date.
3. **Render everything:** `quarto render book` (HTML, PDF and EPUB). If the PDF fails, report the error with the fix from the README's troubleshooting section, and stop.
4. **Commit and tag:** `git add -A && git commit -m "release: <tag>"`, then `git tag <tag>`.
5. **Report:** where the outputs are (`book/_book/`), the counts (chapters, claims by evidence tag, distinct sources), and the "current as of" date.
