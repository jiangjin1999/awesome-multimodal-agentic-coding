# Simulator Quality Evaluation: A Fidelity Ladder

**English** · [简体中文](simulator-evaluation.zh-CN.md)

Works from [3.3 Simulator quality evaluation](../README.md#s3-3), organized by fidelity level; method details are in the [Stage 3 guide](README.md#section-3).

## Contents

- [Overview](#overview)
- [L0a Semantic fidelity](#l0a-semantic-fidelity)
- [L0b Visual and reconstruction fidelity](#l0b-visual-and-reconstruction-fidelity)
- [L1 Static physical plausibility](#l1-static-physical-plausibility)
- [L2 Interaction plausibility](#l2-interaction-plausibility)
- [L3 Dynamics fidelity](#l3-dynamics-fidelity)
- [L4 Sim-to-real predictivity](#l4-sim-to-real-predictivity)
- [Observations](#observations)
- [Terminology sources](#terminology-sources)

## Overview

| No. | Level | Core question | Formal term |
|---|---|---|---|
| L0a | Semantic fidelity | Does it do what the requirements say? | Semantic Fidelity |
| L0b | Visual / reconstruction fidelity | Does it look the same as the reference? | Visual / Reconstruction Fidelity |
| L1 | Static physical plausibility | Left at rest, does it stand stably and can people get through? | Static Physical Plausibility |
| L2 | Interaction plausibility | Push it or open it: does it respond correctly? | Interaction Plausibility |
| L3a | Dynamics: looks right | Does the motion match the reference video? | Motion Fidelity |
| L3b | Dynamics: truly simulated | Rerun under changed conditions: does the result change correctly? | Model Verification |
| L3c | Dynamics: numerically accurate | Do parameters match reality? Given the first seconds, can it predict the rest? | Validation & System Identification |
| L4 | Sim-to-real predictivity | Used for evaluation or training, do the conclusions hold in the real world? | Sim-to-Real Predictivity |

```
  Requirement-driven: L0a semantic ──┐
                                     ├─→ L1 static → L2 interaction → L3 dynamics → L4 downstream
  Reference-driven:   L0b visual  ───┘   (at rest)    (poked)          (evolving)     (put to use)
```

L0a and L0b are parallel starting points; each level checks a different failure mode rather than adding up to a score. † marks evaluators (works whose main contribution is an evaluation tool).

## L0a Semantic fidelity

**Checks:** Decompose written requirements and commonsense expectations into constraints on objects, attributes and relations, and verify each.
**Limit:** Says nothing about physical properties.

| Work | What it checks |
|---|---|
| [SceneEval](../README.md#paper-2503-14756) † | Objects, attributes and relations in the text, plus implicit support, collision and navigability |
| [Apples on the Table? (LEGO-Eval)](../README.md#paper-2511-03001) † | Fine-grained constraints from the description, verified one by one with tools |
| [SceneCritic](../README.md#paper-2604-13035) † | Symbolic scenes checked for scale, orientation and overlap against spatial commonsense from data |
| [Code4Scene](../README.md#paper-2609-36777) | Requirement satisfaction, completeness and static validity of agent-built and edited 3D scenes |

## L0b Visual and reconstruction fidelity

**Checks:** Compare against a target image, video, scene or drawing; rendered similarity asks "does it look alike", native geometry and structure ask "is the structure right".
**Limit:** Looking identical does not make colliders, masses or joints correct.

| Work | What it checks |
|---|---|
| [IR3D-Bench](../README.md#paper-2506-23329) | Localization, counts, spatial relations and appearance after reconstructing images as programmatic scenes |
| [BlenderGym](../README.md#paper-2504-01786) | Blender program edits that match a target, scored by multi-view image metrics and 3D distances |
| [BlenderWorld](../README.md#paper-system-blenderworld) | 3D creation from real references, using re-rendering and native scene checks |
| [Parametric CAD Bench v3](../README.md#paper-2611-02659) | Native parametric geometry against engineering specifications, not renderings |
| [BVB](../README.md#paper-2609-15478) | Video content rebuilt as Blender programs, by reconstruction similarity and retained QA information |
| [Frontier3DBench](../README.md#paper-2611-09017) | Object, scene and interactive-world creation across Blender and Unreal |

## L1 Static physical plausibility

**Checks:** Without running physics, use geometry to check interpenetration, support, reachability and navigability.
**Limit:** Fine at rest does not mean correct in motion.

| Work | What it checks |
|---|---|
| [GREP](../README.md#paper-2611-05802) † | Room-specific checks covering physical validity, visual harmony and everyday usability |
| [SceneTeract](../README.md#paper-2603-29798) † | Whether an activity is feasible for a given user (for example, a wheelchair user) |

## L2 Interaction plausibility

**Checks:** Apply actions and see whether the physical response is plausible or program state changes as specified.
**Limit:** A door that opens with the right state may still have the wrong mass and damping.

| Work | What it checks |
|---|---|
| [ScIntBench](../README.md#paper-2610-37326) | Standard pushes, openings and surface probes on generated scenes |
| [WorldCoder-Bench](../README.md#paper-2606-01869) | Runtime state after scripted actions, against hidden assertions with tolerances (including conservation laws) |
| [Lab2Sim](../README.md#paper-2611-02928) | Step-by-step replay of web experiments, compared with real experiment footage |

## L3 Dynamics fidelity

Take "a ball rolls down a ramp and hits a box". The three sub-questions get progressively harder:

| Sub-question | How | What can fool it |
|---|---|---|
| **L3a Dynamics: looks right** | Frame-wise positions, optical flow, masks, or VLM judging | Hand-written keyframe animation |
| **L3b Dynamics: truly simulated** | Rerun with changed conditions (a steeper ramp, a heavier ball); physical assertions and conservation checks | Hard to fool, provided interventions are actually run |
| **L3c Dynamics: numerically accurate** | Compare with independently measured parameters; predict what follows from the first seconds | Compensating parameters fool trajectories, not extrapolation or measurements |

With an existing engine, the engine supplies the physical laws, so the check is whether the agent actually let the engine compute and chose the right model; when the agent writes its own solver, the laws themselves must be checked too.

### L3a Dynamics: looks right

| Work | What it checks |
|---|---|
| [ExeWorldBench](../README.md#paper-2610-15166) | Code-built runnable 3D worlds, judged mainly from rendered frames on structure, motion and causality |
| [4DCodeBench](../README.md#paper-2610-03715) | Executable 4D scenes rebuilt from reference videos, compared on appearance, motion and geometry; keyframes allowed |
| [VisPhyWorld](../README.md#paper-2602-13294) | Physical videos rewritten as simulator code, compared on frames and motion |
| [Physics-Inspired Animations](../README.md#paper-2602-10840) | Animation code depicting physical phenomena, checked by a VLM |
| [PhyRubric](../README.md#paper-2611-13576) † | Physical-commonsense errors in generated videos, diagnosed with pre-specified rubrics |
| [Latent Prediction Error and Physical Surprise](../README.md#paper-2611-01815) | Whether video world models' prediction error separates physical violations from appearance changes |

### L3b Dynamics: truly simulated

| Work | What it checks |
|---|---|
| [PhysCodeGym](../README.md#paper-2610-17288) | Motion must come from physical mechanisms; scenes are re-simulated after counterfactual interventions |
| [PhysCodeBench](../README.md#paper-2604-23580) | Expert physical assertions and conservation checks beyond visual metrics |
| [WorldSolver](../README.md#paper-2610-08720) | Solver code written within a given scene and framework, checked for execution, events and physical behavior |

### L3c Dynamics: numerically accurate

| Work | What it checks |
|---|---|
| [IRIS](../README.md#paper-2603-16432) | Recovered parameters against independent measurements with uncertainty, plus identifiability and extrapolation |
| [Δynamics](../README.md#paper-2605-20576) | Parameter configurations replayed by an engine, with parameter error where ground truth exists |
| [MPMWorlds](../README.md#paper-2606-01538) | MPM programs generated from a ~2.5 s prefix to predict what follows, compared in video space only |

## L4 Sim-to-real predictivity

**Checks:** Whether the same conclusion holds in simulation and reality, such as policy rankings or task outcomes in a reconstructed environment.
**Limit:** Controllers may compensate for world errors; attributing failures to the environment needs a fixed controller and a reference environment.

| Work | What it checks |
|---|---|
| [SIMPLER](../README.md#paper-2405-05941) | The same policies in simulation and on real robots, compared on performance and ranking (Pearson, MMRV) |
| [YUBI-Real2Sim](../README.md#paper-2610-17521) | Only reconstruction artifacts vary; visual scores fail to predict policy-ranking failures |
| [Video2World](../README.md#paper-2610-04432) | Environments and behaviors rebuilt from real demonstration videos, compared on geometry, trajectories and task results |
| [Real2Sim Benchmark](../README.md#paper-real2sim-benchmark) | A frozen reconstructed scene compared by rendering, action replay and fixed-policy closed loop |

## Observations

- **Uneven coverage:** Work concentrates in L0 and L3a; few works check mechanisms, parameters or downstream use, and evaluators appear only in L0, L1 and L3a.
- **Open question:** Which lower-level checks predict higher-level failures? YUBI-Real2Sim is a counterexample: visual quality does not predict policy rankings.

## Terminology sources

Level names borrow existing terms from the works below; combining them into a ladder is this repository's synthesis.

- Fidelity taxonomies: Alexander et al., [From Gaming to Training](https://www.cs.uky.edu/~sgware/reading/papers/alexander2005gaming.pdf) (2005); [The Interaction Fidelity Model](https://arxiv.org/abs/2402.16665)
- V&V (L3b, L3c): [NAFEMS: Verification and Validation](https://www.nafems.org/training/learning-hub/introduction-to-simulation-credibility/verification-and-validation); Roache; Roy & Oberkampf
- Scene generation and embodied simulation (L0a, L1): [3D Scene Generation: A Survey](https://arxiv.org/abs/2505.05474); [3D Generation for Embodied AI and Robotic Simulation: A Survey](https://arxiv.org/abs/2604.26509); [SceneEval](https://arxiv.org/abs/2503.14756)
- Sim–real agreement (L4): [SIMPLER](https://arxiv.org/abs/2405.05941); [BWM](https://arxiv.org/abs/2607.29302)
