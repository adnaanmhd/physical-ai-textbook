# ch40 scan · World action models (WAMs) (scanned 2026-10-06)
## What is new since 2025
- The term is confirmed: the DreamZero paper (Feb 2026) says "We term this architecture a World Action Model" and chose WAM over "Video Action Model" so tactile, force or latent futures can fit later. It also labels earlier work (Kim 2026, Liao 2025, Pai 2025; the works behind these citations were not resolved) as WAMs after the fact. So: "introduced" is right; "invented the idea" is not.
- Two surveys exist: June (2606.20781) and September (2609.16074). A May survey, "World Model for Robot Learning" (2605.00080), is broader (world models, not WAM-specific). Seed text says "May and September": adjust.
- Design-space studies arrived: Fast-WAM (imagination may matter only in training), OpenWAM, "What Matters in Designing WAMs".
- Productisation: FLUX 3 Action (7B, Sept 2026), Cosmos 3 (June), Rhoda AI DVA (March), 1X world-model policy; NVIDIA blog (15 Jun 2026) by Moritz Reuss.
- GR00T N2 "based on DreamZero" appears only in aggregators: unconfirmed; trace to NVIDIA newsroom before use.
## Key primary sources
- World Action Models are Zero-shot Policies (DreamZero) — Ye et al., NVIDIA — 2026-02-17 — https://arxiv.org/abs/2602.15922 — preprint — origin of the term
- Cosmos Policy — NVIDIA, Stanford — 2026-01 (arXiv 2601.16163) — https://arxiv.org/abs/2601.16163 — preprint — single-stage video-model policy; action as latent frames
- Fast-WAM — Yuan et al. — 2026-03-17 — https://arxiv.org/abs/2603.16666 — preprint — drops test-time imagination; 190 ms
- Cosmos 3 — NVIDIA — 2026-06-01 — https://arxiv.org/abs/2606.02800 — tech-report — omnimodal; world-action models; RoboArena claim
- World Action Models: A Survey — Shen et al. — 2026-06-18 — https://arxiv.org/abs/2606.20781 — preprint — taxonomy: rendered, latent, no-video futures
- World-Action Models for Robot Learning and Control: A Survey — Lu et al. — 2026-09-13 — https://arxiv.org/abs/2609.16074 — preprint — joint vs video-then-inverse-dynamics
- Pretrained to Imagine, Fine-Tuned to Act — Moritz Reuss, NVIDIA — 2026-06-15 — https://developer.nvidia.com/blog/pretrained-to-imagine-fine-tuned-to-act-the-rise-of-world-action-models/ — company-claim — explainer; names ~10 systems
- What Matters in Designing WAMs — Tang et al. — 2026-09-21 — https://arxiv.org/abs/2609.24048 — preprint — controlled ablation of causal structure, latents, objectives
- OpenWAM — Wang et al. — 2026-09-07 — https://arxiv.org/abs/2609.07398 — preprint — open modular pretraining, ~6,400 h
- FLUX 3 Action — Black Forest Labs — 2026-09 — https://bfl.ai/models/flux-3-action — company-claim — 7B, 15 Hz; page has odd partner claims
- Rhoda AI exits stealth — The Robot Report — 2026-03-12 — https://www.therobotreport.com/rhoda-ai-exits-stealth-with-450m-to-train-robots-from-video/ — press — DVA, FutureVision (find Rhoda primary)
- 1X World Model — 1X — date unconfirmed — https://www.1x.tech/discover/world-model-self-learning — company-claim — 14B; 900 h ego + 70 h robot (unconfirmed, not opened)
## Suggested sections
Lineage (UniPi to GR-1/GE); definition and scope; architectures (joint, video-then-inverse-dynamics, latent, no-imagination); training recipes; speed and control rates; strengths; comparison table.
## Surprises and controversies
Fast-WAM questions whether imagining the future is needed at test time. Several WAM names in OUTLINE (ProWAM, OA-WAM, GigaWorld-Policy, UVA, UWM, WorldVLA) were not checked. Rapid leaderboard churn (RoboArena) comes from aggregators only.
