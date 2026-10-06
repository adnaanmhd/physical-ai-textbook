# ch48 scan · The data flywheel (scanned 2026-10-06)
## What is new since 2025
Deployment learning moved from one lab's recipe (Recap, Nov 2025) to fleet-scale systems: a 16-robot fleet now feeds rollouts and human interventions into one shared policy and redeploys it. Failed episodes are now treated as data: VLM-based hindsight relabelling turns a failure into a success on a different instruction. Failure detection and VLM judges (auto-labelling) are measured, with weak spots reported. Federated VLA training appeared as a privacy route, though only on benchmarks so far. Waymo published its long-tail mining recipe with numbers.
## Key primary sources
- pi*0.6: a VLA That Learns From Experience — Physical Intelligence — 2025-11-18 — https://arxiv.org/abs/2511.14759 — tech-report, company-claim — Recap; already in ch20/ch34 scans, reuse
- Learning While Deploying — Wang et al. (Luo) — 2026-05-01 (rev. 2026-09-16) — https://arxiv.org/abs/2605.00416 — preprint — 16 robots, 8 tasks, 95% average
- Learning More from Less: RL from Hindsight — Xu et al. (Agrawal) — 2026-07-10 — https://arxiv.org/abs/2607.09042 — preprint — VLM relabels failures; 5x sample efficiency
- FAR: Failure-Aware Retry — Hao et al. — 2026-07-01 — https://arxiv.org/abs/2607.01111 — preprint — failures become preferences; continual improvement
- FailBench — Navasardyan et al. — 2026-09-03 — https://arxiv.org/abs/2609.03611 — preprint — how reliable VLM success judges are (from ch34 scan)
- ROVE — Xiao et al. — 2026-06-15 — https://arxiv.org/abs/2606.17011 — preprint — filters intervention data (ch20 scan)
- WOD-E2E — Xu et al. (Waymo) — 2025-10-30 — https://arxiv.org/abs/2510.26125 — preprint, company-claim — mining 6.4M miles for under-0.03% long-tail events
- ForgeVLA: Federated VLA Learning without Language Annotations — Zhou et al. — 2026-05-08 — https://arxiv.org/abs/2605.07474 — preprint — raw data stays local
- Tesla data engine / shadow mode — unconfirmed: only secondary pages and a patent (US 12,195,021) surfaced; no primary talk found.
## Suggested sections
Logging triggers; failures and edge cases (Waymo analogue); interventions as data; hindsight relabelling and judges; prioritising retraining data; privacy (federated, on-device, health data); seasonal flywheel; economics.
## Surprises and controversies
Auto-judges are imperfect (FailBench), so flywheel labels carry noise. Fleet results come from lab fleets, not homes. No primary Tesla source; avoid blogs. Federated VLA evidence is thin for home privacy. Physical Intelligence's pi0.7 (Apr 2026) is only seen via secondary pages; primary page blocked (403), unconfirmed.
