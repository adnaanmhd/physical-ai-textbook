# ch34 scan · Reinforcement learning for robot policies (scanned 2026-10-06)

## What is new since 2025
RL has moved from small policies to fine-tuning large VLAs, in three styles: advantage-conditioned (Recap), on-policy PPO/GRPO (SimpleVLA-RL, πRL), and a small RL head on a frozen VLA (RL Token). 2026 work targets speed and sample cost: real-world RL with minutes to hours of robot data. Imagination-based RL (RISE) avoids resets by training in a learned world model (preview of ch39). Reward quality is now the bottleneck: progress-reward models and VLM judges are surveyed, and one benchmark finds judges unreliable on contact-rich tasks.

## Key primary sources
- Precise and Dexterous Robotic Manipulation via HIL-RL (HIL-SERL) — Luo, Xu, Wu, Levine — 2024-10-29 — https://arxiv.org/abs/2410.21845 — preprint — human corrections plus RL; 1–2.5 h training (Science Robotics version unconfirmed)
- π*0.6: a VLA That Learns From Experience — Physical Intelligence — 2025-11-18 — https://arxiv.org/abs/2511.14759 — tech-report/preprint, company-claim — Recap; deployment-style RL (also in earlier scans)
- SimpleVLA-RL — Li et al. — 2025-09-11 — https://arxiv.org/abs/2509.09674 — preprint — outcome-only 0/1 reward; simulation; "pushcut"
- πRL — Chen et al. (RLinf) — 2025-10-29, v latest 2026-01-29 — https://arxiv.org/abs/2510.25889 — preprint — PPO/GRPO for flow-matching VLAs
- RISE: Self-Improving Robot Policy with Compositional World Model — Yang et al. — 2026-02-11 — https://arxiv.org/abs/2602.11075 — preprint — RL in imagination; real-robot gains
- RL Token — Xu, Springenberg, Equi, Levine, Ke et al. — 2026-04-24 — https://arxiv.org/abs/2604.23073 — preprint — online RL on a VLA within hours
- RL for Real-Time VLA Policies — Dong, Hung, Sadigh, Finn — 2026-09-16 — https://arxiv.org/abs/2609.18207 — preprint — 42% to 97% with 10 min online data
- FailBench — Navasardyan et al. — 2026-09-03 — https://arxiv.org/abs/2609.03611 — preprint — best VLM judge 0.77 balanced accuracy
- Progress Reward Modeling for Robotic Learning: survey — 2026 — https://arxiv.org/pdf/2607.21655 — preprint — unconfirmed (search result only)
- ROVE (humanoid RL from interventions) — https://arxiv.org/abs/2606.17011 — in earlier scan

## Suggested sections
Why imitation plateaus; real-world RL and human corrections (HIL-SERL, Recap); RL fine-tuning of VLAs (three styles); rewards and judges; sim RL and RL in world models; safe exploration and resets; results and limits.

## Surprises and controversies
- Recap's headline results (18-hour espresso, laundry) are company-reported; no open Recap training code (openpi issue asks).
- Judges bias toward "success" under ambiguity (FailBench).
- Many VLA-RL results are simulation benchmarks (LIBERO); real-world transfer is thinner.
- Not yet found: ConRFT, VLA-RL, RL4VLA, Dyna reward claims (searched only partly; confirm in section scouting).
