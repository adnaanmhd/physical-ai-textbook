# ch41 scan · Where world models and WAMs fail, and what data fixes it (scanned 2026-10-06)
## What is new since 2025
- Robot-specific diagnostics have joined the physics benchmarks. RoboTrustBench (June) finds coherent video but weak constraint reasoning, counterfactual grounding and physical interaction. A late-August paper finds action-conditioned world models trained on expert data ignore off-expert actions and hallucinate success.
- The WAM-vs-VLA robustness study (23 Mar 2026, revised 30 Jul) reports WAMs more robust on RoboTwin 2.0-Plus and LIBERO-Plus, but π0.5 can match with diverse data.
- Touch and force remedies multiplied: FAWAM (force), Tactile-WAM, TacWAM, TacDyn-WAM, TacPAC. Tactile-WAM names "tactile pollution". Only FAWAM was opened.
- Data: T-Rex (100 h tactile). Also surfaced by search, not opened: EgoVerse, EgoDex, EgoTouch, EgoTac, "Data Pyramid for Embodied Manipulation: A Survey" (2607.24744).
## Key primary sources
- Do WAMs Generalize Better than VLAs? A Robustness Study — Zhang et al. — 2026-03-23 — https://arxiv.org/abs/2603.22078 — preprint — core WAM-vs-VLA robustness evidence
- Do Robotic World Models Really Follow Actions? — Chen et al. — 2026-08-25 — https://arxiv.org/abs/2608.24885 — preprint — action non-compliance, optimistic futures
- RoboTrustBench — Li et al. — 2026-06-01 — https://arxiv.org/abs/2606.01600 — preprint — trustworthiness of manipulation video models
- VideoPhy-2 — 2025-03 — https://arxiv.org/abs/2503.06800 — preprint — action-centric physical commonsense (date from arXiv ID; not opened)
- WorldModelBench — 2025-02 — https://arxiv.org/abs/2502.20694 — preprint — physics laws, robotics domain (not opened)
- FAWAM — He et al. — 2026-06-07 — https://arxiv.org/abs/2606.08555 — preprint — force as prediction and correction signal
- Tactile-WAM — 2026-06 — https://arxiv.org/abs/2606.26663 — preprint — touch-aware WAM (listed by search; not opened)
- T-Rex — Niu et al. — 2026-06-15 — https://arxiv.org/abs/2606.17055 — preprint — 100 h tactile-rich dataset
- Robots Need More than VLA and World Models — Karcini et al. — 2026-06-04 — https://arxiv.org/abs/2606.06556 — preprint — data, embodiment, world, reward interfaces missing
## Suggested sections
Failure taxonomy; benchmarks and probes; data root causes by modality; remedies (force/tactile, action-diverse data, failures and recoveries); measuring progress.
## Surprises and controversies
The robustness study is pro-WAM yet concedes data closes the gap. Physics-IQ, PhyGenBench, WorldScore not confirmed this scan. DreamZero says video is only one possible future modality, so touch WAMs are on-brief.
