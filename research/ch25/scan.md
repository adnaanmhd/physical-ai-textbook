# ch25 scan · Bridging bodies: retargeting and cross-embodiment action spaces (scanned 2026-10-06)
## What is new since 2025
GMR has a tech report ("Retargeting Matters") and an ICRA 2026 listing; its repo notes real-time CPU use, and the paper argues retargeting quality drives tracking-policy quality. Cross-embodiment VLAs now use either soft prompts per data source (X-VLA, ICLR 2026) or latent actions (UniVLA, RSS 2025; a Jan 2026 follow-up uses VLMs for task-centric latents). Being-H0.5 (Jan 2026) unifies human hand motion and robot data in one action space, with a Mixture-of-Flow design; it has a successor, Being-H0.7 (Apr 2026), a latent world-action model. EgoScale (Feb 2026) scales dexterous learning from egocentric human data.
## Key primary sources
- Retargeting Matters: General Motion Retargeting for Humanoid Motion Tracking — Araujo, Ze, Xu, Wu, Liu — 2025-10-02 — https://arxiv.org/abs/2510.02252 — preprint — the GMR report
- X-VLA: Soft-Prompted Transformer for Cross-Embodiment VLA — Zheng, Li et al. — 2025-10-11 — https://arxiv.org/abs/2510.10274 — preprint (ICLR 2026 per repo) — per-source embodiment prompts
- UniVLA: Learning to Act Anywhere with Task-centric Latent Actions — Bu, Yang et al. — 2025-05-09 — https://arxiv.org/abs/2505.06111 — peer-reviewed (RSS 2025 per repo) — latent actions from video
- Vision-Language Models Unlock Task-Centric Latent Actions — Nikulin, Zisman et al. — 2026-01-30 — https://arxiv.org/abs/2601.22714 — preprint — newer latent-action line
- Being-H0.5 — Luo, Wang et al. — 2026-01-19 — https://arxiv.org/abs/2601.12993 — preprint — unified human-robot action space
- Being-H0.7: Latent World-Action Model from Egocentric Videos — Luo, Zhang et al. — 2026-04-30 — https://arxiv.org/abs/2605.00078 — preprint — Being-H successor
- EgoScale — Zheng, Niu et al. — 2026-02-18 — https://arxiv.org/abs/2602.16710 — preprint — egocentric human data scaling
- GMR repository — Ze et al. — https://github.com/YanjieZe/GMR — tech-report (code) — supported robots
## Suggested sections
The embodiment gap; body retargeting (GMR); hand retargeting; physics-based tracking (PHC, OmniH2O: not rescanned, unconfirmed); latent actions; embodiment prompts; human-data pretraining; results and limits.
## Surprises and controversies
Evidence that retargeting artefacts (foot sliding, penetration) harm policies. Latent-action methods claim big compute savings versus OpenVLA, from the authors' own benchmarks. Several 2026 results are unreviewed preprints. Gap: PHC and OmniH2O were not searched; independent cross-embodiment benchmarks not found.
