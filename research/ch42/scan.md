# ch42 scan · How WAMs and VLAs converge on physical AI (scanned 2026-10-06)
## What is new since 2025
- Convergence is visible in named systems. Kairos (June) is a 4B native world-action stack. DM0 (Feb) is a VLA built embodied-native from pretraining. Cosmos 3 folds world-action models into one omnimodal family. FLUX 3 Action claims VLA speed with WAM quality.
- Layered hybrids: π0.7 (Physical Intelligence) takes subgoal images from a small BAGEL-based world model. Its blog page returned 429, so details come from search snippets: unconfirmed.
- Head-to-head evidence is mixed. DreamZero ranks above π0.5 on RoboArena (aggregator-reported). A benchmark comparison reports a 1.58-point clean-score gap and says no model wins every axis. Treat both as unconfirmed.
- Position paper "Robots Need More than VLA and World Models" argues both are layers of a bigger stack; author list is academic (Schwager, Peters, Hutter).
## Key primary sources
- Robots Need More than VLA and World Models — Karcini et al. — 2026-06-04 — https://arxiv.org/abs/2606.06556 — preprint — position: neither alone suffices
- Kairos — Kairos Team — 2026-06-15 — https://arxiv.org/abs/2606.16533 — preprint — native world-action stack, efficiency first
- DM0 — Yu et al. — 2026-02-16 — https://arxiv.org/abs/2602.14974 — preprint — embodied-native VLA
- Cosmos 3 — NVIDIA — 2026-06-01 — https://arxiv.org/abs/2606.02800 — tech-report — world-action inside omnimodal model
- Do WAMs Generalize Better than VLAs? — Zhang et al. — 2026-03-23 — https://arxiv.org/abs/2603.22078 — preprint — direct comparison
- World Action Models: A Survey — Shen et al. — 2026-06-18 — https://arxiv.org/abs/2606.20781 — preprint — frames WAM versus VLA
- DreamZero — Ye et al. — 2026-02-17 — https://arxiv.org/abs/2602.15922 — preprint — the WAM bet
- π0.7 — Physical Intelligence — 2026 — https://www.pi.website/blog/pi07 — company-claim — hybrid; unconfirmed (page not opened)
- IndustrialVLA-Bench — 2026-09 — https://arxiv.org/pdf/2609.25562 — preprint — multi-axis comparison (unconfirmed, not opened)
- Think Like a World Model, Act Like a VLA — 2026-09 — https://arxiv.org/pdf/2609.24682 — preprint — distillation route (unconfirmed, not opened)
## Suggested sections
Two bets; five routes; head-to-head evidence and its limits; deciders (data, compute, latency, evaluation); scenarios with signals; deployment implications.
## Surprises and controversies
WAMs cost about 7x more training compute (aggregated claim, unconfirmed). Fast-WAM drops imagination, blurring the WAM/VLA line. VLA-JEPA, DreamVLA, UniVLA, τ0-VLA not checked.
