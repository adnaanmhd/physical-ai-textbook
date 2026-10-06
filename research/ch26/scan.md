# ch26 scan · Designing datasets and data mixtures (scanned 2026-10-06)
## What is new since 2025
Mixture design now has two levels. Re-Mix (2024) learns domain weights with distributionally robust optimisation; DataMIL (2025, ICLR 2026) selects individual samples with datamodels. Influence-based attribution followed: CUPID (CoRL 2025), QoQ (Mar 2026), ATHENA (Jun 2026), plus TUCO for sim-to-real co-training (listed in search results; unopened). Frontier recipes keep to co-training: π0.5 mixes multi-robot, web and subtask-prediction data; GR00T N1 uses a data pyramid, and N1.6 is out (NVIDIA model card/blog, unopened).
## Key primary sources
- Re-Mix: Optimizing Data Mixtures for Large Scale Imitation Learning — Hejna, Bhateja et al. — 2024-08-26 — https://arxiv.org/abs/2408.14037 — peer-reviewed (CoRL 2024; venue unconfirmed) — domain weights beat uniform
- DataMIL: Selecting Data for Robot Imitation Learning with Datamodels — Dass, Khaddaj et al. — 2025-05-14 — https://arxiv.org/abs/2505.09603 — preprint (ICLR 2026 per a secondary note) — sample-level selection
- π0.5: a VLA with Open-World Generalization — Physical Intelligence — 2025-04-22 — https://arxiv.org/abs/2504.16054 — tech-report — co-training mixture
- GR00T N1 — NVIDIA — 2025-03-18 — https://arxiv.org/abs/2503.14734 — tech-report — data pyramid
- CUPID — Agia et al. — 2025-06-23 — https://arxiv.org/abs/2506.19121 — peer-reviewed — attribution to returns
- ATHENA — Xu, Wang et al. — 2026-06-15 — https://arxiv.org/abs/2606.16208 — preprint — multi-task influence
- Quality over Quantity (QoQ) — Lee, Min et al. — 2026-03-10 — https://arxiv.org/abs/2603.09056 — preprint — curation by influence
- Open X-Embodiment paper — not searched; unconfirmed
## Suggested sections
Coverage and long tail; taxonomies; mixture weights (Re-Mix); co-training recipes; attribution and ablation; budgets and ROI; dataset documentation.
## Surprises and controversies
Human-judged "quality" may not match policy-useful data (DataMIL). Re-Mix's headline gains (38% over uniform, 75% less data) are the authors' own and on RT-X data. Gaps: Open X-Embodiment lessons, GR00T N1.6 tech report, and independent mixture benchmarks not confirmed; ROI and budget sources are thin.
