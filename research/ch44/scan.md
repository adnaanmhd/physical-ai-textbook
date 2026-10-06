# ch44 scan · Safety engineering for learned robots (scanned 2026-10-06)
## What is new since 2025
- Runtime safety layers for VLA policies are a 2026 research wave: CBF filters on policy output, attention-guided filters, policy-library CBFs, latent safety filters.
- Semantic safety: ASIMOV (DeepMind, Mar 2025) plus generated "constitutions"; Gemini Robotics 1.5 reports ASIMOV results (company claim).
- Humanoid fall management is now learned: fall prediction plus protective policies, safe-stop value functions.
- Cybersecurity: documented Unitree G1 flaws, including a 2026 chained Bluetooth-to-root report.
- Certification theory: the "fail-passive gap" (cutting power makes a balancing biped fall).
## Key primary sources
- Generating Robot Constitutions & Benchmarks for Semantic Safety — Sermanet et al. (DeepMind) — 2025-03-11 — https://arxiv.org/abs/2503.08663 — preprint — ASIMOV; 84.3% alignment with generated constitutions
- Gemini Robotics 1.5 — Google DeepMind — 2025 (date unconfirmed) — https://arxiv.org/pdf/2510.03342 — tech-report — ASIMOV results; opened only via search
- Your Model Already Knows: Attention-Guided Safety Filter for VLA Models — Park et al. — 2026-06-08 — https://arxiv.org/abs/2606.09749 — preprint — CBF filter on VLA, SafeLIBERO
- Toward Certified Functional Safety for Industrial Humanoid Robots — Ding et al. — 2026-08-03 — https://arxiv.org/abs/2608.02809 — preprint — fail-passive gap; no PL e/SIL 3 claim
- SafeFall: Learning Protective Control for Humanoid Robots — Meng et al. — 2025-11-23 — https://arxiv.org/abs/2511.18509 — preprint — 68.3% lower peak contact force
- The Cybersecurity of a Humanoid Robot — Mayoral-Vilches — 2025-09-17 — https://arxiv.org/abs/2509.14096 — preprint — static keys, telemetry on Unitree G1
- Two Unitree G1 EDU flaws enable root RCE — The Hacker News — 2026-08 — https://thehackernews.com/2026/08/two-unitree-g1-edu-humanoid-robot-flaws.html — press — secondary; trace CVEs to a primary advisory (unconfirmed)
- Humanoid Safe Stop via Learned Stoppability Value — arXiv 2609.02358 — https://arxiv.org/pdf/2609.02358 — preprint — unconfirmed, search only
## Suggested sections
Hazard analysis; functional safety and the fail-passive problem; speed/force limiting; runtime filters and certified fallbacks; semantic safety; fall management; cybersecurity and privacy; incident response.
## Surprises and controversies
Learned filters carry no certification path yet. Cybersecurity claims about data sent to China come from researchers and press; treat as attributed. Incident-response sources not yet found: gap.
