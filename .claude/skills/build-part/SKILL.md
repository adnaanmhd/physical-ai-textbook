---
description: Build every chapter in one Part, in order, then check the whole book for regressions, write the Part summary and render the book (a soft gate). Use after gates G1 and G2 are approved.
argument-hint: "[part id, e.g. P5]"
allowed-tools:
  - Bash(python3 scripts/*)
  - Bash(quarto render *)
  - Bash(git add *)
  - Bash(git commit *)
---
**Part:** $ARGUMENTS.

0. **Check the gates.** `PROGRESS.md` must record both `G1 approved` and `G2 approved` with a date. If either is missing, stop and say which.
1. **List the chapters:** `python3 scripts/progress.py part $ARGUMENTS`. Skip chapters already marked `done`. For P0, build ch02 and ch03 first and ch01 last (`python3 scripts/progress.py next` shows the order).
2. **Build each chapter in order** with the `build-chapter` skill, one chapter in writing or editing at a time.
   - **Pipelining is allowed.** While chapter N is in Check or Revise, you may start Scout and Research for chapter N+1.
3. **Catch regressions across the book.** Run `python3 scripts/check_chapter.py --all --stage final`. A finished chapter can break when a claim it shares is later flagged, failed or superseded. For each chapter that fails, append each error to its `checks/chNN-feedback.md` as `- [ ] (YYYY-MM-DD) <error>`, set it to `checked`, and rebuild it with `build-chapter` before closing the Part.
4. **Close the Part:**
   - Render the HTML book: `quarto render book --to html`.
   - Append a Part summary to `PROGRESS.md`:
     - chapters done or blocked;
     - the claim total by evidence tag (`python3 scripts/ledger_tool.py stats`);
     - open issues;
     - outline drift;
     - notes on usage.
   - Commit: `git add -A && git commit -m "Part $ARGUMENTS complete"`.
5. **Decide whether to continue.** Read `FEEDBACK.md`.
   - If it says `Mode: continuous`, start the next Part in the production order in `docs/PIPELINE.md` with this skill. After the last Part (P0), stop and suggest `/release`.
   - Otherwise stop and tell the human the Part is ready for review. When they approve it, record `Part $ARGUMENTS reviewed YYYY-MM-DD` in `PROGRESS.md`.
