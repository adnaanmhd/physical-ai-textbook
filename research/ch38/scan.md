# ch38 scan · Training world models: pre-, mid- and post-training and RL (scanned 2026-10-06)
## What is new since 2025
- NVIDIA's Cosmos line moved from the 2025 platform paper to Cosmos-Predict2.5 (200M curated clips, RL post-training, 2B/14B; v2 Feb 2026) and a Cosmos 3 report dated 2026-06-22 (unconfirmed: PDF too large to open).
- World action models (WAMs) now start from a pretrained video diffusion backbone: DreamZero (14B) trains video and actions jointly.
- RL post-training for video models is now a crowded field: Flow-GRPO (image, 2025), then world-model variants (WorldCompass, VGGRPO, WorldCycle, WorldReward, PhysRVG), all surfaced by search only.
- Genie 3 disclosed capabilities but, as far as the announcement shows, no training recipe.
## Key primary sources
- World Simulation with Video Foundation Models for Physical AI (Cosmos-Predict2.5) — NVIDIA — 2025-10-28 (v2 2026-02-24) — https://arxiv.org/abs/2511.00062 — preprint — pre-training data scale plus RL post-training
- Cosmos World Foundation Model Platform for Physical AI — NVIDIA — 2025-01 — https://arxiv.org/abs/2501.03575 — preprint — curation pipeline, tokenizers, post-training examples (date not opened)
- Cosmos 3: Omnimodal World Models for Physical AI — NVIDIA — 2026-06-22 — https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf — tech-report — unconfirmed; newest Cosmos recipe
- V-JEPA 2 — Assran et al., Meta — 2025-06-11 — https://arxiv.org/abs/2506.09985 — preprint — 1M+ hours pre-training, then action-conditioned post-training (-AC)
- World Action Models are Zero-shot Policies (DreamZero) — Ye et al., NVIDIA GEAR — 2026-02-17 — https://arxiv.org/abs/2602.15922 — preprint — video backbone turned robot policy
- Flow-GRPO — Liu et al. — 2025-05-08 — https://arxiv.org/abs/2505.05470 — preprint — online RL for flow-matching models
- World-VLA-Loop — Liu et al. — 2026-02-06 — https://arxiv.org/abs/2602.06508 — preprint — world model and policy co-improve in a loop
- Genie 3: A new frontier for world models — Google DeepMind — 2025-08-05 — https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/ — company-claim — capabilities; no training details
- 1X World Model — Monas, Jang, 1X — 2024-09-17 — https://www.1x.tech/discover/1x-world-model — company-claim — data scale; evaluation framed as future goal
## Suggested sections
Follow the seed list; add "Recipes by stage" as a table (Cosmos, V-JEPA 2, DreamZero, Genie 3, 1X), marking undisclosed stages.
## Surprises and controversies
- Recipes are opaque for closed models (Genie 3, 1X): the stage map will have gaps.
- DanceGRPO and the physics-reward RL papers were not opened; treat as leads.
- Cosmos 3 detail needs a second route to the PDF.
