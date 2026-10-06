# ch08 scan · The senses: cameras, depth, inertial, force, touch and sound (scanned 2026-10-06)
## What is new since 2025
- Large tactile datasets and benchmarks arrived: TacVerse (about 107k images from 7 sensors); T-Rex (100 hours, Sharpa fingertips), cited by a survey and not yet opened.
- Cross-sensor transfer is weak. Models degrade on unseen tactile sensors.
- Whole-body skins are maturing: a 3D-printed EIT skin (2026-08-03, 6 mm localisation) and a capacitive origami e-skin (Nature-family journal, March 2026, from search snippet, not opened).
- Sim study: whole-hand coverage beats fingertip-only. Proprioception alone was inadequate.
- Atlas (CES 2026) and its new hand carry fingertip and palm pressure sensing. Figure 03 has palm cameras and wider-field cameras.
## Key primary sources
- Introducing Figure 03 — Figure AI — 2025-10-09 — https://www.figure.ai/news/introducing-figure-03 — company-claim — camera and fingertip claims
- Meta FAIR: Sparsh, Digit 360, Digit Plexus — Meta — 2024-10-31 — https://ai.meta.com/blog/fair-robotics-open-source/ — company-claim — Digit 360: 1 mN, 18 features
- Tactile Beyond Pixels (Sparsh-X) — Higuera et al. — 2025-06-17 — https://arxiv.org/abs/2506.14754 — preprint — image, audio, motion, pressure fused
- TacVerse — Wei et al. — 2026-06-24 — https://arxiv.org/abs/2606.25877 — preprint — cross-sensor benchmark
- Tactile Genesis — Chung et al. — 2026-06-21 — https://arxiv.org/abs/2606.22332 — preprint — what placement and resolution buy
- Vision-Based Tactile Intelligence survey — Zhou et al. — 2026-08-16 — https://arxiv.org/abs/2608.15490 — preprint — taxonomy and datasets
- 3D-Printed Conformal EIT Skin — Chen et al. — 2026-08-03 — https://arxiv.org/abs/2608.02080 — preprint — whole-body humanoid skin
## Suggested sections
Cameras; depth and LiDAR; IMU and proprioception; force/torque; tactile (optical, capacitive, magnetic, EIT); sound; degraded conditions; sensor suites compared; what each adds to learning.
## Surprises and controversies
Sensor-suite comparisons come mostly from aggregator sites (rejected). Primary spec sheets are needed for Atlas, Optimus and Digit. Gaps: GelSight/DIGIT originals, magnetic-skin primaries (ReSkin, AnySkin appeared in search but were not opened), microphones, and sun/steam/dust evidence.
