# Production pipeline

## Phases
| # | Phase | Command | Exit condition |
|---|---|---|---|
| 0 | Setup | `/setup-check` | Tools installed; self-test passes; skeleton book renders. |
| 1 | Planning | `/plan-book` | `docs/OUTLINE-DETAILED.md` written. **Gate G1: human approval.** |
| 2 | Pilot | `/build-chapter 29` | ch29 done and rendered. **Gate G2: human feedback folded into STYLE.md** (and ch29 revised to match, if the style changed substantially). |
| 3 | Production | `/build-part P1` … `/build-part P12`, then `/build-part P0` | Every chapter `done`. Soft review after each Part. |
| 4 | Back matter | `/release` | Appendices A–F and the preface done. **Final read.** |
| 5 | Release | `/release build v1.0` | Checks pass; no volatile claim in the book older than 60 days; PDF toolchain checked; "current as of" stamped; HTML, PDF and EPUB built; git tag. |
| 6 | Maintenance | `/refresh` | Volatile claims re-verified on a schedule (default every 60 days). |

**Part order.** Production runs P1 → P12, then P0. Within a Part, follow chapter order, except that chapter 01 (The lifecycle on one page) summarises the whole book and is written after every other chapter (`book.last` in `state/progress.json`; `progress.py next` respects it).

## Parts and chapters (summary; full list in `state/progress.json`)
| Part | Title | Chapters |
|---|---|---|
| P0 | Orientation | 01–03 |
| P1 | The body | 04–10 |
| P2 | Foundations from zero | 11–15 |
| P3 | The software stack | 16 |
| P4 | Data | 17–26 |
| P5 | Simulation | 27–29 |
| P6 | Training robot policies | 30–35 |
| P7 | World models | 36–39 |
| P8 | World action models and convergence | 40–42 |
| P9 | Evaluation and safety | 43–45 |
| P10 | Deployment | 46–47 |
| P11 | After deployment | 48–49 |
| P12 | Landscape and frontier | 50–52 |
| APP | Appendices | A–F |

## Per-chapter stages
Every stage reads its inputs from files and writes its outputs to files. Subagents return summaries of at most 150 words. The main session commits after each stage; subagents never run git.

### Stage 1: Scout (status → `scouted`)
- **Agent:** `scout`, one per 1–3 sections, at most 6 in parallel.
- **Inputs:** the chapter's entry in `docs/OUTLINE-DETAILED.md` (or `docs/OUTLINE.md` before G1), `docs/SOURCES.md`.
- **Outputs:** `research/chNN/sSS-sources.json` (a JSON list) and `research/chNN/sSS-rejected.md` (with `BAN:` lines for whole domains).
- **Then the main session runs:**
  - `python3 scripts/research_tool.py merge-bans NN` (the only way domains enter `scripts/banned_domains.txt`; new bans are logged in `PROGRESS.md` for the human to review);
  - `python3 scripts/research_tool.py summary NN --expect <number of sections>`.
- **Exit:** every section has at least 5 usable sources, including at least 2 with priority 1, and the newest-version check is done for every named system. Thin sections get one more scouting round.

### Stage 2: Research (status → `researched`)
- **Agent:** `researcher`, one per section, at most 6 in parallel.
- **Output:** `ledger/chNN/sSS.jsonl`, written only through `python3 scripts/ledger_tool.py add`.
- **Exit:**
  - `python3 scripts/ledger_tool.py validate NN` passes;
  - every section has at least 8 claims (`ledger_tool.py stats NN`), or the outline says fewer suffice;
  - conflicts are logged.

### Stage 3: Blueprint (status → `blueprinted`)
- **Agent:** `synthesizer`.
- **Output:** `blueprints/chNN.md`.
- **Gap loop:** at most one extra research round per chapter, targeting only the listed gaps. Gaps that remain afterwards become explicit `[inference]` with visible reasoning, or are cut.

### Stage 4: Draft (status → `drafted`)
- **Agents, in order:** `writer` (draft mode), then `figure-maker`, which replaces the draft's `<!--FIG: ...-->` markers.
- **Outputs:** `book/chapters/chNN-<slug>.qmd`; figures in `book/figures/chNN/` or as Mermaid blocks.
- **Exit:** `python3 scripts/check_chapter.py NN --stage draft` passes (warnings allowed).

### Stage 5: Check (status → `checked`)
- **Fact-check, split by section groups.** `python3 scripts/check_chapter.py NN --stats` prints the claim tags per section. Group the sections into batches of roughly 40–60 tags (tags from other chapters join the last batch) and run one `fact-checker` per batch, at most 6 in parallel. Every tag is checked; nothing is sampled.
- **Then** `skeptic` and `cold-reader`, in parallel.
- **Outputs:** `checks/chNN-factcheck-sAA-sBB.md` (one per batch), `checks/chNN-skeptic.md`, `checks/chNN-coldread.md`.
- **Ledger statuses describe claims, not sentences.** A fact-checker marks a claim `failed` or `flagged` only when its source does not support it as recorded. A sound claim misused by one sentence stays `verified`; the fix goes in the report.
- **Sentence problems are ranked and tickable:** each is a `- [ ] [critical|major|minor] …` line in the fact-check report, which the writer ticks when fixed.
- **Regressions elsewhere.** A claim can be tagged in several chapters. `python3 scripts/ledger_tool.py usages --status failed,flagged,superseded` lists every place a non-verified claim is used. Other chapters on that list get a `- [ ] (YYYY-MM-DD) …` note in their `checks/chMM-feedback.md` and, if they are past `checked`, go back to `checked`.

### Stage 6: Evidence top-up (status stays `checked`)
- **Trigger:** `python3 scripts/research_tool.py pending NN` lists the `<!--TODO-->` markers in the draft, unticked requests in `checks/chNN-requests.md` (from the writer, and later from the editor), and counter-evidence in `research/chNN/extra-sources.json` (from the skeptic) not yet marked `done`. Nothing pending, no top-up.
- **Agent:** `researcher` in top-up mode, for the sections concerned only, one round. New claims go through `ledger_tool.py add`; the researcher ticks each request and marks each counter-evidence entry `done` with the new claim ids.

### Stage 7: Revise (status → `revised`)
- **Agent:** `writer`, in revise mode. It reads every report plus `checks/chNN-feedback.md`, applies every critical and major finding, every failed or flagged claim and every sentence problem, uses the top-up claims, ticks the human notes it applied, and logs each fix (with the claim ids touched) in `checks/chNN-fixlog.md`.
- **Then:** `fact-checker`s in re-verify mode, same batches: every claim not yet `verified`, plus the ids and sentences in the fix log.
- **Rounds:** a round is recorded without advancing the status (`set NN checked --note "revise round 1 done"`). The chapter becomes `revised` only when a round passes: no failed or flagged claims, no unticked critical or major sentence problems, no untagged facts, and `check_chapter.py NN --only claims,facts --stage final` exits 0. After two failed rounds the chapter is `blocked`, and it resumes at Revise.

### Stage 8: Edit (status → `edited`)
- **Agents, in order:** `prompt-designer` → `bibliographer` → `editor`.
- **The editor runs:**
  1. `python3 scripts/sources_table.py NN`
  2. `python3 scripts/check_chapter.py NN --stage final`
  3. `python3 scripts/check_svg.py --ch NN`
  4. `quarto render book/chapters/chNN-*.qmd --to html` (warnings about references to other chapters are expected in a single-chapter render)
- **Send-backs:** the editor never adds facts. Anything that needs one goes to `checks/chNN-requests.md`; the main session runs one top-up, a limited revise, a re-verify and the editor again, then blocks the chapter if items remain.
- **Takeaways:** the editor records the chapter's final Key takeaways in `state/takeaways.md`.

### Stage 9: Done (status → `done`)
- **Main session:**
  - writes a three-line entry in `PROGRESS.md`: what the chapter covers, its counts (words, claims, sources, figures), and open issues;
  - sets the status;
  - commits.

### What the reader knows
Before a chapter is planned, the main session writes `checks/chNN-known.md` with `python3 scripts/progress.py known NN`: the takeaways of finished chapters numbered below NN, and the titles of earlier chapters not yet written. The synthesizer, writer, cold-reader and editor treat that file, and nothing later in the book, as the reader's knowledge. This matters most for the pilot (written first) and for Part P0 (written last).

### Resuming
- A chapter resumes from its recorded status. A `blocked` chapter shows the stage it can resume from (`progress.py show NN`); set it back to that status once the cause is fixed.
- In a fan-out stage (scouts, researchers, fact-checkers), re-run only the units whose output file is missing or incomplete.

## Delegation template (the message you send each subagent)
```
Chapter: 29 (The sim-to-real gap)
Task: <scout | research | blueprint | draft | revise | figures | fact-check | re-verify | skeptic | cold-read | prompts | bibliography | edit>
Sections: 03 (Closing the gap I: randomisation), 04 (Closing the gap II: identification)
Inputs: docs/OUTLINE-DETAILED.md §29; research/ch29/s03-sources.json; ...
Output: <exact path(s)>
Feedback to apply: <items from FEEDBACK.md or checks/ch29-feedback.md, or "none">
Return: a summary of at most 150 words. Do not paste file contents.
```

## Planning (`/plan-book`)
1. **Light scans.** For each Part, spawn `scout` agents (at most 6 in parallel) in light-scan mode: 4–6 searches per chapter. Each writes `research/chNN/scan.md` (300 words or fewer): what is new since 2025, the key primary sources, and suggested sections.
2. **Section outlines.** The `synthesizer` (one call per Part, Parts in turn) turns the scans plus `docs/OUTLINE.md` into section-level outlines and appends them to `docs/OUTLINE-DETAILED.md` itself. Each chapter gets:
   - 5–12 sections, each with a purpose and a concept list;
   - running-example hooks;
   - must-cite sources;
   - dependencies;
   - estimated length.
3. **Summarise the changes.** At the top of `docs/OUTLINE-DETAILED.md`, a "Changes from seed" section explains every split, merge or rename, and "Open questions for the human" lists at most 10.
4. **Freeze the chapter list.** If chapters changed, update `state/progress.json`, then run `python3 scripts/sync_quarto.py`. After G1 the chapter numbers are frozen.
5. **Gate G1:** stop and wait for approval, then record it in `PROGRESS.md`.

## Part review (soft gate)
At the end of each Part:
1. Run `python3 scripts/check_chapter.py --all --stage final` and rebuild any finished chapter that a shared claim has broken.
2. Render the HTML book.
3. Append a Part summary to `PROGRESS.md`:
   - chapters done or blocked;
   - total claims, broken down by evidence tag;
   - open issues;
   - any outline drift.
4. Check `FEEDBACK.md`. Continue only if it says `Mode: continuous`.

## Back matter (`/release`)
| Item | How it is built |
|---|---|
| A. Data dictionary | Compiled from ch21, plus the streams named in the P1 and P4 chapters. |
| B. Hardware component reference | Compiled from P1. |
| C. Metrics and KPI catalogue | Compiled from every Deployment lens and from ch43–49. |
| D. Equations reference | Every labelled equation, with its plain-words meaning and a link back. |
| E. Glossary | Maintained continuously; deduplicate and alphabetise at the end. |
| F. Reading paths | Fast tracks through the book for different goals. |

- **Appendices add no new facts.** Every number reuses the claim tag and citation of the chapter that established it; appendices have no ledger of their own.
- Appendices that state facts (A–D) go through the fact-checker in appendix mode (it reports problems but never changes claim statuses), a writer revise loop of at most two rounds, and the editor.
- The preface (`book/index.qmd`) is revised last, to describe the finished book.

## Usage and cost management (Max 20x, local)
- **Models:**
  - scouts, researchers, cold-reader, figure-maker and prompt-designer run on Sonnet;
  - the bibliographer runs on Haiku;
  - the synthesizer, writer, fact-checker, skeptic and editor run on Opus;
  - the main session runs on Opus (`/model opus`).
  - Optional: a Mythos-tier model (Claude Fable) can be tried for the writer or synthesizer by changing `model:` in that agent's file, if your plan offers it. Check its usage cost first, and try it on one chapter before switching: it carries extra safeguards around AI research and development, which a book about training AI models may run into.
- **Web searches:** Claude Code caps web searches per session. The project raises the cap in `.claude/settings.json` (`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`), because one chapter can need several hundred searches across its subagents.
- **Parallelism:** at most 6 at once by default. Drop to 3 if weekly usage runs hot.
- **Measuring:** after the pilot, note in `PROGRESS.md` how much of the weekly allowance one chapter used (the human checks with `/usage`). Use it to estimate the rest of the book.
- **Usage limits:** let the session wait (the `autoContinueAtUsageLimit` user setting). Never restart a finished stage.
- **Context:** the main session's context grows over a Part. The human can run `/compact` between Parts, or start a fresh session; the main session cannot do either itself. All state is in files, so nothing is lost.

## Resume protocol (every new session)
1. `python3 scripts/progress.py show`
2. Read `FEEDBACK.md` and the gate approvals in `PROGRESS.md`.
3. Continue the earliest chapter that is not done in the current Part, from its recorded status.
