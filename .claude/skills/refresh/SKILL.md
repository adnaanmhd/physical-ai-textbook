---
description: Keep the book current. Re-verifies the volatile claims the book uses (versions, deployments, prices, funding, regulation, benchmark leaders) older than N days, updates every affected chapter and appendix, and bumps the "current as of" date.
argument-hint: "[days, default 60]"
disable-model-invocation: true
allowed-tools:
  - Bash(python3 scripts/*)
  - Bash(quarto render *)
  - Bash(git add *)
  - Bash(git commit *)
---
**Age threshold:** $ARGUMENTS days (default 60 if empty).

1. **List stale claims the book uses:** `python3 scripts/ledger_tool.py volatile --older-than <days> --used`.
2. **Group them by chapter.** For each chapter, spawn the `fact-checker` in refresh mode (at most 6 in parallel). Each writes `checks/chNN-refresh.md`, listing every location that uses a superseded claim.
3. **Update every affected file.** A superseded claim may be tagged in several chapters and appendices (`python3 scripts/ledger_tool.py usages --status superseded` lists them all). For each chapter or appendix that uses one:
   - spawn the `writer` (revise mode), restricted to those locations, using the new claim ids;
   - spawn the `fact-checker` in re-verify mode for the changed sentences;
   - spawn the `bibliographer` (new sources need entries), then the `editor`.
4. **Check the whole book:** `python3 scripts/check_chapter.py --all --stage final` must exit 0. Route any failure as in `build-part` step 3.
5. **Also scan for new frontier work.** For the chapters on VLAs, world models, WAMs, evaluation, standards and the landscape (ch31–34, ch36–43, ch45, ch50–53), spawn `scout` in light-scan mode. If it finds major new work, add a feedback item to `FEEDBACK.md` proposing an update; do not rewrite silently.
6. **Stamp the date:**
   - `python3 scripts/progress.py current-as-of YYYY-MM-DD`, using today's date;
   - `quarto render book --to html`;
   - `git add -A && git commit -m "refresh: <date>"`.
7. **Report:**
   - claims re-checked, changed and superseded;
   - chapters and appendices touched;
   - proposed updates awaiting approval.
