# ch50 scan · Lab-by-lab teardowns (scanned 2026-10-06)

## What is new since 2025
- Data strategy is now the main axis of difference: human egocentric video (Dyna-2 over 1M hours, Generalist GEN-1 over 500K hours, Figure Index), versus teleoperation and fleet data (Apptronik Robot Park, Tesla Optimus Academy).
- World-action models have reached products: Dyna-2, GR00T N2 (preview), Unitree UnifoLM-WMA-0, AgiBot GE-Sim 2.0, 1X World Model.
- Skild S1 (Aug 2026) is in-context learning from one video. Helix is at 2.5. Generalist has GEN-1.
- OpenAI re-entered robotics (division from 31 May 2026; Altman said a humanoid is coming) and Meta bought ARI (May 2026). Both have almost no technical disclosure yet.
- Boston Dynamics now ships a production Atlas to Hyundai and Google DeepMind. Tesla is converting Fremont lines for Optimus.

## Key primary sources
- Figure — Helix 2.5: Zero-Shot 30-Home Generalization — 2026-09-17 — https://www.figure.ai/news/helix-2-5-zero-shot-30-home-generalization — company-claim — Index human-video pretraining; zero-shot across 30 homes
- Neura Robotics — 4NE1 Datasheet (PDF; not readable by tool) — 2026 (date unconfirmed) — https://neurarobotics.px.media/plk/cE/NEURA_Robotics_4NE1_Datasheet_Web.pdf — company-claim — unconfirmed; specs only. Other Neura claims come from aggregators.
- Dyna Robotics — Dyna-2: A 1-Million-Hour Scaling Law for World-Action Models — 2026-08 (day unconfirmed) — https://www.dyna.co/dyna-2 — company-claim — mixture-of-transformers WAM; 1M hours egocentric video
- Skild AI — Introducing S1: In-Context Learning for Robotics — 2026-08-18 (day from search; page says August) — https://www.skild.ai/blogs/s1 — company-claim — video-prompted tasks; teleop, UMI, sim mix
- Physical Intelligence — π0.7: a Steerable Model with Emergent Capabilities — 2026-04-16 — https://www.pi.website/blog/pi07 — company-claim — context-conditioned generalist; paper at arXiv 2604.15483
- Google DeepMind — Gemini Robotics 2 — 2026-07-30 — https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/ — company-claim — reasoner, whole-body VLA, on-device VLA (from ch16 scan)
- NVIDIA — GR00T N1.7 — 2026-04-17 — https://huggingface.co/blog/nvidia/gr00t-n1-7 — tech-report — open 3B VLA; human-video pretraining (from ch31 scan). GR00T N2 is preview only, release end-2026 (newsroom link unconfirmed).
- Tesla — Q2 2026 Update (SEC 8-K Exhibit 99.1) — 2026-07-22 — https://www.sec.gov/Archives/edgar/data/0001318605/000162828026049213/exhibit991.htm — company-claim — Fremont Optimus lines; "Optimus Academy" data collection
- 1X — 1X World Model — 2025-06-16 — https://www.1x.tech/discover/redwood-ai-world-model — company-claim — video world model used to evaluate policies; no sizes
- Agility Robotics — Training a Whole-Body Control Foundation Model — 2025-08-28 — https://www.agilityrobotics.com/content/training-a-whole-body-control-foundation-model — company-claim — sim RL, LSTM under 1M parameters, zero-shot transfer
- Boston Dynamics with TRI — Large Behavior Models and Atlas Find New Footing — 2025-08-20 (date from press; page not opened) — https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/ — company-claim — single language-conditioned whole-body policy. May 2026 heavy-lift RL post known only via press; primary link not found.
- Apptronik — Robot Park / Apollo 2 press release — 2026-06-30 — https://www.globenewswire.com/news-release/2026/06/30/3319598/0/en/welcome-to-robot-park-where-apptronik-s-apollo-goes-to-work-training-the-next-generation-of-humanoid-robot-intelligence.html — company-claim — data-collection site feeding Gemini Robotics (search snippet; not opened)
- Generalist AI — GEN-1: Scaling Embodied Foundation Models to Mastery — 2026-04-02 — https://generalistai.com/blog/gen-1 — company-claim — over 500K hours wearable data; RL stage
- OpenAI — no primary technical source. Only press on hiring and Altman remarks (Forbes 2026-09-03, page returned 403, unconfirmed).
- Meta — V-JEPA 2 — 2025-06-11 — https://arxiv.org/abs/2506.09985 — preprint — 1M-hour video pretraining; 62 hours of robot data (from ch36 scan). ARI acquisition: Engadget 2026-05-02, https://www.engadget.com/2162606/meta-acquires-assured-robot-intelligence-humanoid-ai/ — press.
- Unitree — UnifoLM-WMA-0 — 2025-09-15 (date from press) — https://huggingface.co/unitreerobotics/UnifoLM-WMA-0-Base — tech-report — open world-model-action; Z1 and G1; data not detailed
- AgiBot — GE-Sim 2.0 — 2026-05-26 — https://arxiv.org/abs/2605.27491 — preprint — 2B video simulator; GO-2 (2026-04-09) via press only
- Galbot — Galbot picks up $153M (Robot Report) — 2025-07-02 — https://www.therobotreport.com/galbot-picks-up-153m-commercialize-g1-semi-humanoid/ — press — synthetic pre-training, real post-training; retail deployments. Primary: GraspVLA paper (not searched).
- UBTech — Thinker: a vision-language foundation model for embodied intelligence — 2026-01 (arXiv 2601.21199) — https://arxiv.org/abs/2601.21199 — preprint — VLM; Walker S2 deployment figures are press only

## Suggested sections
1. Method and evidence grading. 2. One section per lab (OpenAI, Tesla, Meta short). 3. Comparison table. 4. What is unknown.

## Surprises and controversies
- No primary technical disclosure: OpenAI, Meta (humanoid), Neura, Tesla (only investor deck), UBTech (hardware).
- Several GO-2, Atlas 2026 and Apptronik claims reach us only through press.
- Self-reported benchmarks everywhere; no independent replication.
- Gaps: Neura, Galbot, Unitree, UBTech primaries; Dyna exact dates; Skild technical report.
