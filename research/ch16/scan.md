# ch16 scan · The layered robot brain (scanned 2026-10-06)
## What is new since 2025
- Three-layer designs: Helix 02 adds System 0 (1 kHz learned whole-body controller) under System 1 (200 Hz) and System 2 (variable rate).
- Gemini Robotics 2 (2026-07-30) is a family: ER 2 reasoner, a whole-body VLA, and an on-device VLA.
- Real-time chunking (RTC) matured: a training-time variant (Dec 2025) cuts inference overhead.
## Key primary sources
- Helix (original) — Figure AI — 2025-02-20 — https://www.figure.ai/news/helix — company-claim — S2 7-9 Hz, S1 200 Hz, asynchronous
- Introducing Helix 02 — Figure AI — 2026-01-27 — https://www.figure.ai/news/helix-02 — company-claim — S0 1 kHz, S1 200 Hz, S2 variable
- GR00T N1 — NVIDIA — 2025-03-18 — https://arxiv.org/abs/2503.14734 — preprint — dual-system VLM plus diffusion action module
- GR00T N1.6 — NVIDIA GEAR — 2025-12-15 — https://research.nvidia.com/labs/gear/gr00t-n1_6/ — tech-report — latest GR00T; no control rates stated
- Gemini Robotics 1.5 — Gemini Robotics Team — 2025-10-02 — https://arxiv.org/abs/2510.03342 — tech-report — reasoner and VLA split
- Gemini Robotics 2 — Google DeepMind — 2026-07-30 — https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/ — company-claim — ER 2, VLA, On-Device VLA
- Real-Time Execution of Action Chunking Flow Policies — Black, Galliker, Levine — 2025-06-09 — https://arxiv.org/abs/2506.07339 — peer-reviewed (NeurIPS 2025) — freezing and inpainting under latency
- Training-Time Action Conditioning for Efficient RTC — Black et al. — 2025-12-05 — https://arxiv.org/abs/2512.05964 — preprint — removes inference-time inpainting cost
- Asynchronous Inference — Hugging Face LeRobot — undated — https://huggingface.co/docs/lerobot/en/async — tech-report — policy server, robot client, chunk threshold
- ros2_control Controller Manager docs — ros-controls — rolling, 2026 — https://control.ros.org/rolling/doc/ros2_control/controller_manager/doc/userdoc.html — standard — update_rate, SCHED_FIFO, overrun warnings
## Suggested sections
Seed list stands. Add a latency-budget worked example (torque-tool timing) and a layer-by-layer rate table.
## Surprises and controversies
- Gemini Robotics 2 success rates (about 46-76% on Apollo 2) are company-reported.
- Gaps: independent latency measurements; DDS and real-time OS primary sources; safety-layer sources (Gemini Robotics 2 Safety Technical Report is on deepmind-media; not opened).
