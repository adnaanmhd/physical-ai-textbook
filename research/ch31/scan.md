# ch31 scan · Pre-training the robot brain (scanned 2026-10-06)
## What is new since 2025
- π0.7 (Apr 2026): 5B-parameter model, trained with rich context (subgoal images, quality metadata) so mixed and failure data are usable.
- Human egocentric video is now a headline pre-training source: GR00T N1.7 (about 20.9K hours), Helix 2.5 (Index data), Being-H0.5.
- Scaling evidence is multiplying: GEN-0, TRI LBM, EgoScale, GE-Act 2.0.
- World-action models are emerging beside VLAs (GR00T N2 announced; DreamZero lead).
## Key primary sources
- π0.7: a Steerable Generalist Robotic Foundation Model — Physical Intelligence — 2026-04-16 — https://arxiv.org/abs/2604.15483 — preprint — newest π; context conditioning
- π0.5: a VLA with Open-World Generalization — Physical Intelligence — 2025-04-22 — https://arxiv.org/abs/2504.16054 — preprint — co-training recipe
- FAST: Efficient Action Tokenization — Pertsch et al. — 2025-01-16 — https://arxiv.org/abs/2501.09747 — preprint — DCT action tokens
- GR00T N1.7 — NVIDIA — 2026-04-17 — https://huggingface.co/blog/nvidia/gr00t-n1-7 — tech-report — open, 3B, human-video pretraining
- GR00T N1 — NVIDIA — 2025-03 — https://arxiv.org/pdf/2503.14734 — preprint — dual-system original
- Gemini Robotics 1.5 — Google DeepMind — 2025-10-02 — https://arxiv.org/abs/2510.03342 — tech-report
- Gemini Robotics 2 — Google DeepMind — 2026-07-30 — https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/ — company-claim — no technical report seen
- A Careful Examination of Large Behavior Models — TRI LBM Team — 2025-07 — https://arxiv.org/abs/2507.05331 — preprint — blind-tested pretraining benefit
- GEN-0 — Generalist — 2025-11-04 — https://generalistai.com/blog/gen-0 — company-claim — 270K hours, 7B threshold
- Being-H0.5 — BeingBeyond — 2026-01-19 — https://arxiv.org/abs/2601.12993 — preprint — 35K hours, 30 embodiments
- GE-Act 2.0 — AgiBot — 2026-09-04 — https://arxiv.org/abs/2609.05588 — preprint — 300 to 30,000 hours scaling
- Helix 2.5 — Figure — 2026-09-17 — https://www.figure.ai/news/helix-2-5-zero-shot-30-home-generalization — company-claim
- Skild S1 — Robot Report — 2026-08-31 — https://www.therobotreport.com/skild-ai-unveils-s1-flagship-robot-foundation-model/ — press — find primary Skild post
## Suggested sections
Keep the seed list; add "Human data as pre-training" and "From VLA to world-action model".
## Surprises and controversies
- Seed's "π0.7" confirmed; π1 not found.
- Skild S1 is the newest Skild model, replacing Skild Brain. Helix is now 2.5.
- Not confirmed: SmolVLA, X-VLA primaries, DYNA-1/Dyna-2, GO-1, Galbot, GR00T N2, EgoScale paper.
- Vendor scaling claims lack independent replication.
