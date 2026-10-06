# ch14 scan · Reinforcement learning from zero (scanned 2026-10-06)
## What is new since 2025
- RL for large models is now mainstream: GRPO (2024) drives DeepSeek-R1, published in Nature in 2025.
- GRPO theory is catching up: a 2026 paper treats its gradient as a U-statistic.
## Key primary sources
- Reinforcement Learning: An Introduction, 2nd ed. — Sutton, Barto — 2018-11-13 (per MIT Press listing) — http://incompleteideas.net/book/the-book-2nd.html — peer-reviewed (book) — the foundation text, free online
- Proximal Policy Optimization Algorithms — Schulman et al. — 2017-07-20 — https://arxiv.org/abs/1707.06347 — preprint — PPO original
- Soft Actor-Critic — Haarnoja, Zhou, Abbeel, Levine — 2018-01-04 — https://arxiv.org/abs/1801.01290 — preprint — off-policy, maximum-entropy original
- Conservative Q-Learning — Kumar et al. — 2020-06-08 — https://arxiv.org/abs/2006.04779 — preprint — offline RL, conservative values
- Offline RL with Implicit Q-Learning — Kostrikov, Nair, Levine — 2021-10-12 — https://arxiv.org/abs/2110.06169 — preprint — offline RL without querying unseen actions
- DreamerV3 (Mastering Diverse Domains through World Models) — Hafner et al. — 2023-01-10 — https://arxiv.org/abs/2301.04104 — preprint — model-based RL, one setting for many domains
- DeepSeekMath — Shao et al. — 2024-02-05 — https://arxiv.org/abs/2402.03300 — preprint — introduces GRPO
- DeepSeek-R1 — DeepSeek-AI — 2025-01-22 — https://arxiv.org/abs/2501.12948 — peer-reviewed (Nature 2025) — GRPO-style RL incentivises reasoning
- Demystifying GRPO: Policy Gradient is a U-Statistic — Zhou et al. — 2026-03-01 — https://arxiv.org/abs/2603.01162 — preprint — theory of GRPO
## Suggested sections
Seed list stands. Add: verifiable rewards versus learned reward models (links to preferences); RL's role in robot post-training (forward pointer to later chapters).
## Surprises and controversies
- Gap: no confirmed primary source yet for RLHF/DPO/reward hacking; scout in Mode A.
