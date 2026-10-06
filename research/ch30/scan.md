# ch30 scan · A primer on training stages: pre-, mid- and post-training and RL (scanned 2026-10-06)
## What is new since 2025
- "Mid-training" is now a named LLM stage (two October 2025 surveys) and has crossed into robotics: DM0 (Feb 2026) and EmbodiedMidtrain (Apr 2026) both use it.
- Labs label stages differently. DM0: pre-train, mid-train (adds actions), post-train. π0.5: pre-training, then post-training. Helix 2.5: pre-training on human data only, then task adaptation.
- RL after deployment is now a lab theme (π0.6 "Recap" lead, unconfirmed: pi.website blocked fetch).
## Key primary sources
- Mid-Training of Large Language Models: A Survey — Mo et al. — 2025-10 — https://arxiv.org/abs/2510.06826 — preprint — data, LR schedule, long-context taxonomy
- A Survey on LLM Mid-Training — arXiv 2510.23081 — 2025-10 — https://arxiv.org/abs/2510.23081 — preprint — formal definition of mid-training (authors not opened)
- DM0: An Embodied-Native VLA towards Physical AI — En Yu et al. — 2026-02 — https://arxiv.org/abs/2602.14974 — preprint — three-stage recipe; blocks action gradients to VLM
- EmbodiedMidtrain — Du, Guo, Ye, Ren, Xiong — 2026-04-21 — https://arxiv.org/abs/2604.20012 — preprint — selects VLA-like VLM data for mid-training
- π0.5: a VLA with Open-World Generalization — Physical Intelligence — 2025-04-22 — https://arxiv.org/abs/2504.16054 — preprint — pre-training then post-training co-training recipe
- Gemini Robotics 1.5 — Google DeepMind — 2025-10-02 — https://arxiv.org/abs/2510.03342 — tech-report — Motion Transfer; stage detail not yet read
- GR00T N1.7 blog — NVIDIA — 2026-04-17 — https://huggingface.co/blog/nvidia/gr00t-n1-7 — tech-report — human-video pretraining; thin on stages
- Helix 2.5 — Figure — 2026-09-17 — https://www.figure.ai/news/helix-2-5-zero-shot-30-home-generalization — company-claim — human-data pretraining, then adaptation
## Suggested sections
Follow the seed list; add "Stage names across labs" as a comparison table, and "Where RL fits" using π0.6 Recap (to confirm).
## Surprises and controversies
- No shared definition: "mid-training" means different things in LLMs and robots.
- Helix 2.5 claims pretraining from random initialisation on human data alone, unlike VLM-initialised recipes.
- GR00T N1.x technical report beyond N1 (arXiv 2503.14734) not found; N1.6/N1.7 stages unconfirmed.
