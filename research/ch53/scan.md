# ch53 scan · Open problems and where the field is heading (scanned 2026-10-06)
## What is new since 2025
- A June 2026 position paper argues the bottleneck is converting unstructured behaviour data into grounded robot supervision, not just scaling VLAs.
- Safety certification is now concretely framed: a "fail-passive gap" (cutting power makes a biped fall) blocks top safety levels under existing standards. ISO 25785-1 for legged and balancing industrial robots is still in draft (secondary report; ISO page blocked).
- Surveys name long-horizon reliability, evaluation without standard protocols, and whole-body humanoid control as open.
- Tactile and touch-aware world-action models are a fast-growing 2026 arXiv theme.
## Key primary sources
- Robots Need More than VLA and World Models — Karcini, Schwager, Hutter, Peters, Bou-Ammar et al. — 2026-06-04 — https://arxiv.org/abs/2606.06556 — preprint — data, reward, embodiment interfaces
- Toward Certified Functional Safety for Industrial Humanoid Robots — Ding, Cui, Wang, Wen — 2026-08-03 — https://arxiv.org/abs/2608.02809 — preprint — the fail-passive gap, tested on Unitree G1
- Foundation Models in Robotics: A Comprehensive Review — Psiris et al. — 2026-04-16 (TMLR, July 2026) — https://arxiv.org/abs/2604.15395 — peer-reviewed — challenges list, datasets
- ISO/CD 25785-1 — ISO — date unconfirmed — https://www.iso.org/standard/91469.html — standard — unconfirmed (403); draft status
- Learning Versatile Humanoid Manipulation with Touch Dreaming — arXiv 2604.13015 — 2026 — https://arxiv.org/html/2604.13015v1 — preprint — unconfirmed; touch in humanoid policies
- Why Today's Humanoids Won't Learn Dexterity — Rodney Brooks — 2025-09-26 — https://rodneybrooks.com/why-todays-humanoids-wont-learn-dexterity/ — press — leading sceptical view (also in ch02 scan)
## Suggested sections
Follow the seed list. Add "what would change our mind" per problem, and a signals table linked to ch51 indicators. Fill from the ch40s evaluation, safety and world-model chapters rather than repeating them.
## Surprises and controversies
- Whether touch and dexterity need new hardware or just more data (Brooks versus data-scaling camps).
- Whether certification can ever cover a learned balancing policy.
- Gaps: no 2026 roadmap on energy and runtime, cost curves, or physics fidelity in world models found yet; ICML 2026 position papers list (https://icml.cc/virtual/2026/events/2026-position-papers) is unmined.
