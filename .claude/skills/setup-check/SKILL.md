---
description: Verify the production environment before the first run. Checks tools, the script self-test, the citation style, the Quarto skeleton render, the PDF toolchain and git. Run once after unpacking, and again after upgrades.
disable-model-invocation: true
allowed-tools:
  - Bash(python3 *)
  - Bash(quarto *)
  - Bash(git *)
  - Bash(curl -sSL *)
  - Bash(ls *)
  - Bash(which *)
---
Check the environment, and report one line per check: PASS, or FAIL with the exact fix. Do not install anything yourself; give the human the command.

1. **Tool versions.**
   - `python3 --version` must be 3.9 or newer (the macOS system Python is fine).
   - `quarto --version` must be 1.5 or newer. If missing: `brew install --cask quarto`.
   - `git --version`.
2. **Helpers:** `which pdftotext` and `which rsvg-convert`. If either is missing: `brew install poppler librsvg`. pdftotext lets `scripts/fetch_text.py` read PDF papers; rsvg-convert puts SVG figures into the PDF.
3. **Script self-test:** `python3 scripts/selftest.py` must print `ALL TESTS PASSED`.
4. **Citation style.** If `book/ieee.csl` is missing, download it:
   `curl -sSL https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl -o book/ieee.csl`
   Then confirm the file starts with `<?xml`.
5. **Book skeleton.**
   - `python3 scripts/sync_quarto.py` writes `book/_quarto.yml` and creates the chapter stubs.
   - `quarto render book --to html` must succeed.
6. **PDF toolchain** (needed for the release; better found now): `python3 scripts/pdf_check.py` renders a one-page sample and confirms that Greek letters and symbols survive (π0, τ0, ≤, ≈, →). It names the fix when something is missing:
   - `quarto install tinytex` (LaTeX);
   - `brew install --cask font-dejavu` (the book's PDF fonts);
   - `quarto install chrome-headless-shell` (Mermaid diagrams);
   - `brew install librsvg` (SVG figures).
7. **Git.** If `.git` does not exist: `git init`, then `git add -A && git commit -m "Initial production setup"`.
8. **Reminders for the human:**
   - `~/.claude/settings.json` should contain `"autoContinueAtUsageLimit": true`. It is a user-level setting, so the project cannot set it.
   - Keep the Mac awake and on power during long runs: `caffeinate -dimsu` in a separate terminal tab.
   - If tools keep asking for permission, the folder may not be trusted yet: project permissions apply only after the folder-trust prompt is accepted.

Finish by printing the next step: "Run `/plan-book` to create the section-level outline (gate G1)."
