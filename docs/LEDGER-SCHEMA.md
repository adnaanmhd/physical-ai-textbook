# Claim ledger schema

The ledger is the evidence base of the book. **No ledger entry, no claim.**

## Layout
- One file per section: `ledger/chNN/sSS.jsonl`, with one JSON object per line.
- Appendices have no ledger of their own. They reuse the claims (tags and citations) of the chapters they summarise.
- **All writes go through `scripts/ledger_tool.py`.** It locks the section file, validates every change and writes atomically, so parallel agents cannot corrupt a file. Direct edits to `ledger/` are blocked in `.claude/settings.json`.

| Command | Who uses it | What it does |
|---|---|---|
| `add NN SS --file claims.json` | researcher, fact-checker (refresh) | Adds claims: assigns ids, sets `status: "extracted"`, defaults `accessed` to today, skips duplicates (same claim text and source), and writes nothing if any claim is invalid. Input: one JSON object, a list, or JSON Lines. |
| `mark ID STATUS --note "..."` | fact-checker; main session for `superseded` | Sets `status`, `checked_by`, `checked_at` and `note`. |
| `update ID --set field=value` | researcher, fact-checker | Corrects a field. Changing the substance of a checked claim sends it back to `extracted`. |
| `rekey OLD NEW` | bibliographer | Merges two citation keys that name the same document, across the ledger and every book file. Refuses to merge different documents. |
| `repoint KEY URL` | bibliographer, fact-checker | Moves every claim of a key to a corrected URL, and sends them back to `extracted` for re-verification. |
| `usages ID …` · `usages --status failed,flagged,superseded` | main session, fact-checker | Where claims are tagged in the book, to route problems to every chapter that uses them. |
| `get ID` · `stats [NN]` · `validate NN \| --all` · `volatile --older-than DAYS [--used]` | everyone | Read-only views and checks. `--used` limits `volatile` to claims the book actually tags. |

## Fields
| Field | Req. | Type | Notes |
|---|---|---|---|
| `id` | yes | string | `C` + chapter + `.` + section + `-` + 3-digit counter, e.g. `C29.03-014`. Assigned by `add`. |
| `chapter` | yes | string | `"29"` (assigned by `add`) |
| `section` | yes | string | `"03"` (assigned by `add`) |
| `claim` | yes | string | One atomic fact, paraphrased in your own words, 60 words or fewer. |
| `type` | yes | enum | `definition`, `mechanism`, `number`, `date`, `result`, `limitation`, `comparison`, `forecast`, `opinion`, `spec` |
| `value` | no | string | Value with unit, e.g. `"56 %"` or `"200 Hz"`. Expected when `type` is `number` or `spec`. |
| `conditions` | no | string | For performance numbers: task, setting, trials, and what counted as success. |
| `source_key` | yes | string | BibTeX key: `firstauthorYYYYword`, or `orgYYYYword` for organisations (e.g. `nvidia2025gr00t`). One key means one document: the tool rejects a key used for two different documents. Versions of one arXiv paper, and arXiv's own DOI for it, count as one document; a published version (journal or conference DOI) is a different document with its own key. Different videos, OpenReview papers or legal acts are told apart by their URL parameters. Make keys distinctive. |
| `url` | yes | string | The primary URL (DOI link, arXiv abs page, official page). Never a banned domain. |
| `source_type` | yes | enum | `peer-reviewed`, `preprint`, `tech-report`, `company-blog`, `press-release`, `press`, `standard`, `regulator`, `talk`, `social`, `dataset`, `code`, `docs` |
| `evidence` | yes | enum | `peer-reviewed`, `preprint`, `tech-report`, `company-claim`, `demo`, `standard`, `press`. Must fit the source type (below). |
| `autonomy` | no | enum | `autonomous`, `teleoperated`, `unspecified`. Required when `evidence` is `demo`. |
| `published` | yes | string | The source's own date: `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. Never in the future. |
| `accessed` | yes | string | `YYYY-MM-DD` |
| `access` | yes | enum | `full`, `abstract` |
| `support` | yes | string | The shortest verbatim passage (50 words or fewer) that supports the claim, captured with `scripts/fetch_text.py` where possible. Internal only; never published. |
| `locator` | no | string | Section, page, table or figure in the source. |
| `volatile` | yes | bool | `true` for fast-changing facts (see `docs/SOURCES.md`). |
| `status` | yes | enum | `extracted`, `verified`, `failed`, `flagged`, `superseded` |
| `conflict_with` | no | list | IDs of conflicting claims. |
| `superseded_by` | no | string | Claim id. Required when `status` is `superseded`. |
| `checked_by` | no | string | `fact-checker` (set by `mark`) |
| `checked_at` | no | string | `YYYY-MM-DD` (set by `mark`) |
| `note` | no | string | Free text: the reason for a failure or flag, the fix applied, or how the support passage was captured. |

**Evidence allowed per source type** (enforced by the tool):

| `source_type` | allowed `evidence` |
|---|---|
| `social` | `company-claim`, `demo` |
| `press-release` | `company-claim`, `demo` |
| `company-blog` | `company-claim`, `demo`, `tech-report` |
| `press` | `press`, `company-claim`, `demo` |
| `peer-reviewed` | `peer-reviewed` |
| `standard`, `regulator` | `standard` |
| others | any |

## Example input for `add` (shown wrapped; ids and status are assigned by the tool)
```json
{"claim": "Training an object detector only on synthetic images with randomised textures, lighting and camera positions let it localise objects in real camera images.",
 "type": "result", "source_key": "tobin2017domain", "url": "https://arxiv.org/abs/1703.06907",
 "source_type": "peer-reviewed", "evidence": "peer-reviewed", "published": "2017-03",
 "access": "full",
 "support": "<the shortest verbatim passage from the source that supports the claim>",
 "locator": "Abstract", "volatile": false}
```

## Rules
- **Never delete claims.** To retire one, mark it `superseded` with `--superseded-by`.
- **One fact per claim.** Split compound statements.
- **Who sets status:** researchers create claims, which start as `extracted`. Only the fact-checker sets `verified`, `failed` or `flagged`. `superseded` is set by the fact-checker (refresh mode) or the main session.
- **Status describes the claim, not a sentence.** `failed` and `flagged` mean the source does not support the claim as recorded. A sentence that misuses a sound claim is fixed in the text, and the claim stays `verified`, because other chapters may tag the same claim.
- **Verbatim vs paraphrase:** `support` is verbatim; `claim` is a paraphrase.
- **Volatile claims carry dates.** A claim about a version, deployment, count, price, funding or ranking must carry `published` and set `volatile: true`.
- **Validate after every change:** `python3 scripts/ledger_tool.py validate NN`.
- **Tag in the text:** each claim used in a chapter appears after its sentence as `<!--C:29.03-001-->`, and the sentence cites the claim's `source_key`.
