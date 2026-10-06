---
description: Create the section-level outline for the whole book (gate G1). Light-scans every chapter for the current state of the art, proposes sections, dependencies and changes from the seed outline, then stops for human approval.
disable-model-invocation: true
allowed-tools:
  - Bash(python3 scripts/*)
  - Bash(git *)
---
Produce `docs/OUTLINE-DETAILED.md` for human approval. Write no chapters.

1. **Read** `docs/BRIEF.md`, `docs/OUTLINE.md`, `docs/RUNNING-EXAMPLES.md`, `docs/PIPELINE.md` (the Planning section) and `FEEDBACK.md`.
2. **Start the file.** Create `docs/OUTLINE-DETAILED.md` with a title and two empty sections at the top: "Changes from seed" and "Open questions for the human".
3. **Light scans.** Work Part by Part, in book order. Spawn `scout` subagents in light-scan mode, at most 6 at a time and 2–4 chapters each. Each writes `research/chNN/scan.md`. Wait for each batch before starting the next.
4. **Section outlines.** For each Part in turn, spawn the `synthesizer` in planning mode with that Part's scans and `docs/OUTLINE.md`. It appends the Part's outline (same structure as `docs/OUTLINE.md`, with numbered sections `29.01`, `29.02`, …) to `docs/OUTLINE-DETAILED.md` itself and returns a short summary. Run Parts one at a time, so the appends never collide.
5. **Fill the two top sections:**
   - **"Changes from seed":** every split, merge, rename or addition, with its reason, gathered from the Parts.
   - **"Open questions for the human":** at most 10.
6. **Update the chapter list.** If chapters changed, update `state/progress.json` (ids, slugs, titles, parts, lifecycle flags), then run `python3 scripts/sync_quarto.py`. Commit: `git add -A && git commit -m "plan: detailed outline for G1"`.
7. **Stop.** Tell the human: "Gate G1: please review `docs/OUTLINE-DETAILED.md` (start with 'Changes from seed' and 'Open questions'). Reply 'approved' or add notes to `FEEDBACK.md`." Do not start any chapter until the human approves.
8. **On approval,** apply any notes, write `G1 approved YYYY-MM-DD` in the Gates section of `PROGRESS.md`, and commit. The chapter numbers are now frozen.
