# ch32 scan · Mid-training: steering a general model toward the physical world (scanned 2026-10-06)
## What is new since 2025
Mid-training is now named and measured. EmbodiedMidtrain (Apr 2026) selects VLM data close to robot data with a small proximity classifier, and reports a 1.1B mid-trained model competitive with VLAs on 3-8x larger backbones. DM0 (Feb 2026) writes mid-training into a three-stage recipe and blocks action-expert gradients from the VLM. Embodied reasoning models keep moving: RoboBrain 2.5 (Jan 2026, depth-aware 3D grounding, dense progress estimation), Gemini Robotics-ER 2 preview (July 2026; ER 1.6 being retired). Memory for VLAs has matured (MemoryVLA, MEM). A counter-voice, VLM4VLA, finds VLM general ability predicts VLA success poorly.
## Key primary sources
- EmbodiedMidtrain: Bridging the Gap between VLMs and VLAs via Mid-training — Du, Guo, Ye, Ren, Xiong — 2026-04-21 — https://arxiv.org/abs/2604.20012 — preprint — core mid-training evidence, proximity-based mixture curation
- DM0: An Embodied-Native VLA Model towards Physical AI — En Yu et al. — 2026-02-16 — https://arxiv.org/abs/2602.14974 — preprint — pretrain/mid/post recipe; insulated action expert
- Knowledge Insulating VLA Models — Driess et al., Physical Intelligence — 2025-05-29 — https://arxiv.org/abs/2505.23705 — preprint (NeurIPS 2025 spotlight per OpenReview listing) — original insulation method
- VLM4VLA: Revisiting VLMs in VLA Models — Zhang et al. — 2026-01-06 — https://arxiv.org/abs/2601.03309 — preprint — independent, sceptical: VLM skill poorly predicts VLA
- RoboBrain 2.5: Depth in Sight, Time in Mind — BAAI — 2026-01-20 — https://arxiv.org/abs/2601.14352 — preprint — newest embodied-brain VLM; successor to 2.0 (2507.02029)
- Gemini Robotics-ER API documentation (ER 2 preview, ER 1.6 deprecated) — Google — July 2026 update — https://ai.google.dev/gemini-api/docs/robotics-overview — company-claim — current ER version; ER 1.5 paper is in ch31 scan
- Robotic Control via Embodied Chain-of-Thought Reasoning — Zawalski et al. — 2024-07 (day unconfirmed) — https://arxiv.org/abs/2407.08693 — preprint — ECoT original
- MemoryVLA — Shi et al. — 2025-08-26 — https://arxiv.org/abs/2508.19236 — preprint — memory bank (ICLR 2026); successor MemoryVLA++ 2606.09827 unconfirmed
- MEM: Multi-Scale Embodied Memory for VLAs — Torne, Pertsch et al. — 2026-03-04 — https://arxiv.org/abs/2603.03596 — preprint — video plus text memory, 15-minute tasks
- Cosmos-Reason2 model card — NVIDIA — undated page — https://huggingface.co/nvidia/Cosmos-Reason2-8B — company-claim — 2B/8B/32B; no Reason2 paper found (Reason1: 2503.15558)
## Suggested sections
Why mid-train; embodied reasoning data (RoboBrain, Cosmos-Reason, ER); proximity-based mixtures; embodied CoT; insulation and co-training; memory; evidence and its limits.
## Surprises and controversies
VLM4VLA says better VLM does not mean better VLA; the visual encoder may be the bottleneck. Mid-training evidence is mostly small models on simulated benchmarks (self-reported). Gemini ER versions retire fast; cite dates.
