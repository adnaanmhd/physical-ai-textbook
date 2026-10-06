---
description: Re-verify an existing chapter after manual edits, new feedback or a style change, by running the scripts, the fact-checkers and the skeptic, then the writer, bibliographer and editor wherever anything needs changing.
argument-hint: "[chapter number]"
allowed-tools:
  - Bash(python3 scripts/*)
  - Bash(quarto render *)
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(git log *)
---
**Chapter:** $ARGUMENTS. Normalise it to two digits.

1. **Measure.** Run `python3 scripts/check_chapter.py NN --stage final`, `python3 scripts/check_chapter.py NN --stats` and `python3 scripts/progress.py known NN --out checks/chNN-known.md`.
2. **Check.** Spawn `fact-checker`s on every claim tag, split by section groups as in `build-chapter` step 5 (no sampling). Then spawn the `skeptic`. Route regressions in other chapters as in `build-chapter` step 5.
3. **Decide whether the writer must run.** It must when any of these holds:
   - a finding is critical or major, a claim failed or was flagged, or a sentence problem was reported;
   - the checker fails;
   - `checks/chNN-feedback.md` has unticked `- [ ]` items;
   - `docs/STYLE.md` changed after the chapter was last edited. Compare `git log -1 --format=%ct -- docs/STYLE.md` with `git log -1 --format=%ct -- book/chapters/chNN-*.qmd`.
4. **If so, revise:**
   - top up evidence if needed (`build-chapter` step 6);
   - spawn the `writer` (revise mode), then the `fact-checker`s in re-verify mode;
   - spawn the `bibliographer`, then the `editor`;
   - at most two rounds. If problems remain, set the chapter to `blocked` with the reason.
5. **When everything is clean:**
   - Set the status to `done`.
   - Add a one-line entry to `PROGRESS.md`.
   - Commit: `git add -A && git commit -m "chNN: re-verified"`.
