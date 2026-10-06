# ch37 scan · Inside a video world model (scanned 2026-10-06)

## What is new since 2025
- Streaming generation matured: Self Forcing (2025) then Causal Forcing (ICML 2026) for distilling bidirectional teachers into causal students.
- Search shows many 2026 follow-ups (Causal Forcing++, Vidu S1, KV-cache compression, long-horizon benchmarks such as WorldRoamBench, WBench); these were not opened.
- Wan moved past 2.1 (2.5, 2.7, 3.0 reported), but only third-party pages describe them. No technical report found.
- Cosmos 3 adds a two-tower design and action output.
- Memory work: Infinite-World reaches 1000+ frames.

## Key primary sources
- Wan: Open and Advanced Large-Scale Video Generative Models — Wan Team (Alibaba) — 2025-03-26 — https://arxiv.org/abs/2503.20314 — tech-report — VAE, DiT, 1.3B/14B internals
- HunyuanVideo — Tencent — 2024-12 — https://arxiv.org/abs/2412.03603 — tech-report — 13B open video model; day not confirmed
- Cosmos-Predict2.5 and Transfer2.5 — NVIDIA — 2025-10-28 (v2 2026-02-24) — https://arxiv.org/abs/2511.00062 — tech-report — flow-based, RL post-training
- Self Forcing — Huang et al. — 2025-06-09 — https://arxiv.org/abs/2506.08009 — peer-reviewed (NeurIPS 2025 spotlight) — rolling KV cache, train-test gap
- Causal Forcing — Zhu et al. — 2026-02-02 — https://arxiv.org/abs/2602.02214 — peer-reviewed (ICML 2026) — fixes AR distillation from bidirectional teachers
- Infinite-World — Wu et al. — 2026-02-02 — https://arxiv.org/abs/2602.02393 — preprint — pose-free hierarchical memory, 1000 frames
- Mask World Model — Lou et al. — 2026-04-21 — https://arxiv.org/abs/2604.19683 — preprint — predicts semantic masks, not pixels
- Dreamer 4 — Hafner et al. — 2025-09 — https://arxiv.org/abs/2509.24527 — preprint — shortcut forcing; real time on one GPU
- Genie 3 blog — DeepMind — 2025-08-05 — https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/ — company-claim — 720p, 24 fps, minutes of consistency (not opened)
- NVIDIA Cosmos 3 — 2026-05-31 — https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai — company-claim

## Suggested sections
1. Video VAEs and latents.
2. Diffusion/flow transformers (Wan, Hunyuan, Cosmos).
3. Autoregressive and streaming (diffusion forcing, Self/Causal Forcing).
4. Action, camera, language conditioning.
5. Memory and long-horizon drift.
6. Multi-view and 3D consistency.
7. Real time: distillation and KV caching.
8. Metrics: fidelity vs physics vs control.

## Surprises and controversies
- Mask World Model argues pixels are the wrong target for control.
- Newest Wan versions lack papers; use only primary docs.
- Diffusion forcing original paper not yet located.
- Benchmarks (Physics-IQ, PAI-Bench) are vendor-cited; a scout should find independent evaluations.
