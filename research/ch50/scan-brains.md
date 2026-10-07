# Robot-brain, data and open-source organisations beyond the starting list (scanned 2026-10-07)

## What is new since 2025
- Open releases have moved from academic baselines to company-grade models. Black Forest Labs (FLUX 3 Action, 2026-09-23), Xiaomi, Ant Group's Robbyant, Ai2, Alibaba and X-Humanoid all ship weights. Several also ship training code or recipes.
- Video-first policies are a second family beside VLAs. Rhoda AI and Mimic Robotics pre-train on video, then learn actions from a small amount of robot data.
- Egocentric data is now sold and published as a public good. Build AI released 100K hours under Apache 2.0, and EgoVerse is an academic multi-lab set.
- Hugging Face's LeRobot is now the common glue. Ai2 and BFL both ship LeRobot integrations.
- Big platforms entered with little disclosure: Microsoft (Rho-alpha), Amazon (FAR), Mistral (Robostral Navigate).

## Organisations and open releases
(organisation — kind — source — date — URL — evidence — publishes)
- Hugging Face — open-source stack — LeRobot: An Open-Source Library for End-to-End Robot Learning — 2026-02-26 — https://arxiv.org/abs/2602.22818 — preprint — code, data hub. SmolVLA (arXiv 2506.01844, https://arxiv.org/abs/2506.01844; abstract seen in search only, unconfirmed) has weights.
- Black Forest Labs — model (7B world-action) — FLUX 3 Action: a world action model you can fine-tune — 2026-09-23 — https://huggingface.co/blog/black-forest-labs/flux-3-action — company-claim — weights, code, recipe (FLUX Kommunity License; the open-weights label is looser than OSI-open). Research notes: https://bfl.ai/models/flux-3-action (not opened).
- Ai2 — model + data — MolmoAct 2 — 2026-05-05 — https://allenai.org/blog/molmoact2 — company-claim — weights, code, recipes, 720+ h bimanual dataset.
- Ant Group (Robbyant) — model — A Pragmatic VLA Foundation Model (LingBot-VLA) — 2026-01-26 — https://arxiv.org/abs/2601.18692 — preprint — code, weights, GM-100 benchmark data. About 20K hours. Version 2.0 (60K hours, July 2026) is press only: unconfirmed.
- Xiaomi — model — Xiaomi-Robotics-1 — 2026-07-16 — https://arxiv.org/abs/2607.15330 — preprint — weights and code on Hugging Face (https://huggingface.co/XiaomiRobotics/Xiaomi-Robotics-1-5B, seen in search); the 100K-hour data is in-house.
- X Square Robot — model — Igniting VLMs toward the Embodied Space (WALL-OSS) — 2025-09-15 — https://arxiv.org/abs/2509.11766 — preprint — weights and training code (per press).
- X-Humanoid (Beijing) — model — Pelican-VL 1.0 — 2025-10-30 — https://arxiv.org/abs/2511.00108 — preprint — open 7B to 72B; DPPO recipe (RL, refine, diagnose, SFT loop).
- Alibaba DAMO / Qwen — model — RynnBrain — 2026-02-24 — https://www.alibabacloud.com/blog/alibaba-unveiled-open-sourced-embodied-foundation-model-for-robotics_602898 — company-claim — weights, code; data undisclosed. Qwen-Robot suite (Manip, Nav, World) — 2026-06-17 — https://www.alibabacloud.com/blog/qwen-robotworld-boundless-worlds-for-embodied-agents_603268 — company-claim — 8.6M video-text pairs for RobotWorld; open status unconfirmed.
- ByteDance Seed — model — GR-3 Technical Report — 2025-07-23 — https://arxiv.org/abs/2507.15493 — tech-report — recipe (web VL co-training, VR human trajectories); weights not confirmed.
- RLWRLD (Korea) — model — RLDX-1 Technical Report — 2026-05-05 — https://arxiv.org/abs/2605.03269 — preprint — recipe; release not stated.
- Mimic Robotics (Zurich) — model — mimic-video — 2025-12-17 — https://arxiv.org/abs/2512.15692 — preprint — code at https://github.com/mimic-video/mimic-video (seen in search, unopened).
- Rhoda AI — model (video-action) — Causal Video Models Are Data-Efficient Robot Policy Learners — 2026-03-10 — https://www.rhoda.ai/research/direct-video-action — company-claim — none (10–20 h robot data per task). Scaling post 2026-09-10: https://www.rhoda.ai/research/scaling-web-video-pretraining — none. $450M Series A confirmed on its news page.
- Sunday Robotics — model + data hardware — ACT-1, "zero robot data" — 2025-11-19 — https://www.sunday.ai/blog/no-robot-data — company-claim — none. The page gives no data volume; the "10 million routines, 500 homes" figure is press only.
- Microsoft Research — model — Rho-alpha (tactile VLA+) — 2026-01 — https://www.microsoft.com/en-us/research/story/advancing-ai-for-the-physical-world/ — company-claim — none (early-access programme).
- Amazon FAR — model — DeepFleet / robotics model post — https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model — company-claim — none; page undated.
- Mistral AI — model — Robostral Navigate (8B, navigation) — 2026-07-08 — Bloomberg https://www.bloomberg.com/news/articles/2026-07-08/mistral-ai-releases-robotics-model-to-support-physical-ai-push (not opened; unconfirmed) — press — weights not public per secondary sources.
- Genesis AI — model + simulator — GENE-26.5 — 2026-05 — https://www.therobotreport.com/genesis-ai-introduces-gene-foundation-model-more-dexterous-manipulation/ — press — none. Its press page fetch returned the wrong content: unconfirmed.
- Physical Intelligence (already listed) — openpi — https://github.com/Physical-Intelligence/openpi — code — weights for π0, π0-FAST, π0.5.
- Build AI — data — Egocentric-100K — 2025-12 (per search) — https://huggingface.co/datasets/builddotai/Egocentric-100K — dataset card — data: 100K+ h factory video, Apache 2.0. Egocentric-1M: unconfirmed.
- EgoVerse (multi-institution) — data — EgoVerse — 2026-04-08 — https://arxiv.org/abs/2604.07607 — preprint — data: 1,362 h, 80K episodes.
- Stanford / Toyota Research Institute / Berkeley — data and stack — DROID, Open X-Embodiment, UMI (https://arxiv.org/abs/2402.10329) — preprint/peer-reviewed — data and code. Foundational; DROID details from search only.
- Hexagon — AEON humanoid; uses GR00T post-training and Isaac Sim, with no model of its own published. Primary page returned 403, so claims are press-derived: unconfirmed.

## Suggested additions to ch50 (and ch17–ch19, ch31–ch34)
- ch50: a short "Open and academic stacks" section (LeRobot, openpi, MolmoAct 2, FLUX 3 Action, Xiaomi, LingBot, Pelican, WALL-OSS), then a one-paragraph profile each for Sunday, Rhoda, Mimic, Genesis, Microsoft, Amazon, Mistral. Hexagon is a user of GR00T, not a brain builder.
- ch17–ch19: Build AI, EgoVerse, DROID, Open X and UMI as the open data layer. Sunday (gloves) and Genesis (hand plus simulator) as proprietary capture.
- ch31–ch34: only open recipes can be checked. Use MolmoAct 2, FLUX 3 Action, LingBot, Pelican (DPPO as a post-training RL example) and openpi as worked recipes. Contrast with the closed ones (Rhoda, Sunday).

## Surprises and controversies
- "Open" varies widely: Apache 2.0 data, versus the FLUX Kommunity License, versus "will be released" (Xiaomi abstract promised checkpoints, and Hugging Face pages now exist).
- Rhoda and Sunday publish strong claims with no weights, data size or model size.
- Mistral's open-weights habit stopped at robotics.
- Gaps: no primary found for Amazon's FAR model, Genesis, Qwen-Robot licensing or Hexagon. I found no confirmed European VLA beyond Mimic. Samsung, Toyota and Korean labs were not covered.
