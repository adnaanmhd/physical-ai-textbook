---
paths:
  - "book/chapters/**/*.qmd"
  - "book/appendices/**/*.qmd"
  - "book/index.qmd"
---
# Rules for book files
- **Concept headings** carry `{.concept}`. Each contains, in order:
  1. `::: {.callout-tip title="ELI5"}`
  2. `::: {.callout-note title="First principles"}`
  3. a `**How it's actually done.**` paragraph
  4. `::: {.callout-important title="Deployment lens"}`
- **Every factual sentence** carries `[@key]` and `<!--C:NN.SS-XXX-->`, and the claim's `source_key` must be the key cited in that sentence. Never state a fact that has no ledger entry; use `<!--TODO: ...-->` instead.
- **Illustrative numbers** (a made-up example, not a fact about the world) end their sentence with `<!--nofact-->`. An illustrative table gets `<!--nofact-->` on its own line just above it. Never use the marker to dodge a missing source.
- **Figure claim tags:** inside the caption for image figures (`![Caption [@key]. <!--C:…-->](path){#fig-…}`); on the line right after the closing fence for Mermaid figures.
- **Headings:** every `###` heading carries `.concept` (and the five layers) or `.aside`.
- **Attribute** company claims and demos, and badge them with `[company claim]{.ev}` or `[demo]{.ev}`.
- **Quotes:** at most 15 words, one per source per chapter. No copied figures.
- **Cross-references** point only to labels that exist. Forward references go to chapter labels (`@sec-chNN`) only.
- **Spelling:** British, with -ise forms. Never "correct" proper names (product, paper and company names keep their own spelling).
- **After editing** a chapter, run `python3 scripts/check_chapter.py NN --stage draft` while drafting, and `--stage final` before the chapter can be marked done.
