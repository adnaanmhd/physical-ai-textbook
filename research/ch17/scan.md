# ch17 scan · Why data is the bottleneck (scanned 2026-10-06)
## What is new since 2025
Claimed volumes now run to 100,000+ hours. Companies report data-scaling curves (GEN-0, Xiaomi-Robotics-1, Dyna-2). Evidence is shifting from teleoperated robot data to egocentric human video as the cheap axis. Figure launched a paid crowd-capture app (Index). Academic papers (EgoScale, HumanScale, EgoVerse) report that human-video scaling transfers to robots.
## Key Primary Sources
- Data Scaling Laws in Imitation Learning for Robotic Manipulation — Lin et al. — 2024-10-24 (rev. 2026-06-26) — https://arxiv.org/abs/2410.18647 — preprint — diversity beats volume; power law in environments/objects
- GEN-0: Embodied Foundation Models That Scale with Physical Interaction — Generalist — 2025-11-04 — https://generalistai.com/blog/nov-04-2025-GEN-0 — company-claim — 270k hours; 10k hours/week; 7B threshold
- AgiBot World Colosseo — AgiBot-World-Contributors — 2025-03-09 — https://arxiv.org/abs/2503.06669 — preprint — 1M+ trajectories, 217 tasks; open dataset
- Xiaomi-Robotics-1 — Xiaomi Robotics Team — 2026-07-16 — https://arxiv.org/abs/2607.15330 — tech-report — scaling with 100k+ hours real trajectories
- Dyna-2: A 1-Million-Hour Scaling Law for World-Action Models — Dyna Robotics — 2026-08 (day unconfirmed) — https://www.dyna.co/dyna-2 — company-claim — 1M hours human video; second half unread
- EgoScale — Zheng et al. (NVIDIA, Berkeley) — 2026-02-18 — https://arxiv.org/abs/2602.16710 — preprint — 20,854 hours; log-linear scaling
- HumanScale — Ma et al. — 2026-06-18 — https://arxiv.org/abs/2606.20521 — preprint — egocentric video beats robot data for pretraining
- Project Go-Big — Figure — 2025-09-18 — https://www.figure.ai/news/project-go-big — company-claim — human-video-only Helix navigation
- Sunday ACT-1 "zero robot data" — Sunday — 2025-11 (date unconfirmed) — https://www.sunday.ai/blog/no-robot-data — company-claim — glove data replaces teleoperation
## Suggested sections
No internet of actions; data pyramid; scaling evidence and limits (Lin vs GEN-0 vs Dyna-2); diversity vs volume; cost per hour; the data race, with a claims table attributed to each company.
## Surprises and controversies
- Company scaling claims (GEN-0, Dyna-2) are unreviewed and use inconsistent "hours".
- Figure Index stats (16M videos, 108 countries, Aug 2026) reached me only through an aggregator (explainx.ai). Primary Figure post not found: unconfirmed.
- Cost per hour: only vendor blogs (Dexset, Avala, Cervo) found. They quote $28-60 per hour for teleoperation and $15-40 for egocentric video. Treat as unreliable; find a primary or independent source.
- AgiBot World's hour count (2,976.4) came from a search snippet; unconfirmed.
