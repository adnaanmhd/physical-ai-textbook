---
paths:
  - "ledger/**"
---
# Rules for the claim ledger
- **Never edit ledger files by hand,** and never write them with Write or Edit. Use `python3 scripts/ledger_tool.py`:
  - `add NN SS --file claims.json` to add claims (it assigns ids, dedupes, validates and locks the file);
  - `mark ID STATUS --note "..."` to change status (fact-checker only);
  - `update ID --set field=value` to correct a field;
  - `repoint KEY URL` to correct the URL of every claim of a key (they return to `extracted`);
  - `rekey OLD NEW` to merge two keys that name the same document (bibliographer only).
- Each section has one file, `ledger/chNN/sSS.jsonl`, following `docs/LEDGER-SCHEMA.md`. Appendices have no ledger: they reuse chapter claims.
- Never delete claims. Retire one by marking it `superseded` with `--superseded-by`.
- `support` is verbatim, 50 words or fewer, and internal only. `claim` is a paraphrase.
- Validate after every change: `python3 scripts/ledger_tool.py validate NN`.
