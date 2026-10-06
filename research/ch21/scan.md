# ch21 scan · Modalities and the data dictionary (scanned 2026-10-06)
## What is new since 2025
- LeRobotDataset v3.0 (Sept 2025) packs many episodes per Parquet/MP4 file, with relational metadata and a streaming class; the docs now also mention Lance layouts and HF storage buckets.
- NVIDIA's GR00T line has moved on to N1.7 (GA, per repo README). It still uses a "flavour of LeRobot v2" plus a `meta/modality.json` that splits state/action vectors into named fields. Converters from v3 exist in the repo.
- Aria Gen 2 pilot dataset (Oct 2025) gives a modern egocentric sensor/rate list (RGB, 4 CV cameras, 2 IMUs at 800 Hz, audio, PPG).
## Key primary sources
- LeRobotDataset v3.0 docs — Hugging Face — undated (page current 2026) — https://huggingface.co/docs/lerobot/lerobot-dataset-v3 — tech-report — field names, info.json, stats.json, tasks, normalisation stats
- LeRobotDataset:v3.0 blog — Capuano et al. (HF) — 2025-09-16 — https://huggingface.co/blog/lerobot-datasets-v3 — tech-report — design rationale for v3
- Isaac-GR00T N1.7 repository — NVIDIA — undated — https://github.com/Nvidia/Isaac-GR00T — tech-report — GR00T data format, data-preparation guide
- GR00T N1 — NVIDIA — https://arxiv.org/abs/2503.14734 — preprint — date unconfirmed (page not opened); original GR00T paper
- DROID — Khazatsky et al. — 2024-03-19 (v2 2025-04-22) — https://arxiv.org/abs/2403.12945 — preprint — fields: 3 cameras, calibration, depth, language
- Open X-Embodiment — Open X-Embodiment Collaboration — 2023-10-13 (v9 2025-05-14) — https://arxiv.org/abs/2310.08864 — preprint — 22 embodiments; cross-robot schema and action conventions
- RLDS — Ramos et al. — 2021-11-04 — https://arxiv.org/abs/2111.02767 — preprint — episode/step data model
- Aria Gen 2 Pilot Dataset — Kong et al. — 2025-10-17 — https://arxiv.org/abs/2510.16134 — preprint — sensor rates and sizes for egocentric capture
## Suggested sections
Observation modalities with rates and sizes; action spaces and conventions; language and metadata; episode data model (RLDS vs LeRobot vs GR00T modality.json); normalisation (stats.json); data dictionary for Appendix A.
## Surprises and controversies
- No single standard: "LeRobot" now means v2.1 or v3.0, and GR00T pins to a v2 flavour.
- Action-space conventions (delta vs absolute, frames) are not specified by any format; they live in dataset cards. Gap: Open X field list not yet read in full.
