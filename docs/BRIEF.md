# Brief and decision record

This file records every requirement and decision agreed with the reader before production started (October 2026). When a question is not answered here, follow the spirit of the brief and log the decision in `PROGRESS.md`.

## 1. Purpose
The reader leads product at a company whose north star is enabling robot deployment, ensuring deployment readiness, and improving robot performance after deployment. They want to understand every step, data point, modality and mechanical part that goes into building, training, post-training, deploying and improving an intelligent humanoid robot, however granular.

## 2. Shape of the book
- **Exhaustive textbook, no length cap.** Every concept and component gets an ELI5 and a first-principles explanation inline (see `docs/STYLE.md`). Raw specs go in tables next to the concept they belong to; individual numbers do not need their own ELI5.
- **Neutral reference.** No company-strategy layer, no mention of the reader's company, no vendor promotion.
- **From zero to the frontier.** Assume no prior knowledge of ML, transformers, generative models, RL, kinematics and control, robot software, capture, calibration, data formats or annotation. Start each topic from the basics and go all the way to the 2026 state of the art.
- **Equations:** include the core ones, each explained in plain, easy language.
- **Hardware depth:** component level, explained by what each part means for data, learning and deployment. This is not a full engineering bill of materials.
- **Economics, people and tools:** for each lifecycle stage, cover what it costs (where public), who does the work (roles), and which software and tools they use.
- **Learning aids:**
  - a Key takeaways box per chapter;
  - Research prompts instead of quizzes: questions the text does not answer, which push the reader into external research;
  - optional "Try it" pointers to open models, datasets and tools (no code, no notebooks).
- **Audience:** written for the reader, readable by a smart non-specialist. Written as if it may be shared publicly, so diagrams are original and quotes are short.
- **Spelling:** British.
- **Output:** a Quarto book (HTML site, PDF and EPUB).
- **Freshness:**
  - everything reflects the state of the art at the build date, and foundational ideas cite their originals;
  - every source is dated, and the book carries a "current as of" stamp;
  - `/refresh` re-checks fast-moving facts.
- **Deployment lens:** what breaks in the field, what gets measured, and how it improves after launch. Kept generic, with no company layer.

## 3. Scope
### Embodiment
- Humanoids come first. Arms, mobile manipulators and wheeled robots appear where a technique was developed on them (much of robot learning), and are flagged as such.
- Show where wheels, rails or tracks beat legs: wheeled humanoids in battery halls, pipe-rail trolleys in greenhouses.

### Settings
- Factory, warehouse, retail, home and healthcare, with the most depth where real deployments exist.
- Plus the settings where the next wave of deployment looks imminent; chapter 52 makes that case with evidence (chapter 51 before the G1 split of the teardowns).

### Labs
Teardowns are in ch50 (humanoid makers) and ch51 (robot brains, platforms, open projects and world-model builders), split at gate G1, and the labs are referenced throughout. The list below is the agreed starting point, not a closed set (decided at gate G1, 2026-10-07): cover every organisation that matters, comprehensively, in ch50 and wherever a topic needs it.
- Figure, Neura Robotics, Dyna Robotics, Skild AI, Physical Intelligence, Google DeepMind, NVIDIA, Tesla, 1X;
- Agility Robotics, Boston Dynamics with Toyota Research Institute, Apptronik, Generalist AI, OpenAI, Meta;
- Unitree, AgiBot, Galbot, UBTech.

Rules for the teardowns:
- OpenAI and Tesla publish little about their stacks, so keep those teardowns short and strictly evidence-bound.
- Go beyond the starting list wherever an organisation matters: other humanoid makers (for example Hexagon), robot-brain and data companies (for example Sunday Robotics and Rhoda AI), world-model builders (for example Odyssey, and Black Forest Labs for FLUX 3 Action) and open-source projects.
- Research up-and-coming world-model builders and open-source releases actively: they often publish their recipes, weights and data in detail, filling gaps that closed labs leave.
- Where a lab discloses nothing, say so ("not disclosed") in tables and teardowns rather than leave it out.

### Training coverage (mandatory and comprehensive)
- Cover pre-training, mid-training, post-training, RL, and RL gyms and simulators.
- Cover them for robot policies (VLAs) and, separately, for world models.
- Show how each major lab's recipe maps onto those stages.

### World models, WAMs, simulation and failure modes
**Required chapters:**
- world models;
- WAMs;
- training in simulation;
- the sim-to-real gap;
- how to train world models (pre-, mid- and post-training and RL);
- how WAMs and VLAs converge on physical AI;
- where and how world models and WAMs fail, and how to address those failures, especially through training data (volume, modality, richness, diversity, labels).

**Definitions and depth:**
- **WAM = World Action Model:** a policy built on a pretrained video or world-model backbone that predicts future world states and actions together. The term was introduced by NVIDIA's DreamZero in February 2026.
  - Cover the joint models in depth.
  - Map the adjacent families:
    - video-then-inverse-dynamics policies;
    - latent WAMs;
    - world models wrapped around policies for evaluation, RL and verification.
- **World models:** cover every family, with self-driving world models as side lessons:
  - video/pixel generative models;
  - latent predictive models (the JEPA line);
  - 3D/4D scene models;
  - model-based RL (the Dreamer line);
  - interactive, game-style models.
- **World-model training stages:**
  - **pre-training** on internet-scale video;
  - **mid-training** on data heavy in physics and embodiment, while adding action and camera conditioning;
  - **post-training** for a target robot, covering control, long-horizon consistency and real-time distillation;
  - **RL** as reward-driven post-training for physical plausibility and instruction following, plus RL inside world models.

  Map each major model's recipe onto these stages.
- **Generative internals:** full depth from the basics.
- **Training in simulation:**
  - RL at scale for balance, walking, whole-body control and dexterity;
  - synthetic demonstrations;
  - teleoperation in simulation;
  - sim+real co-training;
  - simulation for evaluation.

  World models appear there only as a bridge.
- **Sim-to-real gap:** both directions:
  - policies transferring to hardware;
  - simulated and world-model evaluations predicting real results;
  - plus the gap between world models and reality.
- **Convergence chapter:** map the routes, weigh the head-to-head evidence, and end with competing scenarios, each with confidence levels and signals to watch. Do not commit to a single thesis.
- **Running examples:** each one gets the simulator, world model and gym it would need, and the places where today's tools break down.

## 4. Running examples
See `docs/RUNNING-EXAMPLES.md` (approved). There are four tasks:
- home: dinner for five, with allergies and grocery ordering;
- home: the kitchen reset, which follows the dinner;
- factory: an EV battery-pack connection station;
- farm: greenhouse tomato harvest and crop work.

They share one legged reference humanoid, with variants noted where they matter.

## 5. Production
- **Machine and plan:** built by Claude Code on the reader's MacBook (M5 Pro, 64 GB) on a Max 20x plan. Runs are local, with no deadline.
- **Models:**
  - the strongest model for synthesis, writing, fact-checking, skeptic and editing (Opus by default);
  - cheaper models for source triage, figures and bibliography (Sonnet and Haiku);
  - a Mythos-tier model (Claude Fable) is optional for the writer or synthesizer, if the plan offers it: check its usage cost and try it on one chapter first, since it carries extra safeguards around AI research and development that a book about training AI models may run into.
- **Verification is strict:** every claim tag is fact-checked against its source, with no sampling, and verbatim passages are matched word for word where the source can be fetched.
- **Web searches:** the per-session search cap is raised in `.claude/settings.json`, because each chapter needs hundreds of searches across its subagents.
- **Gates:**
  - G1: outline approval;
  - G2: pilot chapter;
  - a soft review after each Part;
  - a final read.
- **Progress:** the `PROGRESS.md` log, plus a summary after each Part.
- **Seed materials:** none supplied. The agreed lab list is the only seed.
