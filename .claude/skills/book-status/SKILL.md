---
description: Show production status, covering chapters by status, blocked items, claim totals, open feedback and the next action. Use when the human asks how the book is going.
allowed-tools:
  - Bash(python3 scripts/*)
---
1. Run `python3 scripts/progress.py show`.
2. Run `python3 scripts/ledger_tool.py stats`.
3. Run `python3 scripts/progress.py next`.
4. Count the open items in `FEEDBACK.md`, and check `PROGRESS.md` for the gates approved so far.
5. Reply in 15 lines or fewer:
   - chapters done / in progress / blocked (with reasons);
   - the current Part, and the gates passed;
   - claims by status and evidence tag;
   - open feedback items;
   - the single next action.
