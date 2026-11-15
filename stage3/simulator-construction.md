# Simulator construction: every work, step by step

**English** · [简体中文](simulator-construction.zh-CN.md)

All 68 works in [3.2 Simulator construction](../README.md#s3-2), labelled by the same rule: who does each step. The representative chart in the README picks 15 works and names the model or tool in every cell; this is the full version, where a cell shows only the kind of actor and the last column says how each work does it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/stage-chart/stage-full-en-dark.svg">
  <img src="../assets/stage-chart/stage-full-en-light.svg" alt="Chart of all 68 works in Section 3.2 and two reference benchmarks: for each of the nine build steps, plus verification &amp; revision and variant expansion, whether the Agent or VLM does it, a specialised tool does it, it is given, or it is not involved. Agents take most of task planning (55 works), layout (43) and verification &amp; revision (49), while perception goes to specialised models (32). 46 works run a physics engine, 10 only build a scene, 9 stop at sim-ready and 3 do not name one." width="100%">
</picture>

## How to read it

- **Nine steps**: the first nine columns are the nine steps of building a simulator, in four groups: A Perception & Planning (① task planning, ② perception & measurement), B Scene Construction (③ object assets, ④ articulation, ⑤ layout & alignment), C Physics Modeling (⑥ physical parameters, ⑦ physics engine) and D Task & Control (⑧ robot control, ⑨ task definition). B plus C is the simulator itself; adding D gives an environment you can train and evaluate in.
- **Two more columns**: verification & revision and variant expansion are not parts of a simulator, so they sit apart from the nine steps. Verification & revision is a loop that runs between the steps; who checks, and which step a problem goes back to, decides a work's organization. Variant expansion is optional: it turns one finished simulator into many.
- **Cells**: solid means the Agent or VLM does it itself, hatched means a specialised tool, model or engine, outlined means given in advance or by hand, and grey dashed means not involved or not stated. In column ⑦, red dashes mean no physics engine, and a blue outline means sim-ready: the result can be loaded into a physics engine, but the method does not run one.
- **Tags**: each work's physics-engine tier: full simulator, sim-ready, scene only, or engine not stated.
- **Totals**: the top row counts all 68 works in each column. The two Bench rows are for reference only and are not counted.

## What the 68 works show

- **The four kinds of work differ mostly in the verification & revision column, not in the nine steps.** Within the nine steps, the Agent does 42% of the cells in End-to-End work and 41% in Closed-loop work, almost the same; Open-loop work is at 25% and Model-based at 0. In verification & revision, all 22 End-to-End and all 20 Closed-loop works have the Agent check; none of the 13 fixed-pipeline Open-loop works does (GenSim filters by rule), while 7 of the 8 with a final local Agent do.
- **⑦ Physics engine: 46 works run one, 10 only build a scene, 9 stop at sim-ready, and 3 do not say.** Only Perceptual Self-Reflection writes its own numerical simulation; every other engine is an existing one. Of the 10 scene-only works, 4 are End-to-End and 4 are Closed-loop.
- **② Perception goes to specialised models almost everywhere**: 32 works hand it to segmentation, depth or pose models; only CUE, RoboSimStudio and D-World have the Agent measure for itself.
- **Later steps involve fewer works**: ④ articulation 21, ⑨ task definition 22, variant expansion 10. 11 works are full simulators but do not touch ⑧ or ⑨: they deliver a scene or assets and leave the task to whoever uses them.

## The works

Grouped by organization; each name jumps to its entry in the README. Works that are not full simulators are marked in brackets.

**Agentic End-to-End · one Agent does it all** (22): [SimuLean](../README.md#paper-2611-10602) · [CUE](../README.md#paper-2611-02691) · [DyCraft](../README.md#paper-2610-40754) (scene only) · [SceneAgent](../README.md#paper-2610-34745) · [Plumb](../README.md#paper-system-plumb) · [GRASE](../README.md#paper-2610-21498) (scene only) · [RoboSimStudio](../README.md#paper-2610-18835) · [USDCraft](../README.md#paper-2610-11322) (sim-ready) · [Agentic RSR](../README.md#paper-2610-10479) · [Real2Gym](../README.md#paper-2609-37089) · [FACT](../README.md#paper-2609-37067) · [CoDimRecon](../README.md#paper-2609-36024) · [WorldAgent](../README.md#paper-2609-33208) (scene only) · [Code as Worlds](../README.md#paper-2608-27549) (scene only) · [GS-Agent](../README.md#paper-2607-21522) · [Articraft](../README.md#paper-2605-15187) (sim-ready) · [SimWorld Studio](../README.md#paper-2605-09423) · [SAGE](../README.md#paper-2602-10116) · [SceneWeaver](../README.md#paper-2509-20414) (sim-ready) · [Eurekaverse](../README.md#paper-2411-01775) · [AHa-3D](../README.md#paper-res-aha-3d) (engine not stated) · [mujoco-workbench](../README.md#paper-mujoco-workbench)

**Closed-loop Workflow · problems go back to the responsible step** (20): [WorldSketch](../README.md#paper-2611-00513) (scene only) · [Gym-Anything](../README.md#paper-2610-40565) · [WorldMirror](../README.md#paper-2610-31834) · [MARC](../README.md#paper-2610-33060) (scene only) · [D-World](../README.md#paper-2610-17114) · [Artisan](../README.md#paper-2610-13947) · [Awomo-SimDataEngine](../README.md#paper-2610-02274) · [Text2Sim](../README.md#paper-2609-36593) · [DiagGen](../README.md#paper-2609-23103) · [DeformSmith](../README.md#paper-2609-18620) · [Agentic Real2Sim](../README.md#paper-2607-19190) · [SimWorlds](../README.md#paper-2607-01766) (scene only) · [MUSE](../README.md#paper-2606-14168) (scene only) · [ChronoAgentic](../README.md#paper-2605-14398) · [ArtiCAD](../README.md#paper-2604-10992) (sim-ready) · [SceneSmith](../README.md#paper-2602-09153) · [Perceptual Self-Reflection](../README.md#paper-2602-12311) · [GRS](../README.md#paper-2410-15536) · [Articulate-Anything](../README.md#paper-2410-13882) · [OMNI-EPIC](../README.md#paper-2405-15568)

**Open-loop Workflow · fixed pipeline, an LLM does some steps** (13): [Spatial Harness](../README.md#paper-2611-11344) · [LabWorld](../README.md#paper-2610-36592) (scene only) · [SceneBloom](../README.md#paper-2610-32978) (sim-ready) · [AgentDreamer](../README.md#paper-2610-30679) · [EmbodiedGen V2](../README.md#paper-2607-07459) · [PerceptTwin](../README.md#paper-2606-04226) (engine not stated) · [Phys2Real](../README.md#paper-2510-11689) · [FactorSim](../README.md#paper-2409-17652) · [RoboTwin](../README.md#paper-2409-02920) (engine not stated) · [Holodeck](../README.md#paper-2312-09067) · [RoboGen](../README.md#paper-2311-01455) · [Gen2Sim](../README.md#paper-2310-18308) · [GenSim](../README.md#paper-2310-01361)

**Open-loop Workflow · fixed pipeline, a local Agent refines at the end** (8): [GIF](../README.md#paper-2609-05927) · [SceneMosaic](../README.md#paper-2609-05594) · [Lucida](../README.md#paper-2608-30821) (scene only) · [Usage-Driven Code Scenes](../README.md#paper-2608-18840) · [LiteReality-Agent](../README.md#paper-2610-01863) (sim-ready) · [SimFoundry](../README.md#paper-2606-28276) · [SceneCode](../README.md#paper-2605-19587) (sim-ready) · [Vid2Sid](../README.md#paper-2602-19359)

**Model-based (without Agent) · models or optimization produce the result** (5): [UniPhysGen](../README.md#paper-2607-13586) (sim-ready) · [Video2Sim2Real](../README.md#paper-2606-08828) · [PhysX-Omni](../README.md#paper-2605-21572) (sim-ready) · [DeformMaster](../README.md#paper-2605-09586) · [Real2Code](../README.md#paper-2406-08474)

## Sources and how to edit

- **Sources**: the method and construction notes recorded for each work in the [Stage 3 reading guide](README.md#section-2), and the paper itself where those notes were unclear. The 15 works in the representative chart were checked tool by tool; the others are labelled by kind only.
- **Judgment calls**: SimuLean runs a discrete-event simulation rather than a physics engine and is still counted as a full simulator. RoboTwin's early version does not name its simulator, so it is "engine not stated". SimFoundry revises only inside its articulation module, so that work is counted under ④ and its verification & revision cell is empty. SceneAgent's ⑧ robot control and SceneBloom's ⑤ layout are described only loosely and were judged from the method description.
- **Editing**: the data is `stage_chart_full` in `data/site.yaml`, one row per work. `steps` is 11 letters for ①–⑨, verification & revision and variant expansion: `a` Agent or VLM, `t` specialised tool, `g` given, `n` not involved, `x` no physics engine, `r` sim-ready. `tier` is the physics-engine tier (`F` `R` `S` `U`) and must match the letter in ⑦, or the build stops with an error. After editing, run `python3 scripts/build_readme.py` to redraw the chart.
