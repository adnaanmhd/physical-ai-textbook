# ch36 scan · What a world model is (scanned 2026-10-06)

## What is new since 2025
- Many 2026 surveys; the field has no single definition. Taxonomies split by function (decision-coupled vs general), time and space, or by capability level.
- Cosmos 3 (May 2026) is a "mixture-of-transformers" model that reasons, generates video and predicts actions (NVIDIA claim).
- Genie 3 became a product (Project Genie, Jan 2026) and is the base of the Waymo World Model (Feb 2026).
- Wayve GAIA-3 (Dec 2025) reframes world models as evaluation tools.
- Dreamer 4 trains agents purely in imagination.

## Key primary sources
- Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond — Chu et al. — 2026-04-24 — https://arxiv.org/abs/2604.22748 — preprint — L1 predictor/L2 simulator/L3 evolver taxonomy
- A Comprehensive Survey on World Models for Embodied AI — Li et al. — 2025-10-19 (rev. 2026-06-25) — https://arxiv.org/abs/2510.16732 — preprint — three-axis taxonomy; physical-plausibility metrics
- V-JEPA 2 — Assran et al. (Meta FAIR) — 2025-06-11 — https://arxiv.org/abs/2506.09985 — preprint — latent/JEPA family; robot planning from 62 hours
- Training Agents Inside of Scalable World Models (Dreamer 4) — Hafner, Yan, Lillicrap — 2025-09 — https://arxiv.org/abs/2509.24527 — preprint — Dreamer-style model-based RL, latest
- Genie 3: A new frontier for world models — Google DeepMind — 2025-08-05 — https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/ — company-claim — interactive family (not opened; date from search)
- NVIDIA Launches Cosmos 3 — NVIDIA — 2026-05-31 — https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai — company-claim — benchmark ranks are self-reported
- World Simulation with Video Foundation Models for Physical AI (Cosmos-Predict2.5) — NVIDIA — 2025-10-28 — https://arxiv.org/abs/2511.00062 — tech-report — video family, 2B/14B
- GAIA-3 — Wayve — 2025-12-02 — https://wayve.ai/thinking/gaia-3/ — company-claim — 15B latent diffusion; evaluation focus
- The Waymo World Model — Waymo — 2026-02-06 — https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation/ — company-claim — Genie 3 based; no sizes or data disclosed
- 1X World Model — 1X — date unconfirmed — https://www.1x.tech/discover/world-model-self-learning — company-claim — unconfirmed, not opened
- World Labs Marble — https://www.worldlabs.ai/blog/announcing-the-world-api — unconfirmed, not opened; 3D family; public release reported 2025-11-12 (press)

## Suggested sections
1. Prediction as understanding; Ha and Schmidhuber origin.
2. Definitions across fields; why they clash.
3. Taxonomy: pixel, latent, 3D/4D, Dreamer-style RL, interactive.
4. Passive vs action-conditioned.
5. Uses (data, evaluation, RL, planning, verification).
6. Self-driving lessons (Wayve, Waymo, Tesla).
7. World models vs simulators.

## Surprises and controversies
- Tesla: only keynote talks (ICCV 2025) found; no peer-reviewed paper confirmed. Treat as demo/company-claim.
- Waymo and Wayve disclose little (no data, latency, consistency methods).
- Cosmos 3 rankings are NVIDIA's own claims.
- A survey (2608.23070, unopened) asks whether world models are true simulators.
- Not yet found: Ha and Schmidhuber 2018 and the Genie 2 page, both unfetched.
