# ch10 scan · Safety hardware, reliability and maintenance (scanned 2026-10-06)
## What is new since 2025
- Figure published the first named deployment write-up (Nov 2025): 1,250+ hours, forearm as top failure point, but no MTBF or uptime figure.
- BMW (June 2026) moved to Figure 03 with soft components and wireless charging.
- Agility Digit 5 (Sept 2026) adds an independent safety controller on NVIDIA Halos; FORT Robotics partnership.
- ISO 25785-1 for actively balanced robots was still a working draft in early 2026 (secondary report; unconfirmed since).
- Fall-safety research grew: SafeFall, VIGOR, soft protective materials.
## Key primary sources
- F.02 Contributed to the Production of 30,000 Cars at BMW — Figure AI — 2025-11-19 — https://www.figure.ai/news/production-at-bmw — company-claim — only deployment failure data; qualitative
- BMW Group advances Physical AI with Figure 03 project — BMW Group — 2026-06-25 — https://www.press.bmwgroup.com/global/article/detail/T0458778EN/bmw-group-advances-the-use-of-physical-ai-in-production-with-figure-03-project-in-spartanburg?language=en — company-claim — customer-side confirmation
- Toward Certified Functional Safety for Industrial Humanoid Robots — Ding, Cui, Wang, Wen — 2026-08-03 — https://arxiv.org/abs/2608.02809 — preprint — "fail-passive gap": power-off is itself hazardous
- SafeFall: Learning Protective Control — Meng et al. — 2025-11-23 — https://arxiv.org/abs/2511.18509 — preprint — learned falls cut peak force 68%
- Soft Responsive Materials Enhance Humanoid Safety — Wang et al. — 2026-01-06 — https://arxiv.org/abs/2601.02857 — preprint — protective materials survived 3 m drops
- Agility Unveils Digit 5 — Agility Robotics — 2026-09-15 — https://www.agilityrobotics.com/content/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale — company-claim — independent safety controller; 65,000+ fleet hours
- Introducing Figure 03 — Figure AI — 2025-10-09 — https://www.figure.ai/news/introducing-figure-03 — company-claim — foam, washable soft goods, battery protection layers
## Suggested sections
E-stop/STO and the fail-passive problem; limiting and collision detection; falling safely; reliability evidence (what is and is not published); maintenance and swappable parts; soft covers; standards status.
## Surprises and controversies
- No public MTBF or uptime figures found; "minimal failures" is unquantified.
- Standards fit badly: de-energising a biped causes a fall.
- Gaps: ISO 25785-1 primary page, VIGOR/stoppability papers (2602.16511, 2609.02358; not opened), Atlas design notes.
