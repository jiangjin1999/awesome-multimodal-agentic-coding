# Simulator Quality Evaluation: A Fidelity Ladder

**English** · [简体中文](simulator-evaluation.zh-CN.md)

This page reorganizes the works related to [3.3 Simulator quality evaluation](../README.md#s3-3) by **fidelity level**. It answers one question: **which property of a simulated world does a work actually check, and how far can its conclusion be trusted?** Method and validation details for each work are in [Section 3 of the Stage 3 guide](README.md#section-3).

## Contents

- [0. Reading guide](#0-reading-guide)
- [1. L0a Semantic fidelity](#1-l0a-semantic-fidelity)
- [2. L0b Visual and reconstruction fidelity](#2-l0b-visual-and-reconstruction-fidelity)
- [3. L1 Static physical plausibility](#3-l1-static-physical-plausibility)
- [4. L2 Interaction plausibility](#4-l2-interaction-plausibility)
- [5. L3 Dynamics fidelity](#5-l3-dynamics-fidelity)
  - [5.1 L3a Dynamics: looks right](#51-l3a-dynamics-looks-right)
  - [5.2 L3b Dynamics: truly simulated](#52-l3b-dynamics-truly-simulated)
  - [5.3 L3c Dynamics: numerically accurate](#53-l3c-dynamics-numerically-accurate)
- [6. L4 Sim-to-real predictivity](#6-l4-sim-to-real-predictivity)
- [7. Cross-cutting observations](#7-cross-cutting-observations)
- [8. Terminology sources](#8-terminology-sources)

---

## 0. Reading guide

### Three questions

| Question | Name | Purpose |
|---|---|---|
| **What is checked** | Fidelity level (main axis) | Which property of the world the work checks; this page is organized by it |
| **Why trust it** | Evidence attributes (tags) | Where the reference comes from, who sets the criteria, how evidence is obtained |
| **Who is checked** | Evaluation setting (tags) | How much the agent is responsible for, and what role the work itself plays |

### Levels at a glance

| No. | Level | Formal term | Core question | State of the world |
|---|---|---|---|---|
| L0a | Semantic fidelity | Semantic Fidelity | Does it do what the requirements say? | Static |
| L0b | Visual / reconstruction fidelity | Visual / Reconstruction Fidelity | Does it look the same as the reference? | Static |
| L1 | Static physical plausibility | Static Physical Plausibility | Left at rest, does it stand stably and can people get through? | A frozen moment |
| L2 | Interaction plausibility | Interaction Plausibility / Functional Fidelity | Push it or open it: does it respond correctly? | Under external actions |
| L3a | Dynamics: looks right | Motion Fidelity | Does the motion match the reference video? (Only frames and trajectories are compared, so hand-written animation can also score well.) | Evolving over time |
| L3b | Dynamics: truly simulated | Model Verification | Rerun under changed conditions (a steeper ramp, a heavier ball): does the result change correctly? | Evolving over time |
| L3c | Dynamics: numerically accurate | Validation & System Identification | Do parameters such as mass and friction match reality? Given the first few seconds, can it predict what follows? | Evolving over time |
| L4 | Sim-to-real predictivity | Sim-to-Real Predictivity | Used for evaluation or training, do the conclusions hold in the real world? | Put to use |

```
  Requirement-driven: L0a semantic ──┐
                                     ├─→ L1 static → L2 interaction → L3 dynamics → L4 downstream
  Reference-driven:   L0b visual  ───┘   (at rest)    (poked)          (evolving)     (put to use)
```

- L0a and L0b are **parallel starting points**: the former is referenced to requirements (user instructions or commonsense priors), the latter to an image, video or target scene.
- Each level checks **a different failure mode**; the levels are not a cumulative score. Passing a higher level does not imply passing a lower one: a controller can compensate for world errors, so L4 succeeds while L3 is wrong.

### Placement rules

- Each work is placed at the level of its **main claimed contribution**; other levels it touches are listed under "Also".
- † marks evaluators, works whose main contribution is an **evaluation tool**; they are placed by the property they evaluate.
- Work names link to entries in the [full research map](../README.md#contents); "guide" links to the detailed note in the Stage 3 guide.

### Tags

| Tag | Values | Meaning |
|---|---|---|
| **Reference source** | Text requirement → commonsense prior → synthetic ground truth → real observation → real-robot result | Further right is closer to the real world |
| **Criteria source** | Unified protocol → per-task contract → real-recording comparison → evaluator-generated per scene | Left is more comparable and reproducible; right adapts to each scene but the evaluator itself must be validated |
| **Evidence** | Rendering plus judging → native-state reading → active intervention → replay or closed-loop execution → parameter identification | From looking at the artifact to probing it |
| **Agent freedom** | Parameters only → write within a given framework → write a program from scratch | More freedom means more levels need checking |
| **Role** | Evaluator / capability benchmark / acceptance protocol | Evaluators are validated against human judgments; benchmarks use quality metrics to assess agents; acceptance protocols ask whether a simulator can be trusted |

---

## 1. L0a Semantic fidelity

**Does it do what the requirements say?**

- **How:** Decompose requirements into checkable constraints (objects, attributes, counts, relative positions) and verify each. Requirements come from **explicit instructions** ("the bed against the wall, a nightstand on each side") and from **implicit expectations** users do not write (spatial commonsense derived from data).
- **Catches:** Missing objects, wrong relations, implausible scale, layouts that violate commonsense.
- **Cannot show:** Any physical property. A room that meets every constraint may consist of immovable single meshes.

| Work | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|
| [SceneEval](../README.md#paper-2503-14756) † · [guide](README.md#work-2503-14756) | L1 | Text plus implicit commonsense | — | Evaluator |
| [Apples on the Table? (LEGO-Eval)](../README.md#paper-2511-03001) † · [guide](README.md#work-2511-03001) | — | Text | — | Evaluator |
| [SceneCritic](../README.md#paper-2604-13035) † · [guide](README.md#work-2604-13035) | L1 | Commonsense from data | — | Evaluator |
| [Code4Scene](../README.md#paper-2609-36777) · [guide](README.md#work-2609-36777) | L1 | Task requirements | Writes programs | Benchmark |

---

## 2. L0b Visual and reconstruction fidelity

**Does it look the same as the reference?**

- **How:** Given a target image, video, scene or engineering drawing, the agent reconstructs or edits with code, and the two are compared. Two kinds of evidence differ:
  - **Rendered similarity** (LPIPS, DINO, masks): "does it look the same";
  - **Native structural agreement** (3D distances, CAD features, scene graphs): "is the structure right", closer to being simulation-ready.
- **Catches:** Deviations in appearance, position, shape and structure.
- **Cannot show:** Whether colliders, masses or joints are correct. A visually identical reconstruction may fall apart on contact.

| Work | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|
| [IR3D-Bench](../README.md#paper-2506-23329) · [guide](README.md#work-2506-23329) | L0a | Images | Writes programs | Benchmark |
| [BlenderGym](../README.md#paper-2504-01786) · [guide](README.md#work-2504-01786) | — | Target scenes | Edits programs | Benchmark |
| [BlenderWorld](../README.md#paper-system-blenderworld) · [guide](README.md#work-system-blenderworld) | — | Real references | Writes programs | Benchmark |
| [Parametric CAD Bench v3](../README.md#paper-2611-02659) · [guide](README.md#work-2611-02659) | — | Text plus engineering drawings | Writes programs | Benchmark |
| [BVB](../README.md#paper-2609-15478) · [guide](README.md#work-2609-15478) | L3a | Video | Writes programs | Benchmark |
| [Frontier3DBench](../README.md#paper-2611-09017) · [guide](README.md#work-2611-09017) | L2 | Task requirements | Writes programs | Benchmark |

---

## 3. L1 Static physical plausibility

**Left at rest, does it stand stably and can people get through?**

- **Why "static":** Only a frozen moment of the scene is examined; time does not advance and no dynamics run. The checks are **geometric computations**:
  - **Physical feasibility:** collision (mesh intersection), support (resting on a surface), bounds;
  - **Usability:** reachability (distance and reach), navigability (floor path planning), operating clearance.
- **Catches:** Floating objects, interpenetration, blocked paths, unreachable targets. Cheap and interpretable, it filters scenes between L0 and L2.
- **Cannot show:** Whether things behave correctly once moving. A scene that passes every static check may still slide apart under zero friction or tip over with a wrong center of mass.

| Work | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|
| [GREP](../README.md#paper-2611-05802) † · [guide](README.md#work-2611-05802) | L0a | Principles plus the specific scene | — | Evaluator |
| [SceneTeract](../README.md#paper-2603-29798) † · [guide](README.md#work-2603-29798) | — | Activity plus user conditions | — | Evaluator (also used for training) |

GREP's evaluation agent actively chooses views and calls geometric tools; that is a capability of the **evaluator**, not evidence of a repair loop in the constructing agent. SceneTeract adds user conditions and asks whether a scene is usable *for this person*.

---

## 4. L2 Interaction plausibility

**Interaction plausibility / functional fidelity · Push it or open it: does it respond correctly?**

- **How:** Apply actions to the world and check the response, moving from looking at the artifact to **probing** it. Two kinds:
  - **(a) Physical interaction response:** whether pushing, opening or surface probing produces plausible physics;
  - **(b) State contract:** whether program state changes as specified after an action, for example by reading coordinates, velocities or flags against hidden assertions.
- **Where criteria come from:** a unified protocol (the same actions for every scene), per-task contracts (hidden requirements written by benchmark authors), or real recordings (step-by-step comparison with footage).
- **Catches:** Objects that cannot be pushed, doors that do not open, state that does not change, correct visuals with wrong logic.
- **Cannot show:** Whether parameters are calibrated. A door that opens with the right state may still have the wrong mass and damping.

| Work | Type | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|---|
| [ScIntBench](../README.md#paper-2610-37326) · [guide](README.md#work-2610-37326) | (a) | L0a, L1 | Unified interaction protocol | — | Benchmark (of scene generators) |
| [WorldCoder-Bench](../README.md#paper-2606-01869) · [guide](README.md#work-2606-01869) | (b) | L3b | Natural language plus hidden contracts | Writes programs (single shot) | Benchmark |
| [Lab2Sim](../README.md#paper-2611-02928) | (b) | — | Real experiment recordings | Writes programs | Method (with independent verification) |

WorldCoder-Bench's StateProbe records state snapshots before and after each scripted action (including physics steps) and checks the delta with hidden assertions under numerical tolerances, including invariants such as conservation laws; it therefore also touches L3b.

---

## 5. L3 Dynamics fidelity

**Physical / dynamics fidelity · Left to evolve on its own, is the process right?**

Take "a ball rolls down a ramp and hits a box". This level asks three questions of increasing difficulty:

| Sub-question | What it asks | How | What can fool it |
|---|---|---|---|
| **L3a Dynamics: looks right** | Does the motion match the reference video? | Frame-wise positions, optical flow, masks, or VLM judging | Hand-written keyframe animation |
| **L3b Dynamics: truly simulated** | Rerun under changed conditions (a steeper ramp, a heavier ball): does the result change correctly? | Counterfactual interventions, physical assertions, conservation checks | Hard to fool, provided interventions are actually run |
| **L3c Dynamics: numerically accurate** | Do parameters such as mass and friction match reality? Given the first few seconds, can it predict what follows? | Comparison with independently measured parameters; held-out future periods | Compensating parameters can fool trajectories but not extrapolation or real measurements |

**What "the right mechanism" means depends on what the agent is responsible for.** With an existing engine (Blender, MuJoCo), the engine supplies the physical laws; the agent must pose the right problem and actually let the engine solve it. When the agent writes its own solver, the laws are its responsibility too. Agent freedom forms a spectrum:

```
Parameters only  →  Write within a framework  →  Write from scratch
Δynamics            WorldSolver                   PhysCodeGym, MPMWorlds
```

More freedom means more ways to fail: bypassing the engine with scripted animation, choosing the wrong physical model (cloth as a rigid body), misconfiguring numerics (a large time step causing tunneling), or writing wrong update rules.

### 5.1 L3a Dynamics: looks right

**Motion fidelity · Does the motion match the reference video?** Correct motion that is *acted out* by animation and correct motion that is *computed* by physics can score the same here.

| Work | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|
| [ExeWorldBench](../README.md#paper-2610-15166) · [guide](README.md#work-2610-15166) | L2 | Visual references or goals | Writes programs | Benchmark |
| [4DCodeBench](../README.md#paper-2610-03715) · [guide](README.md#work-2610-03715) | L0b | Reference videos (synthetic and real) | Writes programs; keyframes allowed | Benchmark |
| [VisPhyWorld](../README.md#paper-2602-13294) · [guide](README.md#work-2602-13294) | L0b | Video | Writes programs | Benchmark |
| [Physics-Inspired Animations](../README.md#paper-2602-10840) · [guide](README.md#work-2602-10840) | — | Physics concept descriptions | Writes programs | Benchmark (also used for training) |
| [PhyRubric](../README.md#paper-2611-13576) † · [guide](README.md#work-2611-13576) | — | Pre-specified rubrics | N/A (evaluates generated videos) | Evaluator (adjacent) |
| [Latent Prediction Error and Physical Surprise](../README.md#paper-2611-01815) | — | Physical violations vs. appearance changes | N/A (evaluates video world models) | Diagnostic study (adjacent) |

### 5.2 L3b Dynamics: truly simulated

**Model verification · Rerun under changed conditions: does the result change correctly?** Counterfactual intervention is the key tool separating L3a from L3b: change the ramp angle or the ball's mass and rerun; a real simulation responds, a scripted animation does not.

| Work | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|
| [PhysCodeGym](../README.md#paper-2610-17288) · [guide](README.md#work-2610-17288) | L0b, L3a | Real videos | Writes programs | Benchmark |
| [PhysCodeBench](../README.md#paper-2604-23580) · [guide](README.md#work-2604-23580) | L3a | Text-described physical phenomena | Writes programs | Benchmark (also proposes a method) |
| [WorldSolver](../README.md#paper-2610-08720) · [guide](README.md#work-2610-08720) | — | Classical physics problems | Writes a solver within a given framework | Benchmark |

### 5.3 L3c Dynamics: numerically accurate

**Validation and system identification · Do parameters match reality? Given the first few seconds, can it predict what follows?** Many parameter sets yield similar trajectories (non-identifiability), so independently measured references or held-out future periods are needed.

| Work | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|
| [IRIS](../README.md#paper-2603-16432) · [guide](README.md#work-2603-16432) | — | **Real measurements** with uncertainty | Any method | Benchmark |
| [Δynamics](../README.md#paper-2605-20576) · [guide](README.md#work-2605-20576) | L3a | Synthetic ground truth; pseudo-labels for real videos | Parameters only | Method plus evaluation |
| [MPMWorlds](../README.md#paper-2606-01538) · [guide](README.md#work-2606-01538) | L3a | Synthetic MPM data, evaluated in video space only | Writes a full solver (best-of-N sampling) | Benchmark (also trains a model) |

MPMWorlds extrapolates in video space only, without reading particle states or parameters, so its evidence is weaker than IRIS's independent physical measurements.

---

## 6. L4 Sim-to-real predictivity

**Used for evaluation or training, do the conclusions hold in the real world?**

- **How:** Instead of the world itself, check whether **conclusions drawn in it** transfer. Two kinds:
  - **(a) Evaluation proxy:** run the same policies in simulation and on real robots and compare performance and rankings (for example Pearson correlation and MMRV);
  - **(b) Scene–behavior pair:** whether a world reconstructed from real data, together with its behavior program, completes the real task.
- **Distinctive difficulty: error attribution.** Controllers may compensate for world errors. Hold the controller fixed, use a known-working reference environment, and cross-execute.
- **Catches:** Evaluation or training conclusions that fail to transfer.

| Work | Type | Also | Reference | Agent freedom | Role |
|---|---|---|---|---|---|
| [Evaluating Real-World Robot Manipulation Policies in Simulation (SIMPLER)](../README.md#paper-2405-05941) · [guide](README.md#work-2405-05941) | (a) | — | Paired real-robot runs | — | Acceptance protocol |
| [YUBI-Real2Sim](../README.md#paper-2610-17521) · [guide](README.md#work-2610-17521) | (a) | L0b | Paired real-robot runs | — | Acceptance protocol |
| [Video2World](../README.md#paper-2610-04432) · [guide](README.md#work-2610-04432) | (b) | L0b, L3 | Real demonstration videos | Writes programs (scene and behavior) | Benchmark |
| [Real2Sim Benchmark](../README.md#paper-real2sim-benchmark) · [guide](README.md#work-real2sim-benchmark) | (b) | L0b, L3 | Real clips | Writes programs | Benchmark |

YUBI-Real2Sim varies only background artifacts while fixing objects and physics, and finds that visual scores do not reliably predict policy-ranking failures: L0b cannot substitute for L4.

---

## 7. Cross-cutting observations

1. **The levels are not strictly cumulative.** Passing a higher level does not imply passing a lower one: an L4 task can succeed with wrong L3 parameters, and an L2 contract can hold despite L1 interpenetration. Each level corresponds to a different failure mode.
2. **Higher levels tend to use real-world references, but not always.** IRIS already uses real measurements at L3, and Lab2Sim uses real recordings at L2.
3. **Coverage is uneven.** Work concentrates in L0 and L3a; few works check mechanisms, parameters or downstream usefulness. Evaluators (†) appear only in L0, L1 and L3a; L2 to L4 have no dedicated evaluation tools yet.
4. **Open question: which lower-level checks predict higher-level failures?** YUBI-Real2Sim provides a counterexample: visual quality does not predict policy rankings. How to calibrate acceptance thresholds to real-world errors and their uncertainty remains open.

---

## 8. Terminology sources

The level names borrow existing terms from the literature below. Combining them into one ladder is this repository's synthesis, not an established unified taxonomy.

- **Fidelity in training simulation and VR:** Alexander et al., [From Gaming to Training: A Review of Studies on Fidelity, Immersion, Presence, and Buy-in](https://www.cs.uky.edu/~sgware/reading/papers/alexander2005gaming.pdf) (2005), distinguishes physical, functional and psychological fidelity; [The Interaction Fidelity Model](https://arxiv.org/abs/2402.16665) distinguishes presentational, behavioral, physical and scenario fidelity.
- **V&V in computational simulation:** Roache's distinction—verification is "solving the equations right", validation is "solving the right equations", which requires comparison with experimental data. See [NAFEMS: Verification and Validation](https://www.nafems.org/training/learning-hub/introduction-to-simulation-credibility/verification-and-validation) and the V&V framework of Roy and Oberkampf. These correspond to L3b and L3c.
- **Evaluation terms in scene generation and embodied simulation:** [3D Scene Generation: A Survey](https://arxiv.org/abs/2505.05474) (semantic consistency, physical plausibility); [3D Generation for Embodied AI and Robotic Simulation: A Survey](https://arxiv.org/abs/2604.26509) (collision rate, reachability, stable-object ratio); [SceneEval](https://arxiv.org/abs/2503.14756) (fidelity and plausibility).
- **Sim–real agreement:** [SIMPLER](https://arxiv.org/abs/2405.05941) (Pearson correlation and MMRV); [BWM](https://arxiv.org/abs/2607.29302) (policy-ranking fidelity).
