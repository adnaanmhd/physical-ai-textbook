# ch18 scan · Learning from people: web video, egocentric video and motion capture (scanned 2026-10-06)
## What is new since 2025
Egocentric data has become the main route for learning from people. EgoDex (829 h, Apple Vision Pro hand tracking) set the template. EgoScale reports a log-linear law over 20,854 h. EgoVerse (1,362 h, 2,087 demonstrators) pools labs. HumanVerse-500 adds whole-body capture for humanoids. Aria Gen 2 shipped to researchers in 2026. Latent-action methods (LAPA, then CLAP and others) and glove capture (Sunday) now compete with hand-pose retargeting.
## Key Primary Sources
- Ego4D — Grauman et al. — 2021-10-13 — https://arxiv.org/abs/2110.07058 — peer-reviewed — 3,670 h baseline; CVPR 2022
- EgoDex — Hoque et al. (Apple) — 2025-05-16 — https://arxiv.org/abs/2505.11709 — preprint — 829 h with 3D hand tracking
- EgoMimic — Kareer et al. — 2024-10-31 — https://arxiv.org/abs/2410.24221 — preprint — Aria-glasses co-training; human data more valuable
- Aria Gen 2 announcement — Meta — 2025-02-27 — https://www.meta.com/blog/project-aria-gen-2-next-generation-egocentric-research-glasses-reality-labs-ai-robotics/ — company-claim — device specs
- Aria Gen 2 Pilot Dataset — Kong et al. — 2025-10-17 — https://arxiv.org/abs/2510.16134 — preprint — cooking, cleaning scenarios
- LAPA — Ye et al. — 2024-10-15 — https://arxiv.org/abs/2410.11758 — peer-reviewed — latent actions from video; ICLR 2025
- EgoScale — Zheng et al. — 2026-02-18 — https://arxiv.org/abs/2602.16710 — preprint — 54% gain from human pretraining
- EgoVerse — Punamiya et al. — 2026-04-08 — https://arxiv.org/abs/2604.07607 — preprint — 1,362 h multi-lab human data
- What Matters When Cotraining on Everyday Human Videos? — Li et al. — 2026-06-04 — https://arxiv.org/abs/2606.06627 — preprint — hand-pose accuracy; +29.7% low-data
- HumanVerse-500 / λ₀ — Xu et al. — 2026-09-30 — https://arxiv.org/abs/2610.00438 — preprint — 500 h whole-body egocentric
## Suggested sections
Follow the seed list; add "scaling human data" (EgoScale, Dyna-2, HumanScale) and "wearable data collection at scale" (AoE, https://arxiv.org/abs/2602.23893; Sunday glove; Figure Index).
## Surprises and controversies
- Human video reportedly beats robot data (HumanScale, Dyna-2). These are new and unreplicated.
- Not found or unconfirmed: Being-H0.5/H0.7, DexUMI, HOT3D, AMASS, 1X data mix, Ego-Exo4D primary paper (only a Meta blog seen).
- Force remains missing; a 2026 glove-force paper (arXiv 2609.14173) appeared in search but is unopened.
