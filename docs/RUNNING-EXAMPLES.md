# Running examples (approved)

Four tasks run through the whole book, from the body to the flywheel. Use them wherever a chapter's topic genuinely applies, never as decoration. The "frontier anchors" are leads gathered in October 2026: re-verify them before citing, and look for newer evidence.

All four share **one legged reference humanoid**, specified in ch04 from today's leading robots (a dated spec table with sources). Variants are discussed where they matter:
- **Battery hall:** a wheeled base, as on BMW Leipzig's wheeled AEON.
- **Greenhouse:** a pipe-rail trolley and a sealed, heat-tolerant body.
- **Home:** a soft exterior and quiet operation.

The book tracks what transfers between sites ("same brain, three deployments") and what must be learned per site.

---

## Home 1 · Dinner for five
**Scenario.** On Thursday the host says: "Five friends are coming on Saturday at 8. Starter, main and dessert." One guest is allergic to tree nuts, one to shellfish, one to sesame. The robot:
1. **Plans the menu.** It plans a menu that is safe for everyone and gets the host's approval. It checks for hidden allergens: some pestos use cashews, many curry pastes contain shrimp, hummus contains sesame.
2. **Takes stock.** It checks the fridge and pantry, reading labels and use-by dates, and lists what is missing.
3. **Orders.** It orders the missing items for delivery before cooking starts, and the host approves the payment. If an item is out of stock, it picks a substitute that also passes the allergen check.
4. **Checks the delivery** against the order and reads every label, including "may contain" warnings.
5. **Preps and cooks.** It runs several dishes at once on the hob and in the oven, timed to be ready at 8.
6. **Judges doneness without tasting,** using a thermometer, colour and texture.
7. **Prevents cross-contamination:**
   - separate boards and utensils;
   - allergen-safe dishes cooked first and covered;
   - cleaning in between.
8. **Plates five portions** and makes sure each guest gets a plate that is safe for them.
9. **Cleans as it goes.** The kitchen reset (Home 2) follows the meal, so the two home tasks form one evening.

**Done means:**
- zero allergen exposure (the one rule where 99% counts as failure);
- safe cooking temperatures;
- each course within 10 minutes of plan;
- spending within the host's budget;
- no burns, cuts or fires.

**Later twist (post-deployment chapters).** The robot remembers the household's tastes and returning guests' allergies. That raises the question of how a home robot should store health information.

**What it tests:**
- a plan spanning days that depends on outside factors (delivery windows, stock-outs);
- online action that needs human approval to spend money;
- reading packaging;
- a hard safety constraint with no margin;
- heat, knives and hot oil;
- ingredients that change as they cook;
- running several jobs at once;
- judging quality without tasting.

**Data and simulation reality.**
- Cooking video is everywhere.
- Simulators barely capture how food behaves.
- "Tastes good" cannot be scored automatically.

**Frontier anchors (re-verify):**
- Demonstrations so far cover single dishes or narrow steps. A humanoid cooked Xinjiang dishes after under a week of training but still trailed experienced chefs (July 2026). LG's CLOiD took milk from a fridge and put a croissant in an oven at CES 2026.
- The ordering half already exists as software (Instacart inside ChatGPT, with checkout in the conversation). Instacart has said only a very small share of its orders come through AI agents.
- No published system yet plans, shops for, cooks and serves an allergen-safe multi-course meal end to end in a real home.

---

## Home 2 · The after-dinner kitchen reset
**Scenario.** It is the robot's first week in a new home. After the dinner, someone says: "Clean up, but leave my glass." The robot:
1. **Clears the table:** plates with scraps, half-full glasses, cutlery (including a chef's knife), serving dishes and cloth napkins.
2. **Deals with food:** scrapes waste, packs leftovers into lidded containers and puts them in the fridge.
3. **Loads the dishwasher.**
4. **Hand-washes** what cannot go in the dishwasher (wine glasses, a cast-iron pan, a wooden board, knives), dries each item, and puts it where this household keeps it, asking when unsure.
5. **Finishes up:** wipes the table and counters, starts the dishwasher, and takes out the bin if it is full.
6. **Stays safe throughout:** it works around people, a toddler or a pet the whole time.

**Done means:**
- everything is in its right place;
- nothing is broken;
- there are no unsafe moments;
- the job takes under an hour;
- at most one remote assist from a human operator.

**Later twist.** Over the following weeks the robot learns this household's preferences, for example "the board never goes in the dishwasher".

**What it tests:**
- fragile, floppy, wet and food items;
- doors, racks and drawers;
- the right force for wiping;
- common sense about what goes where;
- privacy;
- safety around knives and children.

**Data and simulation reality.**
- Kitchens are common in human video.
- Liquids and cloth are hard to simulate.
- "Clean" is hard to score.

**Frontier anchors (re-verify):**
- Figure's Helix 02 ran a continuous kitchen sequence of about four minutes, which Figure describes as autonomous (January 2026; company claim).
- Figure reports that Helix 2.5 completed 56% of whole-task trials (tidying living rooms, folding towels, making beds) in 30 unfamiliar homes, against 9% for a model trained without its human-behaviour dataset (September 2026; company claim).
- 1X says NEO runs autonomously by default, with a remote human expert guiding chores it has not seen before.
- A full reset in a home the robot has never seen is beyond anything published so far.

---

## Factory · EV battery-pack connection station
**Scenario.** An EV battery hall. Each pack arrives with its modules already placed by upstream automation. Within the station's cycle (several minutes), the robot:
1. **Starts the job.** It scans the pack and pulls up the work instructions and torque settings from the plant's systems.
2. **Fits the busbars.** It fits the high-voltage busbars that link the modules and tightens each bolt with a powered torque tool. The tool records the torque and angle of every bolt.
3. **Connects the harness.** It routes the low-voltage monitoring harness and plugs it into every module: it lines each connector up, pushes until it clicks, then tugs to test.
4. **Connects coolant lines** with quick-connect couplings and checks each latch.
5. **Closes out.** It fits the insulating covers and confirms completion in the plant's systems.
6. **Handles problems:** a cross-threaded bolt, a torque reading the tool rejects, a connector that will not latch, a missing part. It retries as the instructions say, then stops and calls the team lead.
7. **Works next to a hazard that cannot be switched off.** Once the modules are linked they carry hundreds of volts, so high-voltage safety rules apply at every step.

**Done means:**
- every bolt within spec and recorded;
- every connector and coupling verified;
- at least 99% of packs pass the final test first time;
- cycle time met;
- zero safety incidents.

**Later twist.** An engineering change brings a revised module with a different connector and torque spec. How fast can the fleet adapt, and how do you prove the update is safe before it touches live hardware?

**What it tests:**
- using a powered tool: seating the socket and absorbing the tool's reaction;
- precise insertion that needs touch and force sensing;
- handling cables and hoses;
- a hazard where learning by trial and error is unacceptable, so most practice must happen in simulation or on unpowered dummy modules;
- record-keeping and certification;
- cost against human workers and fixed automation.

**Data and simulation reality.**
- Rigid parts simulate well from their design files; cables, hoses and connector clicks do not.
- Success is easy to measure.
- The task repeats constantly, so the cycle of collecting data, retraining and redeploying runs fast.

**Why this station (keep in mind).** On mixed-model lines, stations are fixed and the operator at each station handles whichever variant arrives, with parts supplied just in time. Kitting, delivery and installation are separate jobs. The example deliberately stays one real station.

**Frontier anchors (re-verify):**
- BMW is piloting Hexagon's wheeled AEON humanoid in high-voltage battery assembly at Leipzig (first test December 2025; pilot phase from summer 2026). Employees in that work currently wear cumbersome protective gear.
- Hyundai Mobis is piloting robots that connect wiring harnesses to battery modules (September 2026), a task considered among the hardest to automate.
- Confirming that a connector has mated has traditionally relied on a worker hearing and feeling the click. Multisensor research (2026) targets this with acoustic, force and kinematic data.

---

## Farm · Greenhouse tomato harvest and crop work
**Scenario.** A commercial tomato greenhouse: long rows, heating pipes that double as rails, vines trained up strings several metres high, and dense leaves. Over a full shift, the robot:
1. **Moves along the rows** on a trolley that runs on the pipes, raising or lowering itself to reach.
2. **Finds ripe clusters** hidden behind leaves, judging ripeness by colour and variety.
3. **Harvests.** It cuts whole trusses (or picks single fruit) without bruising, lays them in crates, and swaps out full crates.
4. **Strips the lower leaves,** deciding which ones go.
5. **Scouts.** It flags signs of pests and disease, with their location.
6. **Copes with the climate:** heat above 30 °C, high humidity and shifting sunlight.
7. **Recharges** without blocking the row.

**Done means:**
- a picking rate close to a skilled worker's;
- bruising and missed ripe fruit below the grower's limits;
- running for the full shift.

**Later twist.** Plants change weekly and varieties change by season, so some situations come up once a year. Data accumulates more slowly here than in any other example.

**What it tests:**
- living, growing, hidden and fragile objects;
- cutting tools;
- sealing against moisture and managing heat;
- plants that are hard to simulate;
- the toughest business case: a humanoid must beat cheaper single-purpose machines by doing many greenhouse jobs in one body.

**Frontier anchors (re-verify):**
- Daedong and Rainbow Robotics' Agroid humanoid is in field testing, including tomato harvesting, with an AI greenhouse deployment targeted for 2028.
- Dutch grower Harvest House is testing humanoids with the Humanoid Application Center, starting with imitation learning for gentle pepper picking.
- Specialist machines such as eternal.ag's Harvester (launched March 2026) set the bar a humanoid must clear.
- A 2026 greenhouse-simulation paper (Agri-Sim) names cramped space, occlusion, changing light, irregular plant shapes and safe plant contact as the core difficulties.

---

## Threads by Part (what each example contributes)
| Part | Dinner for five | Kitchen reset | Battery station | Greenhouse |
|---|---|---|---|---|
| P1 Body | Hands for knives and tongs; heat near the hob | Wrist and palm cameras; gentle grasps on glass | Torque tool reaction; HV-safe design; wheeled variant | Sealing, heat, cutters; rail-trolley variant |
| P2–P3 Foundations and stack | Days-long planning vs sub-second control | Language grounding ("leave my glass") | Force-controlled insertion loop | Visual ripeness judgement |
| P4 Data | Abundant cooking video; label reading (OCR) | Home teleoperation and privacy | Scarce video; dummy-module demonstrations | Seasonal data; scarce footage |
| P5 Simulation | Food and liquids break simulators | Cloth, water, breakage | CAD-accurate rigid parts; cables and clicks fail | Plant deformation, lighting |
| P6 Training | Tool use, multitasking, reasoning mid-training | Preferences, few-shot adaptation | RL on dummy modules; precision post-training | Few-shot per variety |
| P7–P8 World models and WAMs | Predicting dough and sauce: a WM failure case | Predicting spills | Contact and click prediction; force-aware WAMs | Plant motion when touched |
| P9 Evaluation and safety | Allergen as a hard constraint; fire | Toddler near a knife | Live high voltage; certification | Cutters, chemicals, heat stress |
| P10 Deployment | Ordering and payment approval; remote assist | First week in a new home | Plant systems; takt time; operator ratio | Shift economics vs specialists |
| P11 After deployment | Storing health information; taste memory | Household preference learning | Engineering-change rollout | Seasonal retraining |
