# Open-source world models scan (scanned 2026-10-07)

Method: about 22 searches and 20 page fetches. Details come from abstract pages, repository READMEs and, where noted, the HTML of the report. Fetches were read through a summariser and long reports were only partly read (noted per item). Re-open the report before quoting any number.

## What is new since 2025
The strongest open "recipe" disclosures are not from the big labs but from teams that build on an open video backbone and say so. NVIDIA's Cosmos-Predict2.5 report gives the fullest pre-training and post-training numbers. LingBot-World states the three-stage split (pre, middle, post) outright. Open WAM and interactive-model papers from September 2026 (OpenWAM, SolarWM) promise data, recipes and weights together. RL for world models now has an open implementation: WorldCompass, run on Tencent's WorldPlay.

## Open releases
Stage key: pre / mid / post / RL. "Full recipe" means all four stages are described with data, amounts and conditioning.

- Cosmos-Predict2.5 — NVIDIA — World Simulation with Video Foundation Models for Physical AI — 2025-10-28 (v2 2026-02-24) — https://arxiv.org/abs/2511.00062 — preprint — pre (200M curated clips from over 6B candidate clips; 5-phase resolution curriculum; 4,096 H100s), mid (not separately named), post (five domain models: robotic manipulation 730K videos, driving 3.1M, object permanence 10.4M, high motion 1.0M, complex scenes 1.6M; plus model soup merge), RL (VLM reward model VideoAlign; 256 steps) — NVIDIA Open Model License. Closest to a full recipe. Read from the HTML, first 100,000 of 176,627 characters only; the action-conditioned robot section was not reached.
- Cosmos 3 — NVIDIA — Cosmos 3: Omnimodal World Models for Physical AI — 2026-06-01 (final 2026-06-23) — https://arxiv.org/abs/2606.02800 — tech-report — pre / mid / post disclosed by name (post: text-to-image, image-to-video, robot policy on DROID); no data totals or compute found in the portion read (100,000 of 323,667 characters); RL not found — OpenMDW-1.1. Releases five synthetic datasets (SDG-PhyxSim, -RobotSim, -DriveSim, -SynHuman, -Warehouse).
- LingBot-World — Robbyant (Ant Group; affiliation not checked) — Advancing Open-source World Models — 2026-01-29 — https://arxiv.org/abs/2601.20540 — tech-report — pre (reuses Wan2.2 14B; no new data), mid (game, UE-render and general video; camera as Plucker embeddings; keyboard actions; 5 s to 60 s curriculum; two 14B experts), post (block-causal distillation, DMD; 16 FPS at 480p), RL none — Apache 2.0 (repo). Gives no data sizes or compute. Read first 100,000 of 118,160 characters.
- HY-World 1.5 (WorldPlay) — Tencent Hunyuan — HY-World 1.5: A Systematic Framework for Interactive World Modeling... — 2025-12-16 (v2 2026-06-09) — https://arxiv.org/abs/2512.14614 — tech-report — repo lists pre, mid, RL (WorldCompass) and distillation on HunyuanVideo-1.5 (8B); the arXiv abstract page did not mention RL — MIT (repo). Discrepancy: check the report body.
- WorldCompass — Wang et al. (Tencent Hunyuan) — WorldCompass: RL for Long-Horizon World Models — 2026-02-09 — https://arxiv.org/abs/2602.09022 — preprint — RL only: clip-level rollouts, rewards for interaction-following and visual quality, negative-aware fine-tuning; applied to WorldPlay — licence unconfirmed.
- Matrix-Game 3.0 — Skywork — Matrix-Game 3.0: Real-Time and Streaming Interactive World Model with Long-Horizon Memory — 2026-04 — https://arxiv.org/abs/2604.08995 — tech-report — data engine (Unreal Engine, AAA games, real video); 5B on Wan2.2-TI2V-5B, 28B MoE variant; a search snippet says 700K 17-frame clips (unconfirmed); no RL — Apache 2.0 (model card). Report not opened.
- AlayaWorld — AlayaLab — Interactive Long-Horizon World Modeling: Full Technical Report — 2026-07-21 (v1.1 2026-08-17) — https://arxiv.org/abs/2607.18367 — tech-report — LTX-2.3 (22B) base; bidirectional pre-training, history-encoder plus AR fine-tune, 4-step DMD; 222,147 clips from seven sources; no compute, no RL — LTX-2 Community Licence (non-commercial).
- SolarWM — Huang et al. — SolarWM: Open Data and Scalable Training for Long-Horizon Video World Models — 2026-09-02 — https://arxiv.org/abs/2609.02886 — preprint — 1.43M clips from ten sources; 5B to 33B models on Wan2.2, LTX-2.5, MiniMax-H3 (as the abstract page states); three adaptation stages; no RL — CC BY 4.0 paper; weights promised.
- V-JEPA 2 — Meta — V-JEPA 2: Self-Supervised Video Models... — 2025-06-11 — https://arxiv.org/abs/2506.09985 — preprint — pre (over 1M hours video plus 1M images), post (-AC, under 62 hours of DROID robot video; no reward), RL none — MIT with exceptions (repo). V-JEPA 2.1 checkpoints added 2026-03-16 (per repo; report not opened).
- Cosmos Policy — NVIDIA, Stanford — Cosmos Policy — 2026-01-22 — https://arxiv.org/abs/2601.16163 — preprint — post only (single-stage fine-tune of Cosmos-Predict2; learns from rollouts) — CC BY 4.0; code, models and data released.
- OpenWAM — Wang et al. — OpenWAM — 2026-09-07 — https://arxiv.org/abs/2609.07398 — preprint — mid (about 6,400 h egocentric human and robot data); weights and "data recipes" promised.
- Motus2 — Aug 2026 — https://arxiv.org/abs/2608.30237 — preprint — three stages (mono ego, stereo ego, robot); uses failed rollouts as a learning signal; weights not confirmed.
- GigaWorld-0 — GigaAI — 2025-11-25 — https://arxiv.org/abs/2511.19861 — tech-report — world model as synthetic-data engine; no data sizes found; repo open-gigaai/giga-world-0 (licence not checked).
- Wan 2.2 — Alibaba — released 2025-07-28 per the repo search result; no Wan 2.2 report found (see ch37 scan). Only the Wan 2.1 report is primary.

## Open datasets for world-model training
- Open-AoE — 2026-07-15 — https://arxiv.org/abs/2607.14183 — about 2,000 h smartphone manipulation video, hand pose and camera trajectories — CC BY 4.0.
- EgoVid-5M — 2024-11-13 — https://arxiv.org/abs/2411.08380 — 5M egocentric clips with action labels — CC BY 4.0 (paper); release of data promised.
- EgoCS-400K (10K h of Counter-Strike with inputs; https://arxiv.org/abs/2606.18180), EgoLive (1,680 h stereo; https://arxiv.org/abs/2604.23570), Ego-OSCAR-550h: search snippets only, unconfirmed.
- Cosmos 3 synthetic sets (above); AlayaWorld-v1.1-data (partial, Hugging Face).

## Suggested additions to ch37, ch38 and ch40
- ch38 recipe table: rows Cosmos-Predict2.5, LingBot-World, WorldPlay plus WorldCompass, V-JEPA 2, Cosmos 3, Motus2. Mark "not disclosed" per cell.
- ch37 open comparison: Wan2.2 vs HunyuanVideo-1.5 vs LTX bases, and what each interactive model adds (camera, keys, memory).
- ch40: Cosmos Policy and OpenWAM as open WAM routes.

## Surprises and controversies
- No open release discloses all four stages with numbers; RL appears only in Cosmos-Predict2.5 and WorldPlay/WorldCompass.
- Most "open" interactive models are fine-tunes of a third-party backbone, so the pre-training stage is inherited. Licences differ sharply (Apache, MIT, non-commercial).
- Compute is rarely stated (Cosmos is the exception).
- Cosmos-Predict2.5's reward is a general video-quality model, not a physics check.
