# World-model builders scan (scanned 2026-10-07)

## What is new since 2025
Interactive world models have split into two camps. Closed API products (Odyssey, Decart, Runway, World Labs) disclose capabilities and latency but almost never data, recipe or weights. Open releases (Tencent, Skywork, Ant Group's Robbyant, Alaya Lab, Kairos, SolarWM) publish code and weights, and several describe staged recipes. The staged recipe is now common: bidirectional teacher, then autoregressive adaptation, then distribution-matching distillation (DMD) for real time. Many open models start from Wan or LTX backbones, so they are fine-tunes, not from-scratch builds. Robotics-specific models (AgiBot Genie Envisioner, GigaWorld, Kairos, Runway GWM Robotics, Decart Oasis 3) are described as data engines or policy-evaluation simulators. Independent evaluation has begun (WorldRoamBench, BadWorld).

## Organisations
- Odyssey (London/Menlo Park) — interactive video (closed-loop, action-conditioned) — Introducing Odyssey-1: A Playable World Model — 2025-05-28 — https://odyssey.systems/introducing-odyssey-1 — company-claim — discloses: partial recipe (general pre-train, then post-train on a few densely covered places; $1-2 per user-hour), no weights/code
- Odyssey — same — Odyssey-2 Pro announcement — 2026-01-23 — https://odyssey.systems/the-gpt-2-moment-for-world-models — company-claim — discloses: none (API only)
- Odyssey — same — Introducing Odyssey-2 Max — page says April 21, 2026 but was fetched showing a 5 Oct 2026 publication; date conflict, unresolved — https://odyssey.systems/introducing-odyssey-2-max — company-claim — discloses: 3x size of Pro, several hundred B200s, 10x compute, three stages, VBench 2 and PAI-Bench scores (self-reported); no weights
- Odyssey — multimodal audio-video — Starchild-1 technical report — 2026-05 — https://starchild.odyssey.ml/starchild-1.pdf — tech-report — unconfirmed (PDF not opened; link and causal-distillation-from-Ovi detail come from search and Air Street Press, https://press.airstreet.com/p/odyssey-starchild-1-agora-1)
- World Labs — 3D/persistent worlds — RTFM: A Real-Time Frame Model — 2025-10-16 — https://www.worldlabs.ai/blog/rtfm — company-claim — discloses: architecture (autoregressive diffusion transformer, one H100), no data, no weights
- World Labs — 3D (splats, meshes) — Marble: A Multimodal World Model — 2025-11-12 (per search; page not opened) — https://www.worldlabs.ai/blog/marble-world-model — company-claim — unconfirmed; no paper known
- Decart (with Etched) — interactive game-style — Oasis 500M weights — 2024 — https://huggingface.co/Etched/oasis-500m — tech-report — discloses: weights, inference code, MIT licence; data not stated (release date not on page)
- Decart — driving/robotics simulation — Oasis 3 — 2026-06-10 — https://techcrunch.com/2026/06/10/decarts-new-world-model-can-simulate-hours-of-photorealistic-driving-with-some-caveats/ (primary page https://decart.ai/oasis, undated) — press/company-claim — discloses: none (API, 22 fps, multi-camera)
- Runway — video plus robotics — Introducing Runway GWM-1 — 2025-12-11 — https://runway.com/research/introducing-runway-gwm-1 — company-claim — discloses: none beyond "autoregressive on Gen-4.5"
- Tencent Hunyuan — interactive video (HY-World 1.5/WorldPlay) — HY-World 1.5 tech report and repo — 2025-12-17 — https://github.com/Tencent-Hunyuan/HY-WorldPlay — tech-report — discloses: recipe (pre-, mid-, RL post-training, distillation), weights, training code; data not detailed
- Tencent Hunyuan — 3D (HY-World 2.0) — repo and technical report — 2026-04 — https://github.com/Tencent-Hunyuan/HY-World-2.0 — tech-report — discloses: weights, code (report link not opened; unconfirmed in detail)
- Skywork — interactive game-style — Matrix-Game 3.0 — 2026-04-10 (arXiv; v3 2026-09-29) — https://arxiv.org/abs/2604.08995 — preprint — discloses: data engine (Unreal, AAA games), recipe, weights 5B and 2x14B MoE (Apache 2.0, https://huggingface.co/Skywork/Matrix-Game-3.0), code
- Robbyant (Ant Group) — interactive video — Advancing Open-source World Models (LingBot-World) — 2026-01-28 — https://arxiv.org/abs/2601.20540 — preprint — discloses: weights, code (Apache 2.0); built on Wan2.2; data not described. v2 released 2026-07-09 per search only
- Alaya Lab (Shanda AI Research) — interactive video — AlayaWorld full technical report — 2026-07-20 — https://arxiv.org/abs/2607.18367 — preprint — discloses: recipe, weights, training code, partial data (LTX-2.3 22B base; non-commercial licence), https://github.com/AlayaLab/AlayaWorld
- SolarWM team — open-data video world models — SolarWM — 2026-09-02 — https://arxiv.org/abs/2609.02886 — preprint — discloses: recipe, 1.43M clips, weights 5B-33B, CC BY 4.0
- Kairos team (ACE Robotics/DAXIAO Robotics) — robot world-action model — Kairos — 2026-06-15 — https://arxiv.org/abs/2606.16533 — preprint — discloses: recipe (cross-embodiment curriculum), 4B weights and code (Apache 2.0, https://github.com/kairos-agi/kairos)
- AgiBot — robot world foundation model — Genie Envisioner — 2025-08-07 — https://arxiv.org/abs/2508.05635 — preprint — discloses: recipe, code and models promised (release not checked); successor GE-Act 2.0, 2026-09-04, https://arxiv.org/abs/2609.05588 — 300 to 30,000 hours
- GigaAI — robot data engine (video plus 3D) — GigaWorld-0 — 2025-11-25 — https://arxiv.org/abs/2511.19861 — preprint — discloses: recipe, open code (https://github.com/open-gigaai/giga-world-0)
- Shanghai AI Lab and Fudan — interactive video — Yume-1.5 — 2025-12 — https://arxiv.org/abs/2512.22096 — preprint — discloses: code, 5B weights (Dec 2025, per search)
- University of Geneva/Microsoft — Dreamer-style/diffusion RL — DIAMOND — 2024 — https://arxiv.org/abs/2405.12399 — peer-reviewed (NeurIPS 2024) — discloses: code, weights, CS:GO model
- General Intuition (Medal spin-out) — game-trained action models — no primary publication found — unconfirmed; funding reports conflict.

## Suggested additions to ch36–ch39 and ch50
- ch36: add a "who builds what" table with a disclosure column. Add Odyssey's definition (action-conditioned dynamics model), World Labs RTFM (the "learned renderer" idea) and Kairos (control-relevant state over pixels, echoing Mask World Model).
- ch37: use Matrix-Game 3.0, HY-World 1.5, LingBot-World and AlayaWorld as open worked examples of the teacher-to-DMD pipeline. Add Odyssey's "narrow distribution" trade-off for stability.
- ch38: add rows to the recipe-by-stage table for HY-World 1.5 (RL post-training with released code), Odyssey-2 Max (three stages, 10x compute) and SolarWM (open data).
- ch39: GigaWorld-0, GE-Sim, Runway GWM Robotics and Decart Oasis 3 as data-engine and evaluation uses. Independent checks: WorldRoamBench (https://arxiv.org/abs/2606.31672, 10+ models, none reliable on all axes) and BadWorld (https://arxiv.org/abs/2606.16519, adversarial inputs collapse rollouts).
- ch50: a short "open-source world models" box, and Odyssey/Decart as the non-robotics labs entering robotics. Wayve GAIA-3 (15B, 9 countries, no paper; https://wayve.ai/thinking/gaia-3/) stays a side lesson.

## Surprises and controversies
- Odyssey-2 Max shows a date conflict (April versus October 2026); do not cite a date until resolved.
- "Open" varies: AlayaWorld's weights carry a non-commercial licence; Yume weights and Genie Envisioner releases were staged or promised.
- Open leaders mostly fine-tune Wan or LTX backbones, so credit belongs to the base model.
- Benchmarks (VBench 2, PAI-Bench) are self-reported by the builders; independent benchmarks find big gaps.
- Funding news (General Intuition) conflicts across outlets; leave out of the book.
- Not found: World Labs, Runway, Decart and Odyssey training data; any Odyssey peer-reviewed paper.
