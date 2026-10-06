# ch27 scan · Simulators and RL gyms (scanned 2026-10-06)
## What is new since 2025
- Isaac Lab now has a paper and a 3.0 line (beta 2, 23 June 2026) with swappable physics backends; Newton (Linux Foundation; NVIDIA, Google DeepMind, Disney) is a backend. A GA date was only seen in aggregator text, unconfirmed.
- MuJoCo Warp (GPU MuJoCo) underpins mjlab, an Isaac Lab-style framework.
- Benchmarks scaled: RoboCasa365 (365 tasks, 2,500 kitchens); BEHAVIOR Challenge 2025 winner scored about 26% (secondary report).
- Agri-Sim (Aug 2026) is a Unity/ROS2 tomato-greenhouse sim; sim-only, no real-transfer tests.
## Key primary sources
- Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning — Mittal et al. (NVIDIA) — 2025-11-06 — https://arxiv.org/abs/2511.04831 — preprint — canonical Isaac Lab reference
- Isaac Lab 3.0 Beta 2 Release — NVIDIA/Isaac Lab team — 2026-06-23 — https://github.com/isaac-sim/IsaacLab/discussions/6249 — company-claim — deformable VBD, Newton solvers
- Newton's Integration with Isaac Sim and Isaac Lab — NVIDIA — 2026-05-15 (updated) — https://perspectives.nvidia.com/isaac-sim/newtons-integration-isaac-sim-and-isaac-lab/ — company-claim — Newton 1.0 governance
- MuJoCo Playground — Zakka et al. — 2025-02-12 — https://arxiv.org/abs/2502.08844 — preprint — MJX training and sim-to-real
- mjlab — Zakka et al. — 2026-01-29 — https://arxiv.org/abs/2601.22074 — preprint — MuJoCo Warp robot-learning framework
- ManiSkill3 — Tao et al. — 2024-10-01 (rev. 2025-05-30) — https://arxiv.org/abs/2410.00425 — preprint — GPU state-visual simulation
- RoboCasa365 — Nasiriany et al. — 2026-03-04 — https://arxiv.org/abs/2603.04356 — preprint — large household benchmark
- Agri-Sim — Shi et al. — 2026-08-29 — https://arxiv.org/abs/2608.29100 — preprint — greenhouse example; sim-only
- Task adaptation of VLA: 1st Place, 2025 BEHAVIOR Challenge — Larchenko et al. — https://arxiv.org/abs/2512.06951 — preprint — date not opened; unconfirmed
## Suggested sections
Environment anatomy; engines (rigid, deformable, cloth); GPU parallelism and backend-swapping; assets/USD; benchmarks; real-to-sim; where each running example breaks.
## Surprises and controversies
- Frameworks are converging on one task API over many engines.
- Best BEHAVIOR score is only about 26%.
- Genesis, RoboVerse, LIBERO, RoboTwin 2.0 not confirmed this scan; need scouting.
