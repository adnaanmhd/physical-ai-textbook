# Style contract

The writer, editor and every reviewer apply this file. Feedback from the pilot chapter (gate G2) is folded in here, so re-read it before every chapter.

## Voice
- **Tone:** clear, warm and precise. Write like a great teacher explaining to a smart colleague from another field.
- **Sentences and paragraphs:**
  - Short sentences, averaging 22 words or fewer.
  - One idea per paragraph.
  - Active voice.
- **Terms:** define every technical term at first use, in the sentence where it appears, and add it to `book/appendices/e-glossary.qmd`.
- **No filler:**
  - no hype adjectives ("revolutionary", "game-changing");
  - no rhetorical questions as filler;
  - no "in this chapter we will" padding beyond the opener.
- **Numbers beat adjectives.** Give concrete numbers with units, conditions and dates.
  - Good: "Figure reports 56% whole-task success across 30 unfamiliar homes (September 2026)". (A format example: in a chapter, this fact needs its own verified ledger entry like any other.)
  - Weak: "strong generalisation".
- **Spelling and units:**
  - British spelling with -ise forms. Proper names keep their own spelling: a paper titled "Domain Randomization for…", a model called a "Large Behavior Model".
  - SI units; give a conversion only when the source uses another unit.
  - Number formats: 1,250; 0.5 mm; 30 Hz.
- **Neutrality:** never favour a lab. Attribute claims, and present disagreements fairly.

## Chapter skeleton
~~~markdown
# Chapter title {#sec-chNN}

Opener: 3–5 sentences on what this chapter covers and why it matters for
deployment readiness and post-deployment improvement.

::: {.callout-note title="Before you start"}
Builds on: @sec-chAA (concept), @sec-chBB (concept). New terms: …
:::

## Section heading {#sec-chNN-slug}

### Concept heading {#sec-chNN-concept-slug .concept}
(five-layer template, below)

### A heading that is not a concept {#sec-chNN-aside-slug .aside}
(a worked example, a comparison table: any other third-level heading carries .aside)

## Key takeaways {#sec-chNN-takeaways}
::: {.callout-tip title="Key takeaways"}
- 5–9 bullets, each a complete, self-contained sentence.
:::

## People, tools and costs {#sec-chNN-ptc}
(lifecycle chapters only: roles, tools, public cost figures with sources, cost drivers)

## Research prompts {#sec-chNN-prompts}
1. Prompt… *A strong answer would…*

## Sources for this chapter {#sec-chNN-sources}
{{< include _sources/chNN.qmd >}}
~~~

## The five-layer concept template
Every concept or component heading carries the `.concept` class and contains the following, in this order.

1. **ELI5**: `::: {.callout-tip title="ELI5"}`.
   - 2–5 sentences, no jargon.
   - Use an everyday analogy that maps onto the real mechanism. The analogy must not mislead.
2. **First principles**: `::: {.callout-note title="First principles"}`.
   - Explain why it has to be this way: the physical, mathematical, informational or economic constraint underneath.
   - Derive; do not assert. 3–8 sentences.
3. **How it's actually done**: a paragraph that opens with the bold lead `**How it's actually done.**`.
   - Prose, with tables, figures and equations as needed, running from the basic version to the advanced and frontier versions.
   - Give real numbers, named systems, dates and citations.
4. **Deployment lens**: `::: {.callout-important title="Deployment lens"}`.
   - Cover what breaks in the field, what gets measured (metrics and KPIs), and how it improves after launch.
   - Keep it generic, with no company strategy.
5. **Citations**: inline, in every layer where claims appear. The chapter's source table is generated automatically.

Optional blocks, used where they add value:
- `::: {.callout-caution title="Running example: <name>"}`: apply the concept to one of the four tasks.
- `::: {.callout-note collapse="true" title="Under the hood: the maths"}`: longer derivations.
- `::: {.callout-tip title="Try it"}`: a pointer to an open model, dataset or tool the reader can explore, naming it and saying what to look at. No code.

## Evidence in the text
- **Every factual sentence** gets a citation plus a claim tag:
  `… in 30 unfamiliar homes [@figure2026helix25]. <!--C:42.03-012-->`
  - The tag goes right after the sentence it supports.
  - The citation in the sentence must be the claim's own source (its `source_key` in the ledger).
  - Use one tag per claim; a sentence can carry several tags, and a claim can be tagged again where it is reused (in takeaways, say).
- **Tables:** every row that states a number carries its citation and claim tag inside the row, for example in a final Source column: `[@unitree2025g1] <!--C:05.02-007-->`.
- **Illustrative numbers.** A made-up example ("suppose the box weighs 2 kg") is not a fact about the world. End its sentence with `<!--nofact-->`, or put `<!--nofact-->` on its own line above an illustrative table. The checker treats any untagged number as an unverified fact at the final stage, and the fact-checker audits every `nofact` marker, so never use it for a fact you could not source.
- **Company claims and demos:**
  - Attribute them in the sentence ("Figure reports…", "In a demonstration video, …").
  - Add a badge right after the citation, before the full stop: `… without a fall [@key] [company claim]{.ev}. <!--C:…-->`. Badges are `[company claim]{.ev}`, `[demo]{.ev}` and `[inference]{.ev}`.
  - For demos, say whether the run was autonomous, teleoperated or unspecified.
- **Reasoning that goes beyond the sources:** mark it `[inference]{.ev}` and make the reasoning visible.
- **Disagreements:** state both positions with attribution, then say which evidence is stronger and why.
- **TODOs:** if a needed fact has no claim, write `<!--TODO: need claim for …-->` and never invent one. TODOs must be gone before the final stage.

## Equations
Use this order:
1. A plain-words explanation.
2. The display equation, with a label.
3. A symbol-by-symbol walk-through as a bullet list.
4. What the equation means in practice.

~~~markdown
The policy is trained to make the demonstrated action as likely as possible under its own predictions.

$$
\mathcal{L}(\theta) = -\,\mathbb{E}_{(o,a)\sim\mathcal{D}}\big[\log \pi_\theta(a \mid o)\big]
$$ {#eq-ch31-bc}

- $\pi_\theta(a \mid o)$: how likely the policy with settings $\theta$ thinks action $a$ is after seeing observation $o$.
- $\mathcal{D}$: the dataset of recorded demonstrations.
- $\mathbb{E}$: "on average over the dataset".

In practice: the policy copies what demonstrators did, so it can only be as good and as varied as the demonstrations.
~~~

## Figures and tables
- **Originality:** every figure is original, made by the figure-maker.
  - Use Mermaid for flows and hierarchies, and SVG for schematics.
  - Put a `<!--FIG: name — what it should show-->` marker where a figure belongs.
- **Captions and alt text:** the caption states the takeaway. Always include alt text.
- **Numbers in figures** come from ledger claims. Cite the source in the caption and add the claim tag:
  - image figures: inside the caption, after the citation, as in `![Success fell to 40% [@key]. <!--C:29.03-003-->](../figures/ch29/x.svg){#fig-ch29-x fig-alt="…"}` (a tag on its own line under an image stops Quarto from treating it as a figure);
  - Mermaid figures: on the line right after the closing fence.
- **Labels:** figures use `{#fig-chNN-name}` and tables `{#tbl-chNN-name}`. Refer to them in the text (`@fig-chNN-name`).
- **Spec tables** (hardware, datasets, models) sit next to the concept they belong to, with citations and an "as of" date.

## Cross-references
- Use `@sec-chNN` labels.
- Teach each concept once. Elsewhere, give a one-sentence recap and a cross-reference.
- A chapter may point forward, but only to a chapter label ("covered in @sec-ch29"): sections of chapters not yet written have no labels, so a reference to them would break.

## Lengths
- There is no cap. A typical chapter runs 7,000–14,000 words.
- Above roughly 18,000 words, propose a split in `PROGRESS.md` rather than cutting substance.

## Worked example (format only; ch29 will re-research the content)
~~~markdown
### Domain randomisation {#sec-ch29-domain-randomisation .concept}

::: {.callout-tip title="ELI5"}
Imagine learning to catch only in your own garden on calm days, then playing in a storm.
You would struggle. Now imagine practising with heavy balls, light balls, wind, rain and
glare. When the storm comes, it feels like one more variation. Domain randomisation trains
a robot in thousands of slightly different simulated worlds so that the real world feels
like one more of them.
:::

::: {.callout-note title="First principles"}
A simulator is never an exact copy of reality: friction, masses, motor strength, delays,
lighting and camera noise are all slightly wrong. A policy trained in one fixed simulation
learns to exploit that simulation's exact quirks. If each training episode instead samples
these quantities from ranges wide enough to contain the real values, no single quirk can
be relied on, so the policy must learn behaviour that works across the whole range. Reality
then sits inside the range it has already mastered. The price is caution: a policy robust to
everything may be slower than one tuned to the true world.
:::

**How it's actually done.** The idea was popularised for vision by randomising textures,
lighting and camera poses, so that an object detector trained only on rendered images
worked on real camera images [@tobin2017domain]. <!--C:29.03-001--> Later work widened
the ranges automatically as the policy improved, an approach called automatic domain
randomisation [@openai2019rubiks]. <!--C:29.03-002--> …

::: {.callout-important title="Deployment lens"}
**What breaks:** conditions outside the randomised ranges, such as a new floor surface or
a stiffer connector. **What to measure:** success rate as each physical parameter moves
toward the edges of its range. **How it improves after launch:** field logs reveal which
real parameters fell outside the ranges; widen those ranges and retrain.
:::
~~~
