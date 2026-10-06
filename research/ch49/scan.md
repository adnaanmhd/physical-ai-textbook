# ch49 scan · Continual improvement and release engineering (scanned 2026-10-06)
## What is new since 2025
Forgetting in VLAs is now measured on real-world data, not just LIBERO simulation. One 2026 study finds experience replay mitigates forgetting and beats joint multi-task training. Reinforcement-fine-tuning and regularisation methods (LifeLong-RFT, CRL-VLA) claim gains. Fleet-scale continual post-training exists (see ch48). For release practice, robotics-specific canary or shadow sources were not found; the available pages are LLM-ops blogs (not usable). Automotive is the mature analogue: UN R156 (SUMS, RXSWIN) and ISO 24089.
## Key primary sources
- Can VLA Models Learn from Real-World Data Continually without Forgetting? — Zhu et al. — 2026-05-26 — https://arxiv.org/abs/2605.26820 — preprint — replay vs forgetting, real-world data
- Towards Long-Lived Robots (LifeLong-RFT) — Liu et al. — 2026-02-11 (rev. 2026-05-16) — https://arxiv.org/abs/2602.10503 — preprint — +22% over SFT, 20% data
- CRL-VLA — Zeng et al. — 2026-02-03 — https://arxiv.org/abs/2602.03445 — preprint — stability-plasticity via advantage regularisation; LIBERO
- Learning While Deploying — Wang et al. — 2026-05-01 — https://arxiv.org/abs/2605.00416 — preprint — fleet continual post-training and redeployment
- UN Regulation No. 156 (E/ECE/TRANS/505/Rev.3/Add.155) — UNECE — 2021-03-04 — https://unece.org/transport/documents/2021/03/standards/un-regulation-no-156-software-update-and-software-update — standard — page appeared in search; fetch 403, unconfirmed text
- R156 PDF — UNECE — https://unece.org/sites/default/files/2024-03/R156e%20(2).pdf — standard — not opened, unconfirmed
- ISO 24089:2023 Software update engineering — ISO — 2023 — https://www.iso.org/standard/77796.html — standard — fetch 403; search snippet only, unconfirmed
## Suggested sections
Retraining cadence; forgetting and replay; global vs site models; regression suites and gates; shadow/canary/staged rollout (borrowing automotive); rollback; re-certification (R156 "does the update affect approval"); audit trails; twists (connector spec, preferences, season).
## Surprises and controversies
No robotics release-engineering primary source found: a real gap. Forgetting results are mostly small benchmarks. R156 and ISO 24089 apply to road vehicles; carrying them to humanoids is inference. Both standards need paid or manual access. Gap: look at ISO 10218/IEC 61508 and EU AI Act post-market rules.
