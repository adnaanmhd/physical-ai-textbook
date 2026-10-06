# ch15 scan · Kinematics, dynamics and control (scanned 2026-10-06)
## What is new since 2025
- Sampling-based and inverse-dynamics whole-body MPC now runs on real legged hardware.
- RL-guided or MPC-guided RL hybrids are common for humanoids (titles seen in search, not yet opened).
- Helix 02 replaces a hand-written whole-body controller with a learned one (company claim); see ch16.
## Key primary sources
- Modern Robotics — Lynch, Park — 2017 (Cambridge UP) — http://modernrobotics.org — peer-reviewed (book) — free preprint; frames, Jacobians, dynamics, control
- Real-Time Whole-Body Control of Legged Robots with MPPI — Alvarez-Padilla et al. — 2024-09-16 — https://arxiv.org/abs/2409.10469 — preprint — sampling MPC on hardware
- Whole-Body Inverse Dynamics MPC for Legged Loco-Manipulation — Molnar et al. — 2025-11-24 — https://arxiv.org/abs/2511.19709 — preprint — torque-level MPC at 80 Hz on a quadruped
- Introducing Helix 02 — Figure AI — 2026-01-27 — https://www.figure.ai/news/helix-02 — company-claim — learned 1 kHz whole-body controller replaces hand-written code
## Suggested sections
Seed list stands. Add a worked torque-tool example (stiffness versus impedance) for the battery task.
## Surprises and controversies
- Gaps: ZMP and centroidal-dynamics originals (Vukobratovic; Kajita; Orin), PD/impedance (Hogan 1985), QP whole-body control not yet sourced.
- Science Robotics "Evolution of humanoid locomotion control" appeared in search (https://www.science.org/doi/10.1126/scirobotics.aed3973) but returned 403; not confirmed.
- Debate: learned versus model-based control; company claims need attribution.
