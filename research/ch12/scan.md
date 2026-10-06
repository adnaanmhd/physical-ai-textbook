# ch12 scan · Transformers, language models and vision-language models (scanned 2026-10-06)
## What is new since 2025
- Open VLM backbones: Gemma 3 (Mar 2025) and Gemma 4 (Jul 2026; dense plus MoE, thinking mode); Qwen3-VL (Nov 2025; dense 2B-32B and MoE 30B-A3B/235B-A22B, 256K context).
- Robot models use them: pi0.5 builds on PaliGemma (SigLIP + Gemma); Gemini Robotics 1.5 adds "thinking" before acting; NVIDIA's Cosmos-Reason targets embodied reasoning.
- Reasoning via RL: DeepSeek-R1 appeared in Nature (Sept 2025).
- MoE now mainstream; a 2026 survey exists.
## Key primary sources
- Attention Is All You Need — Vaswani et al. — 2017-06-12 — https://arxiv.org/abs/1706.03762 — preprint — transformer original
- Language Models are Few-Shot Learners (GPT-3) — Brown et al. — 2020-05-28 — https://arxiv.org/abs/2005.14165 — preprint — in-context learning at scale
- Training language models to follow instructions with human feedback — Ouyang et al. — 2022-03-04 — https://arxiv.org/abs/2203.02155 — preprint — InstructGPT/RLHF
- Gemma 3 Technical Report — Gemma Team — 2025-03-25 — https://arxiv.org/abs/2503.19786 — tech-report — open multimodal backbone family
- Gemma 4 Technical Report — Gemma Team — 2026-07-02 — https://arxiv.org/abs/2607.02770 — tech-report — newest open VLM, MoE variants
- Qwen3-VL Technical Report — Bai et al. — 2025-11-26 — https://arxiv.org/abs/2511.21631 — tech-report — open VLM, dense and MoE
- DeepSeek-V3 Technical Report — DeepSeek-AI — 2024-12-27 — https://arxiv.org/abs/2412.19437 — tech-report — 671B MoE, 37B active
- DeepSeek-R1 (Nature) — DeepSeek-AI — 2025-09 (day unconfirmed) — https://www.nature.com/articles/s41586-025-09422-z — peer-reviewed — RL-elicited reasoning
- pi0.5 — Physical Intelligence — 2025-04-22 — https://arxiv.org/abs/2504.16054 — preprint — VLM backbone in a robot model
- Gemini Robotics 1.5 — Gemini Robotics Team — 2025-10-02 — https://arxiv.org/abs/2510.03342 — tech-report — reasoning before acting
## Suggested sections
Tokens; attention; blocks; pre-training; instruction tuning and RLHF; VLMs; reasoning and chain of thought; MoE; context and memory; VLMs as robot backbones.
## Surprises and controversies
- Pi0.5 backbone sizes came from secondary pages; verify in the paper.
- Reasoning-model claims rest largely on company reports; need independent evaluation.
- MoE survey 2608.08650 (2026-08-09) not yet opened.
