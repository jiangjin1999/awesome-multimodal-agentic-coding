# 仿真器质量评估：检验层级

[English](simulator-evaluation.md) · **简体中文**

本文按“检验层级”重新组织 [3.3 仿真器质量评估](../README.zh-CN.md#s3-3) 的相关工作，回答一个问题：**一篇工作到底在检查仿真世界的哪种性质，它的结论能信到什么程度？** 每篇工作的方法与验证细节见 [Stage 3 导读第 3 节](README.zh-CN.md#section-3)。

## 目录

- [0. 导读](#0-导读)
- [1. L0a 需求符合](#1-l0a-需求符合)
- [2. L0b 参照还原](#2-l0b-参照还原)
- [3. L1 静态合理性](#3-l1-静态合理性)
- [4. L2 交互响应](#4-l2-交互响应)
- [5. L3 动力学保真](#5-l3-动力学保真)
  - [5.1 L3a 运动一致](#51-l3a-运动一致)
  - [5.2 L3b 机制来源](#52-l3b-机制来源)
  - [5.3 L3c 参数与外推](#53-l3c-参数与外推)
- [6. L4 下游效用](#6-l4-下游效用)
- [7. 横向观察](#7-横向观察)
- [8. 术语来源](#8-术语来源)

---

## 0. 导读

### 三个问题

| 问题 | 名称 | 作用 |
|---|---|---|
| **检什么** | 检验层级（主轴） | 这篇工作检查世界的哪种性质；本文按它分节 |
| **凭什么信** | 证据属性（标签） | 参照从哪来、标准由谁定、证据怎么取；决定结论有多可靠 |
| **检的是谁** | 评估设定（标签） | Agent 负责到哪一步、这篇工作本身的角色；避免把不同性质的工作混在一起 |

### 层级总览

| 层级 | 英文 | 核心问题 | 世界的状态 |
|---|---|---|---|
| L0a 需求符合 | Semantic Fidelity | 满足给定的需求吗？ | 不动 |
| L0b 参照还原 | Visual / Reconstruction Fidelity | 和参照像吗？ | 不动 |
| L1 静态合理性 | Static Physical Plausibility | 不动的时候站得住、用得了吗？ | 冻结的一刻 |
| L2 交互响应 | Interaction Plausibility / Functional Fidelity | 碰它一下，反应对吗？ | 受到外部动作 |
| L3a 运动一致 | Motion Fidelity | 轨迹像不像？ | 随时间演化 |
| L3b 机制来源 | Model Verification | 运动是否真由合适的物理模型产生？ | 随时间演化 |
| L3c 参数与外推 | Validation & System Identification | 参数准不准，能否预测没见过的时段？ | 随时间演化 |
| L4 下游效用 | Sim-to-Real Predictivity | 拿这个世界去干活，结论在真实世界成立吗？ | 投入使用 |

```
  规范驱动：L0a 需求符合 ─┐
                          ├─→ L1 静态合理性 → L2 交互响应 → L3 动力学保真 → L4 下游效用
  参照驱动：L0b 参照还原 ─┘     (不动)          (被动一下)      (自己演化)       (拿去干活)
```

- L0a 与 L0b 是**平行的两个起点**：前者的参照是需求（用户指令或常识先验），后者的参照是一张图、一段视频或一个目标场景。
- 每一层检查的是**一种不同的失败模式**，不是累积分数。通过上层不代表下层没问题：控制器可以补偿环境误差，让 L4 成功而 L3 是错的。

### 归层规则

- 按论文**主打的创新点**归入主层；同时涉及的其他层写在“也涉及”。
- ★ 表示这篇工作的主要贡献是**评估工具**（评估器），它按所评估的性质归层。
- 作品名链接到[完整研究地图](../README.zh-CN.md#contents)中的条目；“导读”链接到 Stage 3 导读中的详细说明。

### 标签说明

| 标签 | 取值 | 说明 |
|---|---|---|
| **参照来源** | 文本需求 → 常识先验 → 合成真值 → 真实观测 → 实机结果 | 越往右，结论越接近真实世界 |
| **标准来源** | 统一协议 → 每题契约 → 真实录像对照 → 评估器针对场景生成 | 越往左越可比、可复现；越往右越能适应具体场景，但评估器本身需要单独验证 |
| **证据获取** | 渲染加评审 → 原生状态读取 → 主动干预 → 重放或闭环执行 → 参数辨识 | 从“看产物”到“探测产物”，可信度依次提高 |
| **Agent 自由度** | 只填参数 → 在给定框架里写 → 从零写程序 | 自由度越大，需要检查的层越多 |
| **角色** | 评估器 / 能力基准 / 验收协议 | 评估器要看它和人工判断的一致性；能力基准用质量指标评 Agent 构建得好不好；验收协议问这个仿真器能不能信 |

---

## 1. L0a 需求符合

**Semantic Fidelity · 它满足给定的需求吗？**

- **怎么检：** 把需求拆成可逐项核对的约束（物体、属性、数量、相对位置），逐条判断是否满足。需求有两个来源：用户写出的**显式指令**（“床靠墙，两侧各有一个床头柜”），以及用户不会写、但默认应成立的**隐式要求**（从数据中归纳的空间常识）。
- **能发现的错误：** 缺物体、关系错、尺度离谱、摆放违反常识。
- **不能证明：** 任何物理性质。完全满足约束的房间，每个物体都可能是一块不能动的整体网格。

| 作品 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|
| [SceneEval](../README.zh-CN.md#paper-2503-14756) ★ · [导读](README.zh-CN.md#work-2503-14756) | L1 | 文本加隐式常识 | — | 评估器 |
| [Apples on the Table?（LEGO-Eval）](../README.zh-CN.md#paper-2511-03001) ★ · [导读](README.zh-CN.md#work-2511-03001) | — | 文本 | — | 评估器 |
| [SceneCritic](../README.zh-CN.md#paper-2604-13035) ★ · [导读](README.zh-CN.md#work-2604-13035) | L1 | 数据中的常识 | — | 评估器 |
| [Code4Scene](../README.zh-CN.md#paper-2609-36777) · [导读](README.zh-CN.md#work-2609-36777) | L1 | 任务需求 | 写程序 | 能力基准 |

---

## 2. L0b 参照还原

**Visual / Reconstruction Fidelity · 它和参照看起来一样吗？**

- **怎么检：** 给定目标图像、视频、场景或工程图纸，Agent 用程序重建或编辑，再比较两者。要区分两种证据：
  - **渲染空间相似**（LPIPS、DINO、掩码）：回答“看起来像”；
  - **原生结构一致**（三维距离、CAD 特征、场景图）：回答“结构对”，更接近“可以拿去仿真”。
- **能发现的错误：** 外观、位置、形状、结构的偏差。
- **不能证明：** 碰撞体、质量、关节是否正确。看起来完全一致的重建，物理上可能一碰就散。

| 作品 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|
| [IR3D-Bench](../README.zh-CN.md#paper-2506-23329) · [导读](README.zh-CN.md#work-2506-23329) | L0a | 图像 | 写程序 | 能力基准 |
| [BlenderGym](../README.zh-CN.md#paper-2504-01786) · [导读](README.zh-CN.md#work-2504-01786) | — | 目标场景 | 改程序 | 能力基准 |
| [BlenderWorld](../README.zh-CN.md#paper-system-blenderworld) · [导读](README.zh-CN.md#work-system-blenderworld) | — | 真实参照 | 写程序 | 能力基准 |
| [Parametric CAD Bench v3](../README.zh-CN.md#paper-2611-02659) · [导读](README.zh-CN.md#work-2611-02659) | — | 文本加工程图 | 写程序 | 能力基准 |
| [BVB](../README.zh-CN.md#paper-2609-15478) · [导读](README.zh-CN.md#work-2609-15478) | L3a | 视频 | 写程序 | 能力基准 |
| [Frontier3DBench](../README.zh-CN.md#paper-2611-09017) · [导读](README.zh-CN.md#work-2611-09017) | L2 | 任务需求 | 写程序 | 能力基准 |

---

## 3. L1 静态合理性

**Static Physical Plausibility · 它不动的时候站得住、用得了吗？**

- **为什么叫“静态”：** 只看场景某一刻冻结的状态，不让时间往前走，也不运行动力学。检查全部是**几何计算**：
  - **物理可行**：碰撞（网格是否相交）、支撑（底面是否贴着某个表面）、越界；
  - **使用可行**：可达（距离与可达范围）、通行（地面路径规划）、操作空间。
- **能发现的错误：** 悬空、穿插、走不过去、够不着。成本低、可解释，是 L0 与 L2 之间的筛子。
- **不能证明：** 动起来以后是否正确。通过全部静态检查的场景，一开始模拟仍可能因摩擦为零而滑落、因质心错误而倾倒。

| 作品 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|
| [GREP](../README.zh-CN.md#paper-2611-05802) ★ · [导读](README.zh-CN.md#work-2611-05802) | L0a | 原则加具体场景 | — | 评估器 |
| [SceneTeract](../README.zh-CN.md#paper-2603-29798) ★ · [导读](README.zh-CN.md#work-2603-29798) | — | 活动加使用者条件 | — | 评估器（也用于训练） |

GREP 的评估 Agent 会主动选视角、调用几何工具，这是**评估器**的能力，不等于构建 Agent 有修复闭环。SceneTeract 引入使用者条件，问的是“这个场景对这个人能不能用”。

---

## 4. L2 交互响应

**Interaction Plausibility / Functional Fidelity · 碰它一下，反应对吗？**

- **怎么检：** 对世界施加动作，检查响应。从“看产物”变成“**探测产物**”。分两种：
  - **(a) 物理交互响应：** 施力后物理上是否合理，例如推、开合、表面探测；
  - **(b) 状态契约：** 执行动作后，程序状态是否按约定变化，例如读取坐标、速度、开关标志并核对隐藏断言。
- **标准从哪里来：** 统一协议（所有场景同一套动作）、每题契约（基准作者为每道题写好隐藏要求），或真实录像（逐步与实拍过程对照）。
- **能发现的错误：** 推不动、门打不开、状态没变、画面正常但逻辑错误。
- **不能证明：** 参数是否校准。门能打开、状态正确，不代表门的质量和阻尼正确。

| 作品 | 类型 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|---|
| [ScIntBench](../README.zh-CN.md#paper-2610-37326) · [导读](README.zh-CN.md#work-2610-37326) | (a) | L0a、L1 | 统一交互协议 | — | 能力基准（评场景生成方法） |
| [WorldCoder-Bench](../README.zh-CN.md#paper-2606-01869) · [导读](README.zh-CN.md#work-2606-01869) | (b) | L3b | 自然语言加隐藏契约 | 写程序（单次生成） | 能力基准 |
| [Lab2Sim](../README.zh-CN.md#paper-2611-02928) | (b) | — | 真实实验录像 | 写程序 | 方法（含独立验证） |

WorldCoder-Bench 的 StateProbe 在每个预设动作（包括物理步进）前后记录状态快照，用带数值容差的隐藏断言检查变化量，其中包括守恒律等物理不变量，因此同时涉及 L3b。

---

## 5. L3 动力学保真

**Physical / Dynamics Fidelity · 放手让它自己演化，过程对吗？**

以“小球从斜坡滚下，撞上一个箱子”为例，这一层要回答三个问题，难度依次增加：

| 子问题 | 问的是什么 | 怎么检 | 能被什么骗过 |
|---|---|---|---|
| **L3a 运动一致** | 轨迹像不像 | 逐帧比较位置、光流、掩码，或由 VLM 评审 | 关键帧动画 |
| **L3b 机制来源** | 运动是否真由合适的物理模型产生，条件改变后是否仍然正确 | 反事实干预、物理断言、守恒检查 | 很难骗过，前提是真的做了干预 |
| **L3c 参数与外推** | 物理量的数值准不准，能否预测没见过的时段 | 与独立测量的参数比较、留出未来时段 | 参数互相补偿能骗过轨迹，但骗不过外推和真实测量 |

**“机制对不对”取决于 Agent 负责到哪一步。** 调用现成引擎（Blender、MuJoCo）时，物理规律由引擎负责，Agent 负责“交给引擎正确的问题，并且真的交给它算”；自己写求解器时，规律本身也由 Agent 写。按 Agent 的自由度，大致是一条谱：

```
只填参数  →  在给定框架里写  →  从零写程序
Δynamics      WorldSolver          PhysCodeGym、MPMWorlds
```

自由度越大，可能出错的地方越多：绕过引擎直接写动画、选错物理模型（把布料当刚体）、配错数值（步长过大导致穿模）、写错更新规则。

### 5.1 L3a 运动一致

**Motion Fidelity · 轨迹像不像？** 用动画“演”出来的正确运动和用物理“算”出来的正确运动，在这一档得分可能相同。

| 作品 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|
| [ExeWorldBench](../README.zh-CN.md#paper-2610-15166) · [导读](README.zh-CN.md#work-2610-15166) | L2 | 视觉参考或目标 | 写程序 | 能力基准 |
| [4DCodeBench](../README.zh-CN.md#paper-2610-03715) · [导读](README.zh-CN.md#work-2610-03715) | L0b | 参考视频（合成加真实） | 写程序，允许关键帧 | 能力基准 |
| [VisPhyWorld](../README.zh-CN.md#paper-2602-13294) · [导读](README.zh-CN.md#work-2602-13294) | L0b | 视频 | 写程序 | 能力基准 |
| [Physics-Inspired Animations](../README.zh-CN.md#paper-2602-10840) · [导读](README.zh-CN.md#work-2602-10840) | — | 物理概念描述 | 写程序 | 能力基准（也用于训练） |
| [PhyRubric](../README.zh-CN.md#paper-2611-13576) ★ · [导读](README.zh-CN.md#work-2611-13576) | — | 预制 rubric | 不适用（评生成视频） | 评估器（相邻） |
| [Latent Prediction Error and Physical Surprise](../README.zh-CN.md#paper-2611-01815) | — | 物理违规与外观变化对照 | 不适用（评视频世界模型） | 诊断研究（相邻） |

### 5.2 L3b 机制来源

**Model Verification · 运动是否真由合适的物理模型产生？** 反事实干预是区分 L3a 与 L3b 的核心工具：改变斜坡角度或球的质量后重新运行，真实模拟的结果会相应变化，写死的动画不会。

| 作品 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|
| [PhysCodeGym](../README.zh-CN.md#paper-2610-17288) · [导读](README.zh-CN.md#work-2610-17288) | L0b、L3a | 真实视频 | 写程序 | 能力基准 |
| [PhysCodeBench](../README.zh-CN.md#paper-2604-23580) · [导读](README.zh-CN.md#work-2604-23580) | L3a | 文本描述的物理现象 | 写程序 | 能力基准（也提出方法） |
| [WorldSolver](../README.zh-CN.md#paper-2610-08720) · [导读](README.zh-CN.md#work-2610-08720) | — | 经典物理问题 | 在给定框架里写求解器 | 能力基准 |

### 5.3 L3c 参数与外推

**Validation & System Identification · 参数准不准，能否预测没见过的时段？** 很多组参数都能产生相似的轨迹（不可辨识），因此需要独立测量的参照或留出的未来时段。

| 作品 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|
| [IRIS](../README.zh-CN.md#paper-2603-16432) · [导读](README.zh-CN.md#work-2603-16432) | — | **真实测量**，附不确定性 | 不限方法 | 能力基准 |
| [Δynamics](../README.zh-CN.md#paper-2605-20576) · [导读](README.zh-CN.md#work-2605-20576) | L3a | 合成真值；真实视频为伪标注 | 只填参数 | 方法加评测 |
| [MPMWorlds](../README.zh-CN.md#paper-2606-01538) · [导读](README.zh-CN.md#work-2606-01538) | L3a | 合成 MPM 数据，仅在视频空间评测 | 写完整求解器（多采样挑选） | 能力基准（也训练模型） |

MPMWorlds 的外推只在视频空间比较，不读取粒子状态或参数，证据强度不如 IRIS 的独立物理测量。

---

## 6. L4 下游效用

**Sim-to-Real Predictivity · 拿这个世界去干活，结论在真实世界成立吗？**

- **怎么检：** 不再直接看世界本身，而是看**在这个世界里得出的结论**能否迁移到真实世界。分两种：
  - **(a) 评估代理：** 同一批策略在仿真和实机上分别运行，比较表现与排名是否一致（如 Pearson 相关、MMRV）；
  - **(b) 环境—行为组合：** 从真实数据重建的世界，加上对应的行为程序，能否完成真实任务。
- **特有难题：误差归因。** 控制器可能补偿环境误差。需要固定控制器、准备已知可用的参照环境，并做交叉执行。
- **能发现的错误：** 仿真里的评测或训练结论无法迁移。

| 作品 | 类型 | 也涉及 | 参照来源 | Agent 自由度 | 角色 |
|---|---|---|---|---|---|
| [Evaluating Real-World Robot Manipulation Policies in Simulation（SIMPLER）](../README.zh-CN.md#paper-2405-05941) · [导读](README.zh-CN.md#work-2405-05941) | (a) | — | 实机配对 | — | 验收协议 |
| [YUBI-Real2Sim](../README.zh-CN.md#paper-2610-17521) · [导读](README.zh-CN.md#work-2610-17521) | (a) | L0b | 实机配对 | — | 验收协议 |
| [Video2World](../README.zh-CN.md#paper-2610-04432) · [导读](README.zh-CN.md#work-2610-04432) | (b) | L0b、L3 | 真实示范视频 | 写程序（环境加行为） | 能力基准 |
| [Real2Sim Benchmark](../README.zh-CN.md#paper-real2sim-benchmark) · [导读](README.zh-CN.md#work-real2sim-benchmark) | (b) | L0b、L3 | 真实片段 | 写程序 | 能力基准 |

YUBI-Real2Sim 只改变背景伪影、固定物体与物理条件，发现视觉分数不能可靠预测策略排名的失败，直接说明 L0b 不能替代 L4。

---

## 7. 横向观察

1. **层级不是严格累积的。** 通过上层不一定意味着通过了下层：L4 的任务可能成功而 L3 参数是错的，L2 契约满足而 L1 存在穿模。每层对应一种不同的失败模式。
2. **层级越高，参照越倾向于来自真实世界，但两者不完全对应。** IRIS 在 L3 就使用了真实测量，Lab2Sim 在 L2 就使用了真实录像。
3. **分布不均。** 工作集中在 L0 与 L3a；真正检验机制、参数与下游效用的工作偏少。评估器（★）只出现在 L0、L1 与 L3a，L2 至 L4 尚无专门的评估工具。
4. **开放问题：哪些低层检查能预测高层失败？** YUBI-Real2Sim 给出了一个反例：视觉质量不能预测策略排名。如何依据真实误差及其不确定性校准验收阈值，仍待研究。

---

## 8. 术语来源

本文的层级名称借用自以下文献中的已有术语；把它们组合成一个分层框架，是本仓库的整理，不代表存在公认的统一分类。

- **保真度分类（仿真训练与 VR）：** Alexander et al., [From Gaming to Training: A Review of Studies on Fidelity, Immersion, Presence, and Buy-in](https://www.cs.uky.edu/~sgware/reading/papers/alexander2005gaming.pdf)（2005）区分 physical、functional、psychological fidelity；[The Interaction Fidelity Model](https://arxiv.org/abs/2402.16665) 区分 presentational、behavioral、physical、scenario fidelity。
- **V&V（计算仿真）：** Roache 的区分——verification 是“方程解得对不对”，validation 是“解的方程本身对不对”，后者需要与实验数据比较。参见 [NAFEMS: Verification and Validation](https://www.nafems.org/training/learning-hub/introduction-to-simulation-credibility/verification-and-validation) 与 Roy & Oberkampf 的 V&V 框架。对应本文 L3b 与 L3c。
- **场景生成与具身仿真的评估用语：** [3D Scene Generation: A Survey](https://arxiv.org/abs/2505.05474)（semantic consistency、physical plausibility）；[3D Generation for Embodied AI and Robotic Simulation: A Survey](https://arxiv.org/abs/2604.26509)（collision rate、reachability、stable-object ratio）；[SceneEval](https://arxiv.org/abs/2503.14756)（fidelity 与 plausibility）。
- **仿真—实机一致性：** [SIMPLER](https://arxiv.org/abs/2405.05941)（Pearson 相关与 MMRV）；[BWM](https://arxiv.org/abs/2607.29302)（policy-ranking fidelity）。
