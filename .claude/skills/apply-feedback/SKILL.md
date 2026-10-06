---
description: Triage and apply the human's notes in FEEDBACK.md to the style contract, the outline or specific chapters, then mark them done.
disable-model-invocation: true
allowed-tools:
  - Bash(python3 scripts/*)
  - Bash(git add *)
  - Bash(git commit *)
---
1. **Read the open items** in `FEEDBACK.md`.
2. **Classify each item:**
   - **style:** edit `docs/STYLE.md`. Finished chapters pick the change up the next time they are verified (`/verify-chapter NN` notices that the style changed).
   - **outline:** edit `docs/OUTLINE-DETAILED.md` and, if chapters change, `state/progress.json` (then `python3 scripts/sync_quarto.py`);
   - **chapter NN:** append the note to `checks/chNN-feedback.md` as `- [ ] (YYYY-MM-DD) note`. The scouts, synthesizer, writer and editor read that file, and the writer ticks each note it applies;
   - **general:** record it in `docs/BRIEF.md` under a "Later decisions" heading.
3. **Queue chapter revisions.** For a chapter already past `checked` (revised, edited or done), set its status back to `checked` with a note, so the next `/build-chapter NN` revises it from the feedback. A chapter not yet built picks up `checks/chNN-feedback.md` when it is built.
4. **Close the items.** Move handled items to `## Done`, dated, with a one-line note on what changed.
5. **Commit:** `git add -A && git commit -m "feedback applied"`.
6. **Report** one line per item to the human, and name the chapters that now need `/build-chapter NN`.
