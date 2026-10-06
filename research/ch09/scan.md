# ch09 scan · Compute, power, heat and the network (scanned 2026-10-06)
## What is new since 2025
- Jetson Thor shipped (Aug 2025) and is now the default brain: Agility Digit 5 uses IGX Thor; NVIDIA's June 2026 open reference humanoid (Unitree H2 Plus) uses Thor.
- Battery swap is now a product feature: Atlas (production, CES 2026) and UBTech Walker S2 swap their own packs in ~3 min.
- Figure 03 adds 2 kW inductive charging through the feet.
- Agility Digit 5 trades capacity for speed: 90-minute battery, 9-minute charge (company claim).
- IP ratings are now quoted (Atlas IP67, per secondary reports).
## Key primary sources
- NVIDIA Jetson Thor launch coverage (2,070 FP4 TFLOPS, 128 GB, 130 W, $3,499 kit) — The Robot Report — 2025-08-25 — https://www.therobotreport.com/nvidia-jetson-thor-brings-2k-teraflops-of-ai-compute-to-robots/ — press — specs; swap for NVIDIA's own page at write-up
- NVIDIA Isaac GR00T Reference Humanoid for Academic Research — NVIDIA — 2026 (June; exact day unconfirmed) — https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-NVIDIA-Isaac-GR00T-Reference-Humanoid-Robot-for-Academic-Research/default.aspx — company-claim — Thor-based reference build
- Introducing Figure 03 — Figure AI — 2025-10-09 — https://www.figure.ai/news/introducing-figure-03 — company-claim — 2 kW foot charging, UN38.3 battery; no runtime stated
- Boston Dynamics Unveils New Atlas Robot — Boston Dynamics — 2026-01-05 — https://bostondynamics.com/blog/boston-dynamics-unveils-new-atlas-robot-to-revolutionize-industry/ — company-claim — self-swap, -20 to 40 C; IP67 only secondary
- Agility Unveils Digit 5 — Agility Robotics — 2026-09-15 — https://www.agilityrobotics.com/content/agility-unveils-digit-5-humanoid-robot-built-for-cooperatively-safe-work-at-scale — company-claim — 90-min battery, 9-min charge, IGX Thor
- UBTech Walker S2 autonomous battery swap — CnEVPost — 2025-07-17 — https://cnevpost.com/2025/07/17/ubtech-humanoid-robot-autonomous-battery-swap/ — press — find UBTech's own release
## Suggested sections
Compute budgets; edge vs off-board; runtime vs shift reality; swap vs wireless vs fast charge; sealed-body thermals; networks/offline; IP ratings and the greenhouse/battery-hall cases.
## Surprises and controversies
- Runtime claims differ: 2-4 h typical vs 6+ h in listicles (reject those).
- Swap, fast-charge and wireless charge compete; no neutral comparison exists.
- Gaps: Tesla in-house chips, thermal data, 5G/Wi-Fi evidence, Hexagon AEON, DR02 IP66 (only aggregator seen) are unconfirmed.
