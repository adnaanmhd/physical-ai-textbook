# ch35 scan · Connecting brain and body: from policy outputs to whole-body motion (scanned 2026-10-06)

## What is new since 2025
The interface is shifting from hand-written controllers to learned whole-body controllers (WBCs) fed by latent or keypoint commands. Humanoid VLAs and world action models now output unified motion latents instead of split upper/lower-body commands (MotionWAM, OpenHLM). Large motion-tracking models (SONIC) act as general "cerebellum" layers. Companies claim single-network whole-body control (Figure Helix 02 System 0, Atlas LBM). Helix 02 and SONIC appear in earlier scans (ch16/ch28); not repeated below.

## Key primary sources
- TWIST: Teleoperated Whole-Body Imitation System — Ze, Chen, Araújo, Cao, Peng, Wu, Liu — 2025-05-05 — https://arxiv.org/abs/2505.02833 — preprint — one RL+BC controller tracks human motion
- AMO: Adaptive Motion Optimization — Li, Cheng, Huang, Yang, Qiu, Wang — 2025-05-06 — https://arxiv.org/abs/2505.03738 — preprint — RL plus trajectory optimisation; G1, 29 DoF
- SONIC — arXiv 2511.07820 — https://arxiv.org/abs/2511.07820 — preprint — large motion tracker; cited in earlier scans
- GR00T-WholeBodyControl repository — NVlabs — https://github.com/NVlabs/GR00T-WholeBodyControl — code/docs — decoupled WBC used in GR00T N1.5/N1.6 (page not opened; unconfirmed)
- Atlas LBM, Boston Dynamics and TRI announcement — 2025-08-20 — https://www.prnewswire.com/news-releases/ai-powered-robot-by-boston-dynamics-and-toyota-research-institute-takes-a-key-step-towards-general-purpose-humanoids-302534045.html — company-claim — one model, hands and feet alike
- MotionWAM — Zheng, Ma, Fan, Wang, Yang, Liang — 2026-06-08 — https://arxiv.org/abs/2606.09215 — preprint — unified motion latent on Unitree G1
- OpenHLM — Hu et al. (Yang Gao) — 2026-06-20 — https://arxiv.org/abs/2606.22174 — preprint — empirical recipe, whole-body VLA, fewer demonstrations
- HOVER (2024), LeVERB (https://arxiv.org/abs/2506.13751, unconfirmed), TWIST2 — search results only; confirm in section scouting.

## Suggested sections
Action interfaces (joint, end-effector, keypoint, latent); the WBC as cerebellum; loco-manipulation; learned vs model-based control; joint vs separate training; failure modes (falls, self-collision, drift).

## Surprises and controversies
- Boston Dynamics/TRI describes a single model; no paper found, so treat as demo/company-claim.
- Figure's "109,504 lines of C++ replaced" figure came from secondary coverage; trace to Figure's post before use.
- Evidence is mostly Unitree G1 preprints; reproducibility and failure rates are thinly reported.
- Gemini Robotics humanoid work: see ch16 scan.
