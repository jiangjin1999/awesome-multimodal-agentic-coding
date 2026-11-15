# 仿真器构建：全部工作逐步对照

[English](simulator-construction.md) · **简体中文**

[3.2 仿真器构建](../README.zh-CN.md#s3-2) 的全部 68 项工作，按同一套标准逐步标注每一步由谁来做。README 里的代表图只挑了 15 项，逐格写出具体的模型和工具；这里是完整版，格子只标类型，每项的具体做法写在最右一列。

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/stage-chart/stage-full-zh-dark.svg">
  <img src="../assets/stage-chart/stage-full-zh-light.svg" alt="3.2 全部 68 项和两个参照基准的逐步对照：九个构建步骤加上检查与修订、变体扩增，每一步是 Agent 或 VLM 自己做、交给专用工具、事先给定，还是不涉及。任务规划（55 项）、布局对齐（43 项）和检查与修订（49 项）大多由 Agent 做，感知测量多交给专用模型（32 项）。46 项运行了物理引擎，10 项只建场景，9 项只到仿真就绪，3 项没写明引擎。" width="100%">
</picture>

## 怎么读

- **九步**：前九列是仿真器构建的九步，分四组：A 输入理解（① 任务规划、② 感知测量）、B 场景构建（③ 物体资产、④ 关节结构、⑤ 布局对齐）、C 物理建模（⑥ 物理参数、⑦ 物理引擎）、D 任务与控制（⑧ 机器人控制、⑨ 任务定义）。B 加 C 是仿真器本身，再加上 D 就是能拿来训练和评测的环境。
- **另外两列**：检查与修订、变体扩增不是仿真器的组成部分，所以和九步隔开。检查与修订是穿插在各步之间的循环，谁来检查、出错回到哪一步，决定了一项工作属于哪种组织方式；变体扩增是可选的，把一个造好的仿真器扩成多个。
- **格子**：实心是 Agent 或 VLM 自己做，斜线是交给专用工具、模型或引擎，描边是事先给定或人工，灰色虚线是不涉及或没写明。⑦ 列的红色虚线表示没有物理引擎，蓝色描边表示仿真就绪：可以导入物理引擎，但方法里没有运行。
- **行首标签**：每项的物理引擎层级，分为完整仿真器、仿真就绪、只建场景、引擎未写明。
- **合计**：最上面一行是 68 项在每一列的合计。两个 Bench 只作参照，不计入合计。

## 从全部 68 项能看出什么

- **四类工作的差别主要在「检查与修订」这一列，不在九步里。** 九步中由 Agent 自己做的格子，端到端占 42%，闭环 41%，几乎一样；开环 25%，Model-based 为 0。检查与修订这一列，端到端 22 项、闭环 20 项全部由 Agent 做；开环里固定流程的 13 项没有一项有 Agent 检查（GenSim 只按规则筛选），末段精修的 8 项里有 7 项有。
- **⑦ 物理引擎：46 项有引擎，10 项只建场景，9 项只到仿真就绪，3 项没写明。** 有引擎的工作里，只有 Perceptual Self-Reflection 自己写数值仿真，其余都用现成引擎。只建场景的 10 项里，端到端和闭环各占 4 项。
- **② 感知测量几乎都交给专用模型**：32 项交给 SAM、深度、位姿这类模型，只有 CUE、RoboSimStudio、D-World 由 Agent 自己测量。
- **越往后的步骤，涉及的工作越少**：④ 关节结构 21 项，⑨ 任务定义 22 项，变体扩增 10 项。另有 11 项是完整仿真器，却不涉及 ⑧ 和 ⑨：它们只交付场景或资产，任务留给下游。

## 各项工作

按组织方式分组，点名字可以跳到 README 里的条目。括号里标出不是完整仿真器的工作。

**Agentic End-to-End · 一个 Agent 端到端**（22）：[SimuLean](../README.zh-CN.md#paper-2611-10602) · [CUE](../README.zh-CN.md#paper-2611-02691) · [DyCraft](../README.zh-CN.md#paper-2610-40754)（只建场景） · [SceneAgent](../README.zh-CN.md#paper-2610-34745) · [Plumb](../README.zh-CN.md#paper-system-plumb) · [GRASE](../README.zh-CN.md#paper-2610-21498)（只建场景） · [RoboSimStudio](../README.zh-CN.md#paper-2610-18835) · [USDCraft](../README.zh-CN.md#paper-2610-11322)（仿真就绪） · [Agentic RSR](../README.zh-CN.md#paper-2610-10479) · [Real2Gym](../README.zh-CN.md#paper-2609-37089) · [FACT](../README.zh-CN.md#paper-2609-37067) · [CoDimRecon](../README.zh-CN.md#paper-2609-36024) · [WorldAgent](../README.zh-CN.md#paper-2609-33208)（只建场景） · [Code as Worlds](../README.zh-CN.md#paper-2608-27549)（只建场景） · [GS-Agent](../README.zh-CN.md#paper-2607-21522) · [Articraft](../README.zh-CN.md#paper-2605-15187)（仿真就绪） · [SimWorld Studio](../README.zh-CN.md#paper-2605-09423) · [SAGE](../README.zh-CN.md#paper-2602-10116) · [SceneWeaver](../README.zh-CN.md#paper-2509-20414)（仿真就绪） · [Eurekaverse](../README.zh-CN.md#paper-2411-01775) · [AHa-3D](../README.zh-CN.md#paper-res-aha-3d)（引擎未写明） · [mujoco-workbench](../README.zh-CN.md#paper-mujoco-workbench)

**Closed-loop Workflow · 分工事先定好，出错回到对应步骤**（20）：[WorldSketch](../README.zh-CN.md#paper-2611-00513)（只建场景） · [Gym-Anything](../README.zh-CN.md#paper-2610-40565) · [WorldMirror](../README.zh-CN.md#paper-2610-31834) · [MARC](../README.zh-CN.md#paper-2610-33060)（只建场景） · [D-World](../README.zh-CN.md#paper-2610-17114) · [Artisan](../README.zh-CN.md#paper-2610-13947) · [Awomo-SimDataEngine](../README.zh-CN.md#paper-2610-02274) · [Text2Sim](../README.zh-CN.md#paper-2609-36593) · [DiagGen](../README.zh-CN.md#paper-2609-23103) · [DeformSmith](../README.zh-CN.md#paper-2609-18620) · [Agentic Real2Sim](../README.zh-CN.md#paper-2607-19190) · [SimWorlds](../README.zh-CN.md#paper-2607-01766)（只建场景） · [MUSE](../README.zh-CN.md#paper-2606-14168)（只建场景） · [ChronoAgentic](../README.zh-CN.md#paper-2605-14398) · [ArtiCAD](../README.zh-CN.md#paper-2604-10992)（仿真就绪） · [SceneSmith](../README.zh-CN.md#paper-2602-09153) · [Perceptual Self-Reflection](../README.zh-CN.md#paper-2602-12311) · [GRS](../README.zh-CN.md#paper-2410-15536) · [Articulate-Anything](../README.zh-CN.md#paper-2410-13882) · [OMNI-EPIC](../README.zh-CN.md#paper-2405-15568)

**Open-loop Workflow · 固定流程，LLM 负责其中几步**（13）：[Spatial Harness](../README.zh-CN.md#paper-2611-11344) · [LabWorld](../README.zh-CN.md#paper-2610-36592)（只建场景） · [SceneBloom](../README.zh-CN.md#paper-2610-32978)（仿真就绪） · [AgentDreamer](../README.zh-CN.md#paper-2610-30679) · [EmbodiedGen V2](../README.zh-CN.md#paper-2607-07459) · [PerceptTwin](../README.zh-CN.md#paper-2606-04226)（引擎未写明） · [Phys2Real](../README.zh-CN.md#paper-2510-11689) · [FactorSim](../README.zh-CN.md#paper-2409-17652) · [RoboTwin](../README.zh-CN.md#paper-2409-02920)（引擎未写明） · [Holodeck](../README.zh-CN.md#paper-2312-09067) · [RoboGen](../README.zh-CN.md#paper-2311-01455) · [Gen2Sim](../README.zh-CN.md#paper-2310-18308) · [GenSim](../README.zh-CN.md#paper-2310-01361)

**Open-loop Workflow · 固定流程，末段有局部 Agent 精修**（8）：[GIF](../README.zh-CN.md#paper-2609-05927) · [SceneMosaic](../README.zh-CN.md#paper-2609-05594) · [Lucida](../README.zh-CN.md#paper-2608-30821)（只建场景） · [Usage-Driven Code Scenes](../README.zh-CN.md#paper-2608-18840) · [LiteReality-Agent](../README.zh-CN.md#paper-2610-01863)（仿真就绪） · [SimFoundry](../README.zh-CN.md#paper-2606-28276) · [SceneCode](../README.zh-CN.md#paper-2605-19587)（仿真就绪） · [Vid2Sid](../README.zh-CN.md#paper-2602-19359)

**Model-based (without Agent) · 没有 Agent，模型或优化直接产出**（5）：[UniPhysGen](../README.zh-CN.md#paper-2607-13586)（仿真就绪） · [Video2Sim2Real](../README.zh-CN.md#paper-2606-08828) · [PhysX-Omni](../README.zh-CN.md#paper-2605-21572)（仿真就绪） · [DeformMaster](../README.zh-CN.md#paper-2605-09586) · [Real2Code](../README.zh-CN.md#paper-2406-08474)

## 标注依据与修改

- **依据**：各项工作在 [Stage 3 导读](README.zh-CN.md#section-2) 里记录的具体方法和构造流程；记录不清的，看了论文正文。代表图里的 15 项逐格核对过具体工具，其余各项只标类型。
- **拿不准的格子**：SimuLean 用的是离散事件仿真，不是物理引擎，仍记为完整仿真器。RoboTwin 早期版本没写仿真后端，记为引擎未写明。SimFoundry 的修订只在关节模块内进行，算进 ④ 关节结构，检查与修订一列留空。SceneAgent 的 ⑧ 机器人控制、SceneBloom 的 ⑤ 布局对齐，原文写得较笼统，是按方法描述判断的。
- **修改**：数据在 `data/site.yaml` 的 `stage_chart_full`，每项一行。`steps` 是 11 个字母，依次对应 ①–⑨、检查与修订、变体扩增：`a` 是 Agent 或 VLM，`t` 是专用工具，`g` 是事先给定，`n` 是不涉及，`x` 是没有物理引擎，`r` 是仿真就绪。`tier` 是物理引擎层级（`F` `R` `S` `U`），要和 ⑦ 那个字母对得上，否则生成时会报错。改完运行 `python3 scripts/build_readme.py`，这张图会重新生成。
