# The Humanoid Lifecycle: how to run the build

This folder is a ready-to-run Claude Code project. Its `CLAUDE.md` makes Claude Code the editor-in-chief of a team of 11 specialist agents (scout, researcher, synthesizer, writer, figure-maker, fact-checker, skeptic, cold-reader, prompt-designer, bibliographer, editor). The team researches, writes and verifies the textbook as a Quarto book with 52 chapters and 6 appendices.

You stay in control through four gates:
- **G1:** you approve the outline.
- **G2:** you approve a pilot chapter.
- **Part reviews:** you review after each Part.
- **Final read:** you read before the release build.

---

## 1. One-time setup (macOS)
1. **Claude Code.** Install it, or update to the latest version with `claude update`, signed in with your Max plan.
2. **Quarto and helpers:**
   ```bash
   brew install --cask quarto
   brew install poppler librsvg          # PDF text for fact-checks; SVG figures in the PDF
   brew install --cask font-dejavu       # PDF fonts that keep Greek letters (π0, τ0) and ≤ ≈ →
   quarto install tinytex                # for the PDF build
   quarto install chrome-headless-shell  # Mermaid diagrams in the PDF
   ```
3. **Python 3.9 or newer.** The macOS system Python is fine (`python3 --version`). The scripts use the standard library only, so there is nothing to `pip install`.
4. **Wait out usage limits.** Add this line to `~/.claude/settings.json` (create the file if needed), so long runs wait for a usage limit to reset instead of stopping:
   ```json
   { "autoContinueAtUsageLimit": true }
   ```
5. **Unpack** this folder somewhere permanent, for example `~/Books/humanoid-lifecycle`.

## 2. First run
```bash
cd ~/Books/humanoid-lifecycle
claude
```
Accept the prompt to trust the folder: the project's pre-approved tools (web search, the scripts, git commits) only apply in a trusted folder. Then, inside Claude Code:
1. `/model opus`: the main session should run on Opus.
2. `/setup-check`: verifies the tools, runs the script self-test, renders the empty book skeleton, test-builds a one-page PDF and initialises git.
3. `/plan-book`: light-scans every chapter for the current state of the art and writes `docs/OUTLINE-DETAILED.md`. **Gate G1:** read it, starting with "Changes from seed" and "Open questions", then reply `approved` or write notes in `FEEDBACK.md`.
4. `/build-chapter 29`: the pilot chapter (The sim-to-real gap). Preview it with `quarto preview book` in a second terminal tab. **Gate G2:** reply with feedback or `approved`. General points become part of `docs/STYLE.md` for every later chapter, and the pilot is revised to match before you approve it. Check `/usage` after the pilot to see what one chapter costs.
5. `/build-part P1`, then P2 … P12, then P0. Chapter 1 is written last because it summarises the whole book.
6. `/release`: writes the appendices and preface, then stops for your **final read**. `/release build v1.0` then stamps the date, builds HTML, PDF and EPUB, and tags the release.

## 3. Running unattended
- **Keep the Mac awake and on power.** Run `caffeinate -dimsu` in a separate terminal tab for the duration.
- **Permission prompts.**
  - The project settings pre-approve web search, fetches, the build scripts and git commits, and block `git push`, `rm -rf` and hand edits to the claim ledger.
  - Recent versions of Claude Code start in auto mode, where a safety classifier approves routine actions instead of asking you. If yours asks for permission often, start it with `claude --permission-mode auto`.
- **Keep going across turns with `/goal`:**
  ```
  /goal Every chapter in Part P4 has status "done" (show it with python3 scripts/progress.py show), python3 scripts/check_chapter.py --all --stage final exits 0, and quarto render book --to html succeeds. Stop and report if any chapter becomes blocked.
  ```
- **Gates still apply.** By default each Part stops for your review. To let it roll straight into the next Part, change `Mode: gated` to `Mode: continuous` in `FEEDBACK.md`.
- **Context.** Between Parts, run `/compact` (or start a fresh `claude` session). Everything lives in files, so nothing is lost.

## 4. Steering while it runs
- **Notes:** write them in `FEEDBACK.md` at any time, in the form `- [ ] (style|outline|chNN|general) note`. They are applied before the next chapter. `/apply-feedback` applies them immediately.
- **Watching progress:**
  - `/book-status`;
  - `PROGRESS.md` (gate approvals, three lines per chapter, a summary per Part);
  - `quarto preview book` for the live book.
- **Checking a chapter after you edit it by hand:** `/verify-chapter NN`.
- **Keeping it current later:** `/refresh` re-checks every fast-moving fact (versions, deployments, prices, regulation) older than 60 days and stamps a new "current as of" date.

## 5. Commands
| Command | What it does |
|---|---|
| `/setup-check` | Environment check, script self-test, skeleton render, git init |
| `/plan-book` | Section-level outline for gate G1 |
| `/build-chapter NN` | The full pipeline for one chapter, resuming wherever it stopped |
| `/build-part Pn` | Every chapter in a Part, then a Part summary |
| `/verify-chapter NN` | Re-verify a chapter after edits |
| `/apply-feedback` | Apply `FEEDBACK.md` now |
| `/refresh` | Re-verify volatile facts and update the date stamp |
| `/book-status` | Where things stand |
| `/release` | Back matter and final read; then `/release build v1.0` publishes |

## 6. What's inside
```
CLAUDE.md                 the editor-in-chief's brief (loaded every session)
docs/                     brief, style contract, sources policy, ledger schema, pipeline,
                          seed outline (52 chapters), running examples
.claude/agents/           the 11 specialist agents
.claude/skills/           the 9 commands above
.claude/rules/            rules that load when chapter or ledger files are edited
.claude/settings.json     pre-approved tools, blocked actions, the raised web-search cap
state/                    chapter status (source of truth) and the running list of takeaways
research/ ledger/         sources and the verified claim ledger (one file per section)
blueprints/ checks/       teaching plans and review reports
book/                     the Quarto book (chapters, appendices, figures, bibliography)
scripts/                  checker, ledger and research tools, verbatim fetcher, SVG and PDF
                          checks, progress tool, sources-table generator, self-test
FEEDBACK.md PROGRESS.md   your inbox, and the production log
```

## 7. How quality is enforced
- **Claim ledger.** Every factual sentence carries a claim tag that points to a ledger entry. Each entry holds the source, its date, its evidence tag and a verbatim supporting passage. Agents can only write the ledger through `scripts/ledger_tool.py`, which validates every change.
- **Automatic checks.** `scripts/check_chapter.py` refuses to pass a chapter that has:
  - an unverified or failed claim, a claim tag whose source the sentence does not cite, or a citation key whose bibliography entry is a different document from the one the claim came from;
  - an untagged quantity in the prose, a caption or a table: a unit, percentage, amount of money, year, count or "million/billion" (illustrative numbers must be marked as such; other numbers are listed for review);
  - a missing citation, a quote over 15 words, or a broken cross-reference;
  - a concept without all five layers.
- **Independent fact-check.** Fact-checkers that did not write the chapter re-fetch the sources and verify every claim, matching the supporting passage word for word where the source can be fetched. Nothing is sampled. A separate skeptic agent hunts for hype: demos presented as deployments, company claims presented as facts, missing denominators.
- **Honest labelling.** Evidence tags are visible to you in each chapter's source table. Company claims, demos and inference are badged in the text.

## 8. Expectations
- **Scale.** This is a book-length, research-heavy build, so plan for it to run over weeks, not days. The pilot chapter gives you a real per-chapter number for time and usage; extrapolate from that.
- **Hard stops.** The pipeline stops at G1 and G2 by design. Approve them deliberately: they set the shape and voice of every chapter.
- **Model choice.** Opus does the heavy writing and checking. If your plan offers Claude Fable, you can try it for the writer or synthesizer by changing `model:` in that agent's file; check its usage cost and test it on one chapter first, since it has extra safeguards around AI research and development that a book about training AI models may run into.

## 9. Troubleshooting
- **A chapter is `blocked`:** run `python3 scripts/progress.py show NN` to see the reason. Fix the cause, then `/build-chapter NN`.
- **The session ended mid-chapter:** start `claude` again (or `claude --continue`) and run `/build-chapter NN`. All state is on disk, so the chapter resumes from its last finished stage.
- **Tools keep asking for permission:** make sure you accepted the folder-trust prompt, and start with `claude --permission-mode auto`.
- **Research stops early with a web-search limit:** the cap is raised in `.claude/settings.json` (`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`). If your organisation's settings override it, raise it there.
- **A ledger line is invalid JSON:** `python3 scripts/ledger_tool.py validate NN` names the file and line. Agents cannot edit ledger files, so fix or delete that one line yourself, then rerun the chapter.
- **Citations show as `?@key`:** the bibliographer has not added that key yet. Run `/verify-chapter NN`.
- **The PDF build fails, or Greek letters and symbols are missing from it:** run `python3 scripts/pdf_check.py`, which names the fix: `quarto install tinytex`, `brew install --cask font-dejavu`, `quarto install chrome-headless-shell` (Mermaid diagrams) or `brew install librsvg` (SVG figures).
- **Fact-checks report "pdftotext is not installed":** `brew install poppler`.
- **A chapter you already approved changed status:** a claim it shares with another chapter was flagged or superseded. Its `checks/chNN-feedback.md` says which; `/build-chapter NN` revises it.
