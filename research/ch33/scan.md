# ch33 scan · Post-training: fine-tuning, adaptation and making models fast (scanned 2026-10-06)
## What is new since 2025
Inference is now measured systematically: VLA-Perf (Feb 2026) models latency across on-device, edge and cloud. Quantisation moved from ad hoc to a field: QuantVLA (Feb 2026), ActQuant (sub-4-bit), FoldQuantVLA, then VLAQuantBench (Sep 2026) and CHASE-VLA (2 Oct 2026, 97.3% on pi0.5 at W4A4, self-reported). On forgetting, a 2026 study finds plain sequential LoRA with RL forgets little. GR00T N1.7 post-trains on teleoperated LeRobot-format demos.
## Key primary sources
- How Fast Can I Run My VLA? (VLA-Perf) — Jiang, Clemons, Sankaralingam, Kozyrakis (NVIDIA) — 2026-02-20 — https://arxiv.org/abs/2602.18397 — preprint — analytical latency model; 15 takeaways; code https://github.com/NVlabs/vla-perf
- Fine-Tuning VLAs: Optimizing Speed and Success (OpenVLA-OFT) — Kim, Finn, Liang — 2025-02 (day unconfirmed) — https://arxiv.org/abs/2502.19645 — preprint — LIBERO 76.5% to 97.1%, 26x throughput
- VLAQuantBench — 2026-09-21 — https://arxiv.org/abs/2609.25376 — preprint — closed-loop PTQ benchmark; layer choice decides success
- CHASE-VLA — 2026-10-02 — https://arxiv.org/abs/2610.02666 — preprint — W4A4 on pi0.5; newest quantisation result
- QuantVLA — 2026-02-23 — https://arxiv.org/abs/2602.20309 — preprint — first PTQ with diffusion action head
- Simple Recipe Works: VLAs are Natural Continual Learners with RL — Hu, ..., Stone, Martin-Martin — 2026-03-12 — https://arxiv.org/abs/2603.11653 — preprint — LoRA, little forgetting
- Knowledge Insulating VLA Models — Driess et al. — 2025-05-29 — https://arxiv.org/abs/2505.23705 — preprint — trains faster, protects knowledge during fine-tuning
- GR00T N1 (30/100/300 demos per task) — NVIDIA — https://arxiv.org/pdf/2503.14734 — preprint — demo-count evidence; N1.7 repo https://github.com/NVIDIA/Isaac-GR00T (company)
- ActQuant — https://arxiv.org/abs/2605.24011 — preprint — sub-4-bit; date unconfirmed
- vla.cpp runtime — https://arxiv.org/pdf/2606.08094 — preprint — packaging; date unconfirmed
## Suggested sections
SFT recipes (OFT, pi, GR00T); how many demos; new embodiments; LoRA; forgetting; distillation and quantisation; latency budgets (VLA-Perf); packaging runtimes.
## Surprises and controversies
Quantisation is brittle: 4-bit pi0.5 swung from 7.0% to 70.5% by which layers were protected (VLAQuantBench). Demo-count advice online is mostly vendor blogs; use papers. Distillation sources not yet found; pi0.5 fine-tuning primary source not yet located.
