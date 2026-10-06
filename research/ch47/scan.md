# ch47 scan · Running a fleet (scanned 2026-10-06)

## What is new since 2025
- Agility's Digit 5 release (Sept 2026) names fleet KPIs in Arc: uptime, throughput, mean time between incidents (MTBI). Arc links to WMS, WES, MES.
- Digit 4 reported 65,000+ operating hours across GXO, Schaeffler, Amazon and Toyota Canada; one GXO site passed 100,000 totes at about 98% accuracy (company-claim).
- Figure ran a livestreamed package-sorting test (May 2026). Figure has published no intervention rate or uptime numbers that I could find.
- 1X sells scheduled "Expert Mode", where a remote human guides NEO. Staffing ratios are unpublished.
- ISO 25785-1 is still a draft, with Agility and Boston Dynamics co-leading the working group.

## Key primary sources
- Agility unveils Digit 5 — Agility Robotics — 2026-09-15 — https://www.prnewswire.com/news-releases/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale-302878540.html — company-claim — Arc KPIs, battery swap, hours
- Agility Arc launch — Agility Robotics via Robotics Tomorrow — 2024-03-11 (date from URL) — https://www.roboticstomorrow.com/news/2024/03/11/agility-robotics-brings-operational-visibility-to-deployment-of-digit%E2%93%87-fleets-with-the-launch-of-agility-arc/22211/ — company-claim — original Arc feature set; I did not open it (unconfirmed)
- NEO Home Robot — 1X — undated — https://www.1x.tech/neo — company-claim — Expert Mode wording, privacy FAQ
- ISO/CD 25785-1 — ISO — undated — https://www.iso.org/standard/91469.html — standard — safety requirements bearing on remote operation
- Figure 03 BMW report — The Robot Report — 2026-06-29 — https://www.therobotreport.com/bmw-group-deploys-figure-03-humanoid-after-tests-previous-version/ — press — fleet detail absent
- Toward Certified Functional Safety for Industrial Humanoid Robots (arXiv 2608.02809) — already in ch10 scan; reuse.

## Suggested sections
Fleet software and Arc-style KPIs; what to log and privacy; remote assistance staffing as a queueing problem; incidents; OTA with staged rollout; spares and field service; KPI glossary.

## Surprises and controversies
- Operator-to-robot ratios: only vendor blogs (such as Adamo) quote "1:5 to 1:10" and "1:50 by 2029". I rejected them as weak and unsourced. No primary ratio published (gap).
- OTA: UNECE R156 and ISO 24089 are the natural analogues. I only found secondary summaries, so the primary text is still needed (gap).
- AMR analogues: RaaS and ROI figures I found are vendor or SEO pages. A primary source (for example a Locus or Amazon Robotics paper) is still needed (gap).
