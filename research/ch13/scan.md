# ch13 scan · Generative models: autoencoders, diffusion, flow matching and autoregression (scanned 2026-10-06)
## What is new since 2025
- One-step generation: MeanFlow (May 2025) learns average velocity without distillation; Improved MeanFlow (Dec 2025) fixes training and guidance issues.
- Robot policies are moving from diffusion to flow matching, and to one-step versions (One-Step Flow Policy, Mar 2026; ManiFlow, Sep 2025).
- Diffusion Policy now has its journal version (IJRR, 2025).
- Tokenisers for actions: FAST (Jan 2025). Latent diffusion without a VAE (Oct 2025) questions the autoencoder step.
## Key primary sources
- DDPM — Ho et al. — 2020-06-19 — https://arxiv.org/abs/2006.11239 — preprint — diffusion original
- Score-Based Generative Modeling through SDEs — Song et al. — 2020-11-26 — https://arxiv.org/abs/2011.13456 — preprint — unifies score and diffusion views
- Flow Matching for Generative Modeling — Lipman et al. — 2022-10-06 — https://arxiv.org/abs/2210.02747 — preprint — flow matching original (ICLR 2023)
- Rectified Flow — Liu et al. — 2022-09-07 — https://arxiv.org/abs/2209.03003 — preprint — straight-path flows
- Scalable Diffusion Models with Transformers (DiT) — Peebles, Xie — 2022-12-19 — https://arxiv.org/abs/2212.09748 — preprint — transformer denoiser
- Consistency Models — Song et al. — 2023-03-02 — https://arxiv.org/abs/2303.01469 — preprint — few-step sampling
- Diffusion Policy — Chi et al. — 2023-03 (arXiv; IJRR 2025) — https://arxiv.org/abs/2303.04137 — peer-reviewed — journal version; arXiv date unconfirmed
- Learning Fine-Grained Bimanual Manipulation (ACT) — Zhao et al. — 2023-04-23 — https://arxiv.org/abs/2304.13705 — preprint — action chunking
- Mean Flows for One-step Generative Modeling — Geng et al. — 2025-05-19 — https://arxiv.org/abs/2505.13447 — preprint — one-step flow
- One-Step Flow Policy — Li et al. — 2026-03-12 — https://arxiv.org/abs/2603.12480 — preprint — fast visuomotor policy
## Suggested sections
Autoencoders/VAEs; tokenisers; diffusion; flow matching; DiT; autoregression; distillation and consistency; action generation (Diffusion Policy, ACT, pi0's flow head: arXiv 2410.24164, 2024-10-31).
## Surprises and controversies
- "Demystifying Diffusion Policies" (arXiv 2505.05787) argues diffusion policies may memorise actions; unread.
- Several 2026 policy papers are single-group preprints; treat cautiously.
