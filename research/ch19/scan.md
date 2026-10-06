# ch19 scan · Teleoperation: how robot demonstrations are collected (scanned 2026-10-06)

## What is new since 2025
- Whole-body humanoid teleoperation is now a crowded 2026 topic: motion-capture-driven controllers that track running, jumping and fall recovery on a Unitree G1, trained on only hours of mocap data.
- UMI-style handheld grippers have spawned many successors (LiDAR pose, tactile, VR tracking, 100K-episode datasets, a commercial kit). A 2026 survey frames data as a pyramid.
- Handheld devices are now used for human-in-the-loop corrections, linking ch19 to ch20.
- Home teleoperation is now a product (1X NEO "Expert Mode"), with privacy safeguards claimed by the company.
- Public cost and throughput figures exist only in vendor blogs (about $118/hour, 20-40 demos/hour); not usable as primary evidence.

## Key primary sources
- Universal Manipulation Interface — Chi et al. — 2024-02-15 — https://arxiv.org/abs/2402.10329 — preprint — original handheld-gripper foundation
- UMI-3D — arXiv authors — 2026-04-15 — https://arxiv.org/abs/2604.14089 — preprint — LiDAR fixes UMI's pose-tracking weakness
- HIL-UMI — Han et al. — 2026-09-17 — https://arxiv.org/abs/2609.20659 — preprint — handheld corrections for VLA post-training
- FastUMI-100K — arXiv authors — 2025-10 (exact date unconfirmed) — https://arxiv.org/pdf/2510.08022 — preprint — large UMI-style dataset; unconfirmed, not opened
- TeleGate — Li, Tang, Wu — 2026-02-10 — https://arxiv.org/abs/2602.09628 — preprint — whole-body teleoperation, 2.5 h mocap data
- Data Pyramid for Embodied Manipulation: A Survey — Ye et al. — 2026-07-27 — https://arxiv.org/abs/2607.24744 — preprint — organises data sources by scale versus alignment
- NEO Home Robot (Expert Mode) — 1X — undated (unconfirmed) — https://www.1x.tech/neo — company-claim — remote-expert mode and no-go zones
- Teleopit — arXiv authors — unconfirmed — https://arxiv.org/pdf/2608.01834 — preprint — full-embodiment humanoid teleoperation; not opened

## Suggested sections
Keep the seed list; add "handheld successors to UMI", "human-in-the-loop corrections as data" and "home teleoperation and privacy". Merge haptics into VR/exoskeleton. Add a cost-evidence caveat section.

## Surprises and controversies
- HumanoidUMI (arXiv 2606.27239) was withdrawn by its author on 2026-07-07; do not cite.
- Cost and throughput figures come from vendor blogs; Expert Mode autonomy percentages are industry estimates. Both are weak evidence.
- Not yet found: primary sources for Tesla, Figure and AgiBot data factories, ALOHA, GELLO, HumanPlus, OmniH2O, TWIST; Open-TeleVision (leads only).
