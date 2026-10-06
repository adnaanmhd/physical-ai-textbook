---
description: Run the full research, writing and verification pipeline for one chapter, resuming from its recorded status. Use for the pilot (ch29) and whenever a single chapter needs building or revising.
argument-hint: "[chapter number, e.g. 29]"
allowed-tools:
  - Bash(python3 scripts/*)
  - Bash(quarto render *)
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(mkdir *)
---
**Chapter:** $ARGUMENTS. Normalise it to two digits (e.g. `7` becomes `07`). Follow `docs/PIPELINE.md`; the short version is below. Use the delegation template in `docs/PIPELINE.md` for every subagent.

0. **Prepare.**
   - Run `python3 scripts/progress.py show NN` and resume from the recorded status. Never redo a finished stage. If the chapter is `blocked`, fix the cause, then set it back to the "resume from" status it shows.
   - Read `FEEDBACK.md` and route every open item: style items into `docs/STYLE.md`; items for this chapter into `checks/chNN-feedback.md` as `- [ ] (YYYY-MM-DD) note`; items for other chapters as `/apply-feedback` step 3 does. Move handled items to Done.
   - Confirm `docs/OUTLINE-DETAILED.md` has this chapter's sections. Before G1, use `docs/OUTLINE.md` and number its seed sections yourself.
   - Write what the reader knows: `python3 scripts/progress.py known NN --out checks/chNN-known.md`.
1. **Scout → `scouted`.**
   - Spawn `scout` subagents: at most 6 in parallel, 1–3 sections each.
   - Run `python3 scripts/research_tool.py merge-bans NN`, and log any newly banned domains in `PROGRESS.md` for the human to review.
   - Run `python3 scripts/research_tool.py summary NN --expect <number of sections>`. Re-scout THIN or MISSING sections once. If a section is still thin, note it and continue: the synthesizer will plan around it.
2. **Research → `researched`.**
   - Spawn `researcher` subagents: one per section, at most 6 in parallel.
   - Run `python3 scripts/ledger_tool.py validate NN` (must exit 0) and `python3 scripts/ledger_tool.py stats NN`.
   - Re-research any section with fewer than 8 claims once, unless the outline says fewer suffice.
3. **Blueprint → `blueprinted`.**
   - Spawn the `synthesizer`.
   - If it lists gaps, spawn targeted `researcher`s for one round only, then have the synthesizer update the affected concepts.
4. **Draft → `drafted`.**
   - Spawn the `writer` (draft mode). When it has finished, spawn the `figure-maker` for the `<!--FIG-->` markers.
   - The draft must pass `python3 scripts/check_chapter.py NN --stage draft`.
5. **Check → `checked`.**
   - Run `python3 scripts/check_chapter.py NN --stats` and read the "claim tags by section" line. Split the sections into groups of roughly 40–60 claim tags (tags from other chapters join the last group).
   - Spawn one `fact-checker` per group, at most 6 in parallel. Each checks every tag in its group, with no sampling, and writes `checks/chNN-factcheck-sAA-sBB.md`.
   - Then spawn the `skeptic` and the `cold-reader` in parallel.
   - **Route regressions:** run `python3 scripts/ledger_tool.py usages --status failed,flagged,superseded`. For every file listed that belongs to another chapter, append `- [ ] (YYYY-MM-DD) Claim CXX.YY-ZZZ is now <status>: <problem>` to that chapter's `checks/chMM-feedback.md` (skip claims already noted there), and if that chapter is `revised`, `edited` or `done`, set it back to `checked` so it gets revised.
6. **Top up evidence** (status stays `checked`). Run `python3 scripts/research_tool.py pending NN`. If it lists anything (TODO markers, open requests, unprocessed counter-evidence), spawn `researcher`s in top-up mode for the sections concerned (one round, at most 6 in parallel), then run `python3 scripts/ledger_tool.py validate NN`.
7. **Revise → `revised`.**
   - Spawn the `writer` (revise mode).
   - Spawn `fact-checker`s in re-verify mode, with the same groups. Route regressions again, as in step 5.
   - Record the round without advancing the status: `python3 scripts/progress.py set NN checked --note "revise round 1 done"`.
   - The round passes when the re-verify reports list no failed or flagged claims, no unticked critical or major sentence problems and no untagged facts, and `python3 scripts/check_chapter.py NN --only claims,facts --stage final` exits 0. Only then set `revised`.
   - Otherwise run round 2 (top up first if `pending` lists anything; note "revise round 2 done"). If it still does not pass, set the chapter to `blocked`; it will resume at this step.
8. **Edit → `edited`.**
   - Spawn the `prompt-designer`, then the `bibliographer`, then the `editor`.
   - If the editor sent facts back (new open items in `checks/chNN-requests.md`), run one top-up round, a writer revise limited to those items, a re-verify of the changed claims, and the editor again. If items are still open, set the chapter to `blocked`.
   - The editor records the chapter's takeaways in `state/takeaways.md`.
9. **Done → `done`.**
   - Confirm the definition of done in `CLAUDE.md`.
   - Append three lines to `PROGRESS.md`: what the chapter covers; its counts (words, claims by evidence tag, sources, figures; use `python3 scripts/check_chapter.py NN --stats`); and open issues.

**After every stage:**
- `python3 scripts/progress.py set NN <status> --note "<one line>"`
- `git add -A && git commit -m "chNN: <status>"`

**Rules:**
- Subagents write to files and return short summaries. Never paste sources, ledgers or drafts here.
- Only this main session runs git. Subagents never commit.
- **Resuming a fan-out stage** (scouts, researchers, fact-checkers): re-run only the units whose output file is missing or incomplete.
- If a stage fails twice, set the status to `blocked` with the reason (the tool records the last completed stage), log it in `PROGRESS.md`, and stop this chapter.
- **Pilot:** if this is the pilot chapter (ch29 by default), finish by telling the human:
  - "Gate G2: preview with `quarto preview book`, then reply with feedback or 'approved'."
  - Ask them to note the usage this chapter consumed (`/usage`) so it can be recorded in `PROGRESS.md`.
