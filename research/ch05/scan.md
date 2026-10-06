# ch05 scan · Actuators: motors, drives and power electronics (scanned 2026-10-06)

## What is new since 2025
- Boston Dynamics' product Atlas uses actuators supplied by Hyundai Mobis (announced CES 2026): supply-chain-driven design.
- Schaeffler showed a production planetary-gear actuator for humanoids at CES 2026: motor, encoder and controller in one housing, 60-250 N·m.
- Agility's Digit 5 uses proprietary cycloidal leg actuators and a 9-minute charge.
- Figure says Figure 03 actuators run about 2x faster with better torque density than Figure 02.
- Roller-screw knee research is appearing in academic venues (a Springer chapter, "Humanoid Locomotion with Roller Screw-Driven Knee Joints"; date not confirmed).
- Disclosed numbers remain sparse: no maker publishes continuous (thermal) torque.

## Key primary sources
- Proprioceptive actuator design in the MIT Cheetah — Wensing, Wang, Seok, Otten, Lang, Kim — 2017 (IEEE T-RO 33(3)) — https://dl.acm.org/doi/abs/10.1109/TRO.2016.2640183 — peer-reviewed — impact mitigation factor, backdrivability
- Learning agile and dynamic motor skills for legged robots — Hwangbo et al. — 2019 (Sci. Robotics 4(26)) — https://www.science.org/doi/10.1126/scirobotics.aau5872 — peer-reviewed — actuator-network (page returned 403; abstract via search)
- Design principles for a family of direct-drive legged robots — Kenneally, De, Koditschek — 2016-07 (RA-L 1(2)) — https://repository.upenn.edu/ese_papers/705 — peer-reviewed — direct-drive trade-offs
- Atlas spec sheet — Boston Dynamics — 2025-12-23 — https://bostondynamics.com/wp-content/uploads/2026/01/atlas-spec-sheet.pdf — company-claim — rotational joints, ratings
- Hyundai Mobis to supply Atlas actuators — Boston Dynamics — 2026-01 (CES) — https://bostondynamics.com/news/hyundai-mobis-forms-strategic-collaboration-framework-with-boston-dynamics/ — company-claim — date to confirm
- Schaeffler planetary actuator — Schaeffler — 2026-01 — https://www.schaeffler.com/en/media/press-releases/press-releases-detail.jsp?id=88156672 — company-claim — only datasheet-like torque range
- Introducing Figure 03 — Figure AI — 2025-10-09 — https://www.figure.ai/news/introducing-figure-03 — company-claim — actuator speed/torque-density claim
- Agility Digit 5 release — Agility — 2026-09-15 — https://www.agilityrobotics.com/content/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale — company-claim — cycloidal leg actuators

## Suggested sections
Seed list holds. Add "supply chain: who makes the actuator" and "continuous vs peak torque: what spec sheets omit".

## Surprises and controversies
- Tesla's roller-screw/linear-actuator story rests on Gen 2 era material and patents; no Gen 3 primary. Aggregators (humanoid.guide etc.) must not be cited.
- Hydraulics: no new primary seen; Atlas retired hydraulics in 2024 (not re-checked).
- Gap: Unitree motor datasheets, Tesla actuator primaries, thermal derating papers not yet found.
