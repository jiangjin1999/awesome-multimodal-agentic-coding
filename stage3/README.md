# Stage 3 · Bridging Digital & Physical Worlds

<a id="research-map"></a>

**English** · [简体中文](README.zh-CN.md)

How can multimodal coding agents interact with the physical world, build verifiable environments, and improve programs, skills and models through experience? This guide connects six research questions, from early foundations to recent work, with an emphasis on manipulation and directly related scientific and fabrication tasks.

**Literature cutoff: 2026-11-13.** [Full research map](../README.md#contents).

| Research question | Primary entries | Connections |
|---|---:|---|
| [1. Embodied Harnesses](#section-1) | 77 | Observation, execution, skills and receipts |
| [2. Simulator Construction](#section-2) | 62 | References / requirements → executable artifacts |
| [3. Simulator Quality Evaluation](#section-3) | 29 | Artifact quality → usable verification evidence |
| [4. Data](#section-4) | 13 | Observations, code, actions and outcomes → learning material |
| [5. Training and Capability Improvement](#section-5) | 71 | Program / skill / model updates → transfer |
| [6. Physical Applications and Experiments](#section-6) | 34 | Composed mechanisms → task outcomes and physical validation |

**Build verifiable environments → collect interaction experience → improve coding agents** is the connecting research agenda. Individual works establish different parts of this chain; an end-to-end scalable loop requires joint validation. The environment builder, operator and downstream action policy may be different models.

Each work has one primary reading entry, with links for cross-section contributions. Existing full bibliographies link back to the research map. Dates prefer first public release, with venue or version dates distinguished where needed. Standalone benchmarks, evaluations within methods and reusable resources have different roles.

---

<a id="section-1"></a>

## 1. Embodied Harnesses

A harness gives a multimodal coding agent observations, execution interfaces, runtime state, skills and failure receipts. Follow **what the agent emits → who executes it → what evidence returns → what changes next**.

| Execution path | Agent decisions | Execution support | Reading entry points |
|---|---|---|---|
| Tools / control interfaces | Programs, target positions, poses, action order and observation timing | Perception, motion planning, inverse kinematics, controllers and robot adapters | Code as Policies → HexaShell, uni-robot-agent |
| Delegation to existing policies | Subgoals, policy selection, budgets, stopping and recovery conditions | A VLA, action model or existing program performs local control | Harness VLA, HarnessPAI, REA |

The paths can coexist. Code generation, hierarchy, memory and skills describe system designs rather than a third exclusive execution path. A VLA may accept a language subgoal directly. Feedback inside a running program differs from new observations reaching the language model and causing it to write another program.

Early work connects language tasks to programs and robot APIs. Recent systems examine observation timing, recoverable execution, context management and responsibility across policies. Comparisons must account for interfaces, permissions and budgets, separating task completion, correct completion declarations and cost. This section covers the use of available skills; Section 5 covers discovering and improving them.

### Composable execution resources

See the [runtime resources](../README.md#s3-1) and [model capabilities](../README.md#s2-6) for reusable components. A callable component can support a harness without itself implementing agent learning.

| Resource | Interface and role | Evidence boundary |
|---|---|---|
| [Webots MCP](https://github.com/MHasaan/webotMCP) | Scene/controller edits and robot commands; multiview screenshots, motion traces and contact events | Simulator truth and reactive controllers are distinct from learned perception or planning. |
| [Alpamayo 2 Edge](https://huggingface.co/nvidia/Alpamayo2-Edge) | Surround-camera sequences, navigation and ego-motion history → reasoning and driving trajectories | NVIDIA provides weights and inference code; simulation evaluation and partner vehicle demonstrations are separate evidence. |
| [AlpaJudge](https://huggingface.co/nvidia/alpajudge) | Text-reference or visual/action-conditioned evaluation of driving rationales | The two checkpoints score reasoning for selection/rewards; these scores do not certify executed driving safety. |
| [Gemini Robotics 2.5](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/) | Embodied reasoning coordinates work; the action model controls robot motion | Google’s November 10 announcement describes partner access and a specific factory pilot; neither open weights nor an independent general-purpose evaluation is established by that report. |

### Tools and control interfaces

<a id="work-2611-01560"></a>
<!-- stage3-record: {"id": "2611.01560", "scope": "Core", "section": 1} -->

#### Democratizing Robot-Use Agents: A Unified Harness with Open Models

`2026-11-01` · Tsinghua University; University of California, Berkeley

[Bibliographic record](../README.md#paper-2611-01560) · [Paper](https://arxiv.org/abs/2611.01560) · [Code](https://github.com/Open-RUA/uni-robot-agent) · [Project page](https://openrua.ai/uni-robot-agent)

Connects Qwen3.8-Flash-Next and GPT-6 Astra to shared perception and motion tools so agents can run geometric checks, inspect action outcomes, and adjust their next move.

**Method:** The system makes one agent toolset usable across models, simulators and real robots: tools give parameters and results consistent meanings, while backends adapt to hardware. Scheduling allows reasoning to overlap with physical motion while preserving the ordering of operations on shared resources. Its contributions concern consistent interaction, execution efficiency and information boundaries, beyond merely adding robot functions.

**Verification:** RoboDojo comparisons with the same model across harnesses · 19 real-robot tasks · sensor inputs and fine-tuning differ across hardware baselines.

<a id="work-2611-01112"></a>
<!-- stage3-record: {"id": "2611.01112", "scope": "Core", "section": 1} -->

#### Auriga Technical Report: A Task-Agnostic Agent Harness for Zero-Shot Embodied Manipulation

`2026-10-31` · StellarEdge AI Technical Team

[Bibliographic record](../README.md#paper-2611-01112) · [Paper](https://arxiv.org/abs/2611.01112) · [Project page](https://auriga.stelledge.com/) · [Code](https://github.com/lose4578/Auriga)

Coordinates perception tools, generated programs and staged robot actions through one preview-and-execution gateway, using fresh images and measured discrepancies to revise operations within a single simulation episode.

**Verification:** RoboDojo and RoboCasa365 simulation · program/preview/geometry ablations · observation-linked recovery traces; the evaluation harness is frozen and no hardware result is reported.

<a id="work-2610-30043"></a>
<!-- stage3-record: {"id": "2610.30043", "scope": "Adjacent", "section": 1} -->

#### TARSphere: A Robot-Oriented Full-Stack Framework for Long-Horizon Embodied Agents in Evolving Physical and Social Environments

`2026-10-21` · Zhejiang University; Fudan University

[Paper](https://arxiv.org/abs/2610.30043) · [Project page](https://xuyicheng-zju.github.io/TARSphere/) · [Code](https://github.com/xuyicheng-zju/TARSphere)

Organizes long-horizon robot action using hierarchical executable skills, task memory and execution feedback around a frozen model.

**Verification:** Evaluates eight frozen MLLMs on 360 simulated episodes across 30 indoor scenes, pairing navigate-and-report and fetch-and-deliver tasks with five changing-world conditions. Event-dependent scoring checks delivered information and physical completion; collisions, falls and execution fidelity are examined separately from task quality. These are simulated robot and NPC interactions, not real-world deployment results.

<a id="work-2610-23479"></a>
<!-- stage3-record: {"id": "2610.23479", "scope": "Core", "section": 1} -->

#### HexaShell: A Universal Harness for Robot Coding Agents in Simulation and the Real World

`2026-10-16` · HexaFuture

[Bibliographic record](../README.md#paper-2610-23479) · [Paper](https://arxiv.org/abs/2610.23479) · [Code](https://github.com/HexaFuture/HexaShell)

Lets a robot coding agent write a Python cell each turn against shared motion, perception and state tools, with optional task skills drafted from earlier runs.

**Method:** HexaShell fixes a general agent loop, Python sandbox and robot API, with adapters for different simulators and arms. Task experience can be stored as short skills describing success conditions, workable steps and parameters. This separates evaluation of interface transfer from analysis of which failures improve when task experience is added.

**Verification:** GPT-6 Astra across four simulation benchmarks · nine dual-arm hardware tasks, 76/90 episodes judged successful · GPT-6.1 Terra wrote the hardware code and GPT-6 Astra judged the outcomes.

**Related:** [5. Training and Capability Improvement](#section-5)

<a id="work-2610-13862"></a>
<!-- stage3-record: {"id": "2610.13862", "scope": "Adjacent", "section": 1} -->

#### BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation

`2026-10-09` · Stanford University; University of California, Berkeley; NVIDIA

[Bibliographic record](../README.md#paper-2610-13862) · [Paper](https://arxiv.org/abs/2610.13862)

Composes perception and physical-action tools through fixed behavior-tree skills, using structured failures to retry or change task decisions while local guards supervise operator-approved onboard motion.

**Verification:** Text/Habitat task alignment · perception and motion failures · real-robot task completion · guard interruption · interface/feedback ablations.

<a id="work-2610-12457"></a>
<!-- stage3-record: {"id": "2610.12457", "scope": "Adjacent", "section": 1} -->

#### SpatialHarness: Test-Time Spatial Scaffolding for Fine Robotic Manipulation

`2026-10-08` · Fudan University; Singapore Management University

[Paper](https://arxiv.org/abs/2610.12457) · [Project page](https://emilia113.github.io/SpatialHarness/)

Maintains a simulation scene synchronized with real execution and renders task-specific auxiliary viewpoints.

**Method:** SpatialHarness maintains a digital scene that updates from real observations during manipulation. It aligns objects and layout, corrects state using physics advancement, visual comparison and programmatic constraints, and renders task-relevant viewpoints. The digital model supports current action decisions, connecting to reconstruction while emphasizing how spatial information improves operation.

**Verification:** Spatial scaffolding supports a frozen policy; synchronized geometry does not by itself demonstrate accurate full dynamics.

<a id="work-2610-04929"></a>
<!-- stage3-record: {"id": "2610.04929", "scope": "Adjacent", "section": 1} -->

#### RobotUse: Allocating Computation, Context, and Decisions

`2026-10-04` · KAIST; Seoul National University

[Paper](https://arxiv.org/abs/2610.04929) · [Project page](https://robotuse-team.github.io/)

Allocates physical task decisions and detailed interactions to subagents while the parent receives compact results and constraints.

**Method:** RobotUse examines which physical choices an interface leaves to the agent. A function that automatically takes the top-ranked grasp may prevent the model from choosing where to grasp a cup, so the system exposes candidates and poses for agent selection and revision. The backend retains geometric computation, while task-semantic choices remain with the model.

**Verification:** Perception and motion backends realize geometric choices; persistent execution guidance is a separate source of experience.

**Related:** [5. Training and Capability Improvement](#section-5)

<a id="work-2610-02459"></a>
<!-- stage3-record: {"id": "2610.02459", "scope": "Core", "section": 1} -->

#### OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies

`2026-10-01` · University College London; Carnegie Mellon University

[Paper](https://arxiv.org/abs/2610.02459) · [Code](https://github.com/terminalworld/OpenRUA)

Gives an existing coding agent a terminal, ROS 2 documentation and a robot workspace for writing perception and motion programs.

**Method:** OpenRUA treats the robot as an explorable software workspace, exposing native ROS 2 interfaces, documentation and editable starter tools without prescribing a complete task workflow. The model can reuse scripts or write new feedback-control logic. Its agent can extend its operating methods through native interfaces rather than being limited to a fixed tool menu.

**Verification:** The agent chooses when to inspect images and sensor readings; script-level force or position feedback is distinct from LLM updates.

<a id="work-2610-01939"></a>
<!-- stage3-record: {"id": "2610.01939", "scope": "Core", "section": 1} -->

#### Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens

`2026-10-01` · Peking University; National University of Singapore; NVIDIA; Impossible Research

[Paper](https://arxiv.org/abs/2610.01939)

Batches robot primitives, computation, conditions and local retries inside Python cells, returning selected outputs to the model.

**Method:** PyRUA changes both execution and observation granularity: short loops that a program can handle run locally, and evidence returns when the model needs to reconsider. This reduces per-primitive LLM calls and repeated image transmission. Depending on configuration, low-level primitives can include learned policies, so the main comparison concerns program organization and feedback delivery, beyond whether code is generated.

**Verification:** Local program feedback and the model's next reasoning turn occur at different frequencies; the work also studies RL for a smaller coder.

**Related:** [5. Training and Capability Improvement](#section-5)

<a id="work-2610-14018"></a>
<!-- stage3-record: {"id": "2610.14018", "scope": "Adjacent", "section": 1} -->

#### RoboHarness: A Simple Harness Outperforms VLA and World Action Models

`2026-09-29` · Zhejiang University

[Paper](https://arxiv.org/abs/2610.14018)

Gives an LLM a visual-geometric control panel for zero-shot manipulation using existing robot tools.

**Verification:** Results concern the complete harness-and-model configuration, not a standalone action model.

<a id="work-2609-38078"></a>
<!-- stage3-record: {"id": "2609.38078", "scope": "Adjacent", "section": 1} -->

#### MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation

`2026-09-29` · University of Illinois Urbana-Champaign

[Paper](https://arxiv.org/abs/2609.38078)

Combines mid-level parameterized actions, deterministic control and asynchronous monitoring around a frozen VLM.

**Method:** MotorMind adds asynchronous monitoring and memory updates to sequential action so that execution can be tracked during slow model reasoning. Short actions enable incremental correction of spatial errors, while completion checks and exception handling distinguish issuing an action from finishing a task. It compares interfaces around a frozen VLM rather than introducing a code-generation system.

**Verification:** The model checks task progress and can interrupt subgoals; it does not output every servo command.

<a id="work-2609-29389"></a>
<!-- stage3-record: {"id": "2609.29389", "scope": "Adjacent", "section": 1} -->

#### Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation

`2026-09-24` · The Chinese University of Hong Kong; The Hong Kong University of Science and Technology (Guangzhou); Knowin AI

[Paper](https://arxiv.org/abs/2609.29389)

Provides depth, spatial measurement and grasp-candidate tools to a robot-use agent without retraining its visual encoder.

**Method:** K1 separates spatial-information queries from physical movement; queries leave the environment unchanged and can be composed before acting. Persistent object identifiers, spatial anchors and projected candidate poses help the model track targets across viewpoints. The model receives readable images and tool outputs instead of directly processing dense depth or point clouds. Tool-interaction trajectories also train smaller models; reported validation is in simulation.

**Verification:** Annotated images and calibrated geometry support the agent's next measurement or motion decision.

<a id="work-2609-20822"></a>
<!-- stage3-record: {"id": "2609.20822", "scope": "Core", "section": 1} -->

#### Coding Agents with an Obstacle-Aware Harness for Safe Robot Manipulation

`2026-09-17` · University of Southern California; University of Central Florida; University of California, Santa Barbara

[Bibliographic record](../README.md#paper-2609-20822) · [Paper](https://arxiv.org/abs/2609.20822)

Equips code-as-policy agents with visually grounded route checks and contact constraints, replanning from the observed stopped pose when execution encounters an obstacle or an unmodeled physical constraint.

**Method:** SafeHarness separates safety during travel toward a target from safety during contact near it. Path checks account for the occupied volume of both the gripper and any held object, while contact uses separate execution constraints. The two stages require distinct treatment because a collision-free approach does not establish that the following push, pull or grasp is safe.

**Verification:** Task success · collision avoidance · route clearance · recovery under execution-time constraints.

<a id="work-2609-12541"></a>
<!-- stage3-record: {"id": "2609.12541", "scope": "Core", "section": 1} -->

#### Agent as Policy for Robotic Manipulation

`2026-09-11` · University of Notre Dame; University of California San Diego; San Diego State University

[Paper](https://arxiv.org/abs/2609.12541)

Lets a general agent inspect visual evidence, write programs and issue motion requests throughout a manipulation episode.

**Verification:** Subsequent decisions depend on physical execution results, with the actual observation and action interface defining the setting.

<a id="work-2609-10522"></a>
<!-- stage3-record: {"id": "2609.10522", "scope": "Adjacent", "section": 1} -->

#### Show-Harness: Just a VLM Agent Can Play Robots

`2026-09-09` · Show Lab, National University of Singapore

[Paper](https://arxiv.org/abs/2609.10522) · [Project page](https://showlab.github.io/Show-Harness)

Connects a general VLM to a robot interpreter through a compact semantic action interface.

**Verification:** The interface delegates motion realization; model reasoning and downstream control are separate responsibilities.

<a id="work-chemautoagent"></a>
<!-- stage3-record: {"id": "chemautoagent", "scope": "Adjacent", "section": 1} -->

#### ChemAutoAgent: A Multi-Agent System for Evidence-Controlled Laboratory Instrument Driver Generation from Text-Based Manuals

`2026-08-20` · Affiliation not established

[Paper](https://www.mdpi.com/2076-3417/16/16/8291) · [Version notes](https://www.mdpi.com/2076-3417/16/16/8291/notes)

Builds instrument drivers from source-linked manuals within deterministic protocol scaffolds, repairing them through hardware tests.

**Verification:** Three instruments are tested with human confirmation; command-only baselines are not equivalent to matched hardware trials.

<a id="work-2608-03924"></a>
<!-- stage3-record: {"id": "2608.03924", "scope": "Adjacent", "section": 1} -->

#### ETA: A New Agentic Paradigm for Embodied Tasks

`2026-08-04` · Shanghai Innovation Institute; Fudan University; Jilin University; Nanjing University; Zhejiang University

[Paper](https://arxiv.org/abs/2608.03924)

Connects digital agents to observation, target marking and motion through a lightweight embodied interface.

**Method:** OpenETA separates the Agent that proposes operations, the Interface that checks and dispatches them, and the World that executes them. Its key runtime rule is to observe again after a world-changing operation before making another state-dependent decision. The full system and the lightweight Codex plugin are distinct configurations; the latter connects an existing agent through a small set of observation, pointing and motion tools.

**Verification:** Fresh observations and execution receipts govern whether the next state-dependent action can proceed.

<a id="work-2607-16636"></a>
<!-- stage3-record: {"id": "2607.16636", "scope": "Adjacent", "section": 1} -->

#### PhyAgentOS: A Self-Evolving Operating System for Embodied Agents with Decoupled Cognitive Planning and Physical Execution

`2026-07-18` · X-Era Lab; Sun Yat-sen University; Peng Cheng Laboratory

[Paper](https://arxiv.org/abs/2607.16636)

Separates cognitive planning from physical execution through file-based state contracts, tools and persistent execution records.

**Verification:** Track which state and experience reach the agent across runtime boundaries.

<a id="work-2607-05369"></a>
<!-- stage3-record: {"id": "2607.05369", "scope": "Adjacent", "section": 1} -->

#### GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks

`2026-07-06` · University of California, Berkeley; Bosch; NVIDIA

[Paper](https://arxiv.org/abs/2607.05369) · [Project page](https://graph-robots.github.io/gap)

Builds typed computation graphs connecting perception, planning and control skills, then rehearses and revises the graph in simulation.

**Method:** GaP represents policies as inspectable, editable computational graphs, making data dependencies and execution relationships between skills explicit. It targets known workcells and bounded variations in objects and initial states to produce reusable automation. Internal simulation supports rehearsal and graph revision; it does not establish reconstruction of arbitrary unknown real environments.

**Verification:** The optimized graph can execute without invoking the LLM at every action.

<a id="work-2605-26637"></a>
<!-- stage3-record: {"id": "2605.26637", "scope": "Adjacent", "section": 1} -->

#### Enabling Extensible Embodied Capabilities with Tools

`2026-05-26` · Huazhong University of Science and Technology; Hebei University of Technology; Tianjin University; Lehigh University; Tsinghua University

[Paper](https://arxiv.org/abs/2605.26637)

Defines an Embodied Tool Protocol for registering, discovering and invoking perception, reasoning and execution capabilities.

**Verification:** The protocol exposes existing capabilities; task success still depends on the connected agent and tools.

<a id="work-2511-00917"></a>
<!-- stage3-record: {"id": "2511.00917", "scope": "Core", "section": 1} -->

#### MAESTRO: Orchestrating Robotics Modules with Coding Agents for Zero-Shot Generalist Robots

`2025-11-02` · University of Pennsylvania

[Paper](https://arxiv.org/abs/2511.00917) · [Project page](https://maestro-robot.github.io) · [Code](https://github.com/penn-pal-lab/maestro)

Orchestrates perception, planning and control modules through generated programs, checking visual and execution feedback for recovery.

**Method:** MAESTRO studies reliable use of a growing toolset by wrapping error-prone module chains, supplying composition examples, and adding visual checks, caching and execution monitoring. The model organizes these capabilities through planning, execution, inspection and replanning. The main comparison does not invoke a VLA; a separate extension wraps one as a monitored, stoppable tool.

**Verification:** Real-robot tests cover eight tabletop tasks on a Franka/DROID platform and four mobile-manipulation tasks on a Go2-W with a PiPER arm, using five settings per task. Human reviewers score progress independently of the agent monitor. Tabletop comparisons and tool/harness ablations exclude the VLA tool; mobile tests have no competing baseline, and cross-trial improvement is demonstrated through separate case studies.

<a id="work-2510-21302"></a>
<!-- stage3-record: {"id": "2510.21302", "scope": "Adjacent", "section": 1} -->

#### Towards Reliable Code-as-Policies: A Neuro-Symbolic Framework for Embodied Task Planning

`2025-10-24` · Sungkyunkwan University

[Paper](https://arxiv.org/abs/2510.21302)

Combines code-policy generation with symbolic verification and exploratory programs that obtain missing observations.

**Verification:** Verification depends on the modeled conditions and observed evidence, rather than guaranteeing every physical outcome.

<a id="work-2505-07532"></a>
<!-- stage3-record: {"id": "2505.07532", "scope": "Adjacent", "section": 1} -->

#### RAI: Flexible Agent Framework for Embodied AI

`2025-05-12` · Robotec.AI; Warsaw University of Technology

[Paper](https://arxiv.org/abs/2505.07532)

Connects language models, agents, ROS and simulators through modular tools and reusable robot runtime components.

**Verification:** Inspect the concrete tools and robot configuration when interpreting demonstrations.

<a id="work-2503-21969"></a>
<!-- stage3-record: {"id": "2503.21969", "scope": "Core", "section": 1} -->

#### Robotic Long-Horizon Manipulation with Progressive In-Context Code Generation and Episodic Feedback

`2025-03-27` · Technical University of Munich; Ludwig Maximilian University of Munich; Beijing Academy of Artificial Intelligence; Nanjing University

[Paper](https://arxiv.org/abs/2503.21969)

Uses progressive in-context examples to generate robot programs, then a visual reporter summarizes each episode for replanning.

**Verification:** Feedback is episodic rather than necessarily returned to the LLM after every primitive.

<a id="work-2412-04455"></a>
<!-- stage3-record: {"id": "2412.04455", "scope": "Adjacent", "section": 1} -->

#### Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection

`2024-12-05` · Beihang University; Peking University; Beijing Academy of Artificial Intelligence; Galbot

[Paper](https://arxiv.org/abs/2412.04455) · [Project page](https://zhoues.github.io/Code-as-Monitor/)

Generates executable spatial and temporal constraint monitors, using visual tracking to detect failures or impending violations.

**Method:** Code-as-Monitor converts language requirements, such as keeping bread inside a pan, into continuously executable spatiotemporal constraint checks. It connects constraint generation, visual localization and code-based monitoring to detect problems during execution. Its primary artifact is a monitor that can accompany different action-execution paths, rather than a third manipulation workflow.

**Verification:** Monitoring code can trigger replanning; the action policy is a separate component.

<a id="work-bounded-motion"></a>
<!-- stage3-record: {"id": "bounded-motion", "scope": "Adjacent", "section": 1} -->

#### Language-guided Manipulator Motion Planning with Bounded Task Space

`2024-10-11` · Affiliation not established

[Project page](https://proceedings.mlr.press/v270/oelerich25a.html) · [Project page](https://www.acin.tuwien.ac.at/42d2/)

Generates Python calls to a constrained path planner; BoundMPC then realizes smooth robot trajectories.

**Verification:** Includes simulation and physical arms; trajectory constraints are enforced by the planner, not learned dynamics inside the LLM.

<a id="work-2410-06472"></a>
<!-- stage3-record: {"id": "2410.06472", "scope": "Adjacent", "section": 1} -->

#### Enabling Novel Mission Operations and Interactions with ROSA: The Robot Operating System Agent

`2024-10-09` · NASA Jet Propulsion Laboratory; California Institute of Technology

[Paper](https://arxiv.org/abs/2410.06472)

Exposes ROS queries, diagnosis and operations as callable tools for language agents across robot platforms.

**Verification:** Tool availability and demonstrated tasks define its scope; a ROS bridge alone does not establish autonomous recovery.

<a id="work-2312-04474"></a>
<!-- stage3-record: {"id": "2312.04474", "scope": "Adjacent", "section": 1} -->

#### Chain of Code: Reasoning with a Language Model-Augmented Code Emulator

`2023-12-07` · Stanford University; Google DeepMind; University of California, Berkeley

[Paper](https://arxiv.org/abs/2312.04474) · [Project page](https://chain-of-code.github.io)

Executes explicit program logic in an interpreter and asks a language model to emulate unresolved semantic operations.

**Verification:** Robot examples demonstrate composition of code and model calls, not a universal physical controller.

<a id="work-2306-09523"></a>
<!-- stage3-record: {"id": "2306.09523", "scope": "Adjacent", "section": 1} -->

#### Tell Me Where to Go: A Composable Framework for Context-Aware Embodied Robot Navigation

`2023-06-15` · University of Colorado Boulder

[Paper](https://arxiv.org/abs/2306.09523)

Uses generated Python as an intermediate layer between language reasoning, visual scene descriptions and mobile navigation.

**Verification:** Context-dependent navigation tests the composed system rather than learning low-level locomotion inside the LLM.

<a id="work-2305-11176"></a>
<!-- stage3-record: {"id": "2305.11176", "scope": "Adjacent", "section": 1} -->

#### Instruct2Act: Mapping Multi-modality Instructions to Robotic Actions with Large Language Model

`2023-05-18` · Shanghai Jiao Tong University; Shanghai AI Laboratory; University of Chinese Academy of Sciences; Peking University; The Chinese University of Hong Kong

[Paper](https://arxiv.org/abs/2305.11176) · [Code](https://github.com/OpenGVLab/Instruct2Act)

Generates Python to connect SAM, CLIP and action APIs, turning multimodal instructions into perception, planning and execution.

**Method:** Instruct2Act connects multimodal instructions to existing robot capabilities through code: visual modules identify objects, the program composes processing steps, and the controller executes motion. It links perception to action using available models and APIs, without retraining an entire manipulation policy for every new instruction.

**Verification:** Tests six selected VIMABench tabletop meta-tasks in PyBullet across L1 placement, L2 combination and L3 novel-object generalization. Success is determined from the final simulated state; comparisons also vary instruction modality, prompt elements and perception backbones. The reported experiments are simulation-only, constrained by the supplied action primitives; they do not demonstrate post-action visual code repair.

<a id="work-2306-17582"></a>
<!-- stage3-record: {"id": "2306.17582", "scope": "Adjacent", "section": 1} -->

#### ChatGPT for Robotics: Design Principles and Model Abilities

`2023-02-20` · Scaled Foundations; Microsoft Autonomous Systems and Robotics Research

[Paper](https://arxiv.org/abs/2306.17582) · [Project page](https://www.microsoft.com/en-us/research/publication/chatgpt-for-robotics-design-principles-and-model-abilities/)

Combines robot function libraries, prompting and human dialogue to generate and revise programs for arms, drones and mobile robots.

**Method:** This early technical report studies how clear robot-function names, interface documentation and interactive prompts enable general language models to write robot programs. Robot-arm and drone examples share this programming-based approach. Human inspection and feedback remain part of the workflow and should not be omitted when describing its autonomy.

**Verification:** Distinguish automatically returned observations from corrections supplied by a human in individual demonstrations.

<a id="work-2209-11302"></a>
<!-- stage3-record: {"id": "2209.11302", "scope": "Adjacent", "section": 1} -->

#### ProgPrompt: Generating Situated Robot Task Plans using Large Language Models

`2022-09-22` · University of Southern California; NVIDIA

[Paper](https://arxiv.org/abs/2209.11302) · [Project page](http://progprompt.github.io)

Generates program-like plans using available objects, actions and assertions, with recovery steps when action preconditions fail.

**Method:** Defines available functions and objects in the prompt so that generated plans follow the environment’s actual interfaces. Assertions encode checks of action prerequisites before execution. The central contributions are grounded planning and prerequisite checking; recovery depends on which situations the generated plan covers.

**Verification:** Program assertions and action-success feedback available to the model are different mechanisms.

<a id="work-2209-07753"></a>
<!-- stage3-record: {"id": "2209.07753", "scope": "Adjacent", "section": 1} -->

#### Code as Policies: Language Model Programs for Embodied Control

`2022-09-16` · Robotics at Google

[Paper](https://arxiv.org/abs/2209.07753) · [Project page](https://code-as-policies.github.io)

Recursively generates Python policies that combine perception results, geometric calculations and robot APIs.

**Method:** Represents robot policies as composable programs: conditionals, loops, geometric operations and function calls express task logic. Generated code connects language intent to existing robot capabilities, while interfaces supply perception and motion execution. This provides a program representation for later interactive coding agents; control primitives differ in granularity across experiments.

**Verification:** The generated program uses feedback; this does not establish that the language model observes every action and rewrites code.

### Delegation to existing policies

<a id="work-2611-03585"></a>
<!-- stage3-record: {"id": "2611.03585", "scope": "Adjacent", "section": 1} -->

#### Seeing Through the Illusion: Test-Time Scaling for World Action Models

`2026-11-02` · Huawei Technologies Canada; University of British Columbia

[Bibliographic record](../README.md#paper-2611-03585) · [Paper](https://arxiv.org/abs/2611.03585)

Selects frozen world–action model rollouts by combining action validity, inverse-dynamics agreement with imagined motion, and task progress, then executes the chosen action chunk and replans from fresh observations.

**Method:** Combines three signals to select rollouts from a frozen world–action model: action validity, agreement between inverse dynamics and imagined motion, and task progress. It executes the selected action chunk, obtains fresh observations and replans; the procedure changes inference-time selection rather than the frozen model.

**Verification:** RoboLab: 50 simulated episodes · LIBERO: 2,000 episodes per method · matched four-candidate comparisons · component and runtime analysis; small gains over the strongest matched-budget selectors.

<a id="work-system-the-harness-corl2026"></a>
<!-- stage3-record: {"id": "system:the-harness-corl2026", "scope": "Adjacent", "section": 1} -->

#### The Harness: One Agent Harness for Anything that Acts

`2026-11` · University of Michigan; Nanyang Technological University; EPFL; Princeton University; University of Virginia; LMMs-Lab

[Project page](https://web.eecs.umich.edu/~stellayu/publication/2026harnessCoRLL.html) · [Paper](https://web.eecs.umich.edu/~stellayu/publication/doc/2026harnessCoRLL.pdf)

Combines agent-written programs, bounded VLA skills and reactive guards in a shared control hierarchy.

**Method:** Programs compose analytic tools and served policies; generated guards run at control ticks, while unresolved events return to the model. A fixed shield rejects invalid commands.

**Verification:** RoboDojo simulation and component ablations; the short report supports event-driven orchestration, without establishing a full code-repair trajectory.

<a id="work-2610-42053"></a>
<!-- stage3-record: {"id": "2610.42053", "scope": "Adjacent", "section": 1} -->

#### REA: A Routed Embodied Agent Runtime for Asynchronous Brain-Cerebellum Control

`2026-10-30` · National University of Singapore, HPC-AI Lab; InfRec, Cardinal AI Lab; University of California, Berkeley; The University of Tokyo; Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences; Hong Kong University of Science and Technology

[Bibliographic record](../README.md#paper-2610-42053) · [Paper](https://arxiv.org/abs/2610.42053) · [Project page](https://mikeeeeeeeeeeeeee.github.io/REA/)

Separates fast robot execution from asynchronous model judging and route selection, coordinating fixed code policies and action models with visual outcome checks at policy-return boundaries.

**Method:** REA lets fast policies run at their own control rates without waiting for a slower large model at every action. REA-M routes through memory without an online high-level model; REA-A invokes an agent to select policies; REA-V visually checks outcomes when policies return. Comparing these configurations tests where high-level reasoning helps, rather than treating all three as continuous online programming.

**Verification:** 3,000 LIBERO-PRO episodes · shared recovery budgets · simulation versus small hardware studies · fixed test-time code and routing.

<a id="work-2610-21453"></a>
<!-- stage3-record: {"id": "2610.21453", "scope": "Adjacent", "section": 1} -->

#### CarryOn: A Dual-Loop Harness for Personalized and Reliable Robot Assistance

`2026-10-15` · Hong Kong University of Science and Technology; The Chinese University of Hong Kong; SmartMore

[Bibliographic record](../README.md#paper-2610-21453) · [Paper](https://arxiv.org/abs/2610.21453) · [Project page](https://vincent2311.github.io/Projects/CarryOn/) · [Code](https://github.com/JIA-Lab-research/CarryOn)

Coordinates persistent user/scene memory, a frozen VLA, geometric shielding, and visual failure recovery, while offline reflection revises recovery strategies and parameters for later attempts.

**Method:** CarryOn combines two loops: planning determines what remains to be done, while execution determines how to complete an operation reliably. Recovery often restores conditions in which the VLA can continue. Memory improves later plans and failure experience improves recovery skills; neither is equivalent to training the underlying VLA weights.

**Verification:** Preference-consistent planning · scene-memory correction · simulation and hardware safety/recovery tests · cumulative retry success, distinct from single-attempt success.

<a id="work-2609-29166"></a>
<!-- stage3-record: {"id": "2609.29166", "scope": "Core", "section": 1} -->

#### HarnessPAI: An Evolving Harness for Physical AI

`2026-09-24` · Xiaomi Inc.; Tsinghua University; Nanjing University; Shanghai Jiao Tong University; East China Normal University; University College London; King’s College London; Imperial College London; Institute of Automation, Chinese Academy of Sciences; Shanghai Innovation Institute; University of Oxford; University of Edinburgh; Nanyang Technological University

[Paper](https://arxiv.org/abs/2609.29166) · [Project page](https://darwin-agent.github.io/HarnessPAI)

Synthesizes programs over perception and motion primitives, then evolves them across rollouts and extracts reusable skills.

**Method:** HarnessPAI separates two timescales: a fixed program runs within a rollout, and program improvement happens between rollouts. Fixed code can still read sensors and check physical state. Task memories, repair skills and executable code accumulate separately so that later tasks can reuse validated execution methods.

**Verification:** A program is fixed within a rollout; feedback used inside that program differs from later LLM-driven program revision.

**Related:** [5. Training and Capability Improvement](#section-5)

<a id="work-2608-11246"></a>
<!-- stage3-record: {"id": "2608.11246", "scope": "Adjacent", "section": 1} -->

#### Towards the Harness of Embodied Agents

`2026-08-03` · Eastern Institute of Technology, Ningbo

[Paper](https://arxiv.org/abs/2608.11246) · [Project page](https://eit-hai.github.io/thea)

Uses a persistent scene graph and semantically meaningful tool returns to organize robot abilities and task progress.

**Method:** Thea transfers coding-agent tools, context, skills and memory organization to robots while adding the state and outcome semantics required for physical execution. Its purpose goes beyond consistent function names: the model needs to know what a call actually changed in the world. Tools may wrap existing code policies; knowledge-bearing skills and policies that execute actions have different roles.

**Verification:** Skills and existing policies execute below the agent; feedback specifies success or the cause of failure.

<a id="work-2607-08448"></a>
<!-- stage3-record: {"id": "2607.08448", "scope": "Adjacent", "section": 1} -->

#### Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents

`2026-07-09` · Tsinghua University; Striding AI; Purdue University; Institute of Automation, Chinese Academy of Sciences; Infinigence AI; Hong Kong University of Science and Technology; Zhongguancun Academy

[Paper](https://arxiv.org/abs/2607.08448)

Lets a coding agent combine analytic motion primitives with calls to a frozen VLA, assigning language subgoals, budgets and stopping conditions.

**Method:** Harness VLA wraps an existing VLA as a tool alongside other motion primitives. An agent can prepare the scene with analytic operations, delegate contact to the VLA, and reorganize execution after failure; task memory and general experience guide later choices. Delegation can be expressed directly in language without generating a new controller, while learned action capability remains in the frozen downstream policy.

**Verification:** After each call, images, depth, robot state and diagnostics inform whether to retry, change the scene or continue; VLA execution has its own observation loop.

### Agent capability evaluation

<a id="work-2611-12177"></a>
<!-- stage3-record: {"id": "2611.12177", "scope": "Adjacent", "section": 1} -->

#### Embodied First Exam

`2026-11-09` · Northwestern University; Carnegie Mellon University; University of California Berkeley; University of Washington; Stanford University; UNC-Chapel Hill; Texas A&M University; University of Texas at Austin

[Paper](https://arxiv.org/abs/2611.12177)

Tests general-purpose agents across robot embodiments while varying observation access, reset budgets and execution timing.

**Method:** Accepts direct actions, controller code or learned policies. Standard uses a separate simulator service with RGB-D, proprioception and action chunks; Realtime keeps the clock running; Privileged permits full-state access and unlimited resets before independent replay grading.

**Verification:** Hidden predicates and scene source remain outside Standard agents. Most suites still signal completion; removing that signal is a separate ablation. Results mix agent strategies and information regimes, so visual feedback does not establish code repair for every run.

**Related:** [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2611-08209"></a>
<!-- stage3-record: {"id": "2611.08209", "scope": "Adjacent", "section": 1} -->

#### RoboARCade: Benchmarking Agentic Robot Control

`2026-11-05` · Stanford University

[Bibliographic record](../README.md#paper-2611-08209) · [Paper](https://arxiv.org/abs/2611.08209) · [Project page](http://roboarcade.org)

Benchmarks visual robot-control agents on randomized long-horizon MuJoCo tasks, separating interface effects, in-context demonstrations and cross-trial text-harness optimization.

**Verification:** 22 tasks, three embodiments · hidden task predicates · control cost and false-success analysis · five-task adaptation study; simulated control and harness updates, not construction-code repair.

<a id="work-2611-02497"></a>
<!-- stage3-record: {"id": "2611.02497", "scope": "Adjacent", "section": 1} -->

#### RoboColosseum: Evaluating Physical Intelligence at Scale In-The-Wild

`2026-11-02` · National University of Singapore; University of Washington; Stanford University; University of North Carolina at Chapel Hill; Allen Institute for AI; University of Oxford; Hugging Face; BitRobot; Singapore Embodied AI Centre

[Bibliographic record](../README.md#paper-2611-02497) · [Paper](https://arxiv.org/abs/2611.02497) · [Project page](https://robocolosseum.ai/) · [Repository](https://github.com/RoboColosseum)

Compares frozen agents and VLA policies through matched, blinded real-robot trials across sites, with a separate adaptation track and explicit embodiment-dependent ranking analysis.

**Verification:** Matched local trials · human success assessment · cross-site/rank uncertainty · adaptation tracked separately.

<a id="work-2610-34649"></a>
<!-- stage3-record: {"id": "2610.34649", "scope": "Core", "section": 1} -->

#### RobotAgentBench: Towards Open-world Robot Autonomy

`2026-10-26` · Aether AI; University of California San Diego; University of California Davis

[Bibliographic record](../README.md#paper-2610-34649) · [Paper](https://arxiv.org/abs/2610.34649) · [Project page](https://aetherlabsai.github.io/RobotAgentBench/)

Benchmarks household robot autonomy with code-based, learned and hybrid executors, including visual-feedback-driven program execution and reusable control-tool refinement in its coding-agent configurations.

**Verification:** 50 simulated layouts · five task-level capabilities and four open-ended scenarios · matched sim/real subset · harness ablations; coding-agent and standalone-policy tracks are evaluated separately, with human-assisted scene calibration.

<a id="work-2610-34527"></a>
<!-- stage3-record: {"id": "2610.34527", "scope": "Adjacent", "section": 1} -->

#### LLM4Robot-Bench: How Far Can GPT-6 Astra Go in Robotic Manipulation? A Hierarchical, Paired Sim-Real Benchmark

`2026-10-25` · Tuojing Intelligence; The University of Hong Kong; Chinese Academy of Sciences; Nanyang Technological University; University of Michigan, Ann Arbor; Southeast University; Sapient Intelligence; SimpleAI; Mohamed bin Zayed University of Artificial Intelligence; Stanford University; Imperial College London; Tsinghua University; Carnegie Mellon University

[Bibliographic record](../README.md#paper-2610-34527) · [Paper](https://arxiv.org/abs/2610.34527) · [Code](https://github.com/LLM4Robot/LLM4Robot-Bench) · [Project page](https://llm4robot.github.io/bench/)

Originally released as PhysLadder, this benchmark tests GPT-6 Astra on geometric alignment, force regulation and contact reconfiguration in matched simulated and real dual-arm tasks.

**Verification:** 16 tasks · three trials per task/environment · shared outcome criteria · physical/visual matching and failure analysis; single-model evidence, with different real/sim execution budgets.

<a id="work-2610-30051"></a>
<!-- stage3-record: {"id": "2610.30051", "scope": "Adjacent", "section": 1} -->

#### From Reasoning to Action: Benchmarking Frontier AI Models on LIBERO-10 Robot Manipulation Tasks

`2026-10-21` · The University of Texas at Dallas

[Paper](https://arxiv.org/abs/2610.30051) · [Project page](https://irvlutd.github.io/LLM-LIBERO/) · [Code](https://github.com/IRVLUTD/LLM_LIBERO)

Compares frontier models on LIBERO-10 using a shared interaction loop and control interface.

**Verification:** A controlled interface helps distinguish model differences from changes to the robot harness.

<a id="work-2610-27039"></a>
<!-- stage3-record: {"id": "2610.27039", "scope": "Adjacent", "section": 1} -->

#### Embodied Playground: A Long-Horizon Agentic Robotics Benchmark for Physical, Strategic, and Spatial Reasoning

`2026-10-19` · The University of Hong Kong; Sharpa; Tsinghua University; Stanford University; University of North Carolina at Chapel Hill; Massachusetts Institute of Technology; Transcengram

[Paper](https://arxiv.org/abs/2610.27039) · [Project page](https://winniechen2002.github.io/Agent-bench-website/)

Tests coordination of physical, strategic and spatial reasoning in long-horizon robot tasks.

**Verification:** Task progress and execution feedback are central; environment presence does not make this a simulator-quality benchmark.

<a id="work-2610-25287"></a>
<!-- stage3-record: {"id": "2610.25287", "scope": "Adjacent", "section": 1} -->

#### The Bitter Lesson Comes to Robotics

`2026-10-18` · Robocurve; University of Southern California; University of California, Irvine

[Paper](https://arxiv.org/abs/2610.25287)

Studies general multimodal models operating physical robot arms through control interfaces.

**Verification:** Compares nine models in 15 configurations on six real bimanual RoboDojo tasks, with 20 trials per task and a 40-action budget. Camera-video grading records the highest cumulative subtask progress reached, even if later undone; time and API cost include unsuccessful attempts. Partial-progress scores therefore differ from retained final-state success, and complete tasks remain difficult within the budget.

<a id="work-2610-22471"></a>
<!-- stage3-record: {"id": "2610.22471", "scope": "Adjacent", "section": 1} -->

#### Has GPT-6-Astra Achieved Embodied Intelligence?

`2026-10-15` · SenseNova and Joint Research Team

[Bibliographic record](../README.md#paper-2610-22471) · [Paper](https://arxiv.org/abs/2610.22471) · [Article](https://sensenova.ai/has-gpt-6-astra-achieved-embodied-intelligence)

Studies demonstration-informed direct control and VLA-action review across twelve embodied benchmarks, separating gains from extended interaction budgets from zero-shot trials on eight real robot configurations.

**Verification:** Standard versus up-to-10× step budgets · frozen in-context knowledge · action-interface and token-cost ablations · human context/safety supervision · hardware contact, latency, and recovery limits.

<a id="work-2610-16238"></a>
<!-- stage3-record: {"id": "2610.16238", "scope": "Adjacent", "section": 1} -->

#### Embodied Skill Bench: Benchmarking How Well Agents with Embodied Skills Perform on Physical Tasks

`2026-10-12` · Shanghai Jiao Tong University; Shanghai Artificial Intelligence Laboratory; Sun Yat-Sen University; Jilin University; Beihang University

[Paper](https://arxiv.org/abs/2610.16238) · [Code](https://github.com/HanZhi306/EmbodiedSkill-Bench)

Compares native control, skill-only execution and agent selection or modification of embodied skills.

**Method:** EmbodiedSkillBench makes the capabilities supplied to an agent an experimental variable. Skill packages combine instructions, scripts, reference knowledge and configuration, allowing models, code and experience to be composed as needed. It compares agents and skill sets under a shared task protocol, rather than proposing a separate motion-control algorithm.

**Verification:** Skill packages may contain code, instructions or action-model calls; hidden scoring signals are not necessarily agent inputs.

<a id="work-2610-10409"></a>
<!-- stage3-record: {"id": "2610.10409", "scope": "Adjacent", "section": 1} -->

#### RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments

`2026-10-07` · The Hong Kong University of Science and Technology; The Chinese University of Hong Kong; Peking University; Stanford University; University of California, Berkeley; National University of Singapore; Massachusetts Institute of Technology; Tsinghua University; Carnegie Mellon University; Fudan University; The University of Hong Kong

[Bibliographic record](../README.md#paper-2610-10409) · [Paper](https://arxiv.org/abs/2610.10409) · [Code](https://github.com/robotworldai/robotworld) · [Project page](https://robotworldai.github.io/)

Evaluates image- and state-grounded robot tool use across 84 simulated tasks and diverse embodiments, separating auxiliary computation from optional environment-side control code.

**Verification:** Hidden-checker task success · action/non-action budgets · perception/control failures · cross-embodiment coverage.

<a id="work-2610-07594"></a>
<!-- stage3-record: {"id": "2610.07594", "scope": "Adjacent", "section": 1} -->

#### BiGym 2.0: Benchmarking Learned and Agent-Developed Policies for Humanoid Household Manipulation

`2026-10-06` · Imperial College London

[Paper](https://arxiv.org/abs/2610.07594) · [Code](https://github.com/swirl-uk/BiGym2)

Compares learned and agent-developed humanoid policies under matched onboard observations and whole-body controllers.

**Verification:** Released VR demonstrations come from simulation; paired observation interfaces matter when comparing policy families.

<a id="work-2610-00854"></a>
<!-- stage3-record: {"id": "2610.00854", "scope": "Adjacent", "section": 1} -->

#### Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena

`2026-10-01` · The Hong Kong University of Science and Technology (Guangzhou); The Chinese University of Hong Kong; Knowin AI

[Paper](https://arxiv.org/abs/2610.00854) · [Project page](https://embodied-agent-arena.github.io/embodied-agent-arena/)

Compares frontier VLM robot agents under shared budgets and source-task interfaces.

**Verification:** Repairing a program so that it runs and completing the physical task are evaluated separately.

<a id="work-2609-40325"></a>
<!-- stage3-record: {"id": "2609.40325", "scope": "Adjacent", "section": 1} -->

#### WorldAuditBench: Interactive 3D World Auditing with Multimodal Agents

`2026-09-30` · University of California Santa Barbara; MIT CSAIL; MIT-IBM Watson AI Lab

[Bibliographic record](../README.md#paper-2609-40325) · [Paper](https://arxiv.org/abs/2609.40325) · [Project page](https://ucsb-nlp-chang.github.io/WorldAuditBench/)

Measures an agent’s ability to explore interactive worlds and substantiate anomalies with evidence.

**Method:** Compares a VLM that chooses actions, retrieves observations and updates reports with VLA exploration followed by offline VLM analysis; rubric-based grading checks the final report and supporting views.

**Verification:** The output is an audit report, not repaired scene code. Main tasks include anomaly-type hints; paradigms use different exploration budgets, and model comparisons include their harnesses.

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2609-39507"></a>
<!-- stage3-record: {"id": "2609.39507", "scope": "Adjacent", "section": 1} -->

#### LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation

`2026-09-30` · Fudan University; Shanghai Innovation Institute

[Paper](https://arxiv.org/abs/2609.39507)

Turns LIBERO into an interactive setting where general agents inspect observations, use their own tools and issue native actions.

**Verification:** The 30-task primary simulation suite separates perception, short-horizon manipulation and long-horizon composition within a 200-task framework. Primary runs use full observations, no demonstrations and a 1,800-second wall-clock limit; agents compose bounded native action sequences while a separate evaluator retains private task checkers. Performance drops on harder and longer tasks, so easy-task success does not establish broad manipulation reliability.

<a id="work-2609-33807"></a>
<!-- stage3-record: {"id": "2609.33807", "scope": "Core", "section": 1} -->

#### CodeActionBench: Evaluating Agentic Code-as-Policy for Embodied Manipulation

`2026-09-27` · Nanyang Technological University

[Bibliographic record](../README.md#paper-2609-33807) · [Paper](https://arxiv.org/abs/2609.33807) · [Code](https://github.com/lyhkk/CodeActionBench) · [Project page](https://codeactionbench.org/)

Agents execute Python manipulation programs in RoboTwin 2.0 simulation and use camera views, robot state, and contact feedback to revise their policies. A hidden verifier checks the final state independently of the agent’s completion claim.

**Method:** CodeActionBench checks code execution, physical task fulfillment and the reliability of completion declarations. A shared interface supplies observations, geometric computation and constrained motion to different models, while each model organizes the task. Physical outcomes come from simulation; evaluation from fixed initial scenes does not establish broad real-world generalization.

**Verification:** 25 fixed simulated tasks · hidden outcome checks · spatial progress and failure stage · completion-claim accuracy · tool-call and simulated-time budgets.

<a id="work-2609-01404"></a>
<!-- stage3-record: {"id": "2609.01404", "scope": "Adjacent", "section": 1} -->

#### Evaluating Multimodal LLMs as Generalist Vision-Language-Action Agents for Drone Control: Commanding, Approaching, Tracking and Searching

`2026-09-01` · Drone AI Team, NAVER Cloud

[Bibliographic record](../README.md#paper-2609-01404) · [Paper](https://arxiv.org/abs/2609.01404) · [Code](https://github.com/naver-ai/DroneCATS) · [Dataset](https://huggingface.co/datasets/naver-ai/DroneCATS-Pilot-54K)

Evaluates image-conditioned drone actions and commander–sub-agent coordination across simulators and real Tello flights, exposing latency and arrival-declaration failures.

**Method:** Tests how multimodal models convert visual observations into drone actions and coordinate a commander with sub-agents. The task suite covers commanding, approaching, tracking and searching in simulation and real Tello flights, with execution latency and arrival declarations examined as distinct failure sources.

**Verification:** Ten-model simulated benchmark · 100 single-drone and 18 two-drone real episodes · small per-cell samples; 54K RGB-D-derived supervision is not real-flight trajectory data.

<a id="work-2607-04434"></a>
<!-- stage3-record: {"id": "2607.04434", "scope": "Resource", "section": 1} -->

#### RoboDojo: A Unified Sim-and-Real Benchmark for Comprehensive Evaluation of Generalist Robot Manipulation Policies

`2026-07-05` · MMLab@HKU; UC Berkeley; THU; PKU; Stanford; MIT; UNC; Princeton; CMU; NUS; NTU; CUHK; IC; SJTU; NU; HKUST (GZ); ZJU; Yale

[Paper](https://arxiv.org/abs/2607.04434) · [Project page](http://robodojo-benchmark.com/) · [Project page](https://robodojo-benchmark.com/) · [Code](https://github.com/RoboDojo-Benchmark/RoboDojo) · [Leaderboard](https://robodojo-benchmark.com/leaderboard)

Offers paired simulation and real-robot protocols for manipulation across tasks and environments.

**Verification:** Used to evaluate transfer of code-policy agents; simulation scores and hardware success remain separate measures.

<a id="work-2604-25788"></a>
<!-- stage3-record: {"id": "2604.25788", "scope": "Resource", "section": 1} -->

#### KinDER: A Physical Reasoning Benchmark for Robot Learning and Planning

`2026-04-28` · University of Cambridge; Georgia Institute of Technology; Princeton University; NVIDIA; Massachusetts Institute of Technology; Carnegie Mellon University

[Paper](https://arxiv.org/abs/2604.25788) · [Project page](https://prpl-group.com/kinder-site/)

Provides resettable physical-reasoning tasks, parameterized skills and an evaluation interface for planning and learning.

**Verification:** A supporting benchmark used by coding-agent task-and-motion planning studies, not itself a new agent.

<a id="work-2603-22435"></a>
<!-- stage3-record: {"id": "2603.22435", "scope": "Core", "section": 1} -->

#### CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation

`2026-03-23` · NVIDIA; University of California, Berkeley; Stanford University; Carnegie Mellon University

[Bibliographic record](../README.md#paper-2603-22435) · [Paper](https://arxiv.org/abs/2603.22435)

Benchmarks and improves agents that write manipulation code, execute it, observe outcomes, and repair failed behaviors.

**Verification:** Compilation success · dense task reward · task success · privileged-vs-RGB-D robustness.

<a id="work-2601-20334"></a>
<!-- stage3-record: {"id": "2601.20334", "scope": "Adjacent", "section": 1} -->

#### Demonstration-Free Robotic Control via LLM Agents

`2026-01-28` · Independent researchers

[Paper](https://arxiv.org/abs/2601.20334) · [Code](https://github.com/robiemusketeer/faea-sim)

Connects a software-engineering agent framework directly to robot control without demonstrations.

**Verification:** The evaluated configuration can access privileged environment state; it is not a sensor-only deployment result.

<a id="work-2601-19510"></a>
<!-- stage3-record: {"id": "2601.19510", "scope": "Adjacent", "section": 1} -->

#### ALRM: Agentic LLM for Robotic Manipulation

`2026-01-27` · Technology Innovation Institute; Dublin City University

[Paper](https://arxiv.org/abs/2601.19510)

Compares control-code generation with stepwise tool use within a shared ReAct manipulation framework.

**Verification:** Language-varied tasks compare execution interfaces; do not attribute interface changes solely to the model.

<a id="work-2402-14623"></a>
<!-- stage3-record: {"id": "2402.14623", "scope": "Adjacent", "section": 1} -->

#### RoboScript: Code Generation for Free-Form Manipulation Tasks across Real and Simulation

`2024-02-22` · OpenGVLab, Shanghai AI Laboratory; ETH Zurich; The University of Hong Kong; Shanghai Jiao Tong University; Tsinghua University; University of California, Berkeley

[Paper](https://arxiv.org/abs/2402.14623)

Connects free-form robot code generation to ROS, perception and motion tools across simulation and real hardware.

**Method:** RoboScript exposes complex robot systems through object-oriented perception and motion APIs. To open a drawer, for example, the program queries the prismatic-joint direction and uses it to organize a pulling path, while the motion-planning backend handles obstacles and trajectory solving. The language model combines task-relevant geometry without reimplementing low-level robotics algorithms.

**Verification:** Simulation execution and real-robot deployment expose different sources of failure.

<a id="work-2311-11183"></a>
<!-- stage3-record: {"id": "2311.11183", "scope": "Adjacent", "section": 1} -->

#### Deploying and Evaluating LLMs to Program Service Mobile Robots

`2023-11-18` · The University of Texas at Austin; Northeastern University; Wellesley College

[Paper](https://arxiv.org/abs/2311.11183) · [Project page](https://amrl.cs.utexas.edu/codebotler/)

CodeBotler generates service-robot programs in a Python-embedded language; RoboEval tests action order, conditions and task execution.

**Verification:** Program validity and successful physical execution are separate outcomes.

<a id="work-2306-03310"></a>
<!-- stage3-record: {"id": "2306.03310", "scope": "Resource", "section": 1} -->

#### LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning

`2023-06-05` · The University of Texas at Austin; Sony AI; Tsinghua University

[Paper](https://arxiv.org/abs/2306.03310) · [Project page](https://libero-project.github.io)

Provides resettable manipulation tasks, demonstrations and shared interfaces for studying lifelong transfer.

**Verification:** An execution and evaluation substrate used by code-policy agents; the benchmark itself is not a coding-agent method.

### Skills, bridges and runtime resources

<a id="work-kinex"></a>
<!-- stage3-record: {"id": "kinex", "scope": "Resource", "section": 1} -->

#### Kinex

`2026-10-15` · Affiliation not established

[Code](https://github.com/stacx-lab/kinex)

Organizes devices, tools, skills and session execution into a robot runtime with simulation and hardware adapters.

**Verification:** Supported adapters and published examples bound the available functionality.

<a id="work-qwen-mhs"></a>
<!-- stage3-record: {"id": "qwen-mhs", "scope": "Resource", "section": 1} -->

#### Qwen-MM-Plugins — MHS

`2026-09-20` · Affiliation not established

[Code](https://github.com/QwenLM/Qwen-MM-Plugins) · [Project page](https://qwenlm.github.io/qwen-mm-plugins-hub/plugins/mhs/cookbook/)

Packages physical-device operations as multimodal-agent plugins with documented hardware workflows.

**Verification:** The entry concerns MHS hardware capabilities, not every plugin in the broader collection.

<a id="work-safe-lab-agents"></a>
<!-- stage3-record: {"id": "safe-lab-agents", "scope": "Resource", "section": 1} -->

#### Safe Lab Agents

`2026-07` · Affiliation not established

[Code](https://github.com/MaxNaeg/safe_lab_agents) · [Project page](https://safe-lab-agents.org/)

Lets isolated coding agents write scan and analysis scripts and call laboratory tools through host-side MCP and Python interfaces.

**Verification:** The public optical example simulates its power measurements; hardware connectivity is distinct from that example's evidence.

<a id="work-2505-03728"></a>
<!-- stage3-record: {"id": "2505.03728", "scope": "Resource", "section": 1} -->

#### PyRoki: A Modular Toolkit for Robot Kinematic Optimization

`2025-05-06` · University of California, Berkeley

[Paper](https://arxiv.org/abs/2505.03728) · [Project page](https://pyroki-toolkit.github.io)

Provides composable kinematic optimization interfaces that realize agent-selected targets and motion programs.

**Verification:** A solver resource: control and optimization capabilities should not be attributed to the language model.

<a id="work-phys-0"></a>
<!-- stage3-record: {"id": "phys-0", "scope": "Resource", "section": 1} -->

#### phys-0

`First-public date not established` · Affiliation not established

[Project page](https://jvboid.dev/projects/phys-0) · [Code](https://github.com/JacobFV/chem-0)

Connects editable physical scenes, a SO-101 arm and laboratory observations through logged agent tools.

**Verification:** The author distinguishes animation, screen recordings and camera observations; verified hardware support is limited to SO-101.

<a id="work-vbot-lab"></a>
<!-- stage3-record: {"id": "vbot-lab", "scope": "Resource", "section": 1} -->

#### VBOT Lab

`First-public date not established` · Affiliation not established

[Code](https://github.com/VitaDynamics/vbot-lab)

Provides API definitions, examples and skills for coding agents developing applications on VBOT robots.

**Verification:** Support is bounded by the published EDU quadruped hardware and software versions.

<a id="work-robotics-agent-skills"></a>
<!-- stage3-record: {"id": "robotics-agent-skills", "scope": "Resource", "section": 1} -->

#### Robotics Agent Skills

`First-public date not established` · Affiliation not established

[Code](https://github.com/arpitg1304/robotics-agent-skills)

Provides reusable skill files for ROS development, diagnosis and robotics workflows.

**Verification:** Documentation supports reuse; a prompt example alone does not demonstrate general performance improvement.

<a id="work-robouse"></a>
<!-- stage3-record: {"id": "robouse", "scope": "Resource", "section": 1} -->

#### Robo Use

`First-public date not established` · Affiliation not established

[Code](https://github.com/benchflow-ai/robouse)

Exposes robot simulation tasks, actions and episode results through a shared CLI and service interface.

**Verification:** Current interfaces and examples primarily concern simulated tasks.

<a id="work-rosclaw"></a>
<!-- stage3-record: {"id": "rosclaw", "scope": "Resource", "section": 1} -->

#### ROSClaw

`First-public date not established` · Affiliation not established

[Code](https://github.com/ros-claw/rosclaw)

Connects coding agents to ROS workspaces through execution receipts, state interfaces and robot programs.

**Verification:** The project is alpha; demonstrated adapter support should not be generalized to every robot.

<a id="work-ros-mcp-server"></a>
<!-- stage3-record: {"id": "ros-mcp-server", "scope": "Resource", "section": 1} -->

#### ROS MCP Server

`First-public date not established` · Affiliation not established

[Code](https://github.com/robotmcp/ros-mcp-server)

Exposes ROS topics, services, actions and sensor images to coding-agent clients through MCP.

**Verification:** The bridge provides access; task planning, control and completion remain responsibilities of the connected system.

<a id="work-nvidia-robot-skills"></a>
<!-- stage3-record: {"id": "nvidia-robot-skills", "scope": "Resource", "section": 1} -->

#### NVIDIA Agent Skills — Physical AI and Robotics

`First-public date not established` · Affiliation not established

[Code](https://github.com/NVIDIA/skills)

Provides procedural skills for robot development, Isaac simulation, data pipelines and digital-twin validation.

**Verification:** Only the physical-AI and robotics workflows are relevant here; skill documentation is not a performance benchmark.

<a id="work-dimos"></a>
<!-- stage3-record: {"id": "dimos", "scope": "Resource", "section": 1} -->

#### DimOS

`First-public date not established` · Affiliation not established

[Code](https://github.com/dimensionalOS/dimos)

Combines Python modules, perception streams and robot control interfaces into a runtime that agents can orchestrate.

**Verification:** Documented interfaces and examples define available capabilities; no additional hardware replication is claimed here.

### Cross-section reading

- [One Policy for 100 Household Tasks: Our Solution for the 2026 BEHAVIOR Challenge](#work-2611-14432)
- [World In-Context Learning for Agentic Robot Manipulation](#work-2611-12885)
- [Spatial Harness: Grounding Spatial Reasoning in Executable World States with Physics Engines](#work-2611-11344)
- [BlenderFORGE: Framework for Optimizing Reactive 3D-Graphics Editing Ability of MLLMs](#work-2611-10768)
- [PCBRouteAgent: How Close Are LLM Agents to Becoming PCB Routing Engineers?](#work-2611-08175)
- [PyRUA-REAL: Robot Exploration and Adaptive Learning through RSI in the Real World](#work-2611-06768)
- [Open-HumanWAM: An Open Recipe for Scaling Human and Robot Experience for Embodied Foundation Models](#work-2611-06817)
- [WorldSketch: Sketching World Models for Zero-Shot Mobile Manipulation](#work-2611-00513)
- [TinyAstral: Transferring Self-Evolving Harnesses to Tiny Generalist Manipulation Agents](#work-2610-41216)
- [RoboArchitect: Automating the Design of Robotic Agents with Persistent Memory](#work-2610-42141)
- [DyCraft: An Agentic System for Long-Horizon 4D Scene Generation](#work-2610-40754)
- [CaPtain: A Pipeline for Post-Training Code-as-Policy Robot Agents](#work-2610-40799)
- [RoboAuto: Autonomous Robot Program Search through Multi-Level Physical Understanding](#work-2610-36533)
- [Plumb: Coding Agents with 3D Perception Rebuild Physical Scenes from Video](#work-system-plumb)
- [From VLM Planners to Robotic Agents: Self-Evolving Harnesses for History-Dependent Manipulation](#work-2610-29560)
- [Agentic World Action Models](#work-2610-30136)
- [AgenticRoboRL: Bringing Coding-Agent Post-Training to Agentic Robotics](#work-2610-28589)
- [Compile Once, Run Cheap: Frozen, Portable Skills for Embodied Agents, and What Recursive Self-Improvement Adds](#work-2610-25114)
- [InstAgent: A Recursively Self-Improving Agent Operating System for Heterogeneous Robot Collaboration](#work-2610-23098)
- [CoEvolve: Self-Evolving Code Policies from Skills to Strategies for Humanoid Robots](#work-2610-23288)
- [Scaling Online Exploration for Robot Agents](#work-2610-22496)
- [Spatial Memory by Agents, for Agents](#work-2610-22736)
- [RoboSimStudio: An Interactive Toolkit for Human and Agent Rapid Real2Sim of Robot Manipulation Tasks](#work-2610-18835)
- [SEAR: Self-Evolving Agentic Robotics](#work-2610-18792)
- [EmbodiedEvo: Self-Evolving Coding Agent For Physical Intelligence](#work-2610-18867)
- [ChunkAct: Action Chunking for Agentic Robotics](#work-2610-18874)
- [Harness^2: Recursive Agent Harnessing for an Open World](#work-2610-14224)
- [Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](#work-2610-12369)
- [Adaptive Code Generation for Controlling Robots](#work-2610-09588)
- [EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution](#work-2610-10498)
- [PhysEvo: Astra Can Act, Let It](#work-2610-08995)
- [Recova: Agent-Guided Failure Recovery for Autonomous Robotic Manipulation](#work-2610-01178)
- [Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents](#work-2610-02204)
- [SimEX: Simulation-Integrated Robotics AutoResearch](#work-2609-38982)
- [Make Code as Policy Great Again: Frontier Agents Write, Call, and Evolve Robot Tools](#work-2609-39018)
- [ASENA: Self-evolving Agents for Embodied Navigation](#work-2609-39207)
- [Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents](#work-2609-39304)
- [DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents](#work-2609-40306)
- [RoboHarn-Evo: Evolving Hierarchical Physical Knowledge for Self-Improving Robotic Manipulation](#work-2609-37583)
- [Self-Evolving Coding Agents: From Digital Programs to Physical-World Intelligence](#work-2609-35432)
- [Recursive Harness Distillation across Agents for Robot Manipulation](#work-2609-33378)
- [RoboFoundry: System-as-Policy Evolution for Self-Learning Embodied Agents](#work-2609-32862)
- [RACaP: Agentic Reasoning, Acting, and Coding as Policies for Evolvable Robot Learning](#work-2609-29394)
- [Coding Agents for Generalized Task and Motion Planning Problems](#work-2609-30233)
- [HuGo: LLMs as Whole-Body Policy Code Designers for Humanoid Loco-Manipulation](#work-2609-30594)
- [EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics](#work-2609-27308)
- [What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery](#work-2609-31760)
- [MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation](#work-2609-24145)
- [Zetta $ζ$: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence](#work-2608-16590)
- [Self-Evolving Embodied Agents via Skill-Harness Evolution](#work-2608-11350)
- [Skills in Weights, Memory in Code: Hybrid Learning for Memory-Dependent Robot Manipulation](#work-2608-09410)
- [You Don't Need To Stay in The Loop: An Agentic Robotics Loop for Robot-Policy Improvement](#work-2608-07555)
- [A Few Words Go a Long Way: Language Guided Robot Policy Synthesis](#work-2607-23784)
- [LabRobFail: A Benchmark for Robotic Failure Analysis in Chemical Self-driving Laboratory](#work-2607-23704)
- [Stress-testing large language model agents in a robotic chemistry laboratory](#work-2607-23045)
- [EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI](#work-2607-07459)
- [ASPIRE: Agentic /Skills Discovery for Robotics](#work-2607-00272)
- [ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](#work-2606-19980)
- [Playful Agentic Robot Learning](#work-2606-19419)
- [Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness](#work-2606-18363)
- [RHO: Your Coding Agent is Secretly a Roboticist](#work-2606-16458)
- [HARBOR: A Harness Framework for Agentic Robot Reinforcement Learning](#work-2606-08610)
- [PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification](#work-2606-04226)
- [ChronoAgentic: A Code-based Multi-Agent World Simulator for Physically Grounded Simulation Construction](#work-2605-14398)
- [EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents](#work-2605-10332)
- [SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning](#work-2605-09423)
- [Uni-Skill: Building Self-Evolving Skill Repository for Generalizable Robotic Manipulation](#work-2603-02623)
- [Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation](#work-2603-04466)
- [Robotic Ultra-Long-Horizon Manipulation Skills via Human-guided Lifelong Code Generation](#work-2509-18597)
- [HyCodePolicy: Hybrid Language Controllers for Multimodal Monitoring and Decision in Embodied Agents](#work-2508-02629)
- [RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation](#work-2506-18088)
- [INPROVF: Leveraging Large Language Models to Repair High-level Robot Controllers from Assumption Violations](#work-2503-13660)
- [Robotic Programmer: Video Instructed Policy Code Generation for Robotic Manipulation](#work-2501-04268)
- [Creating and Repairing Robot Programs in Open-World Domains](#work-2410-18893)
- [ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation](#work-2409-01652)
- [A Multiagent-Driven Robotic AI Chemist Enabling Autonomous Chemical Research On Demand](#work-chemagents)
- [Lifelong Robot Library Learning: Bootstrapping Composable and Generalizable Skills for Embodied Control with Language Models](#work-2406-18746)
- [RoboCoder: Robotic Learning from Basic Skills to General Tasks with Large Language Models](#work-2406-03757)
- [DrEureka: Language Model Guided Sim-To-Real Transfer](#work-2406-01967)
- [InterPreT: Interactive Predicate Learning from Language Feedback for Generalizable Task Planning](#work-2405-19758)
- [Evaluating Real-World Robot Manipulation Policies in Simulation](#work-2405-05941)
- [RoboCodeX: Multimodal Code Generation for Robotic Behavior Synthesis](#work-2402-16117)
- [Code as Reward: Empowering Reinforcement Learning with VLMs](#work-2402-04764)
- [Eureka: Human-Level Reward Design via Coding Large Language Models](#work-2310-12931)
- [Text2Reward: Reward Shaping with Language Models for Reinforcement Learning](#work-2309-11489)
- [Language to Rewards for Robotic Skill Synthesis](#work-2306-08647)
- [Demo2Code: From Summarizing Demonstrations to Synthesizing Code via Extended Chain-of-Thought](#work-2305-16744)
- [mujoco-workbench](#work-mujoco-workbench)
- [autoresearch-robotics](#work-autoresearch-robotics)
- [An agentic artificially intelligent X-ray scientist](#work-xray-scientist)

[Back to the research map](#research-map)

---

<a id="section-2"></a>

## 2. Simulator Construction

This section asks what an agent must construct before a physical task can be executed and checked. An environment may be an articulated object, a scene, a task API, a task-specific world sketch or a dynamic model. These products offer different guarantees: a good rendering, an executable reset, a stable contact model and a useful policy-training environment are separate achievements.

| Layer | What is constructed | What to inspect |
|---|---|---|
| Scene and assets | Geometry, object identities, scale, articulation, placement and support relations | Editable structure, coordinates, collision geometry and correspondence to observations |
| Physical properties | Mass, inertia, friction, restitution, material laws and contact parameters | Whether parameters are inferred, measured or fitted from interaction; which motions they explain |
| Task interface | Reset states, observations, actions, rewards, success checks and termination | Whether a task can be replayed, whether its checks match the intended behavior, and what controller assumptions it makes |
| Rendering and sensing | Cameras, illumination, materials, sensor outputs and overlays | Visual consistency and whether rendered evidence actually enters construction-time decisions |
| Simulator and solver | Scene formats, execution APIs, integration and contact or deformation solvers | Distinguish the authoring platform from the physics backend; a USD, URDF or MJCF export is not itself a solver |

**Real-to-Sim** starts with a particular observed object, scene or interaction and reconstructs a representation of it. **Generative construction** starts with requirements, goals or design conditions and produces new assets, scenes or tasks. A reconstruction system may use a generative mesh model, and a generative system may retrieve real assets: the source label describes the construction objective. Methods that demonstrably support both retain both labels. Grounding existing digital assets is identified separately when it neither reconstructs a specific observed scene nor generates a new environment.

The records below form one reverse-chronological sequence, using the earliest documented public date where available. Origin, output and engine labels support comparison without splitting methods into competing taxonomies. The expanded abstracts are concise reading notes; the linked papers and projects supply the complete accounts.

Early task generators such as [GenSim](https://arxiv.org/abs/2310.01361) and [RoboGen](https://arxiv.org/abs/2311.01455) connect environment programs to demonstrations, rewards and policy learning. [Real2Code](https://arxiv.org/abs/2406.08474) and [Articulate Anything](https://arxiv.org/abs/2410.13882) make articulated object structure executable. Later systems combine scene editing, physical checks and more targeted repair. These are useful lines of comparison, not a claim that every newer method inherits a single pipeline.

Two recent contrasts help read the catalogue. [WorldSketch](https://arxiv.org/abs/2611.00513) builds only the kinematic structure needed by a planner, whereas [CUE](https://arxiv.org/abs/2611.02691) collects interaction evidence to fit dynamics. [Spatial Harness](https://arxiv.org/abs/2611.11344) uses an executable geometric proxy for spatial reasoning; invoking a physics engine does not turn that proxy into a calibrated dynamic twin. The appropriate fidelity depends on the intended computation.

Construction feedback belongs to the generation procedure: a render, compiler error, geometric probe or failed rollout may trigger an edit. Final quality evaluation asks whether the accepted environment remains useful under independent conditions. Section 3 separates those two roles. Sections 4 and 5 then distinguish using an environment to generate training examples, updating a downstream controller, accumulating external skills and training the coding model itself. A central open question is which environment errors most affect agent learning, and which construction-time checks reliably predict that effect.

**Composable resources.** These existing resources supply appearance generation, runtime access or reusable procedures. They are counted separately from construction methods. PBR appearance parameters do not substitute for contact, inertia or material calibration.

| Resource | Contribution to construction | Availability and interpretation |
|---|---|---|
| [UltraTex](../README.md#paper-res-ultratex-2k-multi-view-diffusion) · [paper](https://arxiv.org/abs/2609.23169) · [code](https://github.com/YiboZ2001/UltraTex) | Reference image and mesh cues → 2K multiview textures with a PBR extension | Surface-appearance component; code and G-buffer data accompany the method |
| [MIKU](../README.md#paper-res-miku) · [paper](https://arxiv.org/abs/2611.07354) | Reference image and geometry → aligned albedo, metallic and roughness maps | Paper-described material capability; code and weights are not linked; generated maps are not measured physical properties |
| [WorldFoundry](../README.md#paper-res-worldfoundry) · [source](https://github.com/OpenEnvision/WorldFoundry) | CLI, Studio and adapters → model execution, artifacts and evaluation workflows | Shared infrastructure with model-specific requirements and explicit readiness; does not itself establish a scene's physical accuracy |
| [Unreal Engine 5.9 MegaJam Preview](../README.md#paper-res-unreal-engine-5-9-megajam-preview) · [official announcement](https://forums.unrealengine.com/t/unreal-engine-5-9-megajam-preview/2852840) | Unreal MCP and Canvas → editor operations, render/debug feedback and composed generation tools | Experimental platform interfaces; an integration announcement, not an autonomous-construction benchmark |
| [blender-agent-skills](../README.md#paper-res-blender-agent-skills) · [source](https://github.com/oh-ashen-one/blender-agent-skills) | Reference and scene → staged construction, visual gates, rig and export checks | Five community expert procedures; reusable external skills, without demonstrated model learning |

<a id="work-2611-11344"></a>
<!-- stage3-record: {"id": "2611.11344", "scope": "Adjacent", "section": 2} -->

#### Spatial Harness: Grounding Spatial Reasoning in Executable World States with Physics Engines

`2026-11-08` · Hong Kong Baptist University; ByteDance Seed

[Bibliographic record](../README.md#paper-2611-11344) · [Paper](https://arxiv.org/abs/2611.11344) · [Code](https://github.com/tmlr-group/Spatial-Harness)

An executable proxy scene grounds spatial reasoning in explicit geometry.

**Method:** A perceiver merges language constraints and visual estimates into object and camera poses. A reasoner calls Python measurements and viewpoint operations in MuJoCo, using numeric results and rendered views.

**Construction flow:** Images and question → Constraints and visual estimates → Shared proxy world → Measurements and viewpoint changes → Grounded answer

**Origin / output / platform:** Real-to-Sim (task-specific spatial proxy) · Executable object and camera state · MuJoCo

**Verification:** Four spatial benchmarks include matched ground-truth-layout controls and perception/feedback ablations. Proxy dimensions are not real-object measurements; static reasoning does not establish dynamics or robot-control fidelity.

<details>
<summary>Abstract summary</summary>

An executable proxy scene grounds spatial reasoning in explicit geometry. A perceiver merges language constraints and visual estimates into object and camera poses. A reasoner calls Python measurements and viewpoint operations in MuJoCo, using numeric results and rendered views.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3)

<a id="work-2611-10602"></a>
<!-- stage3-record: {"id": "2611.10602", "scope": "Adjacent", "section": 2} -->

#### Agentic discrete-event simulation for manufacturing system design: an open 3D simulator, a benchmark and an industrial case

`2026-11-07` · Universidade da Coruña; CITENI; Grupo Integrado de Ingeniería

[Paper](https://arxiv.org/abs/2611.10602)

SimuLean gives agents verified modeling components for manufacturing simulation.

**Method:** Domain commands construct one Unity model for 3D and headless execution; calibrated operation durations accelerate repeated studies. Independent reference models test the resulting system semantics.

**Construction flow:** Manufacturing specification → Domain commands → Shared 3D/headless model → Calibrated durations → Reference comparison

**Origin / output / platform:** Generative task-model construction · Manufacturing discrete-event models and experiment reports · Unity; discrete-event simulation

**Verification:** Across 18 modeling tasks, one frontier agent builds valid models in 93/108 attempts. A welding-workshop case agrees within 1% with a corrected reference; residual errors can survive build/run checks. No hardware deployment is established.

<details>
<summary>Abstract summary</summary>

SimuLean gives agents verified modeling components for manufacturing simulation. Domain commands construct one Unity model for 3D and headless execution; calibrated operation durations accelerate repeated studies. Independent reference models test the resulting system semantics.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2611-02691"></a>
<!-- stage3-record: {"id": "2611.02691", "scope": "Core", "section": 2} -->

#### Closing the Dynamics Gap through Self-Directed Robotic Interaction

`2026-11-02` · Stanford University; ETH Zurich; NVIDIA Research; microagi

[Paper](https://arxiv.org/abs/2611.02691) · [Project page](https://cue-dynamics.github.io/)

An agent designs physical probes, measures their outcomes and calibrates an executable model.

**Method:** The agent writes an initial MuJoCo billiards model and camera tracker. CMA-ES fits parameters by replaying measured shots; residual errors guide further shots and model revisions.

**Construction flow:** Image and goal → Initial model and priors → Shots and camera tracks → CMA-ES replay fitting → Residual-guided experiments → Calibrated predictive model

**Origin / output / platform:** Real-to-Sim · Billiards scene, tracking and fitting code, identified parameters · MuJoCo

**Verification:** Hidden-physics sim-to-sim tests use 25 conditions and at most 30 shots each; 0.91 cm error and the reported 72% reduction refer to these tests. A real tabletop deployment is reported separately.

<details>
<summary>Abstract summary</summary>

An agent designs physical probes, measures their outcomes and calibrates an executable model. The agent writes an initial MuJoCo billiards model and camera tracker. CMA-ES fits parameters by replaying measured shots; residual errors guide further shots and model revisions.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2611-00513"></a>
<!-- stage3-record: {"id": "2611.00513", "scope": "Core", "section": 2} -->

#### WorldSketch: Sketching World Models for Zero-Shot Mobile Manipulation

`2026-10-31` · Affiliation not established

[Bibliographic record](../README.md#paper-2611-00513) · [Paper](https://arxiv.org/abs/2611.00513)

A task-specific kinematic sketch connects RGB-D observations to geometric action planning.

**Method:** The VLM requests points and local views; depth supplies dimensions and axes. Projected overlays help revise the sketch, and a planner computes contacts and whole-body motion. Execution observations update joint hypotheses or trigger reconstruction.

**Construction flow:** Task and calibrated RGB-D → Point and view requests → Measured parts and joints → Overlay inspection and revision → Contact and motion planning → Execution-driven sketch update

**Origin / output / platform:** Real-to-Sim · Minimal kinematic sketch with collision voxels, entities, joints and goals · Not specified; kinematic model

**Verification:** Zero-shot success is reported on RoboCasa, LIBERO-PRO and R2R-CE using simulator depth and calibration. Real hardware, deformable dynamics and articulated chains are outside the reported evaluation.

<details>
<summary>Abstract summary</summary>

A task-specific kinematic sketch connects RGB-D observations to geometric action planning. The VLM requests points and local views; depth supplies dimensions and axes. Projected overlays help revise the sketch, and a planner computes contacts and whole-body motion. Execution observations update joint hypotheses or trigger reconstruction.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2610-40565"></a>
<!-- stage3-record: {"id": "2610.40565", "scope": "Core", "section": 2} -->

#### Gym-Anything for Robotics: Scaling physical simulations with digital agents

`2026-10-29` · Carnegie Mellon University

[Paper](https://arxiv.org/abs/2610.40565) · [Project page](https://gym-anything.github.io/robotics)

Coding agents construct physical simulators and revise them using independent audits.

**Method:** A creator studies work activities, implements scenes and tasks, and submits physical measurements and videos. Four audit types inspect physics, solvability, configuration and robustness; reports drive three rounds of creator revisions.

**Construction flow:** Work activities → Physical-process research → Scene and simulation code → Independent audits → Targeted code revisions → RoboWorld environments and tasks

**Origin / output / platform:** Generative · Interactive simulation code, task verifiers and physical evidence · Multiple backends and custom solvers; Newton, MuJoCo-Warp and Warp in selected cases

**Verification:** Twenty-five RoboWorld simulation families support physics checks, agent evaluation and small-VLA learning from code-generated demonstrations. Learning and transfer results are within simulation.

<details>
<summary>Abstract summary</summary>

Coding agents construct physical simulators and revise them using independent audits. A creator studies work activities, implements scenes and tasks, and submits physical measurements and videos. Four audit types inspect physics, solvability, configuration and robustness; reports drive three rounds of creator revisions.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2610-40754"></a>
<!-- stage3-record: {"id": "2610.40754", "scope": "Core", "section": 2} -->

#### DyCraft: An Agentic System for Long-Horizon 4D Scene Generation

`2026-10-29` · Stanford University; University of Cambridge

[Bibliographic record](../README.md#paper-2610-40754) · [Paper](https://arxiv.org/abs/2610.40754) · [Project page](https://dy-craft.github.io/)

Storyboards and frame-level diagnostics guide code repair for long-horizon animated scenes.

**Method:** A coding agent builds articulated CAD scenes, verifies key poses, then composes continuous motion with motion-capture, IK and Blender simulation tools. Rendered grids and penetration, support and joint-limit reports guide scene and motion revisions.

**Construction flow:** Prompt and expanded brief → CAD scene and joints → Verified storyboard poses → Motion tools and simulation → Frame-level visual and geometric checks → Repaired Blender film

**Origin / output / platform:** Generative animated physical scenes · Editable Blender projects, animated films, plans and briefs · Blender native simulation; backend not specified

**Verification:** Twenty-four multi-shot tasks support human preference, frame-level physical-error metrics and tool ablations. The outputs are rendered animations, not robot-training environments or hardware trials; residual violations remain.

<details>
<summary>Abstract summary</summary>

Verified key poses divide long animations into local motion problems. The agent can revise geometry and motion from render and spatial diagnostics; released film assets support inspection rather than constituting complete training trajectories.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4)

<a id="work-2610-36592"></a>
<!-- stage3-record: {"id": "2610.36592", "scope": "Adjacent", "section": 2} -->

#### LabWorld: Learning Interactive 4D Worlds for Scientific Experimentation

`2026-10-27` · Princeton University; Stanford University; University of Chicago; New York University; Oregon State University; University of Illinois at Urbana-Champaign; University of Texas at Austin

[Paper](https://arxiv.org/abs/2610.36592)

Laboratory videos become editable assets, trajectories and spatially constrained events.

**Method:** A VLM extracts objects and events, while SAM3 and MapAnything provide masks, geometry and cameras. Asset assembly and trajectory optimization combine observations, smoothness, event relations and nonpenetration constraints.

**Construction flow:** Laboratory video → Objects and events → Masks, geometry, cameras and assets → Metric scene → Event-constrained trajectory fitting → Editable 4D representation

**Origin / output / platform:** Real-to-Sim · Editable 4D states and structured events, rather than a complete dynamics simulator · Not specified

**Verification:** Pipetting and shaking videos are evaluated with mask overlap, keypoint accuracy and modeled constraints. Robot deployment, complete fluid dynamics and fully automatic raw-video reconstruction are not established.

<details>
<summary>Abstract summary</summary>

Laboratory videos become editable assets, trajectories and spatially constrained events. A VLM extracts objects and events, while SAM3 and MapAnything provide masks, geometry and cameras. Asset assembly and trajectory optimization combine observations, smoothness, event relations and nonpenetration constraints.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2610-34745"></a>
<!-- stage3-record: {"id": "2610.34745", "scope": "Core", "section": 2} -->

#### SceneAgent: An Agentic Pipeline from 3D and 4D Captures to Simulation Environments

`2026-10-26` · Harvard University

[Bibliographic record](../README.md#paper-2610-34745) · [Paper](https://arxiv.org/abs/2610.34745) · [Project page](https://computationalrobotics.seas.harvard.edu/SceneAgent/)

An agent assembles captured geometry and dynamic observations into interactive simulation scenes.

**Method:** Planning, segmentation, completion, articulation and property tools produce an initial scene. In the video route, the agent compares rendered early, middle and late frames and revises cameras, geometry, initial states or physical parameters before generating variants and demonstrations.

**Construction flow:** 3D captures or video → Object segmentation and mesh completion → Properties and articulation → Simulation and multiframe renders → Visual diagnosis and revision → Interactive scene and variants

**Origin / output / platform:** Real-to-Sim + generative · Editable scenes, 4D construction scripts and demonstrations · PhysX; Warp, Newton or Blast depending on the material case

**Verification:** Evaluation covers one kitchen, one cluttered bin and three synthetic dynamic scenes, plus a pilot Franka transfer study. Real material calibration and real 4D reconstruction remain unverified.

<details>
<summary>Abstract summary</summary>

An agent assembles captured geometry and dynamic observations into interactive simulation scenes. Planning, segmentation, completion, articulation and property tools produce an initial scene. In the video route, the agent compares rendered early, middle and late frames and revises cameras, geometry, initial states or physical parameters before generating variants and demonstrations.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4)

<a id="work-2610-32978"></a>
<!-- stage3-record: {"id": "2610.32978", "scope": "Adjacent", "section": 2} -->

#### SceneBloom: Agentic Indoor Environment Generation with Realistic and Diverse Layouts for Embodied Learning

`2026-10-23` · New York University; University of California, San Diego

[Bibliographic record](../README.md#paper-2610-32978) · [Paper](https://arxiv.org/abs/2610.32978) · [Project page](https://tinaliu0123.github.io/scenebloom/)

Visual layout proposals are compiled into geometrically feasible indoor environments.

**Method:** A VLM divides a room into functional zones. FLUX with asset-specific LoRA proposes layouts; perception lifts objects to 3D and a VLM extracts relational constraints. Hierarchical fitting and pose correction assemble the final room.

**Construction flow:** Room description → Zones and asset lists → FLUX layout proposals → 3D boxes and relations → Geometric fitting → Wall and surface completion → Exported room

**Origin / output / platform:** Generative · Layout JSON, material settings, instantiated meshes and scene.glb · Not specified; Habitat export and Isaac Gym stability evaluation

**Verification:** Fifty scenes across five room types are checked for collisions, bounds, stability, visual quality and layout distributions. Navigation transfer uses held-out real scans in Habitat, not real robots.

<details>
<summary>Abstract summary</summary>

Visual layout proposals are compiled into geometrically feasible indoor environments. A VLM divides a room into functional zones. FLUX with asset-specific LoRA proposes layouts; perception lifts objects to 3D and a VLM extracts relational constraints. Hierarchical fitting and pose correction assemble the final room.

</details>

**Related:** [4. Data](#section-4)

<a id="work-2610-31834"></a>
<!-- stage3-record: {"id": "2610.31834", "scope": "Core", "section": 2} -->

#### WorldMirror: Agentic Real-to-Sim Generation of Interactive Worlds from In-the-Wild Robot Demonstrations

`2026-10-22` · Xspark AI; Tsinghua University; The University of Hong Kong; University College London; Peking University

[Bibliographic record](../README.md#paper-2610-31834) · [Paper](https://arxiv.org/abs/2610.31834) · [Project page](https://worldmirror-page.github.io/)

Recorded robot demonstrations guide construction of editable worlds that support direct trajectory replay.

**Method:** A routing agent coordinates reconstruction, calibration, layout and replay specialists over a shared world state. Render, spatial and physical checks gate changes; classified failures roll back the relevant stage and rebuild affected dependencies.

**Construction flow:** RGB demonstration and robot trajectory → Background and interactive assets → Camera and coordinate calibration → Scene assembly → Replay and failure diagnosis → Targeted reconstruction rollback

**Origin / output / platform:** Real-to-Sim · Camera-aligned world programs and replayable robot scenes · Not specified; Isaac Sim platform

**Verification:** DROID evaluation measures appearance, object and relation errors, and replay of the recorded demonstrations. Replay success is not the success rate of a new policy on real hardware.

<details>
<summary>Abstract summary</summary>

Recorded robot demonstrations guide construction of editable worlds that support direct trajectory replay. A routing agent coordinates reconstruction, calibration, layout and replay specialists over a shared world state. Render, spatial and physical checks gate changes; classified failures roll back the relevant stage and rebuild affected dependencies.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4)

<a id="work-system-plumb"></a>
<!-- stage3-record: {"id": "system:plumb", "scope": "Resource", "section": 2} -->

#### Plumb: Coding Agents with 3D Perception Rebuild Physical Scenes from Video

`2026-10-21` · Westlake University; The University of Hong Kong

[Project page](https://yubel426.github.io/Plumb/) · [Code](https://github.com/Inception3D/Plumb)

A coding agent uses measured video geometry to reconstruct replayable MuJoCo scenes.

**Method:** SAM3 and Pi3X supply tracking, depth and camera poses. Measurement tools estimate planes, dimensions and paths; the agent writes MJCF, initial states, parameters and fitting code, then compares simulated image and depth trajectories.

**Construction flow:** Video → Tracking, depth and cameras → Geometric measurements → MJCF and parameter code → Simulation replay and comparison → Passive executable scene

**Origin / output / platform:** Real-to-Sim · MJCF scene, initial state, physical parameters, fitting code and previews · MuJoCo

**Verification:** Fifty selected PhysInOne/Physion videos are evaluated with 2D/3D trajectories, masks and physical quantities. The official report does not establish real-robot policy transfer.

<details>
<summary>Abstract summary</summary>

A coding agent uses measured video geometry to reconstruct replayable MuJoCo scenes. SAM3 and Pi3X supply tracking, depth and camera poses. Measurement tools estimate planes, dimensions and paths; the agent writes MJCF, initial states, parameters and fitting code, then compares simulated image and depth trajectories.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3)

<a id="work-2610-33060"></a>
<!-- stage3-record: {"id": "2610.33060", "scope": "Core", "section": 2} -->

#### MARC: Mechanism-Aware Reflective Correction for Articulated Object Code Generation

`2026-10-19` · Shanghai Jiao Tong University; Meituan

[Bibliographic record](../README.md#paper-2610-33060) · [Paper](https://arxiv.org/abs/2610.33060) · [Project page](https://demianmusk.github.io/MARC-Home/)

Connection-level diagnostics help agents repair executable mechanisms with loops and coupled motion.

**Method:** An agent writes part geometry and socket-bound joints. A numerical solver fixes driving coordinates and solves dependent motion; graph-linked diagnostics and renders guide Judge, Executor and Reviewer roles through connection or geometry repairs.

**Construction flow:** Reference and motion goal → Geometry and socket program → Constrained motion solve → Graph-linked diagnosis → Connection or geometry repair → Full-path recheck

**Origin / output / platform:** Generative · Executable mechanisms with closed loops, sockets and coupled coordinates · Numerical kinematics; no general dynamics engine specified

**Verification:** Twenty complex mechanisms test executability, structural correctness, motion coverage and coupling. These are numerical kinematic results rather than full dynamics or hardware validation.

<details>
<summary>Abstract summary</summary>

Connection-level diagnostics help agents repair executable mechanisms with loops and coupled motion. An agent writes part geometry and socket-bound joints. A numerical solver fixes driving coordinates and solves dependent motion; graph-linked diagnostics and renders guide Judge, Executor and Reviewer roles through connection or geometry repairs.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2610-21498"></a>
<!-- stage3-record: {"id": "2610.21498", "scope": "Core", "section": 2} -->

#### GRASE: Geometry-native Real-to-sim Agentic Scene Modeling from Video

`2026-10-15` · Xi’an Jiaotong University; Fuzhou University; Adobe Systems; Westlake University

[Bibliographic record](../README.md#paper-2610-21498) · [Paper](https://arxiv.org/abs/2610.21498)

Video-aligned rendering guides local revision of editable room geometry.

**Method:** Multiview depth and shared boundaries initialize the room shell. Large objects use Blender primitives where possible; TRELLIS.2 handles smaller or less expressible shapes. The agent compares video, renders and measurements to repair specific objects without disrupting aligned regions.

**Construction flow:** Input video → Room-shell fitting → Support-aware object placement → Primitives or generated meshes → Render and geometry comparison → Local scene revision

**Origin / output / platform:** Real-to-Sim · Editable static room, objects and parts · Not specified; Blender authoring

**Verification:** Replica and Imaginarium evaluations measure geometric distance, normals, instance overlap and rendering quality. Dynamic robot-task utility is not evaluated.

<details>
<summary>Abstract summary</summary>

Video-aligned rendering guides local revision of editable room geometry. Multiview depth and shared boundaries initialize the room shell. Large objects use Blender primitives where possible; TRELLIS.2 handles smaller or less expressible shapes. The agent compares video, renders and measurements to repair specific objects without disrupting aligned regions.

</details>

<a id="work-2610-18835"></a>
<!-- stage3-record: {"id": "2610.18835", "scope": "Core", "section": 2} -->

#### RoboSimStudio: An Interactive Toolkit for Human and Agent Rapid Real2Sim of Robot Manipulation Tasks

`2026-10-13` · University of California, Berkeley; NVIDIA

[Paper](https://arxiv.org/abs/2610.18835) · [Project page](https://robosimstudio.github.io)

Editable multiphysics models connect video-based construction with robot interaction feedback.

**Method:** The agent builds rigid, soft and robot components from task video. The runtime returns events and visual observations for revisions. A wiping example combines Newton, MuJoCo-Warp and SuperDex; a real support failure leads to replacing a fixed support with a free rigid body.

**Construction flow:** Task video → Robot and material scene → Simulation rollout → Events and visual observations → Model and behavior revision → Pilot real-world feedback

**Origin / output / platform:** Real-to-Sim · Editable multiphysics scenes, robot behavior and interaction feedback · Newton / MuJoCo-Warp; SuperDex FEM; VBD in cloth and cable cases

**Verification:** Eighteen contact-rich simulations and a pilot dual-arm wiping experiment illustrate the workflow. They do not constitute a large-scale sim-to-real success benchmark.

<details>
<summary>Abstract summary</summary>

Editable multiphysics models connect video-based construction with robot interaction feedback. The agent builds rigid, soft and robot components from task video. The runtime returns events and visual observations for revisions. A wiping example combines Newton, MuJoCo-Warp and SuperDex; a real support failure leads to replacing a fixed support with a free rigid body.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2610-17114"></a>
<!-- stage3-record: {"id": "2610.17114", "scope": "Core", "section": 2} -->

#### D-World: An Explicit World-Language-Action Model with Recursive Self-Improvement under Dual Control

`2026-10-12` · Geek+

[Paper](https://arxiv.org/abs/2610.17114)

Real action measurements continually correct an agent-authored digital twin.

**Method:** Sense builds an executable twin; Plan searches within it and dispatches short action segments. Depth, gripper and end-effector measurements revise states or named physical parameters, with replay consistency checks and reconstruction when the model structure is wrong.

**Construction flow:** Physical observations → Executable twin → Simulated action search → Real execution → Measurement comparison → State or parameter update → Replay consistency check

**Origin / output / platform:** Real-to-Sim · Versioned twins, state and parameter revisions, actions and measurements · Not specified; can export MuJoCo scenes

**Verification:** Real dual-arm towel and toaster cases measure residuals and action outcomes. The demonstrations do not provide systematic success-rate or baseline comparisons.

<details>
<summary>Abstract summary</summary>

Real action measurements continually correct an agent-authored digital twin. Sense builds an executable twin; Plan searches within it and dispatches short action segments. Depth, gripper and end-effector measurements revise states or named physical parameters, with replay consistency checks and reconstruction when the model structure is wrong.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2610-13947"></a>
<!-- stage3-record: {"id": "2610.13947", "scope": "Core", "section": 2} -->

#### Towards Physically Grounded Articulated 3D Assets: A Multi-Agent Pipeline and Benchmark

`2026-10-09` · Nanyang Technological University; ETH Zurich; Microsoft; University of Cambridge; University of Oxford

[Bibliographic record](../README.md#paper-2610-13947) · [Paper](https://arxiv.org/abs/2610.13947) · [Project page](https://physicalvision.github.io/artisan/)

Agent teams revise articulated assets using motion, collision and stability evidence.

**Method:** A designer specifies structure and references; a coder uses Python and the Articraft SDK to implement parts, connectors and properties. Multiview renders and MuJoCo reports generate concrete issues for targeted code revision.

**Construction flow:** Design requirements → Structural blueprint → Articraft Python implementation → Renders and physics checks → Review and code revision → Articulated asset

**Origin / output / platform:** Generative · Python-defined articulated assets and physical properties · MuJoCo

**Verification:** Asset, stability and mass-related benchmarks are supplemented by simulated manipulation and human preferences. Real-robot transfer of the downstream tasks is not reported.

<details>
<summary>Abstract summary</summary>

Agent teams revise articulated assets using motion, collision and stability evidence. A designer specifies structure and references; a coder uses Python and the Articraft SDK to implement parts, connectors and properties. Multiview renders and MuJoCo reports generate concrete issues for targeted code revision.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2610-11322"></a>
<!-- stage3-record: {"id": "2610.11322", "scope": "Core", "section": 2} -->

#### USDCraft: Geometrically Grounded Programmatic Modeling of Articulated 3D Assets for Simulation

`2026-10-08` · NVIDIA; Nanyang Technological University; Peking University

[Bibliographic record](../README.md#paper-2610-11322) · [Paper](https://arxiv.org/abs/2610.11322) · [Project page](https://xingyoujun.github.io/usdcraft/)

Programs reconstruct articulated USD assets while distinguishing missing observed surfaces from unseen space.

**Method:** Metric slices and local geometry queries encode partial source meshes. The agent plans parts and writes parametric asset programs; geometry comparisons and renders across views and joint states guide inspection before compilation to USD.

**Construction flow:** Partial mesh and images → Metric slices and queries → Part plan → Parametric asset program → Geometry and articulation checks → USD compilation

**Origin / output / platform:** Real-to-Sim · USD assets with rigid bodies, joints, collision geometry and source programs · NVIDIA PhysX

**Verification:** Two asset benchmarks evaluate parts, geometry and articulation. Three real manipulation tasks test policies trained in simulation; deformable dynamics are outside the validation.

<details>
<summary>Abstract summary</summary>

Programs reconstruct articulated USD assets while distinguishing missing observed surfaces from unseen space. Metric slices and local geometry queries encode partial source meshes. The agent plans parts and writes parametric asset programs; geometry comparisons and renders across views and joint states guide inspection before compilation to USD.

</details>

**Related:** [4. Data](#section-4)

<a id="work-2610-10479"></a>
<!-- stage3-record: {"id": "2610.10479", "scope": "Core", "section": 2} -->

#### Agentic RSR: Real-to-Sim-to-Real through Scene Reconstruction and Execution-Grounded Robot Policies

`2026-10-07` · Sun Yat-sen University; The Hong Kong University of Science and Technology (Guangzhou)

[Bibliographic record](../README.md#paper-2610-10479) · [Paper](https://arxiv.org/abs/2610.10479)

Scene reconstruction and executable policy development share a task-specific sim-to-real workflow.

**Method:** The agent restores scale from workspace video, task and robot information, revises Blender appearance and layout, and checks MuJoCo interactions. Policy development gradually replaces privileged state with visual observations and randomized environments.

**Construction flow:** Workspace video and task → Scale and scene reconstruction → Multiview revision → MuJoCo interaction checks → Policy development and randomization → Real-robot execution

**Origin / output / platform:** Real-to-Sim · Scale-aligned scene, MJCF and executable robot policy · MuJoCo

**Verification:** Eighteen scenes and two robots are evaluated for visual agreement, depth and real execution. Physical plausibility probes do not identify ground-truth material parameters.

<details>
<summary>Abstract summary</summary>

Scene reconstruction and executable policy development share a task-specific sim-to-real workflow. The agent restores scale from workspace video, task and robot information, revises Blender appearance and layout, and checks MuJoCo interactions. Policy development gradually replaces privileged state with visual observations and randomized environments.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2610-02274"></a>
<!-- stage3-record: {"id": "2610.02274", "scope": "Core", "section": 2} -->

#### Awomo-SimDataEngine: Agentic Simulation-Ready World Generation

`2026-10-01` · Affiliation not established

[Bibliographic record](../README.md#paper-2610-02274) · [Paper](https://arxiv.org/abs/2610.02274)

Asset generation, image reconstruction and text-based layout meet in a verified simulation data engine.

**Method:** ISArt generates part trees, meshes and URDF articulation; Unravel reconstructs occluded objects in layers; SimForge plans rooms from text. A dependency graph routes failures to the responsible module before robot and task binding.

**Construction flow:** Text or image inputs → Articulated assets and reconstruction → Scene layout → Module validation and repair → Robot and task binding → Replayable demonstrations

**Origin / output / platform:** Real-to-Sim + generative · Interactive assets, editable scenes and task-conditioned demonstrations · Not specified; Isaac Sim platform

**Verification:** Assets, scenes and policy co-training are evaluated separately. Reported WAM gains from Isaac Sim data on MuJoCo LIBERO-Plus are cross-simulator results, not real-hardware gains.

<details>
<summary>Abstract summary</summary>

Asset generation, image reconstruction and text-based layout meet in a verified simulation data engine. ISArt generates part trees, meshes and URDF articulation; Unravel reconstructs occluded objects in layers; SimForge plans rooms from text. A dependency graph routes failures to the responsible module before robot and task binding.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2609-36593"></a>
<!-- stage3-record: {"id": "2609.36593", "scope": "Core", "section": 2} -->

#### Text2Sim: Agentic Physics-Based Simulation Generation with Distilled Expertise

`2026-09-29` · Tsinghua University; Carnegie Mellon University; Genesis AI; Shanghai Qi Zhi Institute

[Bibliographic record](../README.md#paper-2609-36593) · [Paper](https://arxiv.org/abs/2609.36593)

A planner delegates simulation modules and directs repairs using execution evidence.

**Method:** Four writer roles implement scenes, objects, actions and rendering, obtaining assets as needed. After Genesis execution, a critic combines videos, code and numerical records; the planner routes repairs and retrieves prior simulation experience from Debug Cards.

**Construction flow:** Physical-process request → Global plan → Scene, object, action and render modules → Genesis execution → Video and numerical diagnosis → Targeted module repair

**Origin / output / platform:** Generative · Executable code, assets, physics settings, controls, trajectories and rendered video · Genesis

**Verification:** Forty-two held-out rigid, deformable and cloth prompts use independent physical/visual scoring, blind human preferences and ablations. There are no real-robot experiments.

<details>
<summary>Abstract summary</summary>

A planner delegates simulation modules and directs repairs using execution evidence. Four writer roles implement scenes, objects, actions and rendering, obtaining assets as needed. After Genesis execution, a critic combines videos, code and numerical records; the planner routes repairs and retrieves prior simulation experience from Debug Cards.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2609-37089"></a>
<!-- stage3-record: {"id": "2609.37089", "scope": "Core", "section": 2} -->

#### Real2Gym: Building Gyms from Videos, Bringing Skills to Robots

`2026-09-29` · Shanghai Artificial Intelligence Laboratory; Shanghai Jiao Tong University; Zhejiang University; University of Science and Technology of China; The Chinese University of Hong Kong; The University of Hong Kong

[Paper](https://arxiv.org/abs/2609.37089) · [Project page](https://real2gym.github.io/)

Human or robot demonstrations become visually aligned, executable task environments.

**Method:** Depth, segmentation and multiview cues initialize objects, cameras and robots. Key contact frames expose discrepancies; MuJoCo execution or retargeting then guides scene and action revisions, and physical checks filter generated variants.

**Construction flow:** Demonstration → Depth and object reconstruction → Camera and robot alignment → Contact-frame checks → MuJoCo replay and revision → Validated task environments

**Origin / output / platform:** Real-to-Sim + generative · Blender scenes, MuJoCo models and executable manipulation stages · MuJoCo 3.3.7

**Verification:** Twenty-four reconstructed environments test visual fidelity, task success and token cost. Transfer is evaluated on four Franka task families and is limited to parallel-gripper settings.

<details>
<summary>Abstract summary</summary>

Human or robot demonstrations become visually aligned, executable task environments. Depth, segmentation and multiview cues initialize objects, cameras and robots. Key contact frames expose discrepancies; MuJoCo execution or retargeting then guides scene and action revisions, and physical checks filter generated variants.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2609-37067"></a>
<!-- stage3-record: {"id": "2609.37067", "scope": "Adjacent", "section": 2} -->

#### FACT: Fidelity-Aware Construction of Articulated Twins

`2026-09-29` · ShanghaiTech University

[Paper](https://arxiv.org/abs/2609.37067)

Geometry, contact and response fidelity are developed as distinct stages of articulated-twin construction.

**Method:** An agent measures an image-derived mesh and writes feature programs, revising them with visual and surface diagnostics. It then adjusts collision proxies and fits dynamic response models using passive videos and simulation residuals.

**Construction flow:** Object images → Measurement and feature modeling → Geometry revision → Collision and contact proxies → Passive-response fitting → Calibrated articulated twin

**Origin / output / platform:** Real-to-Sim · Geometry programs, joint graphs, collision proxies and calibrated response models · MuJoCo for dynamic prediction

**Verification:** Geometry, simulated interaction and held-out passive-video prediction are evaluated. Results cover sampled configurations and observed responses, not active real-robot manipulation.

<details>
<summary>Abstract summary</summary>

Geometry, contact and response fidelity are developed as distinct stages of articulated-twin construction. An agent measures an image-derived mesh and writes feature programs, revising them with visual and surface diagnostics. It then adjusts collision proxies and fits dynamic response models using passive videos and simulation residuals.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2609-36024"></a>
<!-- stage3-record: {"id": "2609.36024", "scope": "Core", "section": 2} -->

#### CoDimRecon: Agentic Reconstruction of Sim-Ready 3D Scenes with Deformable Curves, Surfaces, and Volumes

`2026-09-28` · Tsinghua University; Carnegie Mellon University; Genesis AI

[Bibliographic record](../README.md#paper-2609-36024) · [Paper](https://arxiv.org/abs/2609.36024) · [Project page](https://shuzhaoxie.github.io/CoDimRecon/)

Editable reconstruction separates line, surface and volume models for deformable simulation.

**Method:** VGGT-Omega and generative shape references guide Blender geometry, appearance and pose revision. Curves, surfaces and volumes become rod, shell and solid representations; robot interaction diagnoses behavioral, geometric, numerical or material errors.

**Construction flow:** Scene observations → Geometry and generated shape references → Editable Blender reconstruction → Rod, shell or solid representation → Render and interaction checks → Revised simulation scene

**Origin / output / platform:** Real-to-Sim · Editable scenes, joints, rods, shells, volume meshes and physics settings · MuJoCo; IPC-family contact and rod/shell/solid solvers

**Verification:** Six reconstructed indoor scenes test geometry, rendering and rigid stability. Deformable demonstrations and paper-folding control use effective simulation parameters rather than measured material truth.

<details>
<summary>Abstract summary</summary>

Editable reconstruction separates line, surface and volume models for deformable simulation. VGGT-Omega and generative shape references guide Blender geometry, appearance and pose revision. Curves, surfaces and volumes become rod, shell and solid representations; robot interaction diagnoses behavioral, geometric, numerical or material errors.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2609-33208"></a>
<!-- stage3-record: {"id": "2609.33208", "scope": "Core", "section": 2} -->

#### WorldAgent: Verification-Guided Agentic Physical World Construction

`2026-09-27` · University of British Columbia; VAST; Zhejiang University; University of Utah; The University of Texas at Austin; University of California, Los Angeles

[Bibliographic record](../README.md#paper-2609-33208) · [Paper](https://arxiv.org/abs/2609.33208)

World specifications make physical scene construction and revision addressable by object and time.

**Method:** A language prompt becomes a JSON specification. Blender skills implement terrain, scenes and category-specific physics; geometry, causal, stability and contact checks identify failing objects and frames and update the specification.

**Construction flow:** Language prompt → World specification → Scene and physics skills → Simulation and rendering → Object/frame-level checks → Specification revision

**Origin / output / platform:** Generative · World JSON, editable Blender scenes, physics caches and render sequences · Bullet, Mantaflow, Blender Soft Body, Cloth and particles

**Verification:** AgenticSimBench evaluates thirteen long prompts with visual and physical indicators and a human study. Evidence is digital simulation, with approximations in some multiphysics cases.

<details>
<summary>Abstract summary</summary>

World specifications make physical scene construction and revision addressable by object and time. A language prompt becomes a JSON specification. Blender skills implement terrain, scenes and category-specific physics; geometry, causal, stability and contact checks identify failing objects and frames and update the specification.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2609-23103"></a>
<!-- stage3-record: {"id": "2609.23103", "scope": "Core", "section": 2} -->

#### DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation

`2026-09-19` · University of British Columbia; National University of Singapore; University of Cambridge; Friedrich-Alexander-Universität Erlangen-Nürnberg; University of Wisconsin–Madison

[Bibliographic record](../README.md#paper-2609-23103) · [Paper](https://arxiv.org/abs/2609.23103) · [Project page](https://diaggen.github.io/)

Active manipulation probes route asset defects back to their generating stages.

**Method:** Image cleanup, part segmentation, geometry and material inference produce a Genesis asset. A diagnostic agent selects anchors and grasps, then applies contact, displacement and release tests; multiview observations and logs route repairs to segmentation, material or mesh processing.

**Construction flow:** Object photo → Parts, geometry and materials → Genesis asset → Agent-selected physical probes → Multiview diagnosis → Stage-specific repair and rerun

**Origin / output / platform:** Real-to-Sim · Deformable asset packages with parts, meshes, materials, scale and diagnostics · Genesis implicit FEM and SAP frictional contact

**Verification:** Forty assets are inspected, with fourteen revised; perceptual and dynamic comparisons quantify changes. Manipulation examples do not establish large-scale real-policy transfer.

<details>
<summary>Abstract summary</summary>

Active manipulation probes route asset defects back to their generating stages. Image cleanup, part segmentation, geometry and material inference produce a Genesis asset. A diagnostic agent selects anchors and grasps, then applies contact, displacement and release tests; multiview observations and logs route repairs to segmentation, material or mesh processing.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2609-18620"></a>
<!-- stage3-record: {"id": "2609.18620", "scope": "Core", "section": 2} -->

#### DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation

`2026-09-16` · Nankai University; Rightly Robotics, A4x

[Bibliographic record](../README.md#paper-2609-18620) · [Paper](https://arxiv.org/abs/2609.18620) · [Project page](https://can-lee.github.io/DeformSmith_web/)

Layered physical tests guide construction and repair of deformable assets.

**Method:** Geometry and Gaussian appearance are followed by scale, mass and contact setup, then MPM material probes. Robot transport tests drive action, numerical or material revisions; material changes must repeat the lower-level physical checks.

**Construction flow:** Object image → Geometry and appearance → Scale, mass and contact → MPM material probes → Grasp-transport-release test → Targeted revision and retest

**Origin / output / platform:** Generative · Particle physics, Gaussian appearance, material settings and interaction records · Warp MPM; SAPIEN robot simulation

**Verification:** Thirty-nine cases use anonymous VLM ratings, human preferences and physics-test ablations. Real material identification is proposed as an application, not experimentally established.

<details>
<summary>Abstract summary</summary>

Layered physical tests guide construction and repair of deformable assets. Geometry and Gaussian appearance are followed by scale, mass and contact setup, then MPM material probes. Robot transport tests drive action, numerical or material revisions; material changes must repeat the lower-level physical checks.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2609-05927"></a>
<!-- stage3-record: {"id": "2609.05927", "scope": "Adjacent", "section": 2} -->

#### GIF: Agentic Generation of Interactive and Functional Object Compositions for Robot Learning

`2026-09-05` · Galbot; Peking University; Zhejiang University; The University of Hong Kong; Tsinghua University; Beijing Academy of Artificial Intelligence

[Paper](https://arxiv.org/abs/2609.05927) · [Project page](https://fufumeichi.github.io/gif-project-page/)

Generated object combinations are refined for functional contact relationships.

**Method:** CoGen preserves both direct and occlusion-completed mesh candidates. Geometry refinement aligns objects, resolves collisions and searches for stable MuJoCo poses; a VLM selects combinations with the intended relations from rendered views.

**Construction flow:** Reference image and object specification → Direct and completed meshes → Geometric alignment → Collision resolution → MuJoCo stability search → Visual relation checks → Functional combination

**Origin / output / platform:** Generative · Rigid-object scenes with intended contacts and demonstration trajectories · MuJoCo; Drake/SNOPT for collision-constrained optimization

**Verification:** One hundred twenty scenes test appearance, contact relations, collision and human preferences, followed by simulated and real manipulation with synthetic-data-trained policies. The main scope is rigid-object combinations.

<details>
<summary>Abstract summary</summary>

Generated object combinations are refined for functional contact relationships. CoGen preserves both direct and occlusion-completed mesh candidates. Geometry refinement aligns objects, resolves collisions and searches for stable MuJoCo poses; a VLM selects combinations with the intended relations from rendered views.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2609-05594"></a>
<!-- stage3-record: {"id": "2609.05594", "scope": "Adjacent", "section": 2} -->

#### SceneMosaic: Efficient and Diverse Simulation-Ready Scene Generation via Hybrid Agentic Layout Evolution

`2026-09-04` · The University of Hong Kong; University of Electronic Science and Technology of China

[Paper](https://arxiv.org/abs/2609.05594) · [Code](https://github.com/rxjfighting/SceneMosaic) · [Project page](https://rxjfighting.github.io/SceneMosaic/)

Local layout units make simulation-ready scene variation more efficient.

**Method:** SAM3 segmentation and SAM3D reconstruction initialize object meshes and layout. Support and containment relations define local units; orthographic views and simulation diagnostics guide pose revisions before validated local variants are recombined.

**Construction flow:** Reference or generated image → Object segmentation and meshes → Support-aware local units → Gravity settling and local revision → Variant recombination and filtering → Diverse simulation scenes

**Origin / output / platform:** Real-to-Sim + generative · Simulation-ready indoor scenes and variants · Not specified

**Verification:** SceneEval-100 tests semantic placement, orientation, collisions, bounds, navigability, time and diversity, with human ratings. It is not a real-robot task evaluation.

<details>
<summary>Abstract summary</summary>

Local layout units make simulation-ready scene variation more efficient. SAM3 segmentation and SAM3D reconstruction initialize object meshes and layout. Support and containment relations define local units; orthographic views and simulation diagnostics guide pose revisions before validated local variants are recombined.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2608-30821"></a>
<!-- stage3-record: {"id": "2608.30821", "scope": "Adjacent", "section": 2} -->

#### Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling

`2026-08-31` · ByteDance Seed; Peking University; Zhejiang University

[Paper](https://arxiv.org/abs/2608.30821) · [Project page](https://lucida-r2s.github.io/)

A visual editing agent aligns generated assets to measured scene evidence.

**Method:** Posed RGB-D produces an object graph with masks, points, boxes and relations. Multiview completion supplies full assets; GizmoAct inspects overlays and axis views and adjusts translation, rotation and scale through iterative GUI-style actions.

**Construction flow:** Posed RGB-D → Multiview object graph → Occlusion completion → Complete 3D assets → Gizmo views and overlays → Incremental pose editing → Composable scene graph

**Origin / output / platform:** Real-to-Sim · Independent assets, 9-DoF poses, scale and relational scene graphs · Not specified

**Verification:** R2S, CA-1M and ADT evaluations measure 3D detection, pose accuracy and scene geometry. Physical interaction and hardware transfer are not tested.

<details>
<summary>Abstract summary</summary>

A visual editing agent aligns generated assets to measured scene evidence. Posed RGB-D produces an object graph with masks, points, boxes and relations. Multiview completion supplies full assets; GizmoAct inspects overlays and axis views and adjusts translation, rotation and scale through iterative GUI-style actions.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2608-27549"></a>
<!-- stage3-record: {"id": "2608.27549", "scope": "Core", "section": 2} -->

#### Code as Worlds: Agentic Discovery of Executable World Representations for Physical Reasoning

`2026-08-27` · MirroS; Tsinghua University; Peking University; Nanyang Technological University

[Bibliographic record](../README.md#paper-2608-27549) · [Paper](https://arxiv.org/abs/2608.27549) · [Project page](https://mirros-lab.github.io/code-as-world)

Executable world hypotheses connect multimodal evidence to inspectable representations.

**Method:** Adapters extract semantic constraints or video geometry and trajectories. The agent proposes a world representation, executes it, compares keyframe evidence and locally edits the responsible physical, dynamic or appearance components.

**Construction flow:** Text or video → Semantic or geometric evidence → Executable world hypothesis → Instantiation and execution → Render and projection comparison → Local program revision → Validated representation

**Origin / output / platform:** Real-to-Sim + generative · Executable world programs, state/event traces and verification records · Optional MuJoCo dynamics; main reconstruction uses a kinematic animation engine

**Verification:** Video reconstruction compares bounded refinement with budget-matched Best-of-5 using visual, overlap and motion metrics. Main reconstruction uses a kinematic animation engine; video realism does not establish real-robot physics.

<details>
<summary>Abstract summary</summary>

Executable world hypotheses connect multimodal evidence to inspectable representations. Adapters extract semantic constraints or video geometry and trajectories. The agent proposes a world representation, executes it, compares keyframe evidence and locally edits the responsible physical, dynamic or appearance components.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2608-18840"></a>
<!-- stage3-record: {"id": "2608.18840", "scope": "Adjacent", "section": 2} -->

#### Beyond Placement and Articulation: Usage-Driven Code Scenes for Embodied Interaction

`2026-08-19` · Shanghai Jiao Tong University; Meituan

[Paper](https://arxiv.org/abs/2608.18840)

Usage requirements become articulated rooms with executable interaction rules.

**Method:** The system expands room purposes into objects, supports and an interaction graph. ArtiCraft produces movable assets; trigger-condition-effect rules express interactions. FLUX.2 textures surfaces, while geometric and visual checks refine the layout.

**Construction flow:** Room and usage requirements → Object and interaction graphs → Articulated asset programs → Interaction rules and textures → Layout and simulation revision → Interactive scene

**Origin / output / platform:** Generative · Task scenes with articulation and state-transition rules · Not specified

**Verification:** Twenty-eight room prompts evaluate spatial and semantic constraints and supported interactions. Simulated robot examples are reported, without hardware validation.

<details>
<summary>Abstract summary</summary>

Usage requirements become articulated rooms with executable interaction rules. The system expands room purposes into objects, supports and an interaction graph. ArtiCraft produces movable assets; trigger-condition-effect rules express interactions. FLUX.2 textures surfaces, while geometric and visual checks refine the layout.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2610-01863"></a>
<!-- stage3-record: {"id": "2610.01863", "scope": "Core", "section": 2} -->

#### LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction

`2026-08-04` · University of Cambridge; Imperial College London; Independent Researcher

Official project article: 2026-08-04; arXiv v1: 2026-10-01.

[Bibliographic record](../README.md#paper-2610-01863) · [Paper](https://arxiv.org/abs/2610.01863) · [Project page](https://litereality.github.io/agent/)

An editable room program unifies scan geometry, generated assets and reconstruction feedback.

**Method:** Corrected scan layouts route articulated objects to programmatic construction and complex static objects to image-to-3D generation. The agent edits Room.py using calibrated views, points and renders, with geometry, support and collision checks before export.

**Construction flow:** RGB-D scan → Corrected layout and boxes → Programmatic or TRELLIS assets → Initial Room.py → Observe, edit and verify → Editable room and MuJoCo export

**Origin / output / platform:** Real-to-Sim · Room.py, editable scene, object and joint assets, MuJoCo model · MuJoCo for exported interaction demonstrations

**Verification:** Ten real indoor scans test rendering and depth agreement. MuJoCo interactions are demonstrations, not real-robot success-rate experiments.

<details>
<summary>Abstract summary</summary>

An editable room program unifies scan geometry, generated assets and reconstruction feedback. Corrected scan layouts route articulated objects to programmatic construction and complex static objects to image-to-3D generation. The agent edits Room.py using calibrated views, points and renders, with geometry, support and collision checks before export.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2607-21522"></a>
<!-- stage3-record: {"id": "2607.21522", "scope": "Adjacent", "section": 2} -->

#### GS-Agent: Creating 4D Physical Worlds With Generative Simulation

`2026-07-23` · University of Massachusetts Amherst; Genesis AI

[Paper](https://arxiv.org/abs/2607.21522) · [Project page](https://umass-embodied-agi.github.io/gs-agent/)

Generative simulation connects scene language to editable physical programs.

**Method:** The system retrieves assets, uses Meshy when necessary and falls back to primitives only after generation fails. It writes materials, placement, control, cameras and lights, then revises the Genesis world using images, state and errors.

**Construction flow:** Dynamic scene request → Entities, motion and camera plan → Asset retrieval or generation → Physics and rendering code → Genesis rollout and revision → Executable 4D world

**Origin / output / platform:** Generative · Physical simulation programs and dynamic 4D worlds · Genesis

**Verification:** Physics invariants, text alignment, aesthetics and human ratings assess generated dynamic scenes. Policy training and real-robot transfer are not evaluated.

<details>
<summary>Abstract summary</summary>

Generative simulation connects scene language to editable physical programs. The system retrieves assets, uses Meshy when necessary and falls back to primitives only after generation fails. It writes materials, placement, control, cameras and lights, then revises the Genesis world using images, state and errors.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2607-19190"></a>
<!-- stage3-record: {"id": "2607.19190", "scope": "Core", "section": 2} -->

#### Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents

`2026-07-21` · University of British Columbia; National University of Singapore; Johns Hopkins University; Friedrich-Alexander-Universität Erlangen-Nürnberg; University of Cambridge; Columbia University; University of California, Los Angeles; Style3D

[Paper](https://arxiv.org/abs/2607.19190) · [Project page](https://agentic-real2sim.github.io/)

Robot episodes are reconstructed and refined through recorded-trajectory replay.

**Method:** Vision agents select frames, reconstruct and track objects; physics and scene agents assign priors and calibrate the camera, arm and ground. MuJoCo replay drives grasp-offset search or render-guided placement repair, with a registered Gaussian background.

**Construction flow:** RGB-D, calibration and trajectory → Object selection and segmentation → Meshes, scale and tracks → Physics and coordinate setup → Replay and grasp optimization → Executable episode twin

**Origin / output / platform:** Real-to-Sim · Episode twins with assets, cameras, trajectories, properties and replay interfaces · MuJoCo for rigid-body episodes

**Verification:** Five hundred DROID episodes retain failures in the replay-success denominator. Additional appearance and pose metrics and six real-task policy-evaluation comparisons are reported.

<details>
<summary>Abstract summary</summary>

Robot episodes are reconstructed and refined through recorded-trajectory replay. Vision agents select frames, reconstruct and track objects; physics and scene agents assign priors and calibrate the camera, arm and ground. MuJoCo replay drives grasp-offset search or render-guided placement repair, with a registered Gaussian background.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2607-13586"></a>
<!-- stage3-record: {"id": "2607.13586", "scope": "Adjacent", "section": 2} -->

#### UniPhysGen: Unified Physical Grounding for Simulation-Ready 3D Assets

`2026-07-15` · Zhejiang University; Manycore Tech; University of Electronic Science and Technology of China

[Bibliographic record](../README.md#paper-2607-13586) · [Paper](https://arxiv.org/abs/2607.13586) · [Code](https://github.com/breezexian/UniPhysGen) · [Dataset](https://huggingface.co/datasets/spatialverse/UniPhys-Bench)

Asset decomposition and learned physical grounding produce articulated simulation assets.

**Method:** UniPhys combines perceptual part grouping, multimodal physical-property estimates and geometry-constrained joint candidates. Consistency checks filter or refine annotations; UniPhysGen learns physical semantics with rotation-robust articulation supervision.

**Construction flow:** Existing 3D asset → Perceptual decomposition → Physical and joint hypotheses → Consistency filtering → Learned physical grounding

**Origin / output / platform:** Asset grounding (existing synthetic/CAD/artist models) · Articulated assets, physical annotations and a learned model · Isaac Sim validation; backend not specified

**Verification:** UniPhys-40K and the 1,927-object UniPhys-Bench support property, articulation and distribution-shift tests. Isaac Sim interaction examples assess plausibility, not measurement-accurate real-world parameters.

<details>
<summary>Abstract summary</summary>

Asset decomposition and learned physical grounding produce articulated simulation assets. UniPhys combines perceptual part grouping, multimodal physical-property estimates and geometry-constrained joint candidates. Consistency checks filter or refine annotations; UniPhysGen learns physical semantics with rotation-robust articulation supervision.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2607-07459"></a>
<!-- stage3-record: {"id": "2607.07459", "scope": "Resource", "section": 2} -->

#### EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI

`2026-07-08` · Horizon Robotics; WuwenAI

[Paper](https://arxiv.org/abs/2607.07459) · [Project page](https://horizonrobotics.github.io/EmbodiedGen/)

Physical assets, relational placement and stateful editing form a reusable world-building pipeline.

**Method:** The asset pipeline supplies scale, mass, friction and collision proxies. Task decomposition produces a role-aware graph; breadth-first placement and SAPIEN settling produce layouts. An agent-skill layer maintains edit state and exports configurations across simulators.

**Construction flow:** Text, image or task → Physical assets → Roles and spatial relations → BFS placement and settling → Stateful incremental editing → Cross-simulator assets and layouts

**Origin / output / platform:** Generative · URDF/XML/USD assets, scene graphs, layouts, affordances and edit state · Not specified; SAPIEN placement and grasp tests

**Verification:** Asset acceptance, scripted simulated grasp-lift and layout experiments are reported. Real-robot improvements summarized in the paper come from separate downstream VLA studies.

<details>
<summary>Abstract summary</summary>

Physical assets, relational placement and stateful editing form a reusable world-building pipeline. The asset pipeline supplies scale, mass, friction and collision proxies. Task decomposition produces a role-aware graph; breadth-first placement and SAPIEN settling produce layouts. An agent-skill layer maintains edit state and exports configurations across simulators.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4)

<a id="work-2607-01766"></a>
<!-- stage3-record: {"id": "2607.01766", "scope": "Adjacent", "section": 2} -->

#### SimWorlds: A Multi-Agent System for Dynamic 3D Scene Creation

`2026-07-02` · Carnegie Mellon University; Harvard University; University of California, Merced

[Paper](https://arxiv.org/abs/2607.01766) · [Project page](https://dynsimworlds.github.io/)

A staged coding system builds editable scenes that include animated and simulated processes.

**Method:** A fixed scene plan guides modeling, UVs, materials, deformation, motion, cameras and lighting. Deterministic scene and solver checks combine with rendered and runtime review; local retries repair the failing stage.

**Construction flow:** Scene specification → Staged scene program → Geometry and solver checks → Render and runtime review → Local repair → Executable Blender scene

**Origin / output / platform:** Generative · Editable Blender scenes with animation and simulation · Blender built-in simulation systems; backend not specified

**Verification:** 4DBuildBench evaluates 50 scenes using requirement and simulation checks, with additional visual and Blender benchmarks. The results concern digital scenes, not real-world dynamics calibration.

<details>
<summary>Abstract summary</summary>

A staged coding system builds editable scenes that include animated and simulated processes. A fixed scene plan guides modeling, UVs, materials, deformation, motion, cameras and lighting. Deterministic scene and solver checks combine with rendered and runtime review; local retries repair the failing stage.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2606-28276"></a>
<!-- stage3-record: {"id": "2606.28276", "scope": "Adjacent", "section": 2} -->

#### SimFoundry: Modular and Automated Scene Generation for Policy Learning and Evaluation

`2026-06-26` · NVIDIA; Georgia Institute of Technology; Stanford University; The University of Texas at Austin; University of Toronto

[Paper](https://arxiv.org/abs/2606.28276) · [Project page](https://research.nvidia.com/labs/gear/simfoundry/) · [Code](https://github.com/NVlabs/SimFoundry)

Real-video reconstruction expands into task-conditioned digital cousins for policy evaluation and training.

**Method:** Video processing estimates objects, depth, meshes, scale, poses, joints and collision properties. PyBullet settling removes penetrations; object, layout and task variations create digital cousins, with code-based actor–critic refinement for joints.

**Construction flow:** Real video → Object and geometry estimates → Physical configuration → Settling and articulation refinement → Object, layout and task variation → Twins and cousins

**Origin / output / platform:** Real-to-Sim + generative · Digital twins, digital cousins and task environments · PyBullet for preparation; downstream platform varies

**Verification:** Seven tasks and five policy families support simulated–real policy comparisons, including reported mean correlation 0.911 and MMRV 0.018. These are policy-ranking measures, not absolute reconstruction error.

<details>
<summary>Abstract summary</summary>

Real-video reconstruction expands into task-conditioned digital cousins for policy evaluation and training. Video processing estimates objects, depth, meshes, scale, poses, joints and collision properties. PyBullet settling removes penetrations; object, layout and task variations create digital cousins, with code-based actor–critic refinement for joints.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2606-14168"></a>
<!-- stage3-record: {"id": "2606.14168", "scope": "Adjacent", "section": 2} -->

#### MUSE: Agentic 3D Scene Authoring via Memory-Grounded Incremental Requirement Satisfaction

`2026-06-12` · East China Normal University; Fudan University; Shanghai Jiao Tong University

[Paper](https://arxiv.org/abs/2606.14168) · [Project page](https://xujay111.github.io/muse_githubio/)

An architect–builder–inspector workflow incrementally realizes editable indoor requirements.

**Method:** An architect turns requirements into a program; a sculptor retrieves assets and places or moves them. An inspector checks rules and renders, preserving satisfied relations while repairing unmet requirements.

**Construction flow:** Requirements → Architect program → Asset retrieval and placement → Rule and render inspection → Constraint-preserving edits → Editable scene

**Origin / output / platform:** Generative · Editable indoor scenes and relational constraints · Not specified

**Verification:** AuthorBench measures requirement satisfaction, preservation under edits, collisions, bounds and human preference. Navigation continuity is inspected, but dynamics calibration and real-robot transfer are not demonstrated.

<details>
<summary>Abstract summary</summary>

An architect–builder–inspector workflow incrementally realizes editable indoor requirements. An architect turns requirements into a program; a sculptor retrieves assets and places or moves them. An inspector checks rules and renders, preserving satisfied relations while repairing unmet requirements.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2606-04226"></a>
<!-- stage3-record: {"id": "2606.04226", "scope": "Adjacent", "section": 2} -->

#### PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification

`2026-06-02` · Université de Montréal; Mila – Quebec AI Institute

[Paper](https://arxiv.org/abs/2606.04226) · [Project page](https://percept-twin.github.io/)

An object-centric reconstruction adds executable affordances for checking robot plans.

**Method:** Object descriptions, masks and point clouds guide asset retrieval or generation and constrained alignment. An LLM assigns implemented affordances with preconditions and state changes; a separate judge checks plan-induced transitions.

**Construction flow:** Observed object map → Retrieved or generated assets → Constrained alignment → Affordances and preconditions → Plan-state simulation → Verified semantic twin

**Origin / output / platform:** Real-to-Sim · Object-centric twins with executable semantic state transitions · Not specified; AI2-THOR components

**Verification:** Visual reconstruction, a 93-person interpretability study and plan success, error and safety tests are reported. Simulation-based plan verification does not establish successful real-robot execution.

<details>
<summary>Abstract summary</summary>

An object-centric reconstruction adds executable affordances for checking robot plans. Object descriptions, masks and point clouds guide asset retrieval or generation and constrained alignment. An LLM assigns implemented affordances with preconditions and state changes; a separate judge checks plan-induced transitions.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3)

<a id="work-2605-21572"></a>
<!-- stage3-record: {"id": "2605.21572", "scope": "Adjacent", "section": 2} -->

#### PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects

`2026-05-20` · Nanyang Technological University; ACE Robotics

[Paper](https://arxiv.org/abs/2605.21572) · [Project page](https://physx-omni.github.io/)

A multimodal asset model predicts geometry together with articulated and physical structure.

**Method:** A Qwen2.5-VL-based model predicts classes, scale, part hierarchy, physical properties and template-aligned voxel sections. TRELLIS decodes meshes; joints and materials complete assets, with optional depth and segmentation for layout.

**Construction flow:** Image → Semantic and physical structure → Part-wise voxel prediction → Mesh decoding → Joints and materials → Simulatable assets

**Origin / output / platform:** Real-to-Sim · Articulated physical assets and optional scene layouts · Not specified; do not infer engine from the name

**Verification:** PhysXVerse, PhysXMobility and six-dimensional PhysXBench assess asset properties, with simulation demonstrations. These do not establish real-robot transfer; the name does not identify the PhysX engine.

<details>
<summary>Abstract summary</summary>

A multimodal asset model predicts geometry together with articulated and physical structure. A Qwen2.5-VL-based model predicts classes, scale, part hierarchy, physical properties and template-aligned voxel sections. TRELLIS decodes meshes; joints and materials complete assets, with optional depth and segmentation for layout.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2605-19587"></a>
<!-- stage3-record: {"id": "2605.19587", "scope": "Adjacent", "section": 2} -->

#### SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects

`2026-05-19` · The Chinese University of Hong Kong; Shanghai Jiao Tong University; Shanghai AI Laboratory; Microsoft; University of Oxford

[Paper](https://arxiv.org/abs/2605.19587) · [Project page](https://scene-code.github.io/) · [Code](https://github.com/wangpuyi/SceneCode)

Room planning and part-level programs produce editable scenes with physical asset metadata.

**Method:** A room agent issues typed asset requests. Reference images guide object plans and Blender programs, which are executed, repaired and visually checked; compilers add mass, inertia, collisions and joints linked through an asset registry.

**Construction flow:** Room request → Layout and asset routing → Object plan and part program → Execution and render checks → Physical-property compilation → Editable scene and registry

**Origin / output / platform:** Generative · Blender programs, asset registry and articulated physical descriptions · MuJoCo demonstrations; Blender authoring

**Verification:** Thirty prompts across six room types, SceneEval and a nine-user study evaluate scenes and assets. MuJoCo door and sliding demonstrations show execution, not a broad robot-policy benchmark.

<details>
<summary>Abstract summary</summary>

Room planning and part-level programs produce editable scenes with physical asset metadata. A room agent issues typed asset requests. Reference images guide object plans and Blender programs, which are executed, repaired and visually checked; compilers add mass, inertia, collisions and joints linked through an asset registry.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2605-14398"></a>
<!-- stage3-record: {"id": "2605.14398", "scope": "Core", "section": 2} -->

#### ChronoAgentic: A Code-based Multi-Agent World Simulator for Physically Grounded Simulation Construction

`2026-05-14` · University of Wisconsin–Madison

[Bibliographic record](../README.md#paper-2605-14398) · [Paper](https://arxiv.org/abs/2605.14398) · [Project page](https://uwsbel.github.io/chrono-agentic-website/)

A coding agent uses visual and numerical execution reports to build Chrono simulations.

**Method:** Human-reviewed plans, optional images, skills and asset retrieval guide PyChrono code. Headless runs generate initial frames and videos; visual and numerical reports localize code repairs.

**Construction flow:** Instruction and optional image → Reviewed plan and retrieval → PyChrono program → Headless simulation → Visual and numeric review → Targeted repair

**Origin / output / platform:** Generative · Executable PyChrono programs and simulation reports · Project Chrono

**Verification:** The paper reports 82.5% joint success on 80 supported PhyWorldBench tasks and simulated ROS driving. The evaluation remains within supported simulation tasks.

<details>
<summary>Abstract summary</summary>

A coding agent uses visual and numerical execution reports to build Chrono simulations. Human-reviewed plans, optional images, skills and asset retrieval guide PyChrono code. Headless runs generate initial frames and videos; visual and numerical reports localize code repairs.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3)

<a id="work-2605-15187"></a>
<!-- stage3-record: {"id": "2605.15187", "scope": "Adjacent", "section": 2} -->

#### Articraft: An Agentic System for Scalable Articulated 3D Asset Generation

`2026-05-14` · University of Cambridge; University of Oxford; Nanyang Technological University

[Paper](https://arxiv.org/abs/2605.15187) · [Project page](https://articraft3d.github.io/)

A single editable part program is tested with geometric and articulation probes before export.

**Method:** The agent edits model.py using SDK primitives and CadQuery, specifying parts, joint axes and limits. Custom tests and distance, penetration, containment and pose probes produce diagnostics for revisions and URDF export.

**Construction flow:** Object requirement → Part and joint program → Geometry and pose probes → Diagnostic-driven revision → URDF export → Articulated asset

**Origin / output / platform:** Generative · Editable articulated programs and URDF assets · Not specified; CadQuery authoring and Isaac Sim demonstrations

**Verification:** Experiments cover 46 object classes, five prompts each and 125 participants with about 5,000 preferences. Isaac Sim demonstrations assess generated joint data; there is no real-robot transfer test.

<details>
<summary>Abstract summary</summary>

A single editable part program is tested with geometric and articulation probes before export. The agent edits model.py using SDK primitives and CadQuery, specifying parts, joint axes and limits. Custom tests and distance, penetration, containment and pose probes produce diagnostics for revisions and URDF export.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4)

<a id="work-2605-09423"></a>
<!-- stage3-record: {"id": "2605.09423", "scope": "Core", "section": 2} -->

#### SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning

`2026-05-10` · UC San Diego; New York University

[Paper](https://arxiv.org/abs/2605.09423) · [Code](https://github.com/SimWorld-AI/SimWorld-Studio)

Environment construction and policy-learning feedback jointly shape simulated task curricula.

**Method:** A Python, MCP and skill interface edits Unreal Engine scenes using compiler, geometry and visual feedback. A Gymnasium learner supplies task outcomes that revise difficulty, scene distributions and accumulated skills.

**Construction flow:** Task and available skills → Scene-editing tools → Compiler, geometric and visual checks → Policy learning → Outcome-guided curriculum edits → Updated environments and skills

**Origin / output / platform:** Generative · Unreal scenes, task variants, curricula and reusable skills · Unreal Engine 5 platform; engine backend not specified

**Verification:** Three simulated navigation settings use success, SPL, SoftSPL and nDTW. Reported co-evolution gains concern simulated policies; SimCoder model weights remain fixed while context and skills change.

<details>
<summary>Abstract summary</summary>

Environment construction and policy-learning feedback jointly shape simulated task curricula. A Python, MCP and skill interface edits Unreal Engine scenes using compiler, geometry and visual feedback. A Gymnasium learner supplies task outcomes that revise difficulty, scene distributions and accumulated skills.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2605-09586"></a>
<!-- stage3-record: {"id": "2605.09586", "scope": "Adjacent", "section": 2} -->

#### DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos

`2026-05-10` · Nankai University; Zhejiang University; Southern University of Science and Technology; Rightly Robotics, A4X; University of Science and Technology of China

[Paper](https://arxiv.org/abs/2605.09586) · [Project page](https://can-lee.github.io/deformmaster-web/)

A differentiable deformable model recovers material behavior and contact from video.

**Method:** An MPM physical step is combined with a constrained neural velocity residual. Hand motion drives distributed compliant actuators, spatial material mixtures represent different constitutive behavior, and Gaussian skinning renders the result.

**Construction flow:** Video, point clouds and tracks → Contact and material representation → MPM plus residual model → Differentiable fitting → Gaussian rendering → Predictive deformable twin

**Origin / output / platform:** Real-to-Sim · Deformable geometry, material fields and predictive dynamics · Warp-based MPM

**Verification:** Twenty real PhysTwin sequences evaluate future geometry, tracks and images. The model is assessed as a dynamics foundation; robot-control transfer is not established, and thin structures remain difficult.

<details>
<summary>Abstract summary</summary>

A differentiable deformable model recovers material behavior and contact from video. An MPM physical step is combined with a constrained neural velocity residual. Hand motion drives distributed compliant actuators, spatial material mixtures represent different constitutive behavior, and Gaussian skinning renders the result.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2604-10992"></a>
<!-- stage3-record: {"id": "2604.10992", "scope": "Core", "section": 2} -->

#### ArtiCAD: Articulated CAD Assembly Design via Multi-Agent Code Generation

`2026-04-13` · Beihang University; Zhejiang University; The University of Hong Kong

[Bibliographic record](../README.md#paper-2604-10992) · [Paper](https://arxiv.org/abs/2604.10992) · [Project page](https://shui-yuan.github.io/articad/)

Part-local CAD programs and explicit connectors support repairable articulated assembly.

**Method:** A design specifies parts, connector frames, joints and limits. Independent FreeCAD Python programs create parts; deterministic connector assembly and multiview motion-keyframe review route failures to affected components for rollback and repair.

**Construction flow:** Articulated design → Part and connector specification → Independent CAD programs → Deterministic assembly → Multiview and motion review → Local repair and export

**Origin / output / platform:** Generative · Editable CAD parts, articulated assemblies and URDF · No dynamics engine specified; FreeCAD authoring

**Verification:** ArtiCADBench contains 120 tasks measuring geometry, detail, motion validity and construction success. Printing and URDF visualization demonstrate outputs rather than learned robot transfer.

<details>
<summary>Abstract summary</summary>

Part-local CAD programs and explicit connectors support repairable articulated assembly. A design specifies parts, connector frames, joints and limits. Independent FreeCAD Python programs create parts; deterministic connector assembly and multiview motion-keyframe review route failures to affected components for rollback and repair.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2602-10116"></a>
<!-- stage3-record: {"id": "2602.10116", "scope": "Adjacent", "section": 2} -->

#### SAGE: Scalable Agentic 3D Scene Generation for Embodied AI

`2026-02-10` · NVIDIA; University of Illinois Urbana-Champaign; Cornell University; Stanford University

[Paper](https://arxiv.org/abs/2602.10116) · [Project page](https://research.nvidia.com/labs/dir/sage/)

Visual and physical critics guide the generation of diverse robot-learning scenes.

**Method:** An agent plans rooms and uses asset placement, movement and deletion tools. TRELLIS assets receive estimated scale and properties; a visual critic reviews views while an Isaac Sim physics critic rejects unstable placements.

**Construction flow:** Room requirements → Assets and estimated properties → Placement tools → Visual and stability critics → Scene revision → Robot-learning environments

**Origin / output / platform:** Generative · Generated scenes and SAGE-10k environments · Isaac Sim platform; backend not specified

**Verification:** Scene appearance, collisions, stability and downstream imitation learning are evaluated in simulation. SAGE-10k provides generated environments; real-robot transfer is not established.

<details>
<summary>Abstract summary</summary>

Visual and physical critics guide the generation of diverse robot-learning scenes. An agent plans rooms and uses asset placement, movement and deletion tools. TRELLIS assets receive estimated scale and properties; a visual critic reviews views while an Isaac Sim physics critic rejects unstable placements.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2602-09153"></a>
<!-- stage3-record: {"id": "2602.09153", "scope": "Core", "section": 2} -->

#### SceneSmith: Agentic Generation of Simulation-Ready Indoor Scenes

`2026-02-09` · Massachusetts Institute of Technology; Toyota Research Institute

[Paper](https://arxiv.org/abs/2602.09153) · [Project page](https://scenesmith.github.io/)

Hierarchical agents generate physical scenes from architecture down to small objects.

**Method:** Designer, critic and orchestrator roles manage architecture, furniture and small items with edits and rollback. Generated images support static assets, retrieval supplies articulated ones, and physical preparation resolves penetrations and gravity settling.

**Construction flow:** Scene requirements → Hierarchical layout → Static and articulated assets → Designer–critic edits → Physical preparation → Portable scene descriptions

**Origin / output / platform:** Generative · Scenes exportable as SDFormat, MJCF and USD · Drake

**Verification:** Evaluation uses 210 prompts, 205 participants and SceneEval. Drake tests on 179 rooms report collision and stability measures; these remain simulation checks.

<details>
<summary>Abstract summary</summary>

Hierarchical agents generate physical scenes from architecture down to small objects. Designer, critic and orchestrator roles manage architecture, furniture and small items with edits and rollback. Generated images support static assets, retrieval supplies articulated ones, and physical preparation resolves penetrations and gravity settling.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2509-20414"></a>
<!-- stage3-record: {"id": "2509.20414", "scope": "Adjacent", "section": 2} -->

#### SceneWeaver: All-in-One 3D Scene Synthesis with an Extensible and Self-Reflective Agent

`2025-09-24` · State Key Laboratory of General Artificial Intelligence, BIGAI; Tsinghua University

[Paper](https://arxiv.org/abs/2509.20414) · [Project page](https://scene-weaver.github.io/) · [Code](https://github.com/Scene-Weaver/SceneWeaver)

Persistent scene state supports iterative generation, completion and local editing.

**Method:** A planner chooses operations from instructions, scene history and feedback. Blender and Infinigen instantiate geometry and relations; top-view images and state inspection guide subsequent collision and layout repairs.

**Construction flow:** Instruction and scene history → Plan edit or completion → Procedural geometry and layout → Top-view and state evaluation → Local repair → Editable scene

**Origin / output / platform:** Generative · Editable indoor scenes and USD exports · Blender/Infinigen authoring; Isaac Sim demonstration

**Verification:** Room diversity, visual quality and human preference are measured. USD export and a virtual G1 demonstration in Isaac Sim show simulation compatibility, not real-robot validation.

<details>
<summary>Abstract summary</summary>

Persistent scene state supports iterative generation, completion and local editing. A planner chooses operations from instructions, scene history and feedback. Blender and Infinigen instantiate geometry and relations; top-view images and state inspection guide subsequent collision and layout repairs.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3)

<a id="work-2411-01775"></a>
<!-- stage3-record: {"id": "2411.01775", "scope": "Adjacent", "section": 2} -->

#### Eurekaverse: Environment Curriculum Generation via Large Language Models

`2024-11-04` · University of Pennsylvania

[Paper](https://arxiv.org/abs/2411.01775) · [Project page](https://eureka-research.github.io/eurekaverse/)

Policy-learning outcomes drive an expanding curriculum of procedurally coded terrains.

**Method:** An LLM writes heightfields with eight waypoints, followed by runtime and geometry checks. Multiple PPO runs identify generalizing policies; terrain statistics, rewards and success feedback guide the next terrain generation round.

**Construction flow:** Task and terrain history → Heightfield code → Runtime and geometry checks → PPO training → Policy outcome feedback → New terrains and policies

**Origin / output / platform:** Generative · Terrain programs, curricula and locomotion policies · Extreme Parkour platform; engine not specified

**Verification:** Twenty simulated obstacles and real Go1 parkour evaluate downstream locomotion. Improvements update terrain curricula and control policies, not the coding model weights.

<details>
<summary>Abstract summary</summary>

Policy-learning outcomes drive an expanding curriculum of procedurally coded terrains. An LLM writes heightfields with eight waypoints, followed by runtime and geometry checks. Multiple PPO runs identify generalizing policies; terrain statistics, rewards and success feedback guide the next terrain generation round.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2410-15536"></a>
<!-- stage3-record: {"id": "2410.15536", "scope": "Adjacent", "section": 2} -->

#### GRS: Generating Robotic Simulation Tasks from Real-World Images

`2024-10-20` · NVIDIA; Stanford University

[Paper](https://arxiv.org/abs/2410.15536)

Real RGB-D scenes seed executable robot tasks whose code and tests are iteratively repaired.

**Method:** Segmentation and visual descriptions guide asset matching. A language model writes CLIPort task and unit-test code; an oracle execution router uses errors to revise the simulation or tests.

**Construction flow:** RGB-D scene → Objects and matching assets → Task and unit-test code → Oracle execution → Error routing and revision → Executable task variants

**Origin / output / platform:** Real-to-Sim · Scene-derived CLIPort tasks, variants and unit tests · CLIPort/GenSim platform; engine not specified

**Verification:** Ten scenes with 30 generations each are evaluated. Mean reward excludes runtime failures, and the reported task results do not establish calibrated real-world dynamics or real-policy transfer.

<details>
<summary>Abstract summary</summary>

Real RGB-D scenes seed executable robot tasks whose code and tests are iteratively repaired. Segmentation and visual descriptions guide asset matching. A language model writes CLIPort task and unit-test code; an oracle execution router uses errors to revise the simulation or tests.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4)

<a id="work-2410-13882"></a>
<!-- stage3-record: {"id": "2410.13882", "scope": "Core", "section": 2} -->

#### Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model

`2024-10-03` · University of Pennsylvania

[Paper](https://arxiv.org/abs/2410.13882) · [Project page](https://articulate-anything.github.io/) · [Code](https://github.com/vlongle/articulate-anything)

Image and motion feedback guide code that reconstructs articulated objects.

**Method:** Retrieved part meshes initialize Python programs specifying assembly and joints. A critic compares reference observations with simulated images or videos and asks an actor to repair geometry, axes, limits or motion.

**Construction flow:** Reference observation → Part retrieval → Assembly and joint code → Simulated views or motion → Actor–critic repair → Articulated asset

**Origin / output / platform:** Real-to-Sim + generative · Articulated object programs and simulator assets · PyBullet geometry; SAPIEN motion; MuJoCo/robosuite policy training

**Verification:** PartNet-Mobility construction tests are complemented by real Franka tests using four generated assets. Those small-scope results should not be treated as general transfer across all reconstructions.

<details>
<summary>Abstract summary</summary>

Image and motion feedback guide code that reconstructs articulated objects. Retrieved part meshes initialize Python programs specifying assembly and joints. A critic compares reference observations with simulated images or videos and asks an actor to repair geometry, axes, limits or motion.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2409-17652"></a>
<!-- stage3-record: {"id": "2409.17652", "scope": "Adjacent", "section": 2} -->

#### FactorSim: Generative Simulation via Factorized Representation

`2024-09-26` · Stanford University; NVIDIA

[Paper](https://arxiv.org/abs/2409.17652) · [Project page](https://cs.stanford.edu/~sunfanyun/factorsim/)

Factored state and transition models help generate task environments with limited context.

**Method:** Language requirements are decomposed into subtasks and factored POMDP components. The generator updates only relevant state, transition and reward components while maintaining model, control and view code.

**Construction flow:** Language requirements → Subtasks and relevant state factors → Transition and reward code → Incremental component updates → Execution and task checks → Factored environment

**Origin / output / platform:** Generative · Executable games and robot-task environment programs · PyGame and CLIPort; physics engine not specified

**Verification:** Eight games and 50 GenSim tasks assess code validity, human-rated requirements and simulated reinforcement-learning transfer. Oracle-controller checks constrain the interpretation of task solvability.

<details>
<summary>Abstract summary</summary>

Factored state and transition models help generate task environments with limited context. Language requirements are decomposed into subtasks and factored POMDP components. The generator updates only relevant state, transition and reward components while maintaining model, control and view code.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2409-02920"></a>
<!-- stage3-record: {"id": "2409.02920", "scope": "Adjacent", "section": 2} -->

#### RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins

`2024-09-04` · The University of Hong Kong; Shanghai AI Laboratory; Shenzhen University; AgileX Robotics; Institute of Automation, Chinese Academy of Sciences

[Paper](https://arxiv.org/abs/2409.02920) · [Project page](https://robotwin-benchmark.github.io/early-version/)

Reconstructed assets and language-generated motion programs produce bimanual demonstrations.

**Method:** RGB observations and Rodin meshes are enriched with functional contact and approach directions. GPT-4V reasons about key poses; GPT-4 calls trajectory tools to generate expert task programs.

**Construction flow:** Real object image → Mesh and functional directions → Key-pose reasoning → Trajectory-tool program → Expert execution → Bimanual demonstrations

**Origin / output / platform:** Real-to-Sim · Bimanual task programs, assets and expert demonstrations · COBOT Magic platform; engine not specified in this record

**Verification:** The early RoboTwin study evaluates six tasks with 10, 20 and 50 demonstrations for DP3. Policy-learning gains measure data utility, not calibrated scene physics or visual repair by the generator.

<details>
<summary>Abstract summary</summary>

Reconstructed assets and language-generated motion programs produce bimanual demonstrations. RGB observations and Rodin meshes are enriched with functional contact and approach directions. GPT-4V reasons about key poses; GPT-4 calls trajectory tools to generate expert task programs.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2406-08474"></a>
<!-- stage3-record: {"id": "2406.08474", "scope": "Adjacent", "section": 2} -->

#### Real2Code: Reconstruct Articulated Objects via Code Generation

`2024-06-12` · Stanford University; Columbia University

[Paper](https://arxiv.org/abs/2406.08474) · [Project page](https://real2code.github.io/)

Multiview reconstruction and a specialized code model recover articulated object descriptions.

**Method:** Part segmentation and completion produce oriented bounding boxes. A fine-tuned Code Llama maps their geometry to joint types, axes and positions in Python-generated MuJoCo descriptions.

**Construction flow:** Multiview observations → Part segmentation and completion → Oriented part boxes → Code-model joint inference → MJCF program → Reconstructed articulated object

**Origin / output / platform:** Real-to-Sim · Articulated object programs and MJCF · MuJoCo; Blender for training data

**Verification:** PartNet-based tests measure mesh distance and joint errors, including unseen objects with up to ten parts and examples from real views. Real-policy transfer is not evaluated.

<details>
<summary>Abstract summary</summary>

Multiview reconstruction and a specialized code model recover articulated object descriptions. Part segmentation and completion produce oriented bounding boxes. A fine-tuned Code Llama maps their geometry to joint types, axes and positions in Python-generated MuJoCo descriptions.

</details>

**Related:** [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2405-15568"></a>
<!-- stage3-record: {"id": "2405.15568", "scope": "Adjacent", "section": 2} -->

#### OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code

`2024-05-24` · Imperial College London; University of British Columbia; Vector Institute

[Paper](https://arxiv.org/abs/2405.15568) · [Project page](https://dub.sh/omniepic)

An archive of task outcomes supports open-ended generation of executable learning environments.

**Method:** Retrieved tasks and success or failure records guide novel Gymnasium Python environments. Compilation and learning failures trigger revisions; interestingness assessment determines which tasks enter the archive.

**Construction flow:** Task archive and outcomes → Novel task proposal → Environment code → Compilation and learning → Repair and interestingness review → Expanded archive

**Origin / output / platform:** Generative · Environment code, task archive and learned policies · Bullet/PyBullet; DreamerV3 learner

**Verification:** Diversity, open-endedness and simulated policy learning are measured, including long-running task generation. These results do not demonstrate physical-robot deployment.

<details>
<summary>Abstract summary</summary>

An archive of task outcomes supports open-ended generation of executable learning environments. Retrieved tasks and success or failure records guide novel Gymnasium Python environments. Compilation and learning failures trigger revisions; interestingness assessment determines which tasks enter the archive.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2312-09067"></a>
<!-- stage3-record: {"id": "2312.09067", "scope": "Adjacent", "section": 2} -->

#### Holodeck: Language Guided Generation of 3D Embodied AI Environments

`2023-12-14` · University of Pennsylvania; Stanford University; Allen Institute for Artificial Intelligence; University of Washington

[Paper](https://arxiv.org/abs/2312.09067) · [Project page](https://yueyang1996.github.io/holodeck/) · [Code](https://github.com/allenai/Holodeck)

Language-guided spatial constraints turn retrieved assets into interactive indoor environments.

**Method:** A language model proposes architecture, doors, windows, objects and spatial relations. Retrieved Objaverse and ProcTHOR assets are arranged with anchors and constraints for boundaries, relative placement and collisions.

**Construction flow:** Language description → Architecture and object relations → Asset retrieval → Constraint-based placement → Interactive scene → Navigation training and evaluation

**Origin / output / platform:** Generative · Interactive indoor scenes for AI2-THOR · Unity physics through AI2-THOR

**Verification:** A 680-person study evaluates generated scenes; NoveltyTHOR experiments measure ObjectNav improvement after training. Navigation gains are simulated downstream utility, not real-world reconstruction accuracy.

<details>
<summary>Abstract summary</summary>

Language-guided spatial constraints turn retrieved assets into interactive indoor environments. A language model proposes architecture, doors, windows, objects and spatial relations. Retrieved Objaverse and ProcTHOR assets are arranged with anchors and constraints for boundaries, relative placement and collisions.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2311-01455"></a>
<!-- stage3-record: {"id": "2311.01455", "scope": "Adjacent", "section": 2} -->

#### RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation

`2023-11-02` · Carnegie Mellon University; Tsinghua University; Massachusetts Institute of Technology; University of Massachusetts Amherst; MIT-IBM AI Lab

[Paper](https://arxiv.org/abs/2311.01455) · [Project page](https://robogen-ai.github.io/)

Task, environment and supervision generation automate diverse simulated robot-skill learning.

**Method:** An LLM proposes tasks around robots and seed objects, assembles assets and initial relations, then selects reinforcement learning, motion planning or differentiable trajectory optimization with suitable rewards and targets.

**Construction flow:** Robot and seed objects → Task and asset generation → Physical scene setup → Learning-method selection → Reward or target generation → Simulated skill learning

**Origin / output / platform:** Generative · Robot tasks, scenes, supervision and learned skills · Genesis development version

**Verification:** The paper describes 106 diverse tasks and learning results on 69 tasks. Reported simulated success reflects downstream skills, without demonstrating learned updates to the environment-writing agent.

<details>
<summary>Abstract summary</summary>

Task, environment and supervision generation automate diverse simulated robot-skill learning. An LLM proposes tasks around robots and seed objects, assembles assets and initial relations, then selects reinforcement learning, motion planning or differentiable trajectory optimization with suitable rewards and targets.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2310-18308"></a>
<!-- stage3-record: {"id": "2310.18308", "scope": "Adjacent", "section": 2} -->

#### Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models

`2023-10-27` · Carnegie Mellon University

[Paper](https://arxiv.org/abs/2310.18308) · [Project page](https://gen2sim.github.io/)

Image-derived physical assets and generated rewards support simulated manipulation learning.

**Method:** Zero123 and staged score-distillation generate textured meshes. A language model estimates size and mass, MeshLab supplies inertia, and URDF assets support generated task decompositions and reward programs for PPO.

**Construction flow:** Single object image → Textured mesh generation → Physical estimates and URDF → Task and reward code → PPO learning → Simulation and trajectory replay

**Origin / output / platform:** Real-to-Sim · Textured physical assets, URDF, task rewards and policies · Isaac Gym platform; backend not specified

**Verification:** Isaac Gym experiments assess assets and policy learning. The real demonstration replays optimized trajectories open loop; it does not establish closed-loop visual policy transfer.

<details>
<summary>Abstract summary</summary>

Image-derived physical assets and generated rewards support simulated manipulation learning. Zero123 and staged score-distillation generate textured meshes. A language model estimates size and mass, MeshLab supplies inertia, and URDF assets support generated task decompositions and reward programs for PPO.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2310-01361"></a>
<!-- stage3-record: {"id": "2310.01361", "scope": "Adjacent", "section": 2} -->

#### GenSim: Generating Robotic Simulation Tasks via Large Language Models

`2023-10-02` · MIT CSAIL; UC San Diego; University of Washington; CMU; Tsinghua University; Shanghai Jiao Tong University

[Paper](https://arxiv.org/abs/2310.01361) · [Project page](https://liruiw.github.io/gensim) · [Code](https://github.com/liruiw/GenSim)

Executable task generation scales demonstration collection and downstream robot-policy training.

**Method:** A language model proposes tasks, assets and goals with retrieved code examples, then writes Ravens/CLIPort classes. Oracle rollouts, model quality checks and manual filtering populate a task library for further generation and policy training.

**Construction flow:** Task request and retrieved examples → Task class and goal code → Oracle execution → Quality checks and filtering → Reusable task library → Policy pretraining

**Origin / output / platform:** Generative · Task programs, oracle demonstrations and policy-training data · PyBullet through Ravens/CLIPort

**Verification:** Seventy GPT-4-generated tasks support pretraining; twelve real tasks evaluate downstream policies. Real-task success concerns learned policies, not automatic calibration of generated environments.

<details>
<summary>Abstract summary</summary>

Executable task generation scales demonstration collection and downstream robot-policy training. A language model proposes tasks, assets and goals with retrieved code examples, then writes Ravens/CLIPort classes. Oracle rollouts, model quality checks and manual filtering populate a task library for further generation and policy training.

</details>

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-mujoco-workbench"></a>
<!-- stage3-record: {"id": "mujoco-workbench", "scope": "Resource", "section": 2} -->

#### mujoco-workbench

`First-public date not established` · Hebbian Robotics

[Code](https://github.com/Hebbian-Robotics/mujoco-workbench)

A CLI and agent skills support rapid construction and inspection of MuJoCo scenes.

**Method:** The mwb interface runs scenes, renders frames, checks phase contracts and exports multi-camera video. Skills organize these operations into an iterative scene-editing workflow.

**Construction flow:** Description and skills → Scene code → MuJoCo execution → Frames and contract diagnostics → Scene revision

**Origin / output / platform:** Generative tooling · Scene programs and inspection artifacts · MuJoCo

**Verification:** Official examples and diagnostics establish available tooling, not calibrated digital-twin accuracy or a controlled agent benchmark.

<details>
<summary>Abstract summary</summary>

A CLI and agent skills support rapid construction and inspection of MuJoCo scenes. The mwb interface runs scenes, renders frames, checks phase contracts and exports multi-camera video. Skills organize these operations into an iterative scene-editing workflow.

</details>

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4)

### Cross-section reading

- [PneuGen: Task-Driven Agentic Co-Design of Soft Pneumatic Robots](#work-2611-13344)
- [PhysOPSD: Code as Privilege for Physically Plausible Video Generation](#work-2611-12411)
- [BlenderFORGE: Framework for Optimizing Reactive 3D-Graphics Editing Ability of MLLMs](#work-2611-10768)
- [Frontier3DBench: Benchmarking Coding Agents for 3D Creation across Objects, Scenes, and Interactive Open Worlds](#work-2611-09017)
- [TactileLab: Sim-to-Real Dexterous Robot Manipulation with Efficient Shear-Sensitive Tactile Simulation](#work-2611-07881)
- [GREP: Grounding Generated Room Evaluation in Principles](#work-2611-05802)
- [ScIntBench: Physical Interaction Plausibility in 3D Scene Generation](#work-2610-37326)
- [CoDA: Co-Evolution of Data Engines and Action Policies](#work-2610-22362)
- [BlenderWorld: Benchmarking Visual Agents for 3D Creation from Real-World References](#work-system-blenderworld)
- [YUBI-Real2Sim: 3DGS Scene Verification for Reliable Policy Evaluation](#work-2610-17521)
- [PhysCodeGym: Benchmarking Coding Agents for Physically Verifiable 4D Reconstruction](#work-2610-17288)
- [ExeWorldBench: Benchmarking Code-Based Executable 3D World Modeling](#work-2610-15166)
- [WorldSolver: Can LLM Agents Simulate the Physical Dynamics via Solver Generation?](#work-2610-08720)
- [Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos](#work-2610-04432)
- [4DCodeBench: Benchmarking Agents on Inverse Graphics of Dynamic Scenes](#work-2610-03715)
- [Code4Scene: Benchmarking Coding Agents for Constructing and Editing 3D Scenes](#work-2609-36777)
- [DexAgent: An Agentic Human2Sim2Robot Framework for Dexterous Manipulation with Self-Evolving Tool Library](#work-2609-35318)
- [EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics](#work-2609-27308)
- [BVB: Benchmarking Agentic Video Understanding via Programmatic Reconstruction in Blender](#work-2609-15478)
- [WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis](#work-2606-01869)
- [MPMWorlds: Material-Point-Method Simulations for Inferring and Extrapolating Physical Dynamics](#work-2606-01538)
- [Δynamics: Language-Based Representation for Inferring Rigid-Body Dynamics From Videos](#work-2605-20576)
- [AI-designed and AI-implemented control systems for bespoke scientific instrumentation: application to scanning microscopy](#work-bespoke-instrument)
- [PhysCodeBench: Benchmarking Physics-Aware Symbolic Simulation of 3D Scenes via Self-Corrective Multi-Agent Refinement](#work-2604-23580)
- [SceneCritic: A Symbolic Evaluator for 3D Indoor Scene Synthesis](#work-2604-13035)
- [SceneTeract: Probing and Improving Agent-Aware Activity Reasoning in 3D Indoor Scenes](#work-2603-29798)
- [IRIS: A Real-World Benchmark for Inverse Recovery and Identification of Physical Dynamic Systems from Monocular Video](#work-2603-16432)
- [Training and Benchmarking Code Generation for Physics-Inspired Animations](#work-2602-10840)
- [VisPhyWorld: Probing Physical Reasoning via Code-Driven Video Reconstruction](#work-2602-13294)
- [Apples on the Table? Evaluating Text-Guided 3D Scene Synthesis via Fine-Grained Constraint Verification](#work-2511-03001)
- [IR3D-Bench: Evaluating Vision-Language Model Scene Understanding as Agentic Inverse Rendering](#work-2506-23329)
- [RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation](#work-2506-18088)
- [BlenderGym: Benchmarking Foundational Model Systems for Graphics Editing](#work-2504-01786)
- [SceneEval: Evaluating Semantic Coherence in Text-Conditioned 3D Indoor Scene Synthesis](#work-2503-14756)
- [GenSim2: Scaling Robot Data Generation with Multi-modal and Reasoning LLMs](#work-2410-03645)
- [DrEureka: Language Model Guided Sim-To-Real Transfer](#work-2406-01967)
- [Evaluating Real-World Robot Manipulation Policies in Simulation](#work-2405-05941)
- [Real2Sim Benchmark](#work-real2sim-benchmark)

[Back to the research map](#research-map)

---

<a id="section-3"></a>

## 3. Simulator Quality Evaluation

Start with **what is evaluated**, then distinguish agreement with observations, responses to interaction, behavior under unseen conditions and downstream usefulness. These are complementary questions: a visually faithful reconstruction may fail to support contact, while successful control may compensate for an inaccurate world.

| Evaluation object | What is delivered | Representative checks |
|---|---|---|
| Objects and scenes | Geometry, layout, materials and articulated assets | Appearance, size, support, collision, semantic constraints and articulation |
| Task environments | A world with action, observation, reset and success interfaces | Interface consistency, fixed-policy outcomes and agreement with real evaluations |
| Dynamic simulation cases | An executable scene and its time evolution, sometimes with a generated controller | Motion, physical events, task completion and changed-condition execution |
| Dynamics models and solvers | Parameters, governing rules or numerical state updates | Measured parameters, conservation, stability, identifiability and extrapolation |

**Read the evidence boundary.** Static support checks do not validate a solver. Re-rendering by an independent judge does not prove that the constructing agent used visual feedback. Native-state checks, withheld tests and counterfactual interventions add different evidence; their applicability, budgets and failure denominators should be stated. Agent competence benchmarks, including operating and auditing worlds, belong in Section 1.

**Separate world and controller errors.** Hold actions or policies fixed, use a known-working reference environment, and report execution conditions. Cross-execution can diagnose compatibility but is not automatically a causal decomposition. In Video2World, the main result belongs to a submitted scene–behavior pair; the supplementary transferred-controller tests cover a conditioned subset. [Video2World protocol](https://arxiv.org/html/2610.04432#S10.SS1)

**Keep reference provenance explicit.** Measured robot motion, commanded action targets and simulated execution trajectories are different quantities. Video2World combines real observations, fitted geometry/motion and native simulation states across sources; its human-assisted reference (HAR) is a constructed execution with additional information, not the ground-truth observations or a performance ceiling. Its supplementary effector comparison uses actual executed link poses, with source-specific correspondence across embodiments. [Data and reference protocol](https://arxiv.org/html/2610.04432#S8.SS1)

Research questions remain: which quality checks predict success with unseen controllers or interventions, and how can acceptance thresholds be calibrated to real-world errors and uncertainty? A complete environment → experience → improved coding-agent loop requires separate evidence for each connection.

<a id="work-2611-13576"></a>
<!-- stage3-record: {"id": "2611.13576", "scope": "Adjacent", "section": 3} -->

#### PhyRubric: Rubric-Grounded Diagnostic Evaluation of Physical Commonsense in Text-to-Video Generation

`2026-11-10` · University of Illinois Chicago

[Bibliographic record](../README.md#paper-2611-13576) · [Paper](https://arxiv.org/abs/2611.13576) · [Code](https://github.com/chenyil6/phyRubric) · [Dataset](https://huggingface.co/datasets/kittyhy/PhyRubric-Bench)

Diagnoses visible physical-commonsense failures in generated videos through caption-specific rubrics.

**Method:** Fixes semantic and physical requirements before viewing a clip, grounds verdicts in timestamped evidence, and derives scores from those verdicts. Released benchmark and training videos support fine-tuning a VLM judge.

**Evaluation object:** Visible physical phenomena in generated video; adjacent diagnostic reference

**Verification:** Human agreement and held-out generator/domain tests assess the judge. It checks noninteractive video plausibility, not executable dynamics; training updates judge weights rather than a coding agent. Benchmark labels are human-verified, while training labels use an agentic annotator.

**Related:** [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2611-09017"></a>
<!-- stage3-record: {"id": "2611.09017", "scope": "Adjacent", "section": 3} -->

#### Frontier3DBench: Benchmarking Coding Agents for 3D Creation across Objects, Scenes, and Interactive Open Worlds

`2026-11-06` · Navers Lab; Einsia.AI; Tsinghua University

[Bibliographic record](../README.md#paper-2611-09017) · [Paper](https://arxiv.org/abs/2611.09017)

Evaluates code-authored objects, scenes and interactive worlds across Blender and Unreal Engine.

**Method:** Combines rendered evidence and native-scene structure with runtime checks of interaction contracts and persistent state, according to each task’s output requirements.

**Evaluation object:** Objects, scenes and interactive task environments

**Verification:** A broad 3D-creation reference, including functional world checks; visual or interaction success does not establish calibrated physical parameters.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2611-05802"></a>
<!-- stage3-record: {"id": "2611.05802", "scope": "Adjacent", "section": 3} -->

#### GREP: Grounding Generated Room Evaluation in Principles

`2026-11-04` · University of Washington; Tencent AI Lab; HKUST; USTC; Shanghai Jiao Tong University

[Paper](https://arxiv.org/abs/2611.05802)

An evaluation agent diagnoses generated rooms using scene-specific principles and active inspection.

**Method:** Turns physical validity, visual coherence and everyday use into targeted checks, then combines geometry tools with selected rendered views.

**Evaluation object:** Objects and scenes

**Verification:** Collision, support, boundary and access checks primarily establish static quality. An evaluator inspecting a scene is distinct from its generator observing and repairing it.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2610-37326"></a>
<!-- stage3-record: {"id": "2610.37326", "scope": "Adjacent", "section": 3} -->

#### ScIntBench: Physical Interaction Plausibility in 3D Scene Generation

`2026-10-27` · University of Western Australia; University of British Columbia

[Bibliographic record](../README.md#paper-2610-37326) · [Paper](https://arxiv.org/abs/2610.37326)

Tests whether generated indoor scenes support prescribed physical interactions.

**Method:** Runs standardized pushes, articulation actions and surface probes; combines interaction success and integrity with semantic, static and video-based dynamic checks.

**Evaluation object:** Objects and scenes

**Verification:** The target is interaction plausibility, not recovery of one unique real scene. Probe-controller failures must be distinguished from missing or invalid scene capabilities.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-system-blenderworld"></a>
<!-- stage3-record: {"id": "system:blenderworld", "scope": "Core", "section": 3} -->

#### BlenderWorld: Benchmarking Visual Agents for 3D Creation from Real-World References

`2026-10-14` · Zhejiang University; Alibaba Token Hub, Alibaba Group; The Chinese University of Hong Kong; Fudan University; National University of Singapore

[Bibliographic record](../README.md#paper-system-blenderworld) · [Paper](https://arxiv.org/abs/2610.23986) · [Project page](https://blenderworld.github.io/)

Evaluates reusable Blender creations produced from real-world references and specifications.

**Method:** Uses multi-view rendering, native-scene evidence and task-specific rubrics to assess structure, appearance and fulfillment of creative requirements.

**Evaluation object:** Objects and scenes

**Verification:** A useful reference for evaluating executable 3D artifacts; most tasks do not establish a calibrated physical simulator.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2610-17521"></a>
<!-- stage3-record: {"id": "2610.17521", "scope": "Adjacent", "section": 3} -->

#### YUBI-Real2Sim: 3DGS Scene Verification for Reliable Policy Evaluation

`2026-10-13` · AI Robot Association (AIRoA); Waseda University

[Paper](https://arxiv.org/abs/2610.17521) · [Project page](https://research.airoa.io/publications/yubi-real2sim/) · [Dataset](https://huggingface.co/datasets/airoa-org/yubi-real2sim-assets) · [Code](https://github.com/airoa-org/yubi-real2sim)

Studies whether reconstructed 3DGS scenes preserve real robot policy rankings.

**Method:** Combines calibrated wrist-camera views with MuJoCo, compares paired real/simulated policy results, and varies background artifacts while holding objects, physics and rollout conditions fixed.

**Evaluation object:** Task environments

**Verification:** Visual scores alone do not reliably predict ranking failures. The released assets and policies cover declared configurations; assets require access approval and are not an unrestricted open download.

**Related:** [2. Simulator Construction](#section-2) · [4. Data](#section-4)

<a id="work-2610-17288"></a>
<!-- stage3-record: {"id": "2610.17288", "scope": "Core", "section": 3} -->

#### PhysCodeGym: Benchmarking Coding Agents for Physically Verifiable 4D Reconstruction

`2026-10-12` · Shanghai Jiao Tong University; Sun Yat-sen University; Shanghai Innovation Institute; Southeast University; Nanyang Technological University; Carnegie Mellon University

[Bibliographic record](../README.md#paper-2610-17288) · [Paper](https://arxiv.org/abs/2610.17288)

Tests coding agents that reconstruct physical video phenomena as executable Blender scenes.

**Method:** Combines execution, visual and motion checks with program inspection, physical-state measurements and counterfactual resimulation for eligible tasks.

**Evaluation object:** Dynamic simulation cases

**Verification:** Principal motion should arise from physical mechanisms. Intervention coverage varies by task, and hidden parameters need not all be uniquely identifiable from video.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2610-15166"></a>
<!-- stage3-record: {"id": "2610.15166", "scope": "Adjacent", "section": 3} -->

#### ExeWorldBench: Benchmarking Code-Based Executable 3D World Modeling

`2026-10-10` · University of Science and Technology of China; The Chinese University of Hong Kong

[Bibliographic record](../README.md#paper-2610-15166) · [Paper](https://arxiv.org/abs/2610.15166)

Evaluates executable worlds spanning isolated mechanisms, coupled systems and goal-driven design.

**Method:** Assesses generated worlds for visual structure, mechanical motion, apparent causal processes and goal fulfillment using sampled rendered frames.

**Evaluation object:** Dynamic simulation cases

**Verification:** Rendered-frame judgments of causality are not equivalent to native-state auditing or controlled causal intervention.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2610-08720"></a>
<!-- stage3-record: {"id": "2610.08720", "scope": "Adjacent", "section": 3} -->

#### WorldSolver: Can LLM Agents Simulate the Physical Dynamics via Solver Generation?

`2026-10-06` · NLPR & MAIS, CASIA; Peking University; Huawei Noah’s Ark Lab

[Bibliographic record](../README.md#paper-2610-08720) · [Paper](https://arxiv.org/abs/2610.08720)

Asks language-model agents to implement the dynamics solver within a prepared simulation framework.

**Method:** Executes the generated solver and separately checks runnability, visual events and physical behavior under the supplied scene and interfaces.

**Evaluation object:** Dynamics models and solvers

**Verification:** Geometry, parameters and execution scaffolding are provided; this measures solver generation rather than construction of an entire general-purpose simulator.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2610-04432"></a>
<!-- stage3-record: {"id": "2610.04432", "scope": "Core", "section": 3} -->

#### Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos

`2026-10-03` · Aether AI; University of California San Diego

[Bibliographic record](../README.md#paper-2610-04432) · [Paper](https://arxiv.org/abs/2610.04432) · [Documentation](https://github.com/AetherLabsAI/Video2World/blob/main/docs/benchmark.md)

Evaluates joint reconstruction of simulated environments and robot behavior from embodied videos.

**Method:** Executes each submitted scene–behavior pair, then compares geometry, object trajectories and task outcomes. Supplementary cross-execution tests controller–scene compatibility.

**Evaluation object:** Dynamic simulation cases

**Verification:** Success is an end-to-end result, not an environment-only score. Reference geometry/motion may be measured, fitted or simulated; human-assisted reference execution is separate from those targets and is not an upper bound.

**Related:** [2. Simulator Construction](#section-2) · [4. Data](#section-4)

<a id="work-2610-03715"></a>
<!-- stage3-record: {"id": "2610.03715", "scope": "Adjacent", "section": 3} -->

#### 4DCodeBench: Benchmarking Agents on Inverse Graphics of Dynamic Scenes

`2026-10-02` · Johns Hopkins University; Stanford University; Max Planck Institute for Intelligent Systems; Massachusetts Institute of Technology

[Bibliographic record](../README.md#paper-2610-03715) · [Paper](https://arxiv.org/abs/2610.03715)

Measures inverse graphics of dynamic videos through executable scene programs.

**Method:** Compares appearance, 2D motion and 2.5D geometry, with direct 3D geometry and motion checks on the synthetic subset.

**Evaluation object:** Dynamic simulation cases

**Verification:** Keyframes and prescribed trajectories are allowed. Reconstruction fidelity does not establish a correct physical mechanism; real-video depth and motion references partly use estimates.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2609-36777"></a>
<!-- stage3-record: {"id": "2609.36777", "scope": "Core", "section": 3} -->

#### Code4Scene: Benchmarking Coding Agents for Constructing and Editing 3D Scenes

`2026-09-29` · University of California San Diego; University of California Berkeley

[Bibliographic record](../README.md#paper-2609-36777) · [Paper](https://arxiv.org/abs/2609.36777)

Tests scene construction and precise editing through a shared Unreal Engine interface.

**Method:** Inspects native scene state for requirement fulfillment, artifact integrity and static validity; editing also measures target recovery and preservation of unrelated content.

**Evaluation object:** Objects and scenes

**Verification:** Static support and penetration checks do not establish dynamic validity or recovery of real physical parameters.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2611-02659"></a>
<!-- stage3-record: {"id": "2611.02659", "scope": "Adjacent", "section": 3} -->

#### Parametric CAD Bench v3: Evaluating Agentic Parametric CAD Authoring from Text and Engineering Drawings

`2026-09-21` · gNucleus AI, Inc.

Official benchmark release: 2026-09-21; arXiv v1: 2026-11-02.

[Bibliographic record](../README.md#paper-2611-02659) · [Paper](https://arxiv.org/abs/2611.02659) · [Article](https://cadbench.ai/news/cad-bench-v3) · [Dataset](https://huggingface.co/datasets/gnucleus-ai/cad-gen-freecad-bench-v3)

Tests native parametric CAD authoring from text, create-and-edit requests and engineering drawings.

**Method:** Runs agents in pinned FreeCAD/Harbor environments and grades native geometry and specification consistency with an isolated verifier. Versioned tasks are accompanied by released trial records, trajectories and CAD artifacts.

**Evaluation object:** Objects and native parametric CAD geometry

**Verification:** Continuous reward is not binary task success. These are parametric-object and feature-structure checks, not dynamics or manufacturing certification; create-and-edit scores do not prove reuse of the base feature history. Released evaluation runs are experiment artifacts, not a separately validated training dataset.

**Related:** [4. Data](#section-4) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2609-15478"></a>
<!-- stage3-record: {"id": "2609.15478", "scope": "Adjacent", "section": 3} -->

#### BVB: Benchmarking Agentic Video Understanding via Programmatic Reconstruction in Blender

`2026-09-14` · University of Rochester; Sony Group Corporation; Carnegie Mellon University; University of Washington

[Bibliographic record](../README.md#paper-2609-15478) · [Paper](https://arxiv.org/abs/2609.15478)

Uses programmatic Blender reconstruction to test agentic video understanding.

**Method:** Compares rendered representations and retention of spatiotemporal facts through video question answering under shared budgets.

**Evaluation object:** Dynamic simulation cases

**Verification:** Visual reconstruction does not establish physical mechanisms. Camera-induced changes must be separated from object dynamics.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2606-01869"></a>
<!-- stage3-record: {"id": "2606.01869", "scope": "Adjacent", "section": 3} -->

#### WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis

`2026-06-01` · NLPR & MAIS, CASIA; Huawei Noah’s Ark Lab

[Paper](https://arxiv.org/abs/2606.01869)

Tests whether generated interactive 3D programs satisfy executable world contracts.

**Method:** StateProbe executes prescribed actions and reads resulting states and transitions, exposing failures hidden by plausible rendered frames.

**Evaluation object:** Dynamic simulation cases

**Verification:** Its suite also contains rendering and application tasks. The physical subset offers contract checks, not proof of real-world parameter calibration.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2606-01538"></a>
<!-- stage3-record: {"id": "2606.01538", "scope": "Adjacent", "section": 3} -->

#### MPMWorlds: Material-Point-Method Simulations for Inferring and Extrapolating Physical Dynamics

`2026-06-01` · Cornell University

[Paper](https://arxiv.org/abs/2606.01538)

Compares program-based physical inference with video prediction in synthetic 2D material-point worlds.

**Method:** Infers a program from an observed prefix, runs it into held-out time, and compares motion, overlap, object retention and temporal stability.

**Evaluation object:** Dynamic simulation cases

**Verification:** Evaluation mainly compares rendered videos rather than native particle trajectories. The dataset and benchmark are contributions of the same work.

**Related:** [2. Simulator Construction](#section-2) · [4. Data](#section-4)

<a id="work-2605-20576"></a>
<!-- stage3-record: {"id": "2605.20576", "scope": "Adjacent", "section": 3} -->

#### Δynamics: Language-Based Representation for Inferring Rigid-Body Dynamics From Videos

`2026-05-20` · Cornell University; Amazon

[Paper](https://arxiv.org/abs/2605.20576)

Represents video-inferred rigid-body systems as structured simulator configurations.

**Method:** Predicts shape, state, physics and camera settings; executes and refines configurations, comparing object composition, mask overlap, optical flow and available parameter ground truth.

**Evaluation object:** Dynamics models and solvers

**Verification:** Structured configuration prediction is not necessarily a general coding-agent loop. Real-video pseudo-labels do not amount to independently measured physical ground truth.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2604-23580"></a>
<!-- stage3-record: {"id": "2604.23580", "scope": "Adjacent", "section": 3} -->

#### PhysCodeBench: Benchmarking Physics-Aware Symbolic Simulation of 3D Scenes via Self-Corrective Multi-Agent Refinement

`2026-04-26` · Nanjing University; Skywork AI; Jilin University; Great Wall Motor; Tianjin University

[Paper](https://arxiv.org/abs/2604.23580)

Evaluates simulation code for described physical phenomena and studies targeted multi-agent correction.

**Method:** Combines executability, appearance and motion measurements with separately reported expert physical assertions and applicable conservation checks.

**Evaluation object:** Dynamic simulation cases

**Verification:** A composite visual score and a physical-assertion result answer different questions; a high overall score alone does not establish physical correctness.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2604-13035"></a>
<!-- stage3-record: {"id": "2604.13035", "scope": "Adjacent", "section": 3} -->

#### SceneCritic: A Symbolic Evaluator for 3D Indoor Scene Synthesis

`2026-04-14` · Stony Brook University

[Paper](https://arxiv.org/abs/2604.13035)

Provides explainable symbolic assessment of indoor layouts and feedback for revision.

**Method:** Checks object scale, co-occurrence, proximity, orientation, completeness and overlap using structured scene information.

**Evaluation object:** Objects and scenes

**Verification:** These are chiefly static semantic and geometric checks, not validation of physical time evolution.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2603-29798"></a>
<!-- stage3-record: {"id": "2603.29798", "scope": "Adjacent", "section": 3} -->

#### SceneTeract: Probing and Improving Agent-Aware Activity Reasoning in 3D Indoor Scenes

`2026-03-31` · École Polytechnique; Dassault Systèmes; Stanford University; Università della Svizzera italiana

[Paper](https://arxiv.org/abs/2603.29798)

Tests whether a scene can support an activity for a specified body and uses verification feedback to improve activity reasoning.

**Method:** Decomposes activities into object-directed actions, then checks reachability, manipulation space and paths before producing failure explanations.

**Evaluation object:** Objects and scenes

**Verification:** Functional geometric feasibility and a model’s feasibility judgment are distinct from executing robot dynamics in the real world.

**Related:** [2. Simulator Construction](#section-2) · [5. Training and Capability Improvement](#section-5)

<a id="work-2603-16432"></a>
<!-- stage3-record: {"id": "2603.16432", "scope": "Adjacent", "section": 3} -->

#### IRIS: A Real-World Benchmark for Inverse Recovery and Identification of Physical Dynamic Systems from Monocular Video

`2026-03-17` · Hamad Bin Khalifa University; Texas A&M University

[Paper](https://arxiv.org/abs/2603.16432)

Benchmarks inverse identification of physical systems using real videos and independent measurements.

**Method:** Tests parameter or equation recovery against measured references with uncertainty, then assesses identifiability, robustness and temporal extrapolation.

**Evaluation object:** Dynamics models and solvers

**Verification:** A stronger reference for physical calibration, but not a whole-scene coding-agent benchmark. Measurements and their uncertainty remain essential to interpretation.

**Related:** [2. Simulator Construction](#section-2) · [4. Data](#section-4)

<a id="work-2602-10840"></a>
<!-- stage3-record: {"id": "2602.10840", "scope": "Adjacent", "section": 3} -->

#### Training and Benchmarking Code Generation for Physics-Inspired Animations

`2026-02-11` · Mohamed bin Zayed University of Artificial Intelligence; Sun Yat-sen University

[Paper](https://arxiv.org/abs/2602.10840)

Trains and evaluates language models that express physical concepts through executable animations.

**Method:** Checks code execution and whether rendered videos depict the requested phenomena; visual verification rewards support model reinforcement learning.

**Evaluation object:** Dynamic simulation cases

**Verification:** The current title explicitly concerns physics-inspired animations. Depicting qualitative dynamics is different from numerically solving the underlying system.

**Related:** [2. Simulator Construction](#section-2) · [5. Training and Capability Improvement](#section-5)

<a id="work-2602-13294"></a>
<!-- stage3-record: {"id": "2602.13294", "scope": "Adjacent", "section": 3} -->

#### VisPhyWorld: Probing Physical Reasoning via Code-Driven Video Reconstruction

`2026-02-09` · University of Waterloo; Autodesk AI Lab; independent researcher

[Paper](https://arxiv.org/abs/2602.13294)

Probes physical reasoning by reconstructing controlled videos as simulator programs.

**Method:** VisPhyBench compares appearance, motion and judged physical plausibility of executed reconstructions; some settings also supply first-frame structure.

**Evaluation object:** Dynamic simulation cases

**Verification:** These visual and judgment proxies do not establish comprehensive recovery of real physical parameters.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2511-03001"></a>
<!-- stage3-record: {"id": "2511.03001", "scope": "Adjacent", "section": 3} -->

#### Apples on the Table? Evaluating Text-Guided 3D Scene Synthesis via Fine-Grained Constraint Verification

`2025-11-04` · Yonsei University; POSTECH

[Paper](https://arxiv.org/abs/2511.03001)

Evaluates text-guided scenes by verifying fine-grained requirements individually.

**Method:** LEGO provides annotated constraints and reference scenes; LEGO-Eval uses tools and views to check objects, attributes and spatial relations.

**Evaluation object:** Objects and scenes

**Verification:** Requirement fulfillment is complementary to dynamic physical testing. LEGO and LEGO-Eval are contributions of one paper.

**Related:** [2. Simulator Construction](#section-2) · [4. Data](#section-4)

<a id="work-2506-23329"></a>
<!-- stage3-record: {"id": "2506.23329", "scope": "Adjacent", "section": 3} -->

#### IR3D-Bench: Evaluating Vision-Language Model Scene Understanding as Agentic Inverse Rendering

`2025-06-29` · The Chinese University of Hong Kong; Tianjin University; EPFL; HKUST; Xiamen University; Massachusetts Institute of Technology

[Paper](https://arxiv.org/abs/2506.23329)

Uses agentic inverse rendering to test whether visual understanding can produce an executable scene.

**Method:** Agents program and render image-based reconstructions, assessed for localization, counts, relationships, appearance and semantics.

**Evaluation object:** Objects and scenes

**Verification:** Image-space localization or masks are not equivalent to measured 3D physical state; the benchmark does not calibrate dynamics.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2504-01786"></a>
<!-- stage3-record: {"id": "2504.01786", "scope": "Adjacent", "section": 3} -->

#### BlenderGym: Benchmarking Foundational Model Systems for Graphics Editing

`2025-04-02` · Stanford University

[Paper](https://arxiv.org/abs/2504.01786)

Benchmarks programmatic graphics edits and allocation of generation and verification compute.

**Method:** Agents edit Blender programs to match target geometry, materials, lighting, poses or deformation; evaluation uses multi-view images and applicable 3D distances.

**Evaluation object:** Objects and scenes

**Verification:** These distances may miss physical implausibility. They complement rather than replace simulator validation.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2503-14756"></a>
<!-- stage3-record: {"id": "2503.14756", "scope": "Adjacent", "section": 3} -->

#### SceneEval: Evaluating Semantic Coherence in Text-Conditioned 3D Indoor Scene Synthesis

`2025-03-18` · Simon Fraser University; Amii

[Paper](https://arxiv.org/abs/2503.14756)

Provides fine-grained semantic and static checks for text-conditioned indoor scene generation.

**Method:** Checks explicit object, attribute and relation requirements alongside implicit support, collision, traversal and opening clearances.

**Evaluation object:** Objects and scenes

**Verification:** Primarily a static scene-quality framework; its geometric consistency tests do not validate dynamic simulation.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2405-05941"></a>
<!-- stage3-record: {"id": "2405.05941", "scope": "Adjacent", "section": 3} -->

#### Evaluating Real-World Robot Manipulation Policies in Simulation

`2024-05-09` · University of California San Diego; Stanford University; University of California Berkeley; Google DeepMind

[Paper](https://arxiv.org/abs/2405.05941)

Studies whether simulation can predict real-world manipulation policy performance.

**Method:** Reduces visual and control gaps, then compares policies in corresponding simulated and real settings, including sensitivity to environment variation.

**Evaluation object:** Task environments

**Verification:** This evaluates usefulness for policy assessment rather than autonomous scene reconstruction. Results depend on visual, controller and dynamics alignment.

**Related:** [1. Embodied Harnesses](#section-1) · [2. Simulator Construction](#section-2) · [5. Training and Capability Improvement](#section-5)

<a id="work-real2sim-benchmark"></a>
<!-- stage3-record: {"id": "real2sim-benchmark", "scope": "Adjacent", "section": 3} -->

#### Real2Sim Benchmark

`First-public date not established` · Momentum Research Labs

[Project page](https://www.real2sim.bot/)

Tests reconstruction of robot episodes through frozen-scene rendering, action replay and policy execution.

**Method:** Agents receive videos, calibration and action records; frozen deliverables are assessed with image metrics, recorded joint/gripper-command replay and a fixed policy.

**Evaluation object:** Dynamic simulation cases

**Verification:** The reported open-loop review is not blinded. Closed-loop failures without a successful known-good scene control cannot be assigned solely to reconstruction.

**Related:** [2. Simulator Construction](#section-2)

### Cross-section reading

- [PneuGen: Task-Driven Agentic Co-Design of Soft Pneumatic Robots](#work-2611-13344)
- [PhysOPSD: Code as Privilege for Physically Plausible Video Generation](#work-2611-12411)
- [Spatial Harness: Grounding Spatial Reasoning in Executable World States with Physics Engines](#work-2611-11344)
- [Agentic discrete-event simulation for manufacturing system design: an open 3D simulator, a benchmark and an industrial case](#work-2611-10602)
- [TactileLab: Sim-to-Real Dexterous Robot Manipulation with Efficient Shear-Sensitive Tactile Simulation](#work-2611-07881)
- [PCBRouteAgent: How Close Are LLM Agents to Becoming PCB Routing Engineers?](#work-2611-08175)
- [Closing the Dynamics Gap through Self-Directed Robotic Interaction](#work-2611-02691)
- [WorldSketch: Sketching World Models for Zero-Shot Mobile Manipulation](#work-2611-00513)
- [Gym-Anything for Robotics: Scaling physical simulations with digital agents](#work-2610-40565)
- [DyCraft: An Agentic System for Long-Horizon 4D Scene Generation](#work-2610-40754)
- [LabWorld: Learning Interactive 4D Worlds for Scientific Experimentation](#work-2610-36592)
- [SceneAgent: An Agentic Pipeline from 3D and 4D Captures to Simulation Environments](#work-2610-34745)
- [WorldMirror: Agentic Real-to-Sim Generation of Interactive Worlds from In-the-Wild Robot Demonstrations](#work-2610-31834)
- [Plumb: Coding Agents with 3D Perception Rebuild Physical Scenes from Video](#work-system-plumb)
- [MARC: Mechanism-Aware Reflective Correction for Articulated Object Code Generation](#work-2610-33060)
- [Towards Physically Grounded Articulated 3D Assets: A Multi-Agent Pipeline and Benchmark](#work-2610-13947)
- [Agentic RSR: Real-to-Sim-to-Real through Scene Reconstruction and Execution-Grounded Robot Policies](#work-2610-10479)
- [WorldAuditBench: Interactive 3D World Auditing with Multimodal Agents](#work-2609-40325)
- [FACT: Fidelity-Aware Construction of Articulated Twins](#work-2609-37067)
- [CoDimRecon: Agentic Reconstruction of Sim-Ready 3D Scenes with Deformable Curves, Surfaces, and Volumes](#work-2609-36024)
- [WorldAgent: Verification-Guided Agentic Physical World Construction](#work-2609-33208)
- [What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery](#work-2609-31760)
- [DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation](#work-2609-23103)
- [DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation](#work-2609-18620)
- [SceneMosaic: Efficient and Diverse Simulation-Ready Scene Generation via Hybrid Agentic Layout Evolution](#work-2609-05594)
- [Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling](#work-2608-30821)
- [Code as Worlds: Agentic Discovery of Executable World Representations for Physical Reasoning](#work-2608-27549)
- [Beyond Placement and Articulation: Usage-Driven Code Scenes for Embodied Interaction](#work-2608-18840)
- [LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction](#work-2610-01863)
- [GS-Agent: Creating 4D Physical Worlds With Generative Simulation](#work-2607-21522)
- [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](#work-2607-19190)
- [UniPhysGen: Unified Physical Grounding for Simulation-Ready 3D Assets](#work-2607-13586)
- [EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI](#work-2607-07459)
- [SimWorlds: A Multi-Agent System for Dynamic 3D Scene Creation](#work-2607-01766)
- [SimFoundry: Modular and Automated Scene Generation for Policy Learning and Evaluation](#work-2606-28276)
- [MUSE: Agentic 3D Scene Authoring via Memory-Grounded Incremental Requirement Satisfaction](#work-2606-14168)
- [PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification](#work-2606-04226)
- [PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects](#work-2605-21572)
- [SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects](#work-2605-19587)
- [ChronoAgentic: A Code-based Multi-Agent World Simulator for Physically Grounded Simulation Construction](#work-2605-14398)
- [Articraft: An Agentic System for Scalable Articulated 3D Asset Generation](#work-2605-15187)
- [DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos](#work-2605-09586)
- [ArtiCAD: Articulated CAD Assembly Design via Multi-Agent Code Generation](#work-2604-10992)
- [SAGE: Scalable Agentic 3D Scene Generation for Embodied AI](#work-2602-10116)
- [SceneSmith: Agentic Generation of Simulation-Ready Indoor Scenes](#work-2602-09153)
- [SceneWeaver: All-in-One 3D Scene Synthesis with an Extensible and Self-Reflective Agent](#work-2509-20414)
- [GRS: Generating Robotic Simulation Tasks from Real-World Images](#work-2410-15536)
- [Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model](#work-2410-13882)
- [Real2Code: Reconstruct Articulated Objects via Code Generation](#work-2406-08474)

[Back to the research map](#research-map)

---

<a id="section-4"></a>

## 4. Data

Data connect physical experience to learning only when the observations, labels, execution checks and learning target remain distinguishable. Real observations can have synthetic labels; simulated trajectories can be rendered to resemble real video. Neither label makes the resulting episodes real robot executions.

| Data form | Observation and label source | Execution check and use |
|---|---|---|
| Real observations | [DROID](#work-2403-12945) pairs teleoperated robot observations/actions; [Open-HumanWAM](#work-2611-06817) aligns human video, language and hand motion across sources, including generated clips. | Robot rollouts or human recordings ground observations; downstream policy/WAM evaluation measures usefulness. Human hand motion is not measured robot action. |
| Synthetic environments and demonstrations | [RoboTwin 2.0](#work-2506-18088), [EmbodiedSmith](#work-2610-07969) and [CoDA](#work-2610-22362) build tasks and generate trajectories with executable controllers. | Simulator success predicates and rollout review filter episodes; policy training tests whether the data help outside the generated cases. |
| Programs and tool traces | [RAX](#work-2610-22496) releases real-session transcripts, tool calls, robot state, video and generated skills; [CaPtain](#work-2610-40799) uses teacher interaction trajectories for post-training. | A saved program is paired with its actual execution evidence. A public log archive and a curated training set have different roles. |
| Failures and repairs | [LabRobFail](#work-2607-23704) combines injected simulator failures, metadata-derived labels, LLM annotations, rules and human sampling. | Diagnostic accuracy, held-out failures and executed recovery answer different questions; supervision trains a failure-analysis VLM. |
| Paired and controlled data | [DataFarm](#work-2611-05320) pairs simulated actions with image-conditioned rendered videos; [PhysOPSD](#work-2611-12411) aligns programs, physical variants and visual drafts; [TactileLab](#work-2611-07881) aligns real and simulated tactile signals. | Preserve action/video alignment, control changed variables, and evaluate the resulting robot policy, video model or tactile translator separately. |

**Release and training role.** Datasets, generation methods and experimental traces are labeled separately. BlenderFORGE and PhysOPSD describe constructed training material whose release remains forthcoming. Open-HumanWAM provides a corpus with access conditions. Program traces can supervise a coding agent, while demonstration actions usually train a downstream action policy; the same simulator can support both without making them the same experiment.

**Research question.** Which mixture of successful episodes, failed attempts and verified repairs improves a coding agent on unseen physical tasks, once simulator, controller, supervision and evaluation budgets are held fixed?

### Real observations and interaction records

<a id="work-2611-06817"></a>
<!-- stage3-record: {"id": "2611.06817", "scope": "Adjacent", "section": 4} -->

#### Open-HumanWAM: An Open Recipe for Scaling Human and Robot Experience for Embodied Foundation Models

`2026-11-04` · Peking University; National University of Singapore; Massachusetts Institute of Technology; University of California, Santa Barbara; NVIDIA

[Bibliographic record](../README.md#paper-2611-06817) · [Paper](https://arxiv.org/abs/2611.06817) · [Project page](https://dagroup-pku.github.io/open-humanwam/) · [Code](https://github.com/DAGroup-PKU/HumanNet/tree/Open-HumanWAM)

Curates human manipulation experience and aligned actions for world–action model pretraining and robot adaptation.

**Method:** Open-HumanWAM-50K combines five sources, including generated egocentric data; filters hand visibility, motion and inactivity; aligns camera frames, wrist axes and gripper openness; and pairs video with language and hand motion. Human-only and mixed human–robot training update WAM parameters.

**Verification:** RoboTwin/RoboDojo scaling and alignment studies, 20-task physical zero-shot tests, and separate task-specific post-training. Goal-image review checks visible consistency, not physical feasibility. The released corpus requires acceptance of access conditions.

**Related:** [1. Embodied Harnesses](#section-1) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2406-18915"></a>
<!-- stage3-record: {"id": "2406.18915", "scope": "Adjacent", "section": 4} -->

#### Manipulate-Anything: Automating Real-World Robots using Vision-Language Models

`2024-06-27` · University of Washington; Universidad Católica San Pablo; Allen Institute for Artificial Intelligence; NVIDIA

[Paper](https://arxiv.org/abs/2406.18915) · [Project page](https://robot-ma.github.io/)

Collects real demonstrations with visual-language feedback.

**Method:** The system uses model-generated primitive code and visual execution feedback to collect robot demonstrations for behavior cloning.

**Verification:** Real trajectories train a downstream policy; initial human-provided code examples are part of the setup.

<a id="work-2403-12945"></a>
<!-- stage3-record: {"id": "2403.12945", "scope": "Resource", "section": 4} -->

#### DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset

`2024-03-19` · Stanford University; University of California, Berkeley; Toyota Research Institute; Carnegie Mellon University; University of Texas at Austin; University of Montreal; University of Edinburgh; Princeton University; University of Washington; KAIST; University of California, San Diego; Google DeepMind; University of California, Davis; University of Pennsylvania; Columbia University; Yonsei University

[Paper](https://arxiv.org/abs/2403.12945) · [Project page](https://droid-dataset.github.io/)

Supplies real observations for robot-learning pipelines.

**Method:** DROID releases diverse real teleoperation trajectories; RoboPro reuses videos as observations for synthesizing policy-code labels.

**Verification:** Released teleoperation data do not inherently contain agent reasoning, tool calls or code-repair traces.

### Synthetic data and production methods

<a id="work-2611-12411"></a>
<!-- stage3-record: {"id": "2611.12411", "scope": "Core", "section": 4} -->

#### PhysOPSD: Code as Privilege for Physically Plausible Video Generation

`2026-11-09` · Hong Kong University of Science and Technology; Alibaba Token Hub; Alibaba Group

[Bibliographic record](../README.md#paper-2611-12411) · [Paper](https://arxiv.org/abs/2611.12411) · [Project page](https://haroldchen19.github.io/PhysOPSD-site/)

Constructs executable physical scenes and paired visual supervision for video-generator post-training.

**Method:** A coding agent repairs reference-guided MuJoCo/Genesis/Blender programs using execution logs, kinematic diagnostics and preview keyframes. Frozen trajectories produce abstraction-level drafts and controlled parameter variants; shared-noise distillation updates video-model weights, not the coding agent.

**Verification:** VideoPhy-2, PhyGround and VBench with privilege/variation ablations. PhysOPSD-3K counts roughly 3,000 base-scene/variant items; release is forthcoming. The demonstrated repair loop is in data construction; deployed video generation is simulation-free.

**Related:** [2. Simulator Construction](#section-2) · [3. Simulator Quality Evaluation](#section-3) · [5. Training and Capability Improvement](#section-5)

<a id="work-2611-05320"></a>
<!-- stage3-record: {"id": "2611.05320", "scope": "Adjacent", "section": 4} -->

#### PyRUA-DataFarm: LLM Agent as a Cost-Efficient Teleoperator for Real-Ready Robot Data

`2026-11-03` · Peking University; NVIDIA

[Bibliographic record](../README.md#paper-2611-05320) · [Paper](https://arxiv.org/abs/2611.05320) · [Project page](https://dagroup-pku.github.io/PyRUA-Lean/DataFarm) · [Code](https://github.com/DAGroup-PKU/PyRUA-Lean/tree/DataFarm)

Creates action-labelled data with code and video models.

**Method:** An agent writes simulation tasks and expert controllers; real-image-conditioned video generation supplies visual episodes for downstream policy learning.

**Verification:** Five PiPER tasks compare matched datasets and appearance transfer; the released pipeline excludes datasets.

<a id="work-2610-22362"></a>
<!-- stage3-record: {"id": "2610.22362", "scope": "Core", "section": 4} -->

#### CoDA: Co-Evolution of Data Engines and Action Policies

`2026-10-15` · University of Illinois Urbana-Champaign; Chinese University of Hong Kong, Shenzhen; Amazon

[Bibliographic record](../README.md#paper-2610-22362) · [Paper](https://arxiv.org/abs/2610.22362) · [Project page](https://plan-lab.github.io/projects/coda/)

Co-evolves data-generation programs and robot policies.

**Method:** Video-based failure diagnosis produces reusable scene generators and training-potential programs; measured learning progress guides both code and policy updates.

**Verification:** Generator edits change scenes and success rules, while downstream policy learning uses its own training signal.

**Related:** [2. Simulator Construction](#section-2) · [5. Training and Capability Improvement](#section-5)

<a id="work-2610-07969"></a>
<!-- stage3-record: {"id": "2610.07969", "scope": "Core", "section": 4} -->

#### EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation

`2026-10-06` · HKUST (Guangzhou); Xiaomi Robotics; Southeastern University; Tsinghua University; Zhejiang University; Westlake University; Symbiosis Robotics; Peking University; Xi’an Jiaotong University; Beijing Academy of Artificial Intelligence

[Paper](https://arxiv.org/abs/2610.07969)

Builds a self-improving simulation data engine.

**Method:** Assets, scenes, tasks and solver programs form an iterative engine that produces execution-validated robot-learning trajectories.

**Verification:** Data-engine improvement and downstream policy improvement are different outcomes.

<a id="work-2609-35318"></a>
<!-- stage3-record: {"id": "2609.35318", "scope": "Core", "section": 4} -->

#### DexAgent: An Agentic Human2Sim2Robot Framework for Dexterous Manipulation with Self-Evolving Tool Library

`2026-09-28` · Stanford University; Columbia University

[Paper](https://arxiv.org/abs/2609.35318) · [Project page](https://dexagent1.github.io/) · [Project page](https://dexagent123.github.io/)

Converts human videos into simulated dexterous supervision.

**Method:** An agent reconstructs tasks from human video, improves its tool library and uses physics checks to produce robot trajectories.

**Verification:** Real input videos and simulated output demonstrations have different provenance.

**Related:** [2. Simulator Construction](#section-2) · [5. Training and Capability Improvement](#section-5)

<a id="work-2609-27308"></a>
<!-- stage3-record: {"id": "2609.27308", "scope": "Core", "section": 4} -->

#### EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics

`2026-09-23` · ByteDance Seed; Yale University; Princeton University; Carnegie Mellon University; Stanford University; University of California, Los Angeles; University of Washington

[Paper](https://arxiv.org/abs/2609.27308)

Scales verified robot programs into synthetic demonstrations.

**Method:** Coding agents solve long-horizon dexterous tasks, then diversify executable solutions to generate training trajectories.

**Verification:** The main pipeline runs in simulation; a separate physical long-horizon task tests a policy trained on synthetic data.

**Related:** [1. Embodied Harnesses](#section-1) · [2. Simulator Construction](#section-2) · [5. Training and Capability Improvement](#section-5)

<a id="work-2607-23704"></a>
<!-- stage3-record: {"id": "2607.23704", "scope": "Adjacent", "section": 4} -->

#### LabRobFail: A Benchmark for Robotic Failure Analysis in Chemical Self-driving Laboratory

`2026-07-26` · Dalian University of Technology; Shenzhen Loop Area Institute; Harbin Institute of Technology; Shanghai AI Laboratory; HKUST; Chinese University of Hong Kong

[Paper](https://arxiv.org/abs/2607.23704) · [Code](https://github.com/Su-ISE-2001/LabRobFail)

Builds simulated laboratory failure trajectories with structured diagnoses and correction labels.

**Method:** Perturbs controller keyframes, physical parameters and task semantics in LabUtopia; executes trajectories; derives VQA labels from simulator metadata through an LLM, rule filters and human sampling. Hybrid fine-tuning trains a failure-analysis VLM; a fixed action dictionary realizes its corrections.

**Verification:** Reports over 20,000 trajectories, six diagnostic tasks with unseen-object/scene splits, and downstream OpenVLA/ACT recovery. Text correction scores and simulated recovery do not establish real laboratory safety or coding-agent post-training.

**Related:** [1. Embodied Harnesses](#section-1) · [5. Training and Capability Improvement](#section-5) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2506-18088"></a>
<!-- stage3-record: {"id": "2506.18088", "scope": "Adjacent", "section": 4} -->

#### RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation

`2025-06-22` · Lumina EAI; Shanghai AI Lab; Shenzhen University; Nanjing University; TeleAI; Fudan University; Sun Yat-sen University; USTC; Central South University; SUSTech; Tsinghua University; D-Robotics; Shanghai Jiao Tong University; HKU; Northeastern University

[Paper](https://arxiv.org/abs/2506.18088) · [Project page](https://robotwin-platform.github.io/) · [Code](https://github.com/robotwin-Platform/robotwin/) · [Code](https://github.com/robotwin-Platform/robotwin) · [Project page](https://robotwin-platform.github.io/doc/) · [Code](https://github.com/RoboTwin-Platform/RoboTwin)

Generates diverse bimanual training trajectories.

**Method:** Multimodal models write and refine task-execution code in simulation; domain randomization expands verified solutions into demonstrations.

**Verification:** Simulation refinement, dataset generation and real-policy tests provide different evidence; refinement is not real-world calibration.

**Related:** [1. Embodied Harnesses](#section-1) · [2. Simulator Construction](#section-2)

<a id="work-2410-03645"></a>
<!-- stage3-record: {"id": "2410.03645", "scope": "Adjacent", "section": 4} -->

#### GenSim2: Scaling Robot Data Generation with Multi-modal and Reasoning LLMs

`2024-10-04` · Tsinghua University; University of California, San Diego; Shanghai Jiao Tong University; MIT CSAIL

[Paper](https://arxiv.org/abs/2410.03645) · [Project page](https://gensim2.github.io/)

Scales robot demonstrations through generated tasks and solvers.

**Method:** Multimodal reasoning models generate articulated-object tasks; planning and RL solvers produce demonstrations for a downstream robot policy.

**Verification:** Generated tasks, solvers and demonstrations support policy learning, not post-training of the task-writing LLM.

**Related:** [2. Simulator Construction](#section-2) · [5. Training and Capability Improvement](#section-5)

<a id="work-2307-14535"></a>
<!-- stage3-record: {"id": "2307.14535", "scope": "Adjacent", "section": 4} -->

#### Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition

`2023-07-26` · Columbia University; Google DeepMind

[Paper](https://arxiv.org/abs/2307.14535) · [Project page](https://www.cs.columbia.edu/~huy/scalingup/)

Distills generated robot experience into a visuomotor policy.

**Method:** An LLM composes skills and success-checking code to collect language-labelled simulation trajectories for downstream policy learning.

**Verification:** Generated demonstrations train a visuomotor policy; the coding LLM is not the learned policy.

### Cross-section reading

- [PhyRubric: Rubric-Grounded Diagnostic Evaluation of Physical Commonsense in Text-to-Video Generation](#work-2611-13576)
- [One Policy for 100 Household Tasks: Our Solution for the 2026 BEHAVIOR Challenge](#work-2611-14432)
- [World In-Context Learning for Agentic Robot Manipulation](#work-2611-12885)
- [BlenderFORGE: Framework for Optimizing Reactive 3D-Graphics Editing Ability of MLLMs](#work-2611-10768)
- [TactileLab: Sim-to-Real Dexterous Robot Manipulation with Efficient Shear-Sensitive Tactile Simulation](#work-2611-07881)
- [Gym-Anything for Robotics: Scaling physical simulations with digital agents](#work-2610-40565)
- [DyCraft: An Agentic System for Long-Horizon 4D Scene Generation](#work-2610-40754)
- [CaPtain: A Pipeline for Post-Training Code-as-Policy Robot Agents](#work-2610-40799)
- [SceneAgent: An Agentic Pipeline from 3D and 4D Captures to Simulation Environments](#work-2610-34745)
- [SceneBloom: Agentic Indoor Environment Generation with Realistic and Diverse Layouts for Embodied Learning](#work-2610-32978)
- [WorldMirror: Agentic Real-to-Sim Generation of Interactive Worlds from In-the-Wild Robot Demonstrations](#work-2610-31834)
- [Agentic World Action Models](#work-2610-30136)
- [Scaling Online Exploration for Robot Agents](#work-2610-22496)
- [RoboSimStudio: An Interactive Toolkit for Human and Agent Rapid Real2Sim of Robot Manipulation Tasks](#work-2610-18835)
- [YUBI-Real2Sim: 3DGS Scene Verification for Reliable Policy Evaluation](#work-2610-17521)
- [D-World: An Explicit World-Language-Action Model with Recursive Self-Improvement under Dual Control](#work-2610-17114)
- [USDCraft: Geometrically Grounded Programmatic Modeling of Articulated 3D Assets for Simulation](#work-2610-11322)
- [Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos](#work-2610-04432)
- [Awomo-SimDataEngine: Agentic Simulation-Ready World Generation](#work-2610-02274)
- [Text2Sim: Agentic Physics-Based Simulation Generation with Distilled Expertise](#work-2609-36593)
- [Real2Gym: Building Gyms from Videos, Bringing Skills to Robots](#work-2609-37089)
- [Parametric CAD Bench v3: Evaluating Agentic Parametric CAD Authoring from Text and Engineering Drawings](#work-2611-02659)
- [DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation](#work-2609-18620)
- [GIF: Agentic Generation of Interactive and Functional Object Compositions for Robot Learning](#work-2609-05927)
- [Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling](#work-2608-30821)
- [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](#work-2607-19190)
- [UniPhysGen: Unified Physical Grounding for Simulation-Ready 3D Assets](#work-2607-13586)
- [EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI](#work-2607-07459)
- [SimFoundry: Modular and Automated Scene Generation for Policy Learning and Evaluation](#work-2606-28276)
- [MPMWorlds: Material-Point-Method Simulations for Inferring and Extrapolating Physical Dynamics](#work-2606-01538)
- [PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects](#work-2605-21572)
- [Articraft: An Agentic System for Scalable Articulated 3D Asset Generation](#work-2605-15187)
- [SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning](#work-2605-09423)
- [IRIS: A Real-World Benchmark for Inverse Recovery and Identification of Physical Dynamic Systems from Monocular Video](#work-2603-16432)
- [SAGE: Scalable Agentic 3D Scene Generation for Embodied AI](#work-2602-10116)
- [Apples on the Table? Evaluating Text-Guided 3D Scene Synthesis via Fine-Grained Constraint Verification](#work-2511-03001)
- [Robotic Programmer: Video Instructed Policy Code Generation for Robotic Manipulation](#work-2501-04268)
- [Eurekaverse: Environment Curriculum Generation via Large Language Models](#work-2411-01775)
- [GRS: Generating Robotic Simulation Tasks from Real-World Images](#work-2410-15536)
- [FactorSim: Generative Simulation via Factorized Representation](#work-2409-17652)
- [RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins](#work-2409-02920)
- [Real2Code: Reconstruct Articulated Objects via Code Generation](#work-2406-08474)
- [OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code](#work-2405-15568)
- [Holodeck: Language Guided Generation of 3D Embodied AI Environments](#work-2312-09067)
- [RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation](#work-2311-01455)
- [Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models](#work-2310-18308)
- [GenSim: Generating Robotic Simulation Tasks via Large Language Models](#work-2310-01361)
- [mujoco-workbench](#work-mujoco-workbench)

[Back to the research map](#research-map)

---

<a id="section-5"></a>

## 5. Training and Capability Improvement

The organizing question is **what actually changes after experience?** More successful robot behavior can result from improved code, a trained action policy, a better skill library, additional context, or updated agent weights. The three lines below retain those distinctions.

| Line | Updated object | Representative evidence |
|---|---|---|
| Program and downstream-policy development | Reward/controller/source code, training procedure, or the downstream robot policy. | [Eureka](#work-2310-12931) searches reward programs used to train policies; [ENPIRE](#work-2606-19980) develops policies and their learning machinery through physical execution. Agent-written training code does not imply training the agent itself. |
| Experience, memory and skills | Executable skills, retrieval/routing, notes or inference context. | [ASPIRE](#work-2607-00272) accumulates verified skills; [WICL](#work-2611-12885) freezes task memory after rehearsal; [PyRUA-REAL](#work-2611-06768) retains physical-execution experience in programs and skills. |
| Coding-agent model post-training | Parameters of the model that selects tools or generates executable programs. | [CaPtain](#work-2610-40799) combines teacher SFT with physical-critic RL; [BlenderFORGE](#work-2611-10768) trains scene-editing MLLMs through sandbox interaction. Test-time code repair and the parameter update are distinct steps. |

For mixed systems, read the update mechanism within each component. [TinyAstral](#work-2610-41216) first evolves a teacher harness and then trains a smaller agent. [Agentic World Action Models](#work-2610-30136) jointly learn program, video and action outputs. [One Policy for 100 Household Tasks](#work-2611-14432) combines VLA training with an agent route that reuses frozen practice context. [PhysOPSD](#work-2611-12411) trains a video generator, while [Open-HumanWAM](#work-2611-06817) trains world–action models; these provide useful connections to physical data, without becoming coding-agent post-training by association.

Validation should separate development feedback from final held-out execution, and reset or freeze context according to the stated protocol. The [123-round skill-discovery case study](#work-2609-31760) illustrates why passing local tests and accumulating skills need not improve the full task.

**Research question.** Can verified simulator experience improve an agent's parameters while preserving useful executable skills and memory, with gains that transfer to independently evaluated real tasks? Existing component-level results do not yet establish that complete loop.

### Program and policy development

<a id="work-2610-36533"></a>
<!-- stage3-record: {"id": "2610.36533", "scope": "Core", "section": 5} -->

#### RoboAuto: Autonomous Robot Program Search through Multi-Level Physical Understanding

`2026-10-27` · Washington University in St. Louis

[Bibliographic record](../README.md#paper-2610-36533) · [Paper](https://arxiv.org/abs/2610.36533) · [Project page](https://roboauto-ai.github.io/)

Searches programs using staged physical diagnostics.

**Method:** Object knowledge, visual localization and agent-designed diagnostic experiments guide revisions to staged robot programs.

**Verification:** Simulation-to-hardware comparisons retain human judgments and resets in physical trials.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-23288"></a>
<!-- stage3-record: {"id": "2610.23288", "scope": "Core", "section": 5} -->

#### CoEvolve: Self-Evolving Code Policies from Skills to Strategies for Humanoid Robots

`2026-10-16` · Peking University; Renmin University of China; Beijing XYZ Embodied AI Co., Ltd.; Beijing Academy of Artificial Intelligence (BAAI)

[Paper](https://arxiv.org/abs/2610.23288)

Evolves team strategies over fixed humanoid skills.

**Method:** A coding agent searches executable strategies that compose existing motion skills and coordinate multiple robots.

**Verification:** Strategy-code improvement should not be credited as learning the underlying motion skills.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-18792"></a>
<!-- stage3-record: {"id": "2610.18792", "scope": "Core", "section": 5} -->

#### SEAR: Self-Evolving Agentic Robotics

`2026-10-13` · Luma AI

[Paper](https://arxiv.org/abs/2610.18792)

Compares several modes of agentic robot improvement.

**Method:** The framework contrasts program-as-policy, online agent control and automated policy research, tracking what transfers beyond a task.

**Verification:** Seven models on 330 simulated tasks and five physical tasks compare retained libraries, fresh restarts, held-out states and transfer. After up to 12 hours of physical practice per task, frozen-code policies are tested on ten operator-staged scenes; live-agent policies use five. Practice streaks can overestimate held-out performance; physical scores include partial credit and tower height.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-12369"></a>
<!-- stage3-record: {"id": "2610.12369", "scope": "Core", "section": 5} -->

#### Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement

`2026-10-08` · Nanyang Technological University; Ropedia

[Bibliographic record](../README.md#paper-2610-12369) · [Paper](https://arxiv.org/abs/2610.12369)

Develops stateful code for model-free deployment.

**Method:** An offline coding agent reviews failure videos and state traces, revises perception and control code, then validates a shared pure-code policy.

**Verification:** Held-out tasks, state estimation, regressions and deployment cost assess the exported policy; online model inference is not required.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-09588"></a>
<!-- stage3-record: {"id": "2610.09588", "scope": "Core", "section": 5} -->

#### Adaptive Code Generation for Controlling Robots

`2026-10-07` · Technische Universität Berlin, Germany; logsight.ai, Berlin, Germany

[Bibliographic record](../README.md#paper-2610-09588) · [Paper](https://arxiv.org/abs/2610.09588)

Hot-reloads robot workflows after world-state changes.

**Method:** RGB and LiDAR state changes trigger Python replanning; virtual-machine snapshots preserve variables and execution progress across revisions.

**Verification:** Gazebo exploration, syntax validity, adaptation frequency and decision latency assess the system.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-38982"></a>
<!-- stage3-record: {"id": "2609.38982", "scope": "Core", "section": 5} -->

#### SimEX: Simulation-Integrated Robotics AutoResearch

`2026-09-30` · Amazon FAR (Frontier AI & Robotics); The University of Texas at Austin; Carnegie Mellon University

[Paper](https://arxiv.org/abs/2609.38982) · [Project page](https://robo-simex.github.io/)

Combines simulation research with limited physical feedback.

**Method:** A coding agent uses simulated experiments and selected robot observations to develop, debug and search manipulation strategies.

**Verification:** Tests sim-to-sim transfer and physical plate stowing, towel folding and barcode scanning. Five adaptation trials per physical task take about ten minutes of robot interaction, with human resets; subsequent evaluation succeeds in 26 of 30 trials versus at most 3 for any baseline. Simulated discovery and sandbox-guided repair have separate ablations.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-30594"></a>
<!-- stage3-record: {"id": "2609.30594", "scope": "Core", "section": 5} -->

#### HuGo: LLMs as Whole-Body Policy Code Designers for Humanoid Loco-Manipulation

`2026-09-24` · University of California, Berkeley; ShanghaiTech University; Google DeepMind; Nomagic

[Bibliographic record](../README.md#paper-2609-30594) · [Paper](https://arxiv.org/abs/2609.30594) · [Project page](https://iconlab.negarmehr.com/HuGo/)

Designs high-level humanoid policy code.

**Method:** A coding agent programs behavior over a frozen whole-body controller, revising code from execution videos and numerical trajectories.

**Verification:** Held-out simulation, physical transfer and real-feedback revisions are separate evidence, constrained by controller capability.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-30233"></a>
<!-- stage3-record: {"id": "2609.30233", "scope": "Adjacent", "section": 5} -->

#### Coding Agents for Generalized Task and Motion Planning Problems

`2026-09-24` · Fondazione Bruno Kessler; Carnegie Mellon University; Princeton University

[Paper](https://arxiv.org/abs/2609.30233)

Programs solvers for task-and-motion planning.

**Method:** Coding agents implement solvers for planning problems, using executable environments to test generalization across problem instances.

**Verification:** KinDER and PDDLStream experiments concern solver behavior and generalization, not a general learned robot policy.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-24145"></a>
<!-- stage3-record: {"id": "2609.24145", "scope": "Adjacent", "section": 5} -->

#### MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation

`2026-09-21` · Carnegie Mellon University

[Paper](https://arxiv.org/abs/2609.24145) · [Project page](https://luckykantnayak.github.io/mimic-agent/)

Generates reference motion for quadruped policy training.

**Method:** A coding agent turns skill descriptions into reference trajectories, then a learned tracker realizes the behavior.

**Verification:** Kinematically generated reference motion is not guaranteed dynamically feasible; RL learns executable tracking.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2608-07555"></a>
<!-- stage3-record: {"id": "2608.07555", "scope": "Adjacent", "section": 5} -->

#### You Don't Need To Stay in The Loop: An Agentic Robotics Loop for Robot-Policy Improvement

`2026-08-02` · Independent Researcher, United States

[Paper](https://arxiv.org/abs/2608.07555)

Organizes a repeatable loop for policy development.

**Method:** A principal agent coordinates analysis tools and robot trials, retaining inspectable program changes to improve downstream policies.

**Verification:** A described development protocol does not by itself establish fully unattended orchestration.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2606-19980"></a>
<!-- stage3-record: {"id": "2606.19980", "scope": "Core", "section": 5} -->

#### ENPIRE: Agentic Robot Policy Self-Improvement in the Real World

`2026-06-18` · NVIDIA; Carnegie Mellon University; University of California, Berkeley

[Bibliographic record](../README.md#paper-2606-19980) · [Paper](https://arxiv.org/abs/2606.19980) · [Project page](https://research.nvidia.com/labs/gear/enpire/)

Develops robot policies from physical trial evidence.

**Method:** Coding agents analyze video, force, proprioception and rollout results to revise controllers, learning algorithms and training code.

**Verification:** Physical trials support policy-development claims; the coding LLM itself need not receive gradient updates.

**Related:** [1. Embodied Harnesses](#section-1) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2606-16458"></a>
<!-- stage3-record: {"id": "2606.16458", "scope": "Core", "section": 5} -->

#### RHO: Your Coding Agent is Secretly a Roboticist

`2026-06-15` · University of California, Berkeley; Embodied Science; AMD

[Paper](https://arxiv.org/abs/2606.16458) · [Project page](https://rho-robotics.github.io)

Searches reusable policy repositories before deployment.

**Method:** The coding agent develops interpretable, multi-file policy repositories; synthesized programs later organize perception, planning and control directly.

**Verification:** Development search and deployed program execution have different compute and feedback requirements.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2606-08610"></a>
<!-- stage3-record: {"id": "2606.08610", "scope": "Core", "section": 5} -->

#### HARBOR: A Harness Framework for Agentic Robot Reinforcement Learning

`2026-06-07` · TU Darmstadt; Honda Research Institute Europe; Columbia University; Tongji University; Shanghai Research Institute for Intelligent Autonomous Systems; University of Würzburg; Hessian.AI

[Paper](https://arxiv.org/abs/2606.08610)

Makes robot RL development an agent workspace.

**Method:** A coding agent configures environments, rewards, training and evaluation from simulator code and task specifications.

**Verification:** Development-stage artifacts and trained-policy results are checked; the policy learner and coding agent are separate roles.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2603-04466"></a>
<!-- stage3-record: {"id": "2603.04466", "scope": "Core", "section": 5} -->

#### Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation

`2026-03-03` · General Bionix

[Bibliographic record](../README.md#paper-2603-04466) · [Paper](https://arxiv.org/abs/2603.04466)

Learns control programs from execution and visual feedback.

**Method:** A coding agent runs a generated controller, inspects the robot visually and rewrites policy code in context.

**Verification:** Controller compilation, repeated-trial success and failure recovery test program improvement.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2508-02629"></a>
<!-- stage3-record: {"id": "2508.02629", "scope": "Core", "section": 5} -->

#### HyCodePolicy: Hybrid Language Controllers for Multimodal Monitoring and Decision in Embodied Agents

`2025-08-04` · Northeastern University; D-Robotics; HKU MMLab; Shanghai AI Lab; Shenzhen University; SUSTech; Shanghai Jiao Tong University; Tsinghua University

[Bibliographic record](../README.md#paper-2508-02629) · [Paper](https://arxiv.org/abs/2508.02629)

Combines executable policies with multimodal monitoring.

**Method:** A hybrid controller links policy code to visual monitoring so failures can be localized and behavior can be revised during task execution.

**Verification:** Task and subgoal success, completion judgments and repair efficiency assess the combined system.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2503-13660"></a>
<!-- stage3-record: {"id": "2503.13660", "scope": "Adjacent", "section": 5} -->

#### INPROVF: Leveraging Large Language Models to Repair High-level Robot Controllers from Assumption Violations

`2025-03-17` · Cornell University

[Paper](https://arxiv.org/abs/2503.13660)

Uses formal counterexamples to repair robot controllers.

**Method:** An LLM proposes repairs after controller assumptions fail; a verifier checks the candidates and supplies counterexamples for further revision.

**Verification:** Formal validity and physical task performance are different outcomes and require their respective checks.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2410-18893"></a>
<!-- stage3-record: {"id": "2410.18893", "scope": "Adjacent", "section": 5} -->

#### Creating and Repairing Robot Programs in Open-World Domains

`2024-10-24` · Northeastern University; University of Texas at Austin

[Paper](https://arxiv.org/abs/2410.18893)

Repairs programs while preserving completed work.

**Method:** Execution states before a failure guide generation of recovery programs that avoid unnecessarily repeating successful actions.

**Verification:** Recovery quality includes task completion and repeated-action cost; it is program repair rather than weight learning.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2409-01652"></a>
<!-- stage3-record: {"id": "2409.01652", "scope": "Adjacent", "section": 5} -->

#### ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation

`2024-09-03` · Stanford University; Columbia University

[Paper](https://arxiv.org/abs/2409.01652) · [Project page](https://rekep-robot.github.io/)

Programs geometric constraints for online manipulation.

**Method:** RGB-D observations and instructions yield Python functions describing relations between keypoints; hierarchical optimization solves motion under those constraints.

**Verification:** Execution tests constraint-based control; rerunning an optimizer is distinct from rewriting constraints or training the LLM.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2406-01967"></a>
<!-- stage3-record: {"id": "2406.01967", "scope": "Adjacent", "section": 5} -->

#### DrEureka: Language Model Guided Sim-To-Real Transfer

`2024-06-04` · University of Pennsylvania; NVIDIA; University of Texas, Austin

[Paper](https://arxiv.org/abs/2406.01967) · [Project page](https://eureka-research.github.io/dr-eureka/)

Uses generated rewards and randomization for sim-to-real.

**Method:** The LLM designs reward functions and domain-randomization settings, using robot-training results to improve the transfer recipe.

**Verification:** Simulation and hardware comparisons measure policy transfer, not post-training of the coding model.

**Related:** [1. Embodied Harnesses](#section-1) · [2. Simulator Construction](#section-2)

<a id="work-2402-04764"></a>
<!-- stage3-record: {"id": "2402.04764", "scope": "Adjacent", "section": 5} -->

#### Code as Reward: Empowering Reinforcement Learning with VLMs

`2024-02-07` · Mila; McGill University; Google DeepMind; University of California, Berkeley

[Paper](https://arxiv.org/abs/2402.04764)

Compiles visual task understanding into reusable reward code.

**Method:** A VLM interprets the task and visual state, producing reward programs that can be repeatedly evaluated during robot-policy training.

**Verification:** The reward program reduces repeated model queries; policy learning remains a separate optimization process.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2310-12931"></a>
<!-- stage3-record: {"id": "2310.12931", "scope": "Adjacent", "section": 5} -->

#### Eureka: Human-Level Reward Design via Coding Large Language Models

`2023-10-19` · University of Pennsylvania; Caltech; NVIDIA; University of Texas at Austin

[Paper](https://arxiv.org/abs/2310.12931) · [Project page](https://eureka-research.github.io/)

Searches reward programs using policy-training feedback.

**Method:** A coding LLM proposes reward code, launches policy learning and uses training statistics to revise subsequent reward candidates.

**Verification:** Reward search and robot-policy optimization are separate from LLM weight updates.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2309-11489"></a>
<!-- stage3-record: {"id": "2309.11489", "scope": "Adjacent", "section": 5} -->

#### Text2Reward: Reward Shaping with Language Models for Reinforcement Learning

`2023-09-20` · The University of Hong Kong; Carnegie Mellon University; Nanjing University; Microsoft Research; University of Waterloo

[Paper](https://arxiv.org/abs/2309.11489) · [Project page](https://text-to-reward.github.io/)

Makes reward shaping a code-generation problem.

**Method:** The LLM writes dense reward functions from environment descriptions, then revises them using training outcomes and human feedback.

**Verification:** Some feedback is supplied by people watching rollouts; the updated model is the downstream RL policy.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2306-08647"></a>
<!-- stage3-record: {"id": "2306.08647", "scope": "Adjacent", "section": 5} -->

#### Language to Rewards for Robotic Skill Synthesis

`2023-06-14` · Google DeepMind

[Paper](https://arxiv.org/abs/2306.08647) · [Project page](https://language-to-reward.github.io/)

Expresses desired robot skills through generated rewards.

**Method:** The LLM converts instructions into reward parameters for a real-time optimizer; user corrections adjust the resulting behavior.

**Verification:** Behavior optimization and user-guided corrections concern the controller objective, not LLM post-training.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-autoresearch-robotics"></a>
<!-- stage3-record: {"id": "autoresearch-robotics", "scope": "Resource", "section": 5} -->

#### autoresearch-robotics

`First-public date not established` · Not reported

[Code](https://github.com/jellyheadandrew/autoresearch-robotics)

Provides a community robot-RL development example.

**Method:** A coding agent edits training scripts and uses fixed evaluation, learning curves and video feedback to guide further experiments.

**Verification:** This is a community simulation workflow, not a peer-reviewed hardware result.

**Related:** [1. Embodied Harnesses](#section-1)

### Experience, memory and skill learning

<a id="work-2611-14432"></a>
<!-- stage3-record: {"id": "2611.14432", "scope": "Core", "section": 5} -->

#### One Policy for 100 Household Tasks: Our Solution for the 2026 BEHAVIOR Challenge

`2026-11-10` · Independent team

[Paper](https://arxiv.org/abs/2611.14432)

Combines a learned household VLA with task-specific coding-agent practice sessions that are frozen before evaluation.

**Method:** The agent writes short programs over image/depth observation and motion tools, practices on training instances, and retains notes and recipes in context. Fourteen tasks use this agent for the whole episode; other tasks use the VLA. Agent context learning and VLA parameter training are separate mechanisms.

**Verification:** BEHAVIOR/OmniGibson evaluation restarts each agent episode from a frozen practice session, removes privileged training tools, and allows no between-episode updates. Practice image feedback informs subsequent programs; results are simulated and do not demonstrate physical deployment.

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2611-12885"></a>
<!-- stage3-record: {"id": "2611.12885", "scope": "Adjacent", "section": 5} -->

#### World In-Context Learning for Agentic Robot Manipulation

`2026-11-09` · Huazhong University of Science and Technology; ArcheOne AI

[Bibliographic record](../README.md#paper-2611-12885) · [Paper](https://arxiv.org/abs/2611.12885) · [Project page](https://archeone-ai.github.io/RoboScript/) · [Code](https://github.com/ArcheOne-AI/RoboScript)

Uses simulator rehearsal to build transferable task memory while the foundation model stays frozen.

**Method:** RoboScript starts from one demonstration, explores task variants, and consolidates feedback into semantic Task Memory. Deployment freezes that memory; the learned artifact is context and program knowledge, not model weights.

**Verification:** Evaluates 50 RoboTwin 2.0 tasks with separate rehearsal and deployment, plus four physical PiPER tasks. Real execution uses preplanned action sequences without online replanning; simulator adaptation does not by itself establish real-world corrective coding.

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2611-06768"></a>
<!-- stage3-record: {"id": "2611.06768", "scope": "Core", "section": 5} -->

#### PyRUA-REAL: Robot Exploration and Adaptive Learning through RSI in the Real World

`2026-11-04` · Peking University; EngineAI; National University of Singapore

[Bibliographic record](../README.md#paper-2611-06768) · [Paper](https://arxiv.org/abs/2611.06768) · [Project page](https://dagroup-pku.github.io/PyRUA-Lean/real/) · [Code](https://github.com/DAGroup-PKU/PyRUA-Lean/tree/REAL)

Learns reusable robot code from physical exploration.

**Method:** Researcher and engineer agents turn physical execution evidence into revised programs and skills, then run the resulting perception-control code on live observations.

**Verification:** Eight physical tasks and 42 RoboDojo tasks include feedback and transfer ablations; assisted insertion is separated from frozen reliability.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-42141"></a>
<!-- stage3-record: {"id": "2610.42141", "scope": "Core", "section": 5} -->

#### RoboArchitect: Automating the Design of Robotic Agents with Persistent Memory

`2026-10-30` · Stanford University

[Bibliographic record](../README.md#paper-2610-42141) · [Paper](https://arxiv.org/abs/2610.42141) · [Code](https://github.com/roboarchitect-ai/RoboArchitect) · [Project page](https://roboarchitect-ai.github.io/)

Evolves persistent memory and robot-control code.

**Method:** Execution videos and tool outputs guide iterative revisions to control programs and memory around a frozen robot policy.

**Verification:** Held-out scenes and tasks plus ablations assess transfer; reported verification is in simulation.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-29560"></a>
<!-- stage3-record: {"id": "2610.29560", "scope": "Core", "section": 5} -->

#### From VLM Planners to Robotic Agents: Self-Evolving Harnesses for History-Dependent Manipulation

`2026-10-21` · University of Science and Technology of China; Shanghai Artificial Intelligence Laboratory; Shanghai Jiao Tong University; Mohamed bin Zayed University of Artificial Intelligence; Zhejiang University

[Paper](https://arxiv.org/abs/2610.29560)

Adapts harness context for history-dependent tasks.

**Method:** Development trajectories guide revisions to context organization, command checks and feedback processing around a fixed high-level planner.

**Verification:** Held-out tasks evaluate the fixed resulting harness; changes are external to the action policy.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-25114"></a>
<!-- stage3-record: {"id": "2610.25114", "scope": "Core", "section": 5} -->

#### Compile Once, Run Cheap: Frozen, Portable Skills for Embodied Agents, and What Recursive Self-Improvement Adds

`2026-10-18` · Beijing Ou Rui Ling Shi Technology; ChangingTek Robotics Technology (Suzhou); Shanghai Yunfan Intelligent Control Robot Technology

[Paper](https://arxiv.org/abs/2610.25114) · [Code](https://github.com/Orillusion/embodied-skill-rsi)

Builds skills offline for inexpensive frozen reuse.

**Method:** A strong model writes, executes and repairs skills, which pass sampled tests before a lower-cost caller reuses them.

**Verification:** Development and deployment budgets are separate; frozen-skill tests assess what survives after optimization ends.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-23098"></a>
<!-- stage3-record: {"id": "2610.23098", "scope": "Core", "section": 5} -->

#### InstAgent: A Recursively Self-Improving Agent Operating System for Heterogeneous Robot Collaboration

`2026-10-16` · ShanghaiTech University, Shanghai, China.; InstAdapt, Shanghai, China.

[Paper](https://arxiv.org/abs/2610.23098)

Retains repaired programs for heterogeneous robot teams.

**Method:** Generated behavior trees coordinate robots; repaired routines and shared spatiotemporal memory support task handoffs.

**Verification:** Collaboration and handoff checks evaluate the system; stored programs are an external learning artifact.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-22736"></a>
<!-- stage3-record: {"id": "2610.22736", "scope": "Adjacent", "section": 5} -->

#### Spatial Memory by Agents, for Agents

`2026-10-15` · Nanjing University; Princeton University; Carnegie Mellon University; Johns Hopkins University; Mondo Robotics

[Paper](https://arxiv.org/abs/2610.22736) · [Project page](https://ba-fa-3344.github.io/)

Programs the spatial memory used by another agent.

**Method:** A designer agent edits memory construction and retrieval code using task feedback from a fixed query agent.

**Verification:** The memory implementation is frozen before held-out evaluation; designer and query-agent roles remain separate.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-22496"></a>
<!-- stage3-record: {"id": "2610.22496", "scope": "Core", "section": 5} -->

#### Scaling Online Exploration for Robot Agents

`2026-10-15` · Harvard University; NVIDIA; University of California, Berkeley; Massachusetts Institute of Technology; Stanford University

[Paper](https://arxiv.org/abs/2610.22496) · [Project page](https://robot-agent-exploration.com/) · [Dataset](https://huggingface.co/datasets/robot-agent-exploration/robot-session-logs) · [Code](https://github.com/robot-agent-exploration/skills-lib) · [Code](https://github.com/robot-agent-exploration/rax)

Studies how exploration becomes reusable robot experience.

**Method:** General coding agents explore different robots, write control programs and retain simulation and physical interaction records.

**Verification:** Public logs mix physical and simulated sessions, code, sensor outputs and human instructions; provenance must be separated. The official release includes 12 real-robot session logs with tool results, video and generated skills.

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4)

<a id="work-2610-18867"></a>
<!-- stage3-record: {"id": "2610.18867", "scope": "Core", "section": 5} -->

#### EmbodiedEvo: Self-Evolving Coding Agent For Physical Intelligence

`2026-10-13` · Navers Lab, Einsia.AI, Tsinghua University

[Paper](https://arxiv.org/abs/2610.18867)

Separates executable skills from diagnostic lessons.

**Method:** Physical execution feedback is distilled into Skills for action and Lessons for diagnosis, supporting later coding-agent tasks.

**Verification:** Persistent skill and lesson reuse is different from a temporary repair in the same episode.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-18874"></a>
<!-- stage3-record: {"id": "2610.18874", "scope": "Adjacent", "section": 5} -->

#### ChunkAct: Action Chunking for Agentic Robotics

`2026-10-13` · University of Southern California; University of Central Florida; Stony Brook University

[Paper](https://arxiv.org/abs/2610.18874)

Compiles memory into autonomous action chunks.

**Method:** The system turns remembered robot procedures into executable chunks and returns control to the high-level model on failure.

**Verification:** Execution cost and success need joint assessment because reduced reasoning can also change recovery opportunities.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-14224"></a>
<!-- stage3-record: {"id": "2610.14224", "scope": "Adjacent", "section": 5} -->

#### Harness^2: Recursive Agent Harnessing for an Open World

`2026-10-09` · Google Cloud AI Research; Northwestern University

[Paper](https://arxiv.org/abs/2610.14224)

Evolves harnesses within and across tasks.

**Method:** Nested update loops propose reusable harness changes and retain them through validation for open-world tasks.

**Verification:** Recursive update descriptions alone do not establish the full multimodal code-repair chain.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-10498"></a>
<!-- stage3-record: {"id": "2610.10498", "scope": "Core", "section": 5} -->

#### EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution

`2026-10-07` · Columbia University; Princeton University

[Paper](https://arxiv.org/abs/2610.10498)

Chooses robot experiments using explicit hypotheses.

**Method:** A hypothesis graph prioritizes interactions whose outcomes can improve robot code and reusable skills.

**Verification:** Exploration selection and retained skill gains should be assessed separately from total trial count.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-08995"></a>
<!-- stage3-record: {"id": "2610.08995", "scope": "Core", "section": 5} -->

#### PhysEvo: Astra Can Act, Let It

`2026-10-06` · University of Chinese Academy of Sciences; Institute of Automation, Chinese Academy of Sciences; Tsinghua University; Independent researcher

[Bibliographic record](../README.md#paper-2610-08995) · [Paper](https://arxiv.org/abs/2610.08995)

Improves robot tools while keeping the model frozen.

**Method:** Aligned images, states and execution traces guide revisions to action and diagnosis code, which are tested and retained between development episodes.

**Verification:** Held-out layouts, interface ablations and fixed-version tests distinguish development adaptation from final evaluation.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-01178"></a>
<!-- stage3-record: {"id": "2610.01178", "scope": "Core", "section": 5} -->

#### Recova: Agent-Guided Failure Recovery for Autonomous Robotic Manipulation

`2026-10-01` · University of California, San Diego; University of Texas at Austin; NVIDIA

[Paper](https://arxiv.org/abs/2610.01178) · [Project page](https://www.liuisabella.com/Recova)

Practices recovery in digital twins before real execution.

**Method:** An agent tests recovery programs in a reconstructed twin, then uses physical execution to refine task and recovery behavior.

**Verification:** Twin quality, recovery-code quality and the base action policy are distinct contributors.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-02204"></a>
<!-- stage3-record: {"id": "2610.02204", "scope": "Adjacent", "section": 5} -->

#### Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents

`2026-10-01` · UC Berkeley; MIT; Amazon FAR; University of Chicago

[Paper](https://arxiv.org/abs/2610.02204) · [Project page](https://rpg-robot.github.io/)

Uses reconstructed practice environments to improve agents.

**Method:** Offline task materials seed simulated practice; execution feedback improves reusable robot-system components before deployment.

**Verification:** Privileged development diagnostics must be separated from observations available to the deployed agent.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-39304"></a>
<!-- stage3-record: {"id": "2609.39304", "scope": "Core", "section": 5} -->

#### Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents

`2026-09-30` · Not reported

[Paper](https://arxiv.org/abs/2609.39304)

Studies scale and selection in harness optimization.

**Method:** An optimizing coding agent edits another robot agent's prompts, tools and control rules using collected trajectories.

**Verification:** Experiments separate search budget and candidate-selection effects from the executing model.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-39018"></a>
<!-- stage3-record: {"id": "2609.39018", "scope": "Core", "section": 5} -->

#### Make Code as Policy Great Again: Frontier Agents Write, Call, and Evolve Robot Tools

`2026-09-30` · HexaFuture; Peking University; Beijing Institute of Technology; Tsinghua University

[Paper](https://arxiv.org/abs/2609.39018)

Lets agents write and evolve the tools they execute.

**Method:** Programs hold multi-stage behavior while a frontier model chooses strategies, checks results and revises robot-tool implementations.

**Verification:** Tool evolution differs from selecting a fixed tool and from updating model parameters.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-40306"></a>
<!-- stage3-record: {"id": "2609.40306", "scope": "Adjacent", "section": 5} -->

#### DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents

`2026-09-30` · Nanyang Technological University; Nanjing University

[Paper](https://arxiv.org/abs/2609.40306) · [Project page](https://denghaoyuan123.github.io/Dynaharness_page/)

Grounds harness evolution in physical execution contracts.

**Method:** A shared execution contract links semantic reasoning and physical constraints; failures motivate checked capability and harness changes.

**Verification:** Verified code changes are the learning unit, not reflection alone.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-39207"></a>
<!-- stage3-record: {"id": "2609.39207", "scope": "Core", "section": 5} -->

#### ASENA: Self-evolving Agents for Embodied Navigation

`2026-09-30` · NVIDIA; University of California, San Diego; The University of Texas at Austin

[Paper](https://arxiv.org/abs/2609.39207) · [Project page](https://research.nvidia.com/labs/gear/asena)

Retains navigation repairs for subsequent environments.

**Method:** A navigation agent inspects sensor data and execution records, writes programs and preserves repaired routines and experience.

**Verification:** Later-environment performance tests reuse; an individual retry alone is not continual learning.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-37583"></a>
<!-- stage3-record: {"id": "2609.37583", "scope": "Adjacent", "section": 5} -->

#### RoboHarn-Evo: Evolving Hierarchical Physical Knowledge for Self-Improving Robotic Manipulation

`2026-09-29` · Renmin University of China; XYZ Embodied AI; Tsinghua University

[Paper](https://arxiv.org/abs/2609.37583)

Accumulates hierarchical knowledge from physical interaction.

**Method:** Two harness loops turn interaction experience into reusable physical knowledge that guides subsequent manipulation.

**Verification:** The persisted knowledge is external to the base model; later-task tests establish its value.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-35432"></a>
<!-- stage3-record: {"id": "2609.35432", "scope": "Core", "section": 5} -->

#### Self-Evolving Coding Agents: From Digital Programs to Physical-World Intelligence

`2026-09-28` · Not reported

[Bibliographic record](../README.md#paper-2609-35432) · [Paper](https://arxiv.org/abs/2609.35432)

Improves robot tools through explicit world and policy code.

**Method:** World programs track objects and progress; policy programs coordinate perception and action models, while execution evidence revises reusable tools.

**Verification:** Versioned replays, held-out seeds and bounded hardware tests separate tool updates from independently trained models.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-33378"></a>
<!-- stage3-record: {"id": "2609.33378", "scope": "Adjacent", "section": 5} -->

#### Recursive Harness Distillation across Agents for Robot Manipulation

`2026-09-27` · Seoul National University; Korea Advanced Institute of Science and Technology

[Paper](https://arxiv.org/abs/2609.33378)

Transfers external harness guidance between agents.

**Method:** Intervention and repair experience becomes guidance that other agents reuse and validate through later robot execution.

**Verification:** Strong, weak and action models remain frozen; distillation here transfers guidance rather than weights.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-32862"></a>
<!-- stage3-record: {"id": "2609.32862", "scope": "Core", "section": 5} -->

#### RoboFoundry: System-as-Policy Evolution for Self-Learning Embodied Agents

`2026-09-26` · Nanyang Technological University; Beihang University; National University of Singapore; Cloud Butterfly Technology; Shanghai Jiao Tong University

[Paper](https://arxiv.org/abs/2609.32862) · [Project page](https://jingsongliang.com/robofoundry)

Treats the robot support system as an evolving policy.

**Method:** Execution experience produces checked changes to code, memory and interfaces surrounding the robot agent.

**Verification:** Capability gains belong to the combined system; changes to external code must not be described as weight learning.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-29394"></a>
<!-- stage3-record: {"id": "2609.29394", "scope": "Core", "section": 5} -->

#### RACaP: Agentic Reasoning, Acting, and Coding as Policies for Evolvable Robot Learning

`2026-09-24` · Chinese University of Hong Kong; HKUST (Guangzhou); Knowin AI

[Paper](https://arxiv.org/abs/2609.29394)

Separates online decisions from an evolving robot API.

**Method:** A ReAct agent calls reusable APIs while curriculum and execution experience update the API, harness and long-term memory.

**Verification:** API and memory evolution should be assessed separately from within-episode control.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2609-31760"></a>
<!-- stage3-record: {"id": "2609.31760", "scope": "Core", "section": 5} -->

#### What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery

`2026-09-23` · National University of Singapore

[Paper](https://arxiv.org/abs/2609.31760)

Analyzes why repeated code and skill improvements can fail to produce cumulative task success.

**Method:** Coding agents inspect failure keyframes and diagnoses, revise typed Python skills, install external models, and refit routing from logs. Replay and paired simulator trials gate accepted changes; humans retain control of the evaluator and memory harness. LLM weights are not trained.

**Verification:** A 123-round RoboCasa case study reports no success on its target fridge task. It traces weak tests, corrupted memory and early-step bottlenecks; changing models and human harness repairs prevent interpreting the run as a controlled comparison or autonomous end-to-end self-improvement.

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3) · [6. Physical Applications and Experiments](#section-6)

<a id="work-2608-16590"></a>
<!-- stage3-record: {"id": "2608.16590", "scope": "Core", "section": 5} -->

#### Zetta $ζ$: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence

`2026-08-17` · Institute for AI Industry Research (AIR), Tsinghua University; Z-Trans AI

[Paper](https://arxiv.org/abs/2608.16590)

Evolves monitors and recovery around a frozen policy.

**Method:** Runtime monitors gather anomaly evidence for an orchestration agent; an evolution agent revises monitoring code and recovery skills from failures.

**Verification:** Online monitoring and offline code evolution are distinct loops; the action policy remains frozen.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2608-11350"></a>
<!-- stage3-record: {"id": "2608.11350", "scope": "Adjacent", "section": 5} -->

#### Self-Evolving Embodied Agents via Skill-Harness Evolution

`2026-08-11` · Northeastern University; Microsoft Research

[Paper](https://arxiv.org/abs/2608.11350)

Evolves skills and the harness together.

**Method:** Experience updates reusable skills and surrounding harness logic while the underlying action interface and base model can stay fixed.

**Verification:** External-system improvement is distinct from training the foundation model.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2608-09410"></a>
<!-- stage3-record: {"id": "2608.09410", "scope": "Core", "section": 5} -->

#### Skills in Weights, Memory in Code: Hybrid Learning for Memory-Dependent Robot Manipulation

`2026-08-10` · Northwestern University; University of Minnesota; Stanford University

[Bibliographic record](../README.md#paper-2608-09410) · [Paper](https://arxiv.org/abs/2608.09410)

Combines learned skills with programmable memory.

**Method:** Rollouts guide changes to executable memory-management heuristics while multimodal stage verification checks progress during manipulation.

**Verification:** Task and cumulative-stage success are distinguished from proprioceptive or visual completion detection.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2607-23784"></a>
<!-- stage3-record: {"id": "2607.23784", "scope": "Adjacent", "section": 5} -->

#### A Few Words Go a Long Way: Language Guided Robot Policy Synthesis

`2026-07-26` · University of Washington; Microsoft Research; Massachusetts Institute of Technology

[Paper](https://arxiv.org/abs/2607.23784) · [Project page](https://robo-architect.github.io/)

Uses language corrections to improve robot programs.

**Method:** A coding agent combines execution traces with human corrections to resynthesize programs and retain reusable skills.

**Verification:** Franka tests allow up to five expert corrections; automatic VLM correction is a separate ablation.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2607-00272"></a>
<!-- stage3-record: {"id": "2607.00272", "scope": "Core", "section": 5} -->

#### ASPIRE: Agentic /Skills Discovery for Robotics

`2026-06-30` · NVIDIA; Carnegie Mellon University; University of California, Berkeley; University of Michigan; University of Illinois Urbana-Champaign

[Bibliographic record](../README.md#paper-2607-00272) · [Paper](https://arxiv.org/abs/2607.00272) · [Code](https://github.com/NVlabs/ASPIRE) · [Project page](https://research.nvidia.com/labs/gear/aspire/)

Turns verified code repairs into reusable skills.

**Method:** A frozen coding model reads multimodal rollout traces, repairs code-as-policy programs and stores successful repairs as skills with diagnostic guidance.

**Verification:** Re-execution, held-out tasks and transfer test the skill library; the base model remains frozen.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2606-19419"></a>
<!-- stage3-record: {"id": "2606.19419", "scope": "Core", "section": 5} -->

#### Playful Agentic Robot Learning

`2026-06-17` · University of California, Berkeley  Impossible Research

[Paper](https://arxiv.org/abs/2606.19419) · [Project page](https://playful-rats.github.io/)

Turns task-free exploration into persistent code skills.

**Method:** The robot proposes learning goals, writes and repairs programs during exploration, then saves successful behaviors for reuse.

**Verification:** Skill discovery must be distinguished from immediate retries; later execution measures retained capability.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2605-10332"></a>
<!-- stage3-record: {"id": "2605.10332", "scope": "Adjacent", "section": 5} -->

#### EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents

`2026-05-11` · Huazhong University of Science and Technology; University of Science and Technology of China; Microsoft Research; Institute for AI Industry Research (AIR), Tsinghua University

[Paper](https://arxiv.org/abs/2605.10332)

Links reflection to the skills responsible for failures.

**Method:** Execution failures are organized by skill so reflections produce more targeted updates to reusable embodied behaviors.

**Verification:** The learning object is skill-level experience; performance claims require later task execution rather than reflection text alone.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2603-02623"></a>
<!-- stage3-record: {"id": "2603.02623", "scope": "Adjacent", "section": 5} -->

#### Uni-Skill: Building Self-Evolving Skill Repository for Generalizable Robotic Manipulation

`2026-03-03` · Institute of Computing Technology, Chinese Academy of Sciences; University of Chinese Academy of Sciences

[Paper](https://arxiv.org/abs/2603.02623)

Maintains an evolving repository of robot skills.

**Method:** Skill-aware planning retrieves reusable routines while automatic evolution updates the repository from manipulation experience.

**Verification:** Skill transfer is evaluated through repository use; persistent skills are not automatically model-weight learning.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2509-18597"></a>
<!-- stage3-record: {"id": "2509.18597", "scope": "Core", "section": 5} -->

#### Robotic Ultra-Long-Horizon Manipulation Skills via Human-guided Lifelong Code Generation

`2025-09-23` · Beijing Academy of Artificial Intelligence; XYZ Embodied AI

[Bibliographic record](../README.md#paper-2509-18597) · [Paper](https://arxiv.org/abs/2509.18597) · [Code](https://github.com/Ghiara/LYRA) · [Project page](https://ghiara.github.io/LYRA/)

Retains human corrections as long-horizon code skills.

**Method:** Corrections are stored as inheritable, retrievable robot programs; a separate configuration diagnoses RGB-D feedback and revises plans.

**Verification:** Human-guided learning and visual-feedback variants are evaluated separately with memory ablations and hardware trials.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2406-18746"></a>
<!-- stage3-record: {"id": "2406.18746", "scope": "Adjacent", "section": 5} -->

#### Lifelong Robot Library Learning: Bootstrapping Composable and Generalizable Skills for Embodied Control with Language Models

`2024-06-26` · University of Groningen

[Paper](https://arxiv.org/abs/2406.18746) · [Project page](https://gtziafas.github.io/LRLL_project)

Accumulates a library of composable control programs.

**Method:** The system bootstraps reusable routines from robot execution so language-model plans can call increasingly capable library functions.

**Verification:** Transfer is assessed through library reuse across tasks; the stored programs are distinct from learned model weights.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2406-03757"></a>
<!-- stage3-record: {"id": "2406.03757", "scope": "Adjacent", "section": 5} -->

#### RoboCoder: Robotic Learning from Basic Skills to General Tasks with Large Language Models

`2024-06-06` · CUHK; SmartMore

[Paper](https://arxiv.org/abs/2406.03757)

Builds complex tasks from reusable basic skills.

**Method:** An LLM composes basic robotic skills into task programs and retains a skill library for later reuse.

**Verification:** Task execution tests skill composition; reuse of a library should be separated from foundation-model training.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2405-19758"></a>
<!-- stage3-record: {"id": "2405.19758", "scope": "Adjacent", "section": 5} -->

#### InterPreT: Interactive Predicate Learning from Language Feedback for Generalizable Task Planning

`2024-05-30` · University of California, Los Angeles; University of Texas at Austin

[Paper](https://arxiv.org/abs/2405.19758) · [Project page](https://interpret-robot.github.io)

Learns planning predicates from language corrections.

**Method:** Human feedback guides predicate and symbolic-operator learning, after which the learned representation is compiled into PDDL for harder tasks.

**Verification:** Generalization concerns predicates and planning models; human feedback remains part of the learning setup.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2305-16744"></a>
<!-- stage3-record: {"id": "2305.16744", "scope": "Adjacent", "section": 5} -->

#### Demo2Code: From Summarizing Demonstrations to Synthesizing Code via Extended Chain-of-Thought

`2023-05-26` · Cornell University

[Paper](https://arxiv.org/abs/2305.16744) · [Project page](https://portal-cornell.github.io/demo2code/)

Turns demonstrations into reusable robot programs.

**Method:** Demonstrations are recursively summarized into specifications, then expanded into executable programs through intermediate reasoning steps.

**Verification:** Program synthesis and task execution evaluate demonstration-to-code transfer; this does not imply updating the foundation model.

**Related:** [1. Embodied Harnesses](#section-1)

### Post-training the coding agent

<a id="work-2611-10768"></a>
<!-- stage3-record: {"id": "2611.10768", "scope": "Core", "section": 5} -->

#### BlenderFORGE: Framework for Optimizing Reactive 3D-Graphics Editing Ability of MLLMs

`2026-11-07` · Hong Kong University of Science and Technology; SenseTime Research

[Bibliographic record](../README.md#paper-2611-10768) · [Paper](https://arxiv.org/abs/2611.10768) · [Project page](https://sensetime-fvg.github.io/BlenderFORGE/)

Trains an open-weight coding agent to revise explicit Blender scenes using executable edits and rendered feedback.

**Method:** Perturbed assets yield start/goal scenes, images and state targets. Teacher trajectories initialize SFT; sandbox rewards drive multi-turn AgentLoop-RL. The agent requests previews between bpy edits. Training updates the editing MLLM, while scene-state metrics supply supervision.

**Verification:** Four editing families, SFT/RL ablations and camera/BlenderGym transfer; metrics exclude timeout/server failures. Reports 9,000 training and 800 test tasks. The official repository lists code, sandbox, data and weights as forthcoming; these are not yet a released training dataset.

**Related:** [1. Embodied Harnesses](#section-1) · [2. Simulator Construction](#section-2) · [4. Data](#section-4)

<a id="work-2610-41216"></a>
<!-- stage3-record: {"id": "2610.41216", "scope": "Adjacent", "section": 5} -->

#### TinyAstral: Transferring Self-Evolving Harnesses to Tiny Generalist Manipulation Agents

`2026-10-30` · Huawei Technologies Co., Ltd; Huawei Noah Research Institute

[Paper](https://arxiv.org/abs/2610.41216) · [Project page](https://garfield-kh.github.io/TinyAstral/)

Transfers a refined teacher harness to a small agent.

**Method:** Paired trials first evolve a frozen teacher's harness; teacher trajectories in the fixed resulting interface then train a smaller agent.

**Verification:** Harness evolution and student weight learning are separate stages.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2610-40799"></a>
<!-- stage3-record: {"id": "2610.40799", "scope": "Core", "section": 5} -->

#### CaPtain: A Pipeline for Post-Training Code-as-Policy Robot Agents

`2026-10-29` · MMLab, The Chinese University of Hong Kong; NovaXBot

[Bibliographic record](../README.md#paper-2610-40799) · [Paper](https://arxiv.org/abs/2610.40799) · [Code](https://github.com/waltstephen/CaPtain) · [Code](https://github.com/waltstephen/CaPtain-Harness)

Trains a small model to act through robot code.

**Method:** SFT teaches the interface from teacher trajectories; multi-turn RL uses a privileged physical critic to credit requests, while deployment uses ordinary observations and low-level tools.

**Verification:** The coding agent's weights change; privileged critic state is removed at test time, and hardware transfer follows simulation adaptation.

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4)

<a id="work-2610-30136"></a>
<!-- stage3-record: {"id": "2610.30136", "scope": "Adjacent", "section": 5} -->

#### Agentic World Action Models

`2026-10-21` · University of California, Berkeley; NVIDIA; University of Pennsylvania

[Bibliographic record](../README.md#paper-2610-30136) · [Paper](https://arxiv.org/abs/2610.30136) · [Project page](https://agentic-wam.github.io/)

Models programs, predicted video and robot actions together.

**Method:** The model jointly produces skill-program plans, future video and actions; an optional hybrid mode switches between valid program segments and model action chunks.

**Verification:** Jointly learned output streams differ from a frozen agent calling an external action model; no online skill-library learning is claimed.

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4)

<a id="work-2610-28589"></a>
<!-- stage3-record: {"id": "2610.28589", "scope": "Core", "section": 5} -->

#### AgenticRoboRL: Bringing Coding-Agent Post-Training to Agentic Robotics

`2026-10-20` · University of Central Florida; University of Southern California; Michigan State University

[Paper](https://arxiv.org/abs/2610.28589)

Post-trains robot planners across different harnesses.

**Method:** SFT and multi-turn RL train the decision model through adapters for control-code generation or VLA-skill calls while execution components remain fixed.

**Verification:** Planner weight updates are distinct from harness improvement; interface-specific results should not be collapsed into one control mechanism.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2606-18363"></a>
<!-- stage3-record: {"id": "2606.18363", "scope": "Adjacent", "section": 5} -->

#### Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness

`2026-06-16` · University of Maryland College Park; University of Illinois Urbana-Champaign; University of Waterloo; Mohamed bin Zayed University of Artificial Intelligence; University of Pennsylvania; Amazon FAR

[Paper](https://arxiv.org/abs/2606.18363)

Distills a frontier model through a robot harness.

**Method:** The work first studies tool-interface design, then trains a compact agent on the teacher's manipulation trajectories in that interface.

**Verification:** Harness changes and student-model training are separate causes of improvement.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2501-04268"></a>
<!-- stage3-record: {"id": "2501.04268", "scope": "Adjacent", "section": 5} -->

#### Robotic Programmer: Video Instructed Policy Code Generation for Robotic Manipulation

`2025-01-08` · Institute of Computing Technology, Chinese Academy of Sciences; University of Chinese Academy of Sciences

[Paper](https://arxiv.org/abs/2501.04268)

Uses real videos to train a robot code generator.

**Method:** Video2Code generates policy-code labels from robot videos, and RoboPro learns to map observations and instructions to robot programs.

**Verification:** Real video provenance does not mean the generated code was executed on that physical trajectory.

**Related:** [1. Embodied Harnesses](#section-1) · [4. Data](#section-4)

<a id="work-2402-16117"></a>
<!-- stage3-record: {"id": "2402.16117", "scope": "Adjacent", "section": 5} -->

#### RoboCodeX: Multimodal Code Generation for Robotic Behavior Synthesis

`2024-02-25` · University of Hong Kong; OpenGVLab, Shanghai AI Laboratory; ETH Zurich; Shanghai Jiao Tong University; Chinese University of Hong Kong; Tsinghua University; University of California, Berkeley

[Paper](https://arxiv.org/abs/2402.16117)

Trains a multimodal model to write robot behaviors.

**Method:** Multimodal robot-code supervision connects observations, task reasoning and physical preferences to executable behavior synthesis.

**Verification:** Training changes the code-generation model; evaluate generated behavior and transfer separately from data-generation quality.

**Related:** [1. Embodied Harnesses](#section-1)

### Cross-section reading

- [PhyRubric: Rubric-Grounded Diagnostic Evaluation of Physical Commonsense in Text-to-Video Generation](#work-2611-13576)
- [Embodied First Exam](#work-2611-12177)
- [PneuGen: Task-Driven Agentic Co-Design of Soft Pneumatic Robots](#work-2611-13344)
- [PhysOPSD: Code as Privilege for Physically Plausible Video Generation](#work-2611-12411)
- [TactileLab: Sim-to-Real Dexterous Robot Manipulation with Efficient Shear-Sensitive Tactile Simulation](#work-2611-07881)
- [PCBRouteAgent: How Close Are LLM Agents to Becoming PCB Routing Engineers?](#work-2611-08175)
- [Open-HumanWAM: An Open Recipe for Scaling Human and Robot Experience for Embodied Foundation Models](#work-2611-06817)
- [Gym-Anything for Robotics: Scaling physical simulations with digital agents](#work-2610-40565)
- [HexaShell: A Universal Harness for Robot Coding Agents in Simulation and the Real World](#work-2610-23479)
- [CoDA: Co-Evolution of Data Engines and Action Policies](#work-2610-22362)
- [RoboSimStudio: An Interactive Toolkit for Human and Agent Rapid Real2Sim of Robot Manipulation Tasks](#work-2610-18835)
- [Agentic Robot Creation through Generation, Verification, and Revision](#work-2610-17881)
- [D-World: An Explicit World-Language-Action Model with Recursive Self-Improvement under Dual Control](#work-2610-17114)
- [RobotUse: Allocating Computation, Context, and Decisions](#work-2610-04929)
- [Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens](#work-2610-01939)
- [Awomo-SimDataEngine: Agentic Simulation-Ready World Generation](#work-2610-02274)
- [Text2Sim: Agentic Physics-Based Simulation Generation with Distilled Expertise](#work-2609-36593)
- [Real2Gym: Building Gyms from Videos, Bringing Skills to Robots](#work-2609-37089)
- [DexAgent: An Agentic Human2Sim2Robot Framework for Dexterous Manipulation with Self-Evolving Tool Library](#work-2609-35318)
- [HarnessPAI: An Evolving Harness for Physical AI](#work-2609-29166)
- [EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics](#work-2609-27308)
- [DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation](#work-2609-18620)
- [GIF: Agentic Generation of Interactive and Functional Object Compositions for Robot Learning](#work-2609-05927)
- [Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling](#work-2608-30821)
- [LabRobFail: A Benchmark for Robotic Failure Analysis in Chemical Self-driving Laboratory](#work-2607-23704)
- [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](#work-2607-19190)
- [UniPhysGen: Unified Physical Grounding for Simulation-Ready 3D Assets](#work-2607-13586)
- [SimFoundry: Modular and Automated Scene Generation for Policy Learning and Evaluation](#work-2606-28276)
- [PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects](#work-2605-21572)
- [Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback](#work-2605-17448)
- [SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning](#work-2605-09423)
- [SceneTeract: Probing and Improving Agent-Aware Activity Reasoning in 3D Indoor Scenes](#work-2603-29798)
- [Training and Benchmarking Code Generation for Physics-Inspired Animations](#work-2602-10840)
- [SAGE: Scalable Agentic 3D Scene Generation for Embodied AI](#work-2602-10116)
- [Eurekaverse: Environment Curriculum Generation via Large Language Models](#work-2411-01775)
- [GenSim2: Scaling Robot Data Generation with Multi-modal and Reasoning LLMs](#work-2410-03645)
- [Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model](#work-2410-13882)
- [FactorSim: Generative Simulation via Factorized Representation](#work-2409-17652)
- [RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins](#work-2409-02920)
- [Real2Code: Reconstruct Articulated Objects via Code Generation](#work-2406-08474)
- [OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code](#work-2405-15568)
- [Evaluating Real-World Robot Manipulation Policies in Simulation](#work-2405-05941)
- [Holodeck: Language Guided Generation of 3D Embodied AI Environments](#work-2312-09067)
- [RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation](#work-2311-01455)
- [Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models](#work-2310-18308)
- [GenSim: Generating Robotic Simulation Tasks via Large Language Models](#work-2310-01361)

[Back to the research map](#research-map)

---

<a id="section-6"></a>

## 6. Physical Applications and Experiments

Physical applications test whether generated programs, models and designs meet an external objective. Manipulation remains the center of this topic; laboratory operations, instruments and manufacturing provide complementary settings where calibration, measurement and material constraints change what counts as success.

| Application | Artifact and interface | What the experiment must establish |
|---|---|---|
| Robot manipulation | Motion programs, control policies, force/tactile interfaces and executable skills. | Task success and recovery across poses, objects and contact conditions; separately identify simulator trials, physical trials and human assistance. [RAPID](#work-2609-30249) tests demonstration-derived programs, while [FORCA](#work-2610-31841) studies force-aware programming. |
| Scientific experiments and measurement | Instrument drivers, laboratory layouts, robot procedures and analysis programs. | Instrument commissioning, calibrated measurements and reproducible experimental outcomes. [Self-Building Labs](#work-2610-23826) connects laboratory configuration with executable procedures; physical observations must support the scientific conclusion as well as successful tool calls. |
| Design, manufacturing and verification | CAD, robot morphology, actuation programs, PCB routes and fabrication plans. | Geometric or solver checks, manufacturability, and physical testing are successive forms of evidence. [PneuGen](#work-2611-13344) fabricates selected simulated designs; [PCBRouteAgent](#work-2611-08175) reports routing checks without fabricated-board validation. |

For each result, identify the **agent's contribution**, the **controller or solver's contribution**, and the **feedback used for revision**. A physical demonstration can validate a frozen design or program without making hardware part of its optimization loop. Conversely, a policy developed through real robot trials can still require a separate reliability test after development is finished.

**Research question.** What evidence is sufficient to transfer a verified simulator result to a new physical apparatus, and which failures require changing the environment model, the controller, the program or the experimental specification?

### Robot interaction and manipulation

<a id="work-2611-07881"></a>
<!-- stage3-record: {"id": "2611.07881", "scope": "Adjacent", "section": 6} -->

#### TactileLab: Sim-to-Real Dexterous Robot Manipulation with Efficient Shear-Sensitive Tactile Simulation

`2026-11-05` · Beijing Institute of Technology; University of Bristol; Xi’an Jiaotong-Liverpool University

[Bibliographic record](../README.md#paper-2611-07881) · [Paper](https://arxiv.org/abs/2611.07881) · [Project page](https://yijionglin.github.io/tactilelab/)

Transfers simulation-trained manipulation policies using paired real/sim tactile representations.

**Method:** IsaacLab rigid-body contacts generate depth and tangential-flow fields; PETS-Net fuses these with proprioceptive history. Real tactile image streams train translators into the simulated representation. The updated models are tactile translators and control policies, not a coding agent.

**Verification:** Simulation modality/architecture ablations, paired tactile calibration, and physical dual-arm object following and LEAP-hand rotation. Tangential-flow modeling assumes sticking contact; this is a transfer result rather than autonomous simulator construction.

**Related:** [2. Simulator Construction](#section-2) · [3. Simulator Quality Evaluation](#section-3) · [4. Data](#section-4) · [5. Training and Capability Improvement](#section-5)

<a id="work-2611-08321"></a>
<!-- stage3-record: {"id": "2611.08321", "scope": "Adjacent", "section": 6} -->

#### ControlAnything: Generative UI and On-Demand Device Integration for Mixed-Reality Hand Interaction by a Coding Agent

`2026-11-05` · Not reported

[Bibliographic record](../README.md#paper-2611-08321) · [Paper](https://arxiv.org/abs/2611.08321) · [Code](https://github.com/Apolotary/controlanything)

Generates interfaces that connect hand gestures to devices.

**Method:** A coding agent turns visual object selection and language requests into device connectors, AR controls and gesture-mapping programs over existing transport layers.

**Verification:** A single-author technical study verifies communication acknowledgments, not the intended physical effects.

<a id="work-2610-31841"></a>
<!-- stage3-record: {"id": "2610.31841", "scope": "Core", "section": 6} -->

#### FORCA: A Force-Aware Coding Agent for Contact-Rich Robot Manipulation

`2026-10-22` · University of Illinois Urbana-Champaign; Tsinghua University

[Bibliographic record](../README.md#paper-2610-31841) · [Paper](https://arxiv.org/abs/2610.31841) · [Project page](https://tanoom.github.io/forca/)

Uses vision and force traces to repair contact code.

**Method:** The agent rewrites Python contact-control logic using real images and force/torque traces to improve contact decisions, ordering and recovery.

**Verification:** Five UR5e task families assess fixed-controller success, force limits and the cost of physical revisions.

<a id="work-2610-20998"></a>
<!-- stage3-record: {"id": "2610.20998", "scope": "Core", "section": 6} -->

#### MoCaP: Mobile Code-as-Policies for Zero-Shot Mobile Manipulation from Passive Human Videos

`2026-10-14` · New York University; Fudan University; NYU Shanghai

[Bibliographic record](../README.md#paper-2610-20998) · [Paper](https://arxiv.org/abs/2610.20998) · [Project page](https://mocap-7.github.io/MoCAP-page/)

Transfers human-video priors to mobile robot programs.

**Method:** Passive videos provide spatial and approach priors; live RGB-D observations guide short Python programs under robot-specific motion constraints.

**Verification:** YOR navigation and two grasp tasks test feasibility in one environment, not broad cross-household generalization.

<a id="work-2610-12549"></a>
<!-- stage3-record: {"id": "2610.12549", "scope": "Core", "section": 6} -->

#### Fly-by-Code: Embodied Coding Agents for Aerial Manipulation with Active Visual and Physical Feedback

`2026-10-08` · Seoul National University; Carnegie Mellon University; University of Maryland, College Park; All Purpose AI; Kyung Hee University

[Paper](https://arxiv.org/abs/2610.12549) · [Project page](https://fly-by-code.github.io/)

Uses active sensing to program aerial manipulation.

**Method:** The agent chooses views and probes the scene, then revises task programs from visual and action feedback.

**Verification:** Simulation and hardware evidence should be distinguished, including the role of sensing and physical probes.

<a id="work-2609-30249"></a>
<!-- stage3-record: {"id": "2609.30249", "scope": "Adjacent", "section": 6} -->

#### RAPID: Robot Agentic Programming from Demonstrations

`2026-09-24` · Massachusetts Institute of Technology; National University of Singapore; University of Pennsylvania; NVIDIA

[Bibliographic record](../README.md#paper-2609-30249) · [Paper](https://arxiv.org/abs/2609.30249) · [Project page](https://yuyaoliu.me/projects/rapid)

Infers reusable relational robot programs and a verification environment from one visual demonstration.

**Method:** Infer success predicates, reconstruct an interactive scene, and refine trajectory-optimization primitives and relational composition across scene variants before fixed-program deployment.

**Verification:** Evaluated eight contact-rich nonprehensile tasks and LIBERO-Pro in simulation, with real Franka trials on the eight nonprehensile tasks; deployment tests the resulting program rather than online model learning.

<a id="work-2609-23133"></a>
<!-- stage3-record: {"id": "2609.23133", "scope": "Core", "section": 6} -->

#### AquaCap: A Training-Free Underwater Embodied Agent with Code-as-Policy

`2026-09-19` · Sun Yat-sen University; Dalian University of Technology; BIXOCEAN; Southern Marine Science and Engineering Guangdong Laboratory

[Bibliographic record](../README.md#paper-2609-23133) · [Paper](https://arxiv.org/abs/2609.23133)

Adapts underwater programs using execution feedback.

**Method:** Sensor-derived geometry and reliability checks detect unsuccessful actions, prompting changes to subsequent Python programs and plans.

**Verification:** Simulation efficiency and ablations accompany limited pool grasping and transport results; recovery and timeout remain explicit.

<a id="work-2503-23875"></a>
<!-- stage3-record: {"id": "2503.23875", "scope": "Core", "section": 6} -->

#### GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models

`2025-03-31` · Department of Artificial Intelligence, Westlake University, Hangzhou, China; School of Automation Science and Electrical Engineering, Beihang University, Beijing, China; Institute of Engineering and Technology, University of Groningen, Groningen, Netherlands; Department of Computer Science, Technical University of Darmstadt, Darmstadt, Germany; School of Electrical and Electronic Engineering, The University of Sheffield, Sheffield, UK

[Paper](https://arxiv.org/abs/2503.23875) · [Code](https://github.com/WindyLab/GenSwarm)

Generates and deploys multi-robot code policies.

**Method:** Language-model planning decomposes team tasks into hierarchical code, with simulation video and optional human feedback guiding revisions.

**Verification:** Simulation optimization and physical deployment are reported separately; human corrections remain explicit.

<a id="work-2403-07832"></a>
<!-- stage3-record: {"id": "2403.07832", "scope": "Adjacent", "section": 6} -->

#### DeliGrasp: Inferring Object Properties with LLMs for Adaptive Grasp Policies

`2024-03-12` · University of Colorado Boulder

[Paper](https://arxiv.org/abs/2403.07832) · [Project page](https://deligrasp.github.io)

Combines object-property estimates with adaptive grasping.

**Method:** The LLM estimates mass, friction and stiffness and expresses adaptive grasp behavior as a program coupled to feedback control.

**Verification:** Grasping tests use estimated properties; successful handling does not establish exact physical-parameter recovery.

<a id="work-2310-13065"></a>
<!-- stage3-record: {"id": "2310.13065", "scope": "Adjacent", "section": 6} -->

#### Creative Robot Tool Use with Large Language Models

`2023-10-19` · Carnegie Mellon University; Google DeepMind

[Paper](https://arxiv.org/abs/2310.13065) · [Project page](https://creative-robotool.github.io/)

Programs robots to solve tasks with physical tools.

**Method:** Analysis, planning, parameter estimation and code generation produce Python programs for tasks whose constraints include tool-object interactions.

**Verification:** Execution tests assess tool use; physical reasoning claims should be tied to the tested objects and tasks.

<a id="work-2307-05973"></a>
<!-- stage3-record: {"id": "2307.05973", "scope": "Adjacent", "section": 6} -->

#### VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models

`2023-07-12` · Stanford University; University of Illinois Urbana-Champaign

[Paper](https://arxiv.org/abs/2307.05973) · [Project page](https://voxposer.github.io)

Builds spatial value maps for manipulation.

**Method:** Generated programs combine vision tools into spatial value maps; a model-based planner converts these maps into robot trajectories.

**Verification:** Recomputing maps from new observations differs from having the LLM revise its generated code.

### Experiments, measurement and discovery

<a id="work-2610-41717"></a>
<!-- stage3-record: {"id": "2610.41717", "scope": "Adjacent", "section": 6} -->

#### Evaluating Instrument-Centered AI Agents for Table-Top Science Experiments

`2026-10-30` · Massachusetts Institute of Technology; Boston College; University of Washington

[Paper](https://arxiv.org/abs/2610.41717) · [Code](https://github.com/caidish/instrMCP) · [Code](https://github.com/caidish/qdevbench)

Tests instrument-centered reasoning through programmable tools.

**Method:** instrMCP exposes instrument interfaces; q-devBench tests measurement, diagnosis and analysis in virtual tabletop experiments.

**Verification:** Virtual-instrument results are separate from real-device access, permissions and human approvals.

<a id="work-2610-41383"></a>
<!-- stage3-record: {"id": "2610.41383", "scope": "Adjacent", "section": 6} -->

#### BioAgent: Self-Directed Skill Acquisition and Capability Growth for Long-Horizon Laboratory Protocols

`2026-10-30` · Shanghai Jiao Tong University; University of Sussex

[Paper](https://arxiv.org/abs/2610.41383)

Adds laboratory skills through teaching and implementation.

**Method:** The robot identifies capability gaps in long protocols, then acquires and validates tools or skills with human teaching where needed.

**Verification:** Human teaching, implementation review and validation limit claims of autonomous skill discovery.

<a id="work-2610-37649"></a>
<!-- stage3-record: {"id": "2610.37649", "scope": "Core", "section": 6} -->

#### Can LLMs Uncover Hidden Physical Laws through Free Exploration?

`2026-10-27` · HKUST(GZ); ZJU; Alibaba Group; HKUST

[Bibliographic record](../README.md#paper-2610-37649) · [Paper](https://arxiv.org/abs/2610.37649) · [Project page](https://zhenyangcs.github.io/LongChang-website/) · [Code](https://github.com/EnVision-Research/LongChang)

Tests open-ended investigation of simulated physical laws.

**Method:** Agents design measurements and revise apparatus programs in MuJoCo worlds whose physical laws have been deliberately changed.

**Verification:** Discoveries concern modified simulated worlds, not new laws established in real physical experiments.

<a id="work-2610-35385"></a>
<!-- stage3-record: {"id": "2610.35385", "scope": "Adjacent", "section": 6} -->

#### EmbodiedLab: Benchmarking Embodied Agents That Act to Know

`2026-10-26` · HexaFuture; Tsinghua University; National University of Singapore; Peking University

[Paper](https://arxiv.org/abs/2610.35385) · [Code](https://github.com/HexaFuture/EmbodiedLab) · [Project page](https://hexafuture.ai/benchmarks/embodiedlab/)

Evaluates agents that act to obtain scientific evidence.

**Method:** Coding agents operate a simulated laboratory, read instruments and submit conclusions supported by their experiment traces.

**Verification:** Instrument readings and answer checks originate in simulation; this is not physical scientific discovery.

<a id="work-2610-23826"></a>
<!-- stage3-record: {"id": "2610.23826", "scope": "Adjacent", "section": 6} -->

#### Self-Building Labs

`2026-10-16` · University of Toronto; Vector Institute; Acceleration Consortium; University of Amsterdam; CIFAR; NVIDIA

[Paper](https://arxiv.org/abs/2610.23826) · [Project page](https://self-building-labs.github.io/)

Makes experimental apparatus part of the program.

**Method:** Agents design, configure and operate apparatus around scientific goals, extending beyond executing a fixed laboratory workflow.

**Verification:** Apparatus construction, configuration and experiment outcomes require separate evidence of physical execution.

<a id="work-2609-18435"></a>
<!-- stage3-record: {"id": "2609.18435", "scope": "Adjacent", "section": 6} -->

#### WetRobo: A Reproducible Robot Kit for Coding Agents in Biological Laboratories

`2026-09-16` · University of Tokyo; RIKEN; New York University; Google DeepMind; National Institute for Materials Science

[Paper](https://arxiv.org/abs/2609.18435) · [Code](https://github.com/tsudalab/WetRobo)

Provides a laboratory kit for coding-agent experimentation.

**Method:** Hardware, labware, demonstrations and skill files support program development and adjustment on a physical bench.

**Verification:** Human calibration, device preparation and skill teaching remain part of the setup.

<a id="work-2608-01690"></a>
<!-- stage3-record: {"id": "2608.01690", "scope": "Adjacent", "section": 6} -->

#### ProtoAct: Turning Wet-Lab Protocols into Embodied Robotic Actions

`2026-08-03` · East China University of Science and Technology; Ruijin Hospital, Shanghai Jiao Tong University School of Medicine; Shanghai AI Laboratory

[Paper](https://arxiv.org/abs/2608.01690)

Compiles laboratory protocols into robot actions.

**Method:** Protocols become checkable conditions and function sequences; retrieval and revision recover implicit steps before demonstration collection and policy training.

**Verification:** Protocol compilation, demonstration collection and learned-policy execution are separate validation stages.

<a id="work-2607-23045"></a>
<!-- stage3-record: {"id": "2607.23045", "scope": "Adjacent", "section": 6} -->

#### Stress-testing large language model agents in a robotic chemistry laboratory

`2026-07-25` · University of Science and Technology of China; Center for Scientific Intelligence Innovation, Hefei; University of Birmingham

[Paper](https://arxiv.org/abs/2607.23045)

Tests coding agents on laboratory workflows.

**Method:** Machine-readable laboratory skills let agents generate and submit procedures, with physical feedback available for selected revisions.

**Verification:** Large-scale executability judgments are not all hardware runs; one multi-round experiment includes human scientific judgment.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-bespoke-instrument"></a>
<!-- stage3-record: {"id": "bespoke-instrument", "scope": "Resource", "section": 6} -->

#### AI-designed and AI-implemented control systems for bespoke scientific instrumentation: application to scanning microscopy

`2026-05-08` · University of Cambridge

[Project page](https://pubs.rsc.org/en/content/articlelanding/2026/dd/d6dd00177g) · [Paper](https://www.repository.cam.ac.uk/items/cb2e6fef-94c4-4fe9-903a-aaa198da8f4f)

Develops instrument-control code with human oversight.

**Method:** Researchers and a general LLM build microscope controls and a digital sandbox, cross-check them with simulation and model review, then deploy after human approval.

**Verification:** Real SHeM imaging and diffraction validate the instrument; development, review and deployment remain human-led.

**Related:** [2. Simulator Construction](#section-2)

<a id="work-2509-25651"></a>
<!-- stage3-record: {"id": "2509.25651", "scope": "Adjacent", "section": 6} -->

#### AutoLabs: cognitive multi-agent systems with self-correction for autonomous chemical experimentation

`2025-09-30` · Pacific Northwest National Laboratory, Richland, Washington, WA, USA

[Paper](https://arxiv.org/abs/2509.25651) · [Code](https://github.com/pnnl/autolabs)

Produces checked, hardware-ready laboratory protocols.

**Method:** Multiple agents decompose experiment goals, calculate parameters and repair protocols for liquid-handling equipment.

**Verification:** Hardware-ready file validity is distinct from actually executing every protocol on equipment.

<a id="work-2509-24978"></a>
<!-- stage3-record: {"id": "2509.24978", "scope": "Core", "section": 6} -->

#### Agentic Exploration of Physics Models

`2025-09-29` · Max Planck Institute for the Science of Light, Staudtstraße 2, 91058 Erlangen, Germany; Department of Physics, Friedrich-Alexander Universität Erlangen-Nürnberg, Staudtstraße 5, 91058 Erlangen, Germany

[Paper](https://arxiv.org/abs/2509.24978) · [Code](https://github.com/MaxNaeg/SciExplorer)

Uses programmed numerical experiments to study physics.

**Method:** A multimodal agent selects numerical experiments, writes Python analysis and plotting code, and revises models from the resulting observations.

**Verification:** The experiments are numerical simulations, not real robot experiments or discoveries of new real-world laws.

<a id="work-chemagents"></a>
<!-- stage3-record: {"id": "chemagents", "scope": "Adjacent", "section": 6} -->

#### A Multiagent-Driven Robotic AI Chemist Enabling Autonomous Chemical Research On Demand

`2024-07-30` · Not reported

[Paper](https://doi.org/10.1021/jacs.4c17738)

Coordinates robot chemistry through generated API programs.

**Method:** Specialized agents translate experimental goals into robot API calls, review code, execute equipment operations and analyze the resulting data.

**Verification:** The preprint supports code generation and execution; journal full text was access-restricted, and researchers guide goals and design.

**Related:** [1. Embodied Harnesses](#section-1)

<a id="work-2304-05332"></a>
<!-- stage3-record: {"id": "2304.05332", "scope": "Adjacent", "section": 6} -->

#### Autonomous chemical research with large language models

`2023-04-11` · Not reported

[Paper](https://arxiv.org/abs/2304.05332) · [Code](https://github.com/gomesgroup/coscientist)

Connects language reasoning to automated chemistry.

**Method:** An LLM combines literature retrieval, Python calculations and experiment-device APIs to plan and execute chemistry procedures.

**Verification:** Physical chemistry demonstrations use human-configured equipment; the simplified release is not the full deployed system.

<a id="work-xray-scientist"></a>
<!-- stage3-record: {"id": "xray-scientist", "scope": "Adjacent", "section": 6} -->

#### An agentic artificially intelligent X-ray scientist

`First-public date not established` · Stanford University; SLAC National Accelerator Laboratory; University of Texas at Austin; Carnegie Mellon University; Northeastern University; Howard University; Massachusetts Institute of Technology

[Paper](https://www.nature.com/articles/s42256-026-01261-5) · [Code](https://github.com/zhantaochen/llm4xray)

Connects an experimental agent to X-ray instruments.

**Method:** Python and MCP interfaces support workflow preparation in a virtual beamline and measurement-guided single-crystal orientation on real equipment.

**Verification:** People relay real instrument commands as a fixed intermediary; the virtual beamline is researcher-built.

**Related:** [1. Embodied Harnesses](#section-1)

### Physical design, fabrication and validation

<a id="work-2611-13344"></a>
<!-- stage3-record: {"id": "2611.13344", "scope": "Core", "section": 6} -->

#### PneuGen: Task-Driven Agentic Co-Design of Soft Pneumatic Robots

`2026-11-09` · Oxford Robotics Institute, University of Oxford

[Bibliographic record](../README.md#paper-2611-13344) · [Paper](https://arxiv.org/abs/2611.13344)

Iteratively co-designs soft pneumatic robot geometry and actuation through executable design programs and simulation critique.

**Method:** A designer selects parametric modules using fitted response priors; typed programs pass structural checks, generate CAD and tetrahedral meshes, and run SOFA finite-element simulation. A critic uses spatial diagnostics to revise geometry and actuation.

**Verification:** Budgeted grasping and 2D/3D shape-matching comparisons, critic/prior ablations, and fabricated robot demonstrations. Physical demonstrations validate selected designs; real-hardware feedback is not part of the reported optimization loop.

**Related:** [2. Simulator Construction](#section-2) · [3. Simulator Quality Evaluation](#section-3) · [5. Training and Capability Improvement](#section-5)

<a id="work-2611-08175"></a>
<!-- stage3-record: {"id": "2611.08175", "scope": "Core", "section": 6} -->

#### PCBRouteAgent: How Close Are LLM Agents to Becoming PCB Routing Engineers?

`2026-11-05` · University of Texas at Dallas; Texas Instruments; Iowa State University

[Bibliographic record](../README.md#paper-2611-08175) · [Paper](https://arxiv.org/abs/2611.08175) · [Project page](https://chip-ai-agent.github.io/research/pcbrouteagent)

Revises PCB routing guides from native KiCad execution feedback to improve board connectivity.

**Method:** A multimodal global planner combines fixed initial board images with updated obstacle and connectivity reports, then patches route ordering, corridors and layer transitions. KiCad performs detailed geometric routing and bounded recovery, preserving accepted traces.

**Verification:** Evaluates 247 PCBWorld boards using connectivity and zero error-level design-rule violations, with replanning comparisons. Some D3-B results include recovery. No fabricated-board tests, signal-integrity validation or complete manufacturing qualification are reported.

**Related:** [1. Embodied Harnesses](#section-1) · [3. Simulator Quality Evaluation](#section-3) · [5. Training and Capability Improvement](#section-5)

<a id="work-2610-31651"></a>
<!-- stage3-record: {"id": "2610.31651", "scope": "Core", "section": 6} -->

#### BrickWright: Agentic Creation of Physically Feasible Brick Builds

`2026-10-22` · Carnegie Mellon University; Independent Researcher; Stanford University

[Bibliographic record](../README.md#paper-2610-31651) · [Paper](https://arxiv.org/abs/2610.31651) · [Code](https://github.com/avalovelace1/brickwright) · [Project page](https://avalovelace1.github.io/brickwright/)

Checks programmatic brick designs for structural feasibility.

**Method:** Typed connections, collision and unsupported-part checks combine with rendered inspection to repair Python brick models.

**Verification:** The feasibility definition covers connectivity, collision and unsupported parts, not load stability or executable assembly order.

<a id="work-2610-17881"></a>
<!-- stage3-record: {"id": "2610.17881", "scope": "Core", "section": 6} -->

#### Agentic Robot Creation through Generation, Verification, and Revision

`2026-10-13` · ShanghaiTech University

[Bibliographic record](../README.md#paper-2610-17881) · [Paper](https://arxiv.org/abs/2610.17881) · [Project page](https://roboforge-project.github.io/)

Co-develops robot bodies and executable behavior.

**Method:** RoboForge revises procedural reference motions and rewards from simulated body, joint and contact feedback, then deploys learned behavior.

**Verification:** Physical Gorilla demonstrations include human mechanical corrections before fabrication.

**Related:** [5. Training and Capability Improvement](#section-5)

<a id="work-2609-08220"></a>
<!-- stage3-record: {"id": "2609.08220", "scope": "Core", "section": 6} -->

#### Bridging Language and Physics: Automated Design of Continuum Robots with Large Language Models

`2026-09-08` · University of Science and Technology of China; University of North Carolina at Chapel Hill; University of Central Florida

[Bibliographic record](../README.md#paper-2609-08220) · [Paper](https://arxiv.org/abs/2609.08220) · [Code](https://github.com/UNITES-Lab/AID-SR)

Uses physics feedback to improve continuum-robot designs.

**Method:** An agent generates MuJoCo XML morphology, observes simulated physical behavior and uses structured diagnostics to revise the design.

**Verification:** XML validity, stability, downstream task results and sim-real consistency are separate checks.

<a id="work-2605-17448"></a>
<!-- stage3-record: {"id": "2605.17448", "scope": "Core", "section": 6} -->

#### Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback

`2026-05-17` · Seoul National University; OneLineAI; Sungkyunkwan University; Ewha Womans University

[Bibliographic record](../README.md#paper-2605-17448) · [Paper](https://arxiv.org/abs/2605.17448)

Uses visual and finite-element feedback to improve CAD.

**Method:** A coding agent modifies CadQuery assemblies using multiview renders and finite-element reports under engineering constraints.

**Verification:** Hephaestus-CCX tests engineering simulation; some gains involve checker-contract repair, and fabrication is not established.

**Related:** [5. Training and Capability Improvement](#section-5)

<a id="work-2408-14307"></a>
<!-- stage3-record: {"id": "2408.14307", "scope": "Adjacent", "section": 6} -->

#### LLM-3D Print: Large Language Models To Monitor and Control 3D Printing

`2024-08-26` · Carnegie Mellon University

[Paper](https://arxiv.org/abs/2408.14307) · [Code](https://github.com/BaratiLab/LLM-3D-Print-Large-Language-Models-To-Monitor-and-Control-3D-Printing)

Closes the loop between print images and printer control.

**Method:** A VLM examines layer images, queries printer parameters and invokes control tools to correct the printing process.

**Verification:** Real printer images and parameters support diagnosis; people prepare device documents and cross-platform configuration.

<a id="work-ai-cad"></a>
<!-- stage3-record: {"id": "ai-cad", "scope": "Resource", "section": 6} -->

#### ai-cad

`First-public date not established` · Not reported

[Code](https://github.com/BorjaLL/ai-cad) · [Results](https://github.com/BorjaLL/ai-cad/blob/1ef2bf72de799006d069498d3ee146dae2e4f075/data/fits-measured.json)

Connects parametric CAD to manual print-fit feedback.

**Method:** Parametric design programs are iterated with photographs and human judgments from manufactured parts.

**Verification:** People perform and judge fitting; nominal clearance is not an automatically measured precision result.

<a id="work-agentic-fdm-printing"></a>
<!-- stage3-record: {"id": "agentic-fdm-printing", "scope": "Resource", "section": 6} -->

#### Agentic AI for FDM 3D Printing Process Control

`First-public date not established` · Not reported

[Code](https://github.com/jabarkle/AgenticAI-FDM-Printing) · [Code](https://github.com/BaratiLab/LLM-3D-Print-Large-Language-Models-To-Monitor-and-Control-3D-Printing)

Documents a reused agentic 3D-printing workflow.

**Method:** The community project reuses image inspection and G-code control to compare how prompts affect diagnosis, parameter correction and recovery.

**Verification:** Seven runs are documented; one image-processing failure produced hallucinated scoring, explicitly noted upstream.

### Cross-section reading

- [One Policy for 100 Household Tasks: Our Solution for the 2026 BEHAVIOR Challenge](#work-2611-14432)
- [Embodied First Exam](#work-2611-12177)
- [World In-Context Learning for Agentic Robot Manipulation](#work-2611-12885)
- [Agentic discrete-event simulation for manufacturing system design: an open 3D simulator, a benchmark and an industrial case](#work-2611-10602)
- [Open-HumanWAM: An Open Recipe for Scaling Human and Robot Experience for Embodied Foundation Models](#work-2611-06817)
- [Closing the Dynamics Gap through Self-Directed Robotic Interaction](#work-2611-02691)
- [WorldSketch: Sketching World Models for Zero-Shot Mobile Manipulation](#work-2611-00513)
- [LabWorld: Learning Interactive 4D Worlds for Scientific Experimentation](#work-2610-36592)
- [D-World: An Explicit World-Language-Action Model with Recursive Self-Improvement under Dual Control](#work-2610-17114)
- [What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery](#work-2609-31760)
- [Parametric CAD Bench v3: Evaluating Agentic Parametric CAD Authoring from Text and Engineering Drawings](#work-2611-02659)
- [GIF: Agentic Generation of Interactive and Functional Object Compositions for Robot Learning](#work-2609-05927)
- [LabRobFail: A Benchmark for Robotic Failure Analysis in Chemical Self-driving Laboratory](#work-2607-23704)
- [ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](#work-2606-19980)
- [ArtiCAD: Articulated CAD Assembly Design via Multi-Agent Code Generation](#work-2604-10992)
- [Eurekaverse: Environment Curriculum Generation via Large Language Models](#work-2411-01775)
- [Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model](#work-2410-13882)
- [Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models](#work-2310-18308)
- [GenSim: Generating Robotic Simulation Tasks via Large Language Models](#work-2310-01361)

[Back to the research map](#research-map)
