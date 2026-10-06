# ch20 scan · Synthetic, autonomous and deployment data (scanned 2026-10-06)

## What is new since 2025
- Learning from deployment has moved from one company's result to academic fleet-scale work: autonomous rollouts plus interventions across 16 robots reach 95% average success.
- The MimicGen line now reaches humanoid loco-manipulation (HumanoidMimicGen, 2026), reporting synthetic data beating real-only data by 20%.
- Generated video as training data matured: DreamGen (2025) led to Cosmos-Predict2.5 and Cosmos-Transfer2.5, with a DreamGen benchmark.
- Interventions are now treated as noisy data to be filtered (ROVE), not just gold labels.

## Key primary sources
- pi*0.6: a VLA That Learns From Experience — Physical Intelligence — 2025-11-18 — https://arxiv.org/abs/2511.14759 — tech-report — Recap: demos, corrections, autonomous RL
- Learning While Deploying — Wang et al. — 2026-05-01 — https://arxiv.org/abs/2605.00416 — preprint — fleet-scale RL from rollouts and interventions
- ROVE — Xiao et al. — 2026-06-15 — https://arxiv.org/abs/2606.17011 — preprint — filters mixed-quality human interventions
- HumanoidMimicGen — Lin, Mandlekar et al. — 2026-05-26 — https://arxiv.org/abs/2605.27724 — preprint — synthetic humanoid loco-manipulation demonstrations
- DexMimicGen — Jiang et al. — 2024-10-31 — https://arxiv.org/abs/2410.24185 — preprint — 60 source demos become 21,000
- DreamGen — Jang et al. (NVIDIA GEAR) — 2025-05-19 — https://arxiv.org/abs/2505.12705 — preprint — neural trajectories from video world models
- World Simulation with Video Foundation Models for Physical AI — NVIDIA — 2025-10-28 — https://arxiv.org/abs/2511.00062 — tech-report — Cosmos-Predict2.5 and Cosmos-Transfer2.5
- MimicGen — Mandlekar et al. — 2023 (arXiv 2310.17596; date and page not opened) — https://arxiv.org/abs/2310.17596 — preprint — original; unconfirmed

## Suggested sections
Keep the seed list. Add "video world models as data engines" and "interventions: cleaning and weighting". Fold fleet logs and automatic labels into one "deployment loop" section. Cover mixing ratios with human data.

## Surprises and controversies
- Synthetic data beating real data (20%) is a source claim in one benchmark; test it.
- No newer "pi*" successor to Recap found in search; check Physical Intelligence's site directly.
- HG-DAgger and SkillMimicGen not searched; the original papers still need confirming.
- Public evidence that generated video helps on real robots at scale is thin.
