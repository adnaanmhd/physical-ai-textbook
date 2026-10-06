# Seed outline

This is the approved chapter-level plan. `/plan-book` turns it into the section-level `docs/OUTLINE-DETAILED.md` (gate G1).

**How to read the research targets.** They are leads, not facts. Every name, date and number must be re-verified against primary sources at research time. Always search for newer versions or successors before writing.

**Lifecycle chapters** carry a "People, tools and costs" section.

---

## Front matter
- **Preface (`index.qmd`)**: how to read the book (the five-layer template, evidence tags, running examples, research prompts) and the "current as of" date. Written last.

---

## P0 · Orientation

### ch01 · The lifecycle on one page *(write last)*
- **Purpose:** one map of how an intelligent humanoid goes from parts to a deployed, self-improving worker, and where each step is taught in the book.
- **Seed sections:**
  - the map: body → data → simulation → training → world models → evaluation → deployment → flywheel;
  - the layered brain in one picture;
  - where data comes from;
  - training stages in one picture (policies vs world models);
  - readiness and the deployment loop;
  - the four running examples and the reference humanoid;
  - how to read this book.
- **Running examples:** all four, introduced here.
- **Research targets:** the newest 2026 surveys of robot foundation models, world models and WAMs; overview posts from major labs.
- **Lifecycle:** no.

### ch02 · Why a humanoid?
- **Purpose:** the first-principles case for and against the humanoid form, and when legs, hands, wheels, rails or specialist machines win.
- **Seed sections:**
  - a world built for human bodies;
  - human data as the bootstrap;
  - costs of the form: balance, energy, safety, complexity;
  - wheels, rails and specialist machines;
  - when a general-purpose robot beats a specialist;
  - where the debate stands now.
- **Running examples:**
  - battery hall: wheeled humanoids such as Hexagon AEON at BMW Leipzig;
  - greenhouse: rail trolleys, plus specialist harvesters (e.g., eternal.ag) as the bar to beat;
  - home: stairs and doors.
- **Research targets:** BMW Leipzig AEON pilot; Figure at BMW Spartanburg; eternal.ag Harvester (2026); arguments from labs and critics (2025–26); cost-curve analyses.
- **Lifecycle:** no.

### ch03 · A short history: from programmed arms to robot foundation models
- **Purpose:** the arc that explains why 2023–2026 changed robotics.
- **Seed sections:**
  - industrial robots and teach pendants;
  - model-based control and the DARPA Robotics Challenge;
  - deep RL and sim-to-real (2015–21);
  - the imitation-learning revival (ALOHA, Diffusion Policy);
  - transformers meet robots (RT-1, RT-2);
  - cross-embodiment data (Open X-Embodiment);
  - flow-matching VLAs and dual-system humanoid brains;
  - world models and WAMs (2024–26);
  - the first commercial deployments.
- **Research targets:** original papers and dates for each milestone.
- **Lifecycle:** no.

---

## P1 · The body

### ch04 · Anatomy, degrees of freedom and the reference humanoid
- **Purpose:** what a humanoid is made of, how the body's design constrains learning, and the definition of the reference humanoid used throughout the book.
- **Seed sections:**
  - links, joints and degrees of freedom;
  - kinematic chains: legs, torso, arms, neck, hands;
  - workspace, reach and payload;
  - mass, height and centre of mass;
  - designing for manufacture and repair;
  - the reference humanoid, as a spec table derived from current leading robots and dated;
  - variants: wheeled base; sealed, heat-tolerant farm version.
- **Running examples:** reaching into dishwasher racks and high vines; payloads for crates and battery parts.
- **Research targets (verify current specs):** Figure 03, Tesla Optimus (current generation), Boston Dynamics electric Atlas (production version), Agility Digit, Apptronik Apollo, 1X NEO, Unitree G1 and the current H-series, UBTech Walker S2, AgiBot, Galbot, Neura 4NE1, Hexagon AEON.
- **Lifecycle:** yes (who designs bodies; public component and BOM cost estimates).

### ch05 · Actuators: motors, drives and power electronics
- **Purpose:** how a joint is made to move, and why actuator choices shape control, learning and sim-to-real.
- **Seed sections:**
  - electric motors from zero (BLDC/PMSM, torque constant, losses);
  - motor drivers, inverters, field-oriented control;
  - the current-torque inner loop;
  - torque density and thermal limits;
  - hydraulics and why most humanoids are now electric;
  - rotary vs linear actuators;
  - actuator models for simulation (friction, saturation, delay);
  - wear and failure.
- **Research targets:** disclosed actuator designs (Tesla rotary and linear with roller screws, Unitree, Boston Dynamics electric Atlas, Figure); actuator-network papers; thermal derating.
- **Lifecycle:** yes.

### ch06 · Transmissions, joints and sensing the joint
- **Purpose:** gears, screws and compliance between motor and limb, and how a joint knows where it is and how hard it pushes.
- **Seed sections:**
  - why gearing;
  - harmonic, planetary and cycloidal drives;
  - ball and planetary roller screws;
  - quasi-direct drive and backdrivability;
  - series-elastic and variable-stiffness actuators;
  - backlash, friction, transparency;
  - encoders (absolute, incremental, dual) and joint torque sensing;
  - tendons and cable drives.
- **Research targets:** quasi-direct drive (MIT Cheetah line); series elastic actuators (Pratt & Williamson 1995); roller-screw humanoid joints; tendon-driven designs (1X NEO).
- **Lifecycle:** yes.

### ch07 · Hands and end-effectors
- **Purpose:** the hand as the hardest part of the body and the data bottleneck.
- **Seed sections:**
  - grippers vs dexterous hands;
  - degrees of freedom and actuation (direct, tendon, linkage);
  - fingertip and palm sensing, palm cameras;
  - strength vs delicacy;
  - durability and repair;
  - matching human demonstrations;
  - tool use (powered tools, knives, cutters).
- **Running examples:** knife and wine glass (home); torque tool and connectors (battery); cutters and delicate trusses (greenhouse).
- **Research targets:** Figure 03 hands (tactile fingertips, palm cameras) and the F.04 hand preview (October 2026); the current Tesla Optimus hand; Shadow Hand; Psyonic Ability Hand; Inspire hands; Sanctuary's hydraulic hands; tactile sensor technologies.
- **Lifecycle:** yes.

### ch08 · The senses: cameras, depth, inertial, force, touch and sound
- **Purpose:** every sensor stream, what it measures, and what each adds to learning.
- **Seed sections:**
  - cameras: shutter, HDR, field of view; head, wrist and palm placement;
  - depth: stereo, time of flight, structured light;
  - LiDAR;
  - IMUs;
  - proprioception;
  - force/torque sensors;
  - tactile skins (optical, capacitive, magnetic);
  - microphones;
  - sensors in sun, steam and dust.
- **Running examples:** steam and glare (kitchen); shiny battery parts; sunlight and leaf occlusion (greenhouse).
- **Research targets:** published sensor suites of current humanoids; GelSight, DIGIT and Digit 360 (Meta); magnetic and capacitive skins; tactile datasets.
- **Lifecycle:** yes.

### ch09 · Compute, power, heat and the network
- **Purpose:** the onboard computer, battery and thermal envelope, and how they limit models.
- **Seed sections:**
  - onboard compute and inference budgets;
  - edge and off-board inference;
  - batteries, runtime, swapping, wireless charging;
  - power distribution;
  - thermal management in sealed bodies;
  - networks (Wi-Fi, 5G, offline operation);
  - ingress protection (IP ratings) for wet and dusty sites.
- **Research targets:** NVIDIA Jetson Thor (2025); Tesla in-house chips; Figure 03 wireless charging; battery-swap designs (UBTech Walker S2, Hexagon AEON); published runtime claims; IP ratings.
- **Lifecycle:** yes.

### ch10 · Safety hardware, reliability and maintenance
- **Purpose:** designing bodies that fail safely and keep working.
- **Seed sections:**
  - emergency stop, safe torque off, brakes;
  - torque and speed limiting, collision detection;
  - falling safely;
  - reliability and MTBF;
  - lessons from deployments (e.g., the forearm failure point Figure reported from BMW);
  - maintenance, spares and field repair;
  - soft covers;
  - duty cycles and lifetime.
- **Research targets:** Figure's BMW deployment write-up (November 2025); Boston Dynamics production Atlas design notes; safety-rated controllers; any published uptime data.
- **Lifecycle:** yes.

---

## P2 · Foundations from zero

### ch11 · How machines learn: neural networks from scratch
- **Seed sections:**
  - learning as fitting a function;
  - neurons and layers;
  - loss functions;
  - gradient descent and backpropagation;
  - optimisers;
  - overfitting, regularisation, data splits;
  - embeddings;
  - vision encoders (CNNs, ViT, self-supervised encoders such as DINOv2/v3, SigLIP);
  - scaling laws.
- **Research targets:** original papers; current vision encoders used in robot models.
- **Lifecycle:** no.

### ch12 · Transformers, language models and vision-language models
- **Seed sections:**
  - tokens and embeddings;
  - attention;
  - transformer blocks;
  - next-token pre-training;
  - fine-tuning, instruction tuning, RLHF;
  - vision-language models;
  - reasoning models and chain of thought;
  - mixture-of-experts;
  - context and memory.
- **Research targets:** Vaswani 2017; GPT-3; InstructGPT; current open VLMs used as robot backbones (PaliGemma/Gemma, Qwen-VL family); reasoning-model surveys.
- **Lifecycle:** no.

### ch13 · Generative models: autoencoders, diffusion, flow matching and autoregression
- **Seed sections:**
  - autoencoders and VAEs;
  - tokenisers for images, video and actions;
  - diffusion;
  - flow matching and rectified flow;
  - diffusion transformers;
  - autoregressive generation;
  - distillation and consistency models for speed;
  - generating action trajectories (Diffusion Policy, action chunking).
- **Research targets:** DDPM (Ho 2020); score-based models (Song 2021); flow matching (Lipman 2023); DiT (Peebles & Xie 2023); Diffusion Policy (Chi 2023); ACT (Zhao 2023); consistency models.
- **Lifecycle:** no.

### ch14 · Reinforcement learning from zero
- **Seed sections:**
  - MDPs: states, actions, rewards;
  - returns and discounting;
  - value and Q-functions;
  - policy gradients and PPO;
  - off-policy RL (SAC);
  - model-based RL;
  - offline RL;
  - exploration;
  - reward design and reward hacking;
  - learning from preferences;
  - RL for large models (GRPO and relatives).
- **Research targets:** Sutton & Barto; PPO (2017); SAC (2018); IQL/CQL; GRPO (2024); DreamerV3.
- **Lifecycle:** no.

### ch15 · Kinematics, dynamics and control
- **Seed sections:**
  - frames and transforms;
  - forward and inverse kinematics;
  - Jacobians;
  - dynamics and contact;
  - PD/PID and impedance control;
  - balance (centre of mass, ZMP, centroidal dynamics);
  - model predictive control;
  - whole-body control as optimisation;
  - where learning replaces or wraps classical control.
- **Research targets:** Lynch & Park, *Modern Robotics*; humanoid MPC and whole-body control papers.
- **Lifecycle:** no.

---

## P3 · The software stack

### ch16 · The layered robot brain: loops, clock rates and latency
- **Purpose:** how motor loops, whole-body controllers, visuomotor policies and reasoners fit together and run on time.
- **Seed sections:**
  - why layers;
  - motor and joint loops (kHz);
  - the whole-body controller;
  - the visuomotor policy and action chunking;
  - the reasoner and planner;
  - fast-slow designs ("System 1/2", "System 0/1/2");
  - latency budgets and asynchronous inference;
  - safety layer and fallbacks;
  - middleware (ROS 2, real-time OS, DDS) and logging;
  - on-robot vs off-board inference.
- **Running examples:** dinner (a plan days ahead vs sub-second control); battery (torque-tool timing).
- **Research targets:** Figure Helix (2025) and Helix 02 (2026); the NVIDIA GR00T N1 architecture; Gemini Robotics 1.5 (reasoner and VLA split); real-time action chunking (Physical Intelligence 2025); LeRobot asynchronous inference; ROS 2 control.
- **Lifecycle:** yes.

---

## P4 · Data

### ch17 · Why data is the bottleneck
- **Seed sections:**
  - no internet of actions;
  - the data pyramid (web → human video → teleoperation → robot autonomy);
  - scaling evidence and its limits;
  - diversity vs volume;
  - cost per hour by source;
  - the 2025–26 data race and claimed volumes.
- **Research targets:** robot data-scaling studies (e.g., data scaling laws in imitation learning, 2024); Generalist GEN-0 scaling claims; Figure's human-behaviour dataset ("Index") behind Helix 2.5; reports of labs shifting to human video; Sunday Robotics ACT-1; AgiBot World; DROID; Open X-Embodiment.
- **Lifecycle:** yes.

### ch18 · Learning from people: web video, egocentric video and motion capture
- **Seed sections:**
  - web video and its missing actions;
  - egocentric capture devices and datasets;
  - exocentric and multi-view capture;
  - hand pose, gloves and wearable grippers;
  - full-body motion capture;
  - narration and language;
  - extracting actions (latent actions, inverse dynamics, hand pose to robot);
  - limits: the embodiment gap and missing force.
- **Running examples:** cooking video is abundant; battery-station video is scarce; greenhouse video is seasonal.
- **Research targets:** Ego4D, Ego-Exo4D, EPIC-KITCHENS, EgoDex (2025), Project Aria and Aria Gen 2, HOT3D, AMASS; latent action models (Genie, LAPA); EgoMimic; Being-H0.5 and H0.7; DexUMI; Sunday's capture gloves; 1X world-model data mix.
- **Lifecycle:** yes.

### ch19 · Teleoperation: how robot demonstrations are collected
- **Seed sections:**
  - what a demonstration is;
  - leader-follower rigs;
  - VR/AR teleoperation;
  - exoskeletons and mocap suits for whole-body teleoperation;
  - handheld grippers (UMI);
  - haptics;
  - operators: training, fatigue, throughput, cost;
  - quality: consistency, recoveries, failures;
  - remote expert modes as data.
- **Research targets:** ALOHA and Mobile ALOHA; GELLO; UMI; HumanPlus; OmniH2O; TWIST; Open-TeleVision; data factories (AgiBot, Tesla, Figure); 1X Expert mode.
- **Lifecycle:** yes.

### ch20 · Synthetic, autonomous and deployment data
- **Seed sections:**
  - simulation data;
  - data multiplication;
  - generated video and neural trajectories;
  - autonomous rollouts;
  - human interventions and corrections;
  - fleet logs;
  - automatic success and failure labels;
  - mixing with human data.
- **Research targets:** MimicGen, DexMimicGen, SkillMimicGen; DreamGen (2025); Cosmos-Transfer; π*0.6 and Recap (learning from deployment); HG-DAgger.
- **Lifecycle:** yes.

### ch21 · Modalities and the data dictionary
- **Seed sections:**
  - observations (images, depth, proprioception, force/torque, tactile, audio);
  - actions and action spaces (joint, end-effector, deltas, chunks, hands, base);
  - language (instructions, narration, subtasks, reasoning traces);
  - metadata;
  - rates and sizes;
  - normalisation;
  - the data dictionary, which feeds Appendix A.
- **Research targets:** LeRobot dataset spec; RLDS; DROID and Open X-Embodiment field lists; GR00T data formats; published dataset cards.
- **Lifecycle:** yes.

### ch22 · Capture rigs, calibration and time synchronisation
- **Seed sections:**
  - intrinsics and distortion;
  - extrinsics and hand-eye calibration;
  - multi-camera rigs;
  - IMU-camera calibration;
  - robot kinematic calibration;
  - clocks (hardware triggers, PTP, drift);
  - field validation;
  - what bad calibration does to learning.
- **Research targets:** Kalibr; OpenCV calibration; IEEE 1588 PTP; Aria calibration documentation; UMI calibration; studies on how calibration error affects policies.
- **Lifecycle:** yes.

### ch23 · Formats, storage and data pipelines
- **Seed sections:**
  - raw logging (ROS bags, MCAP);
  - training formats (RLDS, LeRobotDataset, HDF5, Zarr, WebDataset);
  - video compression and learning;
  - indexing, search and curation;
  - streaming loaders;
  - storage tiers and costs;
  - lineage and versioning.
- **Research targets:** the MCAP spec; the current LeRobot dataset format version; RLDS; Zarr; published lab data-engine descriptions.
- **Lifecycle:** yes.

### ch24 · Quality, annotation, privacy and consent
- **Seed sections:**
  - quality checks (sync, calibration, coverage, success, idle time);
  - filtering and deduplication;
  - segmentation and subtask labels;
  - language annotation (human and VLM auto-labelling);
  - success and reward labels;
  - annotation tooling and QA;
  - privacy (faces, homes, PII);
  - consent and contributor agreements;
  - licensing and data rights;
  - regulation (GDPR, India's DPDP Act, EU AI Act data governance).
- **Research targets:** VLM auto-labelling studies (2025–26); data quality vs quantity in robot learning; current privacy rules.
- **Lifecycle:** yes.

### ch25 · Bridging bodies: retargeting and cross-embodiment action spaces
- **Seed sections:**
  - the embodiment gap;
  - kinematic retargeting (body and hands);
  - physics-based tracking;
  - latent and unified action spaces;
  - embodiment tokens and prompts;
  - cross-embodiment results.
- **Research targets:** GMR (general motion retargeting); PHC; OmniH2O; Open X-Embodiment; X-VLA; UniVLA; latent action models; Being-H0.5.
- **Lifecycle:** yes.

### ch26 · Designing datasets and data mixtures
- **Seed sections:**
  - coverage, diversity and the long tail;
  - task taxonomies;
  - mixture weights and curricula;
  - co-training (web + robot, sim + real);
  - ablations and data attribution;
  - data budgets and ROI;
  - dataset documentation.
- **Research targets:** Open X-Embodiment mixture lessons; π0.5 co-training; the GR00T data pyramid; Re-Mix (2024); DataMIL (2025).
- **Lifecycle:** yes.

---

## P5 · Simulation

### ch27 · Simulators and RL gyms
- **Purpose:** what a simulator and an RL environment are, and the tools in use today.
- **Seed sections:**
  - anatomy of an environment (state, physics step, observation, reward, reset, termination; the Gym API);
  - physics engines (rigid, contact, soft, cloth, fluids);
  - rendering and simulated sensors;
  - assets and scenes (USD, URDF/MJCF, procedural and generated scenes);
  - GPU-parallel simulation;
  - task suites and benchmarks;
  - digital twins and real-to-sim (e.g., Gaussian splatting);
  - LLM-generated tasks and scenes;
  - a gym for each running example, and where the tools break (liquids, food, cloth, plants, connector clicks).
- **Research targets:** Isaac Lab; MuJoCo, MJX, MuJoCo Playground and MuJoCo Warp; Newton; Genesis; ManiSkill3; BEHAVIOR-1K; RoboCasa; LIBERO; RoboTwin 2.0; RoboVerse; Agri-Sim (2026) for greenhouses.
- **Lifecycle:** yes.

### ch28 · Training in simulation
- **Seed sections:**
  - massively parallel RL for locomotion;
  - curricula;
  - teacher–student (privileged) training;
  - motion imitation and tracking;
  - whole-body controllers as foundation models;
  - dexterous manipulation in simulation;
  - synthetic demonstrations and data multiplication;
  - teleoperation in simulation;
  - sim+real co-training;
  - simulation for evaluation (preview of ch43);
  - compute costs.
- **Research targets:** Rudin et al. 2022 (learning to walk in minutes); DeepMimic; PHC; HOVER; OmniH2O; ExBody2; ASAP (2025); BeyondMimic; GMT; sim-to-real dexterity on humanoids (Lin et al. 2025); DextrAH; legged_gym; Unitree RL Gym; sim+real co-training papers.
- **Lifecycle:** yes.

### ch29 · The sim-to-real gap *(pilot chapter)*
- **Purpose:** why skills learned in simulation stumble on hardware, how the gap is measured and closed, and the reverse problem of trusting simulated or world-model evaluations.
- **Seed sections:**
  - what the gap is (dynamics, actuation, sensing, latency, environment);
  - measuring it (paired tests, sim-real correlation, identification error);
  - closing it I: domain randomisation and curricula;
  - closing it II: system identification, actuator networks, delay modelling;
  - closing it III: adaptation (teacher–student, history encoders), residual policies, real-world fine-tuning;
  - closing it IV: real-to-sim digital twins and sim+real co-training;
  - the reverse gap: when simulated or world-model evaluations mislead;
  - the gap for each running example.
- **Running examples:**
  - dinner: liquids and food;
  - reset: glass and a wet sponge;
  - battery: connector clicks and torque-tool reaction;
  - greenhouse: plant deformation and lighting.
- **Research targets:** Tobin et al. 2017; OpenAI 2019 (automatic domain randomisation); Hwangbo et al. 2019 (actuator networks); RMA (2021); ASAP (2025); Lin et al. 2025; SimplerEnv (sim-real correlation); Gaussian-splat real-to-sim work (2024–26); 2026 surveys.
- **Lifecycle:** yes.

---

## P6 · Training robot policies

### ch30 · A primer on training stages: pre-, mid- and post-training and RL
- **Seed sections:**
  - pre-training (a broad prior);
  - mid-training (domain shift before task work);
  - post-training (supervised fine-tuning, adaptation, distillation);
  - RL (learning from outcomes);
  - why stage order matters (forgetting, interference);
  - compute and data budgets by stage;
  - how different labs label their stages.
- **Research targets:** LLM mid-training literature; stage descriptions in π0.5, GR00T N1.x, Gemini Robotics 1.5, DM0 and EmbodiedMidtrain.
- **Lifecycle:** yes.

### ch31 · Pre-training the robot brain
- **Seed sections:**
  - starting from a VLM;
  - cross-embodiment robot data;
  - human-video pre-training;
  - action representations (tokens/FAST, continuous heads, flow matching, chunks);
  - architectures (single model vs dual system, action experts, mixture-of-transformers);
  - objectives;
  - scaling evidence;
  - compute;
  - open vs closed models.
- **Research targets:** RT-2; OpenVLA; Octo; the π0 family through π0.7; GR00T N1.x; Gemini Robotics 1.5; the Helix family; the TRI Large Behavior Model study; SmolVLA; X-VLA; GEN-0; DYNA-1; Skild Brain; AgiBot GO-1; Galbot models; Being-H0.5.
- **Lifecycle:** yes.

### ch32 · Mid-training: steering a general model toward the physical world
- **Seed sections:**
  - why mid-train;
  - embodied reasoning data (spatial QA, pointing, trajectories, affordances);
  - embodied chain of thought and planning traces;
  - adding actions without erasing knowledge (knowledge insulation, co-training);
  - memory and long context;
  - curating mixtures by proximity to the target domain;
  - evidence for the gains.
- **Research targets:** EmbodiedMidtrain (2026); DM0 (2026); Gemini Robotics-ER 1.5; Cosmos-Reason; RoboBrain 2.x; knowledge insulation (Physical Intelligence 2025); embodied chain-of-thought (ECoT); MemoryVLA.
- **Lifecycle:** yes.

### ch33 · Post-training: fine-tuning, adaptation and making models fast
- **Seed sections:**
  - supervised fine-tuning on task demonstrations;
  - how many demonstrations;
  - adapting to a new body;
  - parameter-efficient fine-tuning;
  - quality over quantity;
  - avoiding forgetting;
  - distillation and quantisation;
  - real-time inference;
  - packaging for the robot.
- **Research targets:** OpenVLA-OFT; π0.5 fine-tuning results; GR00T post-training; LoRA for VLAs; VLA-perf (2026); quantisation studies.
- **Lifecycle:** yes.

### ch34 · Reinforcement learning for robot policies
- **Seed sections:**
  - why imitation plateaus;
  - real-world RL;
  - human-in-the-loop corrections;
  - RL fine-tuning of VLAs (on-policy, offline, advantage-conditioned);
  - rewards (hand-designed, learned reward models, VLM judges, success detectors);
  - RL in simulation for VLAs;
  - RL inside world models (preview of ch39);
  - safe exploration and resets;
  - results and limits.
- **Research targets:** SERL and HIL-SERL; ConRFT; π*0.6 and Recap; SimpleVLA-RL; VLA-RL; RL4VLA; πRL and RLinf; RISE (2026); reward-model papers (2025–26); Dyna's reward-model claims.
- **Lifecycle:** yes.

### ch35 · Connecting brain and body: from policy outputs to whole-body motion
- **Seed sections:**
  - action interfaces (joint targets, end-effector targets, latent commands);
  - the whole-body controller as "cerebellum";
  - loco-manipulation;
  - learned vs model-based whole-body control;
  - joint vs separate training;
  - failure modes (falls, self-collision, drift).
- **Research targets:** Helix 02 "System 0"; GR00T whole-body control; HOVER; AMO; TWIST; the TRI/Boston Dynamics whole-body behaviour model on Atlas; Gemini Robotics on humanoids.
- **Lifecycle:** yes.

---

## P7 · World models

### ch36 · What a world model is
- **Seed sections:**
  - prediction as understanding;
  - definitions across fields;
  - taxonomy by representation (pixel/video, latent/JEPA, 3D/4D scenes, physics-informed hybrids, model-based RL);
  - passive vs interactive (action-conditioned);
  - uses: data, evaluation, RL environment, planning, verification, policies;
  - lessons from self-driving world models;
  - world models vs simulators.
- **Research targets:** Ha & Schmidhuber 2018; the Dreamer line; V-JEPA 2; Genie 2 and 3; the Cosmos family including Cosmos 3; 1X world model; World Labs; Wayve GAIA-2; published world-model work at Tesla and Waymo (verify); 2026 surveys.
- **Lifecycle:** no.

### ch37 · Inside a video world model
- **Seed sections:**
  - compressing video (VAEs, tokenisers, latents);
  - diffusion and flow-matching transformers for video;
  - autoregressive and streaming generation (diffusion forcing, self-forcing);
  - conditioning on actions, camera motion and language;
  - memory and long-horizon consistency;
  - multi-view and 3D consistency;
  - real time (distillation, caching);
  - measuring quality: fidelity vs physics vs controllability.
- **Research targets:** Wan 2.x; HunyuanVideo; Cosmos-Predict; Genie 3; diffusion forcing; self-forcing; causal video models; Mask World Model (2026).
- **Lifecycle:** no.

### ch38 · Training world models: pre-, mid- and post-training and RL
- **Seed sections:**
  - pre-training on internet video;
  - mid-training on physics- and embodiment-heavy data (egocentric, robot, simulation);
  - adding action and camera conditioning;
  - post-training for a target robot (controllability, consistency, speed);
  - RL post-training (physics and instruction rewards, GRPO-style methods for video);
  - RL inside world models;
  - data curation;
  - compute and cost;
  - recipes mapped (Cosmos, Genie, V-JEPA 2, 1X, DreamZero).
- **Research targets:** Cosmos technical reports (2025–26); V-JEPA 2 and its action-conditioned variant; Genie 3; 1X world model; Flow-GRPO; DanceGRPO; physics-aware RL for video (2025–26); World-VLA-Loop.
- **Lifecycle:** yes.

### ch39 · Using world models: data, evaluation, RL and planning
- **Seed sections:**
  - generating training data;
  - policy evaluation in imagination and its correlation with real results;
  - RL inside world models;
  - planning (MPC, search);
  - test-time verification and failure prediction;
  - uncertainty;
  - evidence on reliability.
- **Research targets:** DreamGen; WorldEval and dWorldEval; Interactive World Simulator (2026); Ctrl-World; 1X evaluation; video-model-based policy evaluation at Google DeepMind (verify); V-JEPA 2-AC planning; CheckVLA; self-correcting VLA; RISE; world-model failure detection (2026).
- **Lifecycle:** yes.

---

## P8 · World action models and convergence

### ch40 · World action models (WAMs)
- **Seed sections:**
  - from video prediction to action prediction;
  - the definition (DreamZero, 2026) and its scope;
  - architectures (joint denoising, action-as-image, mixture-of-transformers, latent WAMs, video then inverse dynamics);
  - training recipes;
  - inference speed and control rates;
  - strengths (a physics prior, generalisation, imagining outcomes);
  - a comparison table of current systems.
- **Research targets:** GR-1; GR-2; UniPi; UVA; UWM; Genie Envisioner; WorldVLA; Cosmos Policy; DreamZero; LingBot-VA; GigaWorld-Policy; Fast-WAM; ProWAM (2026); FLUX 3 Action (Black Forest Labs, 2026); Cosmos 3 policy variants; Being-H0.7; Motus; OA-WAM; Rhoda AI DVA; 1X world-model policy; WAM surveys (May and September 2026); NVIDIA WAM blog posts (July and August 2026).
- **Lifecycle:** yes.

### ch41 · Where world models and WAMs fail, and what data fixes it
- **Purpose:** a failure taxonomy traced to root causes, with special attention to training data (volume, modality, richness, diversity, labels), plus remedies and how to measure progress.
- **Seed sections:**
  - **failure taxonomy:** physics violations; object permanence; contact and force blindness; deformables, liquids and plants; long-horizon drift; action non-compliance (the prediction ignores the action); hallucinated success and optimistic evaluation; embodiment mismatch; camera-motion confounds in egocentric video; rare events; multi-view inconsistency; latency;
  - **diagnosis:** benchmarks and probes;
  - **root causes in data:**
    - volume;
    - diversity;
    - modality gaps (no force, touch or audio in video; no proprioception; no depth);
    - richness (action labels, narration, subtask boundaries, success/failure, counterfactuals, recoveries);
    - embodiment (human vs robot; egocentric vs exocentric);
    - quality (calibration, sync, compression);
  - **remedies:**
    - data: what to collect, how much, which modalities;
    - training: action conditioning, 3D and physics losses, RL with physics rewards;
    - architecture: memory, uncertainty;
    - system: hybrids with simulators, guardrails;
  - measuring progress;
  - what each running example needs.
- **Research targets:** Physics-IQ (2025); VideoPhy and VideoPhy-2; PhyGenBench; WorldModelBench; WorldScore (verify); "How far is video generation from world model" (2024); the WAM-vs-VLA robustness study (March 2026); Mask World Model; FAWAM (force-aware WAMs, 2026); DreamWAM; OA-WAM; World Action Verifier; multimodal egocentric datasets with force or tactile streams (verify).
- **Lifecycle:** yes.

### ch42 · How WAMs and VLAs converge on physical AI
- **Seed sections:**
  - two bets: a language-first prior vs a physics-first prior;
  - **convergence routes:**
    - VLAs that predict the future (VLA-JEPA, DreamVLA, UniVLA);
    - WAMs that gain language and reasoning (world-language-action models, Cosmos 3);
    - layered hybrids (π0.7 subgoal images, τ0-VLA test-time compute);
    - world models wrapped around policies;
    - natively unified "embodied-native" models (DM0, Kairos);
  - head-to-head evidence;
  - what decides the outcome (data, compute, latency, evaluation);
  - scenarios with confidence levels and signals to watch;
  - implications for deployment readiness.
- **Research targets:** NVIDIA WAM blog posts (2026); the robustness study; "Robots Need More Than VLAs & World Models" (2026); π0.7; τ0-VLA; the world-language-action model paper (2026); Kairos (2026); DM0; Cosmos 3; FLUX 3 Action results.
- **Lifecycle:** no.

---

## P9 · Evaluation and safety

### ch43 · Evaluating robot policies
- **Seed sections:**
  - why evaluation is hard (variance, cost, resets);
  - success rates and statistics (confidence intervals, sample sizes, sequential tests);
  - simulation benchmarks and how well they correlate with reality;
  - real-world protocols (A/B, blind, distributed);
  - generalisation axes;
  - long-horizon and partial-credit metrics;
  - intervention metrics;
  - world-model-based evaluation;
  - readiness evaluation for the running examples.
- **Research targets:** RoboArena (2025); ManipArena (2026); RoboChallenge; SimplerEnv; LIBERO-Plus and robustness suites (verify); statistical guidance for robot evaluation; the TRI LBM evaluation method; Figure's 30-home protocol (Helix 2.5).
- **Lifecycle:** yes.

### ch44 · Safety engineering for learned robots
- **Seed sections:**
  - hazard analysis (HARA, FMEA);
  - functional safety (SIL/PL);
  - speed and separation, power and force limiting;
  - safety layers around learned policies (runtime monitors, control barrier functions, certified fallbacks);
  - semantic safety (knives, allergens, hot surfaces) and robot constitutions;
  - fall management;
  - cybersecurity;
  - privacy by design;
  - incident response.
- **Running examples:** allergens (dinner); live high voltage (battery); cutters and crop chemicals (greenhouse); a toddler near a knife (reset).
- **Research targets:** ISO/TS 15066; ISO 13849; IEC 61508; Google DeepMind's ASIMOV benchmark and robot constitution (2025); safety-filter literature; humanoid fall research; robot cybersecurity findings (verify).
- **Lifecycle:** yes.

### ch45 · Standards, certification and regulation
- **Seed sections:**
  - why standards matter for deployment;
  - industrial robots (ISO 10218-1/-2, 2025 edition);
  - collaborative operation (ISO/TS 15066);
  - industrial mobile robots (ANSI/A3 R15.08);
  - dynamically stable and legged industrial robots (ISO 25785-1; verify status);
  - personal care robots (ISO 13482);
  - EU Machinery Regulation 2023/1230;
  - EU AI Act (status at build date);
  - product liability;
  - US, China, Japan, Korea and India;
  - the certification path in practice.
- **Research targets:** ISO and IEC catalogues; the EU Official Journal; A3; UL 3300; Chinese humanoid standardisation activity (2025–26); reports of first humanoid certifications.
- **Lifecycle:** yes.

---

## P10 · Deployment

### ch46 · Deployment readiness
- **Seed sections:**
  - task selection and scoping;
  - site assessment;
  - integration (MES/WMS/ERP, home ecosystems, grocery and ordering APIs);
  - readiness criteria and acceptance tests;
  - operator training and change management;
  - remote assistance and teleoperation fallback;
  - uptime, charging and maintenance plans;
  - economics (robots-as-a-service, leasing, per-hour pricing, payback);
  - case studies;
  - a readiness checklist for each running example.
- **Research targets:** Figure at BMW (November 2025 results; Figure 03 in 2026); BMW Leipzig with AEON; Boston Dynamics Atlas at Hyundai (2026); Agility Digit deployments; Apptronik with Mercedes-Benz; 1X NEO home deliveries; published prices and leases.
- **Lifecycle:** yes.

### ch47 · Running a fleet
- **Seed sections:**
  - fleet management software;
  - monitoring and observability;
  - what to log, when, and with what privacy;
  - remote assistance at scale (operator-to-robot ratios);
  - incidents and escalation;
  - over-the-air updates;
  - spares, repair and field service;
  - KPIs (success, interventions per hour, MTBF, uptime, throughput, cost per task).
- **Research targets:** published fleet operations material (Agility Arc, Figure, 1X Expert mode); analogues from AMR fleets; OTA practice.
- **Lifecycle:** yes.

---

## P11 · After deployment

### ch48 · The data flywheel
- **Seed sections:**
  - logging triggers;
  - mining failures and edge cases;
  - interventions as data;
  - hindsight labelling and auto-labelling;
  - prioritising retraining data;
  - privacy-preserving flywheels in homes;
  - seasonal flywheels on farms;
  - the economics of the flywheel.
- **Research targets:** π*0.6 and Recap; data-engine analogues from autonomous driving (primary sources only); active learning and fleet learning for robots (2025–26).
- **Lifecycle:** yes.

### ch49 · Continual improvement and release engineering
- **Seed sections:**
  - retraining cadence;
  - continual learning and forgetting;
  - global vs site-specific models;
  - regression suites and evaluation gates;
  - shadow mode, canaries, staged rollouts;
  - rollback;
  - safety re-validation and re-certification;
  - versioning and audit trails;
  - the running examples' later twists (a new connector spec, household preferences, a new season or variety).
- **Research targets:** continual learning for VLAs (2025–26); MLOps for robotics; automotive OTA safety practice (ISO 24089, UN R156).
- **Lifecycle:** yes.

---

## P12 · Landscape and frontier

### ch50 · Lab-by-lab teardowns
- **Seed sections:**
  - method (what is compared and how evidence quality is graded);
  - one section per lab on the agreed list;
  - a comparison table (hardware, data strategy, model family, training stages, deployment status, evidence quality);
  - what is unknown.
- **Research targets:** each lab's latest primary sources (2025–26).
- **Lifecycle:** no.

### ch51 · Where deployment is happening, and where it's next
- **Seed sections:**
  - automotive manufacturing;
  - logistics and warehousing;
  - retail;
  - homes;
  - healthcare and elder care;
  - hospitality and services;
  - agriculture;
  - labs, data centres and others;
  - what gates each sector (task fit, safety, economics, regulation);
  - leading indicators.
- **Research targets:** verified deployments (primary sources only); sector analyses; pilots announced in 2025–26.
- **Lifecycle:** no.

### ch52 · Open problems and where the field is heading
- **Seed sections:**
  - dexterity and touch;
  - data scale and diversity;
  - long-horizon reliability;
  - safety certification for learned systems;
  - cost and manufacturing;
  - evaluation;
  - physics in world models;
  - energy and runtime;
  - signals to watch.
- **Lifecycle:** no.

---

## Appendices
| Appendix | Contents |
|---|---|
| **A · Data dictionary** | Every stream: name, rate, units, format, typical size per hour, who uses it. |
| **B · Hardware component reference** | Component, function, typical specs, public supplier examples, implications for learning. |
| **C · Metrics and KPI catalogue** | Definition, formula, where measured, typical public ranges. |
| **D · Equations reference** | Every labelled equation with its plain-words meaning and a link back to the chapter. |
| **E · Glossary** | Every defined term. |
| **F · Reading paths** | Fast tracks: deployment-readiness, data, models, safety. |
