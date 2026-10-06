# ch22 scan · Capture rigs, calibration and time synchronisation (scanned 2026-10-06)
## What is new since 2025
- Aria Gen 2 (pilot dataset, Oct 2025) reports multi-device sub-millisecond camera sync (search-result claim; trace to Aria Gen 2 docs before use) and a common nanosecond clock.
- Calibration-tolerant policies: CamVLA (Jul 2026) predicts a hand-eye transform itself, to cope with moved cameras and no explicit calibration.
- The core tools are old and stable: Kalibr (2013), OpenCV, PTP (IEEE 1588-2019). Newer work is mostly on policy-side latency handling.
## Key primary sources
- Unified temporal and spatial calibration for multi-sensor systems — Furgale, Rehder, Siegwart — 2013 (IROS; exact date unconfirmed) — http://vigir.missouri.edu/~gdesouza/Research/Conference_CDs/IEEE_IROS_2013/media/files/0240.pdf — peer-reviewed — the Kalibr method
- IEEE 1588-2019 PTP — IEEE — 2020-06-16 — https://standards.ieee.org/ieee/1588/6825/ — standard — sub-microsecond clock sync protocol
- Aria Gen 1 Device Calibration docs — Meta — undated — https://facebookresearch.github.io/projectaria_tools/docs/tech_spec/device_calibration — tech-report — which sensors have intrinsics/extrinsics
- Aria Gen 2 Pilot Dataset — Kong et al. — 2025-10-17 — https://arxiv.org/abs/2510.16134 — preprint — Gen 2 sensor suite
- UMI — Chi et al. — 2024-02-15 — https://arxiv.org/abs/2402.10329 — preprint — latency matching; handheld-gripper calibration (RSS 2024 version: https://www.roboticsproceedings.org/rss20/p045.pdf)
- From Fixed to Free Cameras (CamVLA) — Li et al. — 2026-07-06 — https://arxiv.org/abs/2607.05396 — preprint — hand-eye error tolerance in VLAs
- OpenCV calibration tutorial — https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html — unconfirmed (HTTP 403)
## Suggested sections
Intrinsics and distortion; hand-eye and extrinsics; multi-camera and IMU-camera (Kalibr); clocks (triggers, PTP, drift); latency in policies (UMI); field validation; effect of bad calibration.
## Surprises and controversies
- Few controlled studies isolate calibration or sync error against policy success; mostly indirect evidence. Gap: Kalibr's exact date, Aria sync docs, a direct sync-error ablation.
- Closed-loop policies tolerate small extrinsic error (CamVLA claim), so rigour may matter less than assumed. Verify.
