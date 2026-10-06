# ch39 scan · Using world models: data, evaluation, RL and planning (scanned 2026-10-06)
## What is new since 2025
- Google's Gemini Robotics team used a Veo-based simulator to rank policies; it reports Pearson 0.88 with 1,600+ real trials (via search summary; novel-object cases only 0.56).
- Policy-evaluation world models multiplied: WorldEval (2025), Ctrl-World (ICLR 2026), dWorldEval (Apr 2026), plus GigaWorld-1, RoboWorld, PiL-World (search only).
- Verification and failure prediction at run time is new in 2026: CheckVLA (Jul 2026), DreamAvoid, Pre-VLA.
- Closed-loop RL in imagination: World-VLA-Loop; WMPO (ICLR 2026).
## Key primary sources
- Evaluating Gemini Robotics Policies in a Veo World Simulator — Gemini Robotics Team, Google — 2025-12-11 — https://arxiv.org/abs/2512.10675 — preprint — verified DeepMind evaluation study with real-world correlation
- WorldEval — Li et al. — 2025-05-25 — https://arxiv.org/abs/2505.19017 — preprint — first policy-ranking world model, safety screening
- Ctrl-World — Guo, Shi, Chen, Finn — 2025 — https://arxiv.org/abs/2510.10125 — preprint — evaluation and improvement in imagination (38.7 to 83.4%, per abstract summary)
- dWorldEval — Li et al. — 2026-04-24 — https://arxiv.org/abs/2604.22152 — preprint — beats WorldEval and Ctrl-World on its benchmarks
- DreamGen — Jang et al., NVIDIA — 2025-05-19 — https://arxiv.org/abs/2505.12705 — preprint — synthetic "neural trajectories" for training
- V-JEPA 2 (V-JEPA 2-AC planning) — Meta — 2025-06-11 — https://arxiv.org/abs/2506.09985 — preprint — zero-shot planning on Franka arms
- World-VLA-Loop — Liu et al. — 2026-02-06 — https://arxiv.org/abs/2602.06508 — preprint — RL in a world model with failure feedback
- CheckVLA — Liu et al. — 2026-07-29 — https://arxiv.org/abs/2607.26789 — preprint — action-conditioned verification; recall 77.9% at 5% false alarms
- 1X World Model: Evaluating Bits, not Atoms — 1X — date unknown — https://www.1x.tech/1x-world-model.pdf — company-claim — unconfirmed (PDF unreadable)
- 1X World Model blog — 1X — 2024-09-17 — https://www.1x.tech/discover/1x-world-model — company-claim — evaluation framed as future goal
## Suggested sections
Follow the seed list; add "When imagined scores mislead" (correlation by condition).
## Surprises and controversies
- Correlation is strong for ranking, weak for novel objects and precise contact.
- Most correlations are self-reported on small policy sets.
- RISE, Interactive World Simulator and "self-correcting VLA" not found; leave as leads.
