# ch28 scan · Training in simulation (scanned 2026-10-06)
## What is new since 2025
- Motion tracking became a scaled foundation-model recipe: SONIC (42M parameters, 700 h mocap, 21k GPU hours; Science Robotics 2026).
- Off-policy RL (FlashSAC) reports humanoid locomotion training cut from hours to minutes.
- Generative 3D worlds feed RL for VLAs: reported real success 21.7% to 75%.
- Sim+real co-training now has mechanistic analysis.
- Sim-to-real dexterity with tactile/force feedback (arXiv 2601.02778 vs 2607.04940, same title; unconfirmed).
## Key primary sources
- SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control — Luo et al. (NVIDIA) — 2025-11-11 (v. 2026-08-13) — https://arxiv.org/abs/2511.07820 — peer-reviewed — scaled whole-body controller
- BeyondMimic — Liao et al. — 2025-08-11 — https://arxiv.org/abs/2508.08241 — preprint — tracking plus guided diffusion
- GMT: General Motion Tracking — Chen et al. — 2025-06-17 — https://arxiv.org/abs/2506.14770 — preprint — adaptive sampling, motion mixture-of-experts
- FlashSAC — Kim et al. — 2026-04-06 — https://arxiv.org/abs/2604.04539 — preprint — fast off-policy humanoid RL (RSS 2026)
- Sim-and-Real Co-Training — Maddukuri et al. — 2025-03-31 — https://arxiv.org/abs/2503.24361 — preprint — reports +38% from sim data
- Mechanistic Analysis of Sim-and-Real Co-Training — Lei et al. — 2026-04-15 — https://arxiv.org/abs/2604.13645 — preprint — why co-training works
- Scaling Sim-to-Real VLA RL with Generative 3D Worlds — Choi et al. — 2026-03-19 — https://arxiv.org/abs/2603.18532 — preprint — CoRL 2026
- mjlab — Zakka et al. — 2026-01-29 — https://arxiv.org/abs/2601.22074 — preprint — motion-imitation reference tasks
- MimicGen — Mandlekar et al. — https://arxiv.org/abs/2310.17596 — preprint — date not opened; unconfirmed
## Suggested sections
Parallel RL recipe; curricula and privileged teacher-student; motion tracking to controllers; dexterity; synthetic data and co-training; compute costs.
## Surprises and controversies
- ASAP not confirmed this scan.
- Tracking-based controllers replace hand-written rewards.
- Real-world RL versus sim RL is disputed (2603.18532 argues scene diversity favours sim).
- Compute reported: 21k GPU hours for one controller.
