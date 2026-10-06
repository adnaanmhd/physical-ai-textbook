# ch43 scan · Evaluating robot policies (scanned 2026-10-06)
## What is new since 2025
- Real-world evaluation has become shared infrastructure: RoboArena (distributed, double-blind pairwise), RoboChallenge (online real-robot, Table30), ManipArena (CVPR 2026 competition, 20 tasks, partial-credit scoring, in-domain/visual-shift/semantic-OOD tiers).
- TRI published its blind, randomised A/B method with sequential testing, now in a journal.
- Sim-and-real correlation is now studied directly (SimplerEnv's MMRV and Pearson metrics; a June 2026 recipe paper).
- Figure's Helix 2.5 (17 Sep 2026) reports 56% zero-shot success across 30 homes: strict no-partial-credit, any safety intervention counts as failure. Company claim, no independent check.
## Key primary sources
- RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies — Atreya et al. — 2025-06-22 — https://arxiv.org/abs/2506.18123 — preprint (CoRL 2025) — blind pairwise ranking, 600+ episodes
- RoboChallenge: Large-scale Real-robot Evaluation of Embodied Policies — RoboChallenge team — 2025-10-20 — https://arxiv.org/abs/2510.17950 — preprint — online real-robot benchmark, Table30
- ManipArena — arXiv 2603.28545 (authors not confirmed) — 2026-03-30 — https://arxiv.org/abs/2603.28545 — preprint — partial-credit, tiered OOD, real-to-sim pairs
- A Careful Examination of Large Behavior Models — TRI LBM Team — 2025-07-07 — https://arxiv.org/abs/2507.05331 — preprint — blind A/B, sequential testing (journal: Science Robotics, DOI 10.1126/scirobotics.aea6201, page 403, unconfirmed)
- Statistical Thinking for Robot Policy Evaluation — TRI — undated (page 403, unconfirmed) — https://medium.com/toyotaresearch/statistical-thinking-for-robot-policy-evaluation-from-rigorous-a-b-testing-to-effective-0ae886fbd68d — company-claim — practitioner statistics guide
- Evaluating Real-World Robot Manipulation Policies in Simulation (SimplerEnv) — Li et al. — 2024-05 — https://arxiv.org/abs/2405.05941 — preprint — MMRV metric; search-confirmed only
- A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation — Wang et al. — 2026-06-09 — https://arxiv.org/abs/2606.10366 — preprint — when sim rankings match real
- Helix 2.5: Zero-Shot 30-Home Generalization — Figure AI — 2026-09-17 — https://www.figure.ai/news/helix-2-5-zero-shot-30-home-generalization — company-claim — strict protocol, no independent review
## Suggested sections
Why evaluation is hard; statistics (intervals, sequential tests, A/B); sim benchmarks and correlation metrics; distributed and blind real-world protocols; partial credit and intervention; world-model evaluation (not yet scanned); readiness evaluation for the four running examples.
## Surprises and controversies
Sim rankings often fail to transfer. Figure's "zero-shot" means no home data, but task data came from elsewhere. Statistics guidance is mostly TRI's own. LIBERO-Plus not scanned.
