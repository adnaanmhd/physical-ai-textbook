# ch29 scan · The sim-to-real gap, pilot (scanned 2026-10-06)
## What is new since 2025
- Review-level survey: The Reality Gap in Robotics (Annual Review 2026).
- The reverse gap is now the live topic: real-to-sim evaluation (PolaRiS, Gaussian-splat soft bodies) and world-model evaluators, with documented failures (models ignore off-expert actions).
- Asset and reconstruction quality measured: Pearson r 0.90 (authored) vs 0.51 (default).
- Differentiable-simulation system identification (HALO) for payload humanoids.
## Key primary sources
- The Reality Gap in Robotics — Aljalbout et al. — 2025-10-23 — https://arxiv.org/abs/2510.20808 — peer-reviewed — survey; causes, fixes, metrics
- Evaluating Real-World Robot Manipulation Policies in Simulation (SIMPLER) — Li et al. — 2024-05-09 — https://arxiv.org/abs/2405.05941 — preprint — sim-real correlation original
- A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation — Wang et al. — 2026-06-09 — https://arxiv.org/abs/2606.10366 — preprint — ranking, correlation, failure patterns
- PolaRiS — Jain et al. — 2025-12-18 — https://arxiv.org/abs/2512.16881 — preprint — splat-based real-to-sim evaluation
- Measuring Asset and Scene Reconstruction Effects in Real-to-Sim Evaluation — Verma et al. — 2026-09-30 — https://arxiv.org/abs/2610.00731 — preprint — r 0.90 vs 0.51
- Do Robotic World Models Really Follow Actions? — Chen et al. — 2026-08-25 — https://arxiv.org/abs/2608.24885 — preprint — world-model evaluators ignore actions
- Interactive World Simulator — Wang et al. — 2026-03-09 — https://arxiv.org/abs/2603.08546 — preprint — world-model correlation claim
- HALO — Wang et al. — 2026-03-16 — https://arxiv.org/abs/2603.15084 — preprint — differentiable-sim system identification
- Real-to-Sim Policy Evaluation with Gaussian Splatting — https://arxiv.org/abs/2511.04665 — preprint — date not opened; unconfirmed
## Suggested sections
Follow the outline; add a measurement section (rank correlation, MMRV, Pearson) and a failure-mode catalogue for the reverse gap.
## Surprises and controversies
- Aggregator figures (Runway GWM-Robotics 0.95 correlation) are untraced; check primary.
- Randomisation (RL-era papers), actuator networks (ANYmal) originals still to be scouted.
- Correlation can hide low absolute accuracy.
