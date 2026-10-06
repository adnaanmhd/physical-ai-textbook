# ch11 scan · How machines learn: neural networks from scratch (scanned 2026-10-06)
## What is new since 2025
- Vision encoders: DINOv3 (Aug 2025) scales self-supervised learning to a 7B teacher on 1.7B images, adds Gram anchoring for dense features, and ships distilled ViT/ConvNeXt students. SigLIP 2 (Feb 2025) adds captioning and self-distillation losses to the contrastive recipe.
- Scaling laws are being re-fitted for data-limited training (2026 preprints), not just Chinchilla's data-rich regime.
- Robot-specific scaling work exists (data and embodiment scaling), but is early.
## Key primary sources
- Adam: A Method for Stochastic Optimization — Kingma, Ba — 2014-12-22 — https://arxiv.org/abs/1412.6980 — preprint — the default optimiser
- An Image is Worth 16x16 Words (ViT) — Dosovitskiy et al. — 2020-10-22 — https://arxiv.org/abs/2010.11929 — preprint — ViT original
- Scaling Laws for Neural Language Models — Kaplan et al. — 2020-01-23 — https://arxiv.org/abs/2001.08361 — preprint — original power laws
- Training Compute-Optimal LLMs — Hoffmann et al. — 2022-03-29 — https://arxiv.org/abs/2203.15556 — preprint — Chinchilla correction
- DINOv2 — Oquab et al. — 2023-04-14 — https://arxiv.org/abs/2304.07193 — preprint — self-supervised encoder baseline
- DINOv3 — Siméoni et al. (Meta) — 2025-08-13 — https://arxiv.org/abs/2508.10104 — preprint — newest self-supervised vision backbone
- SigLIP 2 — Tschannen et al. (Google DeepMind) — 2025-02-20 — https://arxiv.org/abs/2502.14786 — preprint — encoder inside PaliGemma-style VLAs
- OpenVLA — Kim et al. — 2024-06-13 — https://arxiv.org/abs/2406.09246 — preprint — fuses SigLIP and DINOv2 for robots
- Practical Scaling Laws (data-constrained) — Bryant — 2026-05-09 — https://arxiv.org/abs/2605.09189 — preprint — extends Chinchilla past single-epoch
- Data Scaling Laws in Imitation Learning — Lin et al. — 2024-10-24 — https://arxiv.org/abs/2410.18647 — preprint — robot data power laws
## Suggested sections
Learning as function fitting; neurons/layers; losses; gradient descent and backprop; optimisers; overfitting and splits; embeddings; vision encoders (CNN, ViT, DINO, SigLIP); scaling laws (language, then robotics).
## Surprises and controversies
- Chinchilla fits are contested (2026 preprint 2603.22339 on IsoFLOP biases; not yet opened).
- Backprop (1986) and ResNet originals not confirmed this scan; fetch in scouting.
- Which encoder wins for control is unsettled; OpenVLA reported only a small gain from DINOv2.
