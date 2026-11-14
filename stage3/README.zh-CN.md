# Stage 3 · Bridging Digital & Physical Worlds

<a id="research-map"></a>

[English](README.md) · **简体中文**

多模态 Coding Agent 如何获得物理交互能力，构建可验证的环境，并从交互经验中改进程序、技能和模型？本专题按六个相互连接的研究问题组织早期基础与近期进展，以机器人操作为重点，也覆盖直接相关的科学实验和设计制造。

**文献截止：2026-11-13。** [返回完整研究地图](../README.zh-CN.md#contents)。

| 研究问题 | 主条目 | 连接 |
|---|---:|---|
| [1. 具身 Harness](#section-1) | 77 | 观测、执行、Skills 与回执 |
| [2. Simulator 构建](#section-2) | 62 | 参考环境／任务要求 → 可执行产物 |
| [3. Simulator 质量评估](#section-3) | 29 | 产物质量 → 可用的验证证据 |
| [4. 数据](#section-4) | 13 | 观测、代码、动作与结果 → 训练材料 |
| [5. 训练与能力提升](#section-5) | 71 | 程序／技能／模型更新 → 跨任务能力 |
| [6. 物理应用与实验](#section-6) | 34 | 机制组合 → 任务结果与现实验证 |

**构建可验证环境 → 获得交互经验 → 提升 Coding Agent 能力**是贯穿全篇的研究联系。各项工作的证据覆盖其中不同环节，完整的规模化闭环仍需联合检验。环境构建者、环境操作者和下游动作策略可能是不同模型。

每项工作保留一个专题主入口，跨章贡献用链接连接。已有完整书目链接回原研究地图；日期优先采用首次公开时间，会议或版本日期另作说明。独立 Benchmark、方法内的评估和资源分别阅读。

---

<a id="section-1"></a>

## 1．具身 Harness

Harness 为多模态 Coding Agent 提供观测、执行接口、运行状态、Skills 和失败回执。理解一项系统，先追踪 **Agent 输出什么 → 谁执行 → 什么证据返回 → 下一步改变什么**。

| 执行路径 | Agent 决定什么 | 下层负责什么 | 阅读入口 |
|---|---|---|---|
| 工具／控制接口 | 程序、目标位置、姿态、动作顺序与检查时机 | 感知、运动规划、逆运动学、控制器和机器人适配器 | Code as Policies → HexaShell、uni-robot-agent |
| 委派已有策略 | 子目标、选择哪个策略、预算、停止与恢复条件 | VLA／动作模型或已有程序完成局部控制 | Harness VLA、HarnessPAI、REA |

两条路径可以组合。代码生成、分层监督、记忆和 Skills 是具体设计，不再单列第三种互斥执行路径。VLA 可以直接接收语言子目标，无须上层先写控制程序。一次程序内部使用传感器反馈，与 LLM 获得新观测后再写代码，是不同层次的反馈。

较早工作建立“语言任务—程序—机器人 API”的连接；近期系统进一步研究观察时机、可恢复执行、上下文管理及不同策略的分工。评测须固定接口、权限和预算，区分完成任务、正确宣告完成以及调用成本。已有 Skills 如何进入系统在本节阅读；Skills 如何从经验中产生连接第 5 节。

### 可组合的执行资源

可从[运行资源](../README.zh-CN.md#s3-1)与[模型能力](../README.zh-CN.md#s2-6)寻找可复用组件。可调用组件可以支持 Harness，但不等于组件自身实现了 Agent 学习。

| 资源 | 接口与用途 | 证据边界 |
|---|---|---|
| [Webots MCP](https://github.com/MHasaan/webotMCP) | 场景／控制器编辑和机器人命令；返回多视角截图、运动轨迹与接触事件 | 仿真真值与反应式控制器需要和学习式感知、规划区分。 |
| [Alpamayo 2 Edge](https://huggingface.co/nvidia/Alpamayo2-Edge) | 环视相机序列、导航与自车运动历史 → 推理及驾驶轨迹 | NVIDIA 提供权重与推理代码；仿真评测和合作方车辆演示是不同层次的证据。 |
| [AlpaJudge](https://huggingface.co/nvidia/alpajudge) | 基于文本参考，或基于视觉／动作上下文评价驾驶理由 | 两套检查点为筛选／奖励提供推理分数，分数本身不认证执行中的驾驶安全。 |
| [Gemini Robotics 2.5](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/) | 具身推理组织流程，动作模型控制机器人运动 | Google 11 月 10 日公告描述合作方访问和特定工厂试点；该报告不建立开放权重或独立通用评测结论。 |

### 工具与控制接口

<a id="work-2611-01560"></a>
<!-- stage3-record: {"id": "2611.01560", "scope": "Core", "section": 1} -->

#### Democratizing Robot-Use Agents: A Unified Harness with Open Models

`2026-11-01` · Tsinghua University; University of California, Berkeley

[完整书目](../README.zh-CN.md#paper-2611-01560) · [论文](https://arxiv.org/abs/2611.01560) · [代码](https://github.com/Open-RUA/uni-robot-agent) · [项目页](https://openrua.ai/uni-robot-agent)

让 Qwen3.8-Flash-Next 和 GPT-6 Astra 通过统一接口调用感知与运动工具，运行几何检查，观察动作结果并调整下一步操作。

**具体方法：** 它重点解决同一套 Agent 工具怎样跨模型、模拟器和真实机器人使用：工具约定统一的参数与结果含义，后端适配不同硬件。调度还允许推理与物理运动重叠，同时维持共享资源的操作顺序。贡献在统一交互、执行效率与信息边界，而不仅是增加几个机器人函数。

**验证：** 统一接口返回观测快照、实际位姿、动作进度和执行结果，Agent 据此调整目标或后续操作；主要仿真配置不把深度真值和隐藏任务评分直接交给 Agent。

<a id="work-2611-01112"></a>
<!-- stage3-record: {"id": "2611.01112", "scope": "Core", "section": 1} -->

#### Auriga Technical Report: A Task-Agnostic Agent Harness for Zero-Shot Embodied Manipulation

`2026-10-31` · StellarEdge AI Technical Team

[完整书目](../README.zh-CN.md#paper-2611-01112) · [论文](https://arxiv.org/abs/2611.01112) · [项目页](https://auriga.stelledge.com/) · [代码](https://github.com/lose4578/Auriga)

让模型在任务信念、三维测量、轨迹预览与统一执行入口之上选择工具或编写多步 Python 程序。

**验证：** 在 RoboDojo 与 RoboCasa365 仿真中评测，包含程序、预览和几何消融及与观测关联的恢复轨迹；评测 Harness 固定，未报告硬件结果。

<a id="work-2610-30043"></a>
<!-- stage3-record: {"id": "2610.30043", "scope": "Adjacent", "section": 1} -->

#### TARSphere: A Robot-Oriented Full-Stack Framework for Long-Horizon Embodied Agents in Evolving Physical and Social Environments

`2026-10-21` · Zhejiang University; Fudan University

[论文](https://arxiv.org/abs/2610.30043) · [项目页](https://xuyicheng-zju.github.io/TARSphere/) · [代码](https://github.com/xuyicheng-zju/TARSphere)

为冻结多模态模型提供分层可执行技能、任务记忆和执行反馈，组织长时序机器人行动及环境变化处理。

**验证：** 在 30 个室内场景、360 个仿真回合上评测八个冻结 MLLM，将导航汇报与取送任务配对到五类变化条件。依赖事件的评分检查信息实际送达和物理完成，另行分析碰撞、跌倒及执行保真度。这些结果来自仿真机器人与 NPC 交互，不是现实部署结果。

<a id="work-2610-23479"></a>
<!-- stage3-record: {"id": "2610.23479", "scope": "Core", "section": 1} -->

#### HexaShell: A Universal Harness for Robot Coding Agents in Simulation and the Real World

`2026-10-16` · HexaFuture

[完整书目](../README.zh-CN.md#paper-2610-23479) · [论文](https://arxiv.org/abs/2610.23479) · [代码](https://github.com/HexaFuture/HexaShell)

让机器人编程 Agent 在每轮编写一段 Python，调用共享的运动、感知与状态工具，也可复用从历史执行记录提炼的任务 Skills。

**具体方法：** HexaShell 把通用的 Agent 循环、Python 沙箱和机器人 API 固定下来，用适配器处理不同模拟器与机械臂。任务经验可以写成短 Skills，说明成功条件、可行步骤和参数。这样可以分别比较通用接口的迁移能力，以及增加任务经验后究竟改善了哪些失败。

**验证：** 代码执行返回打印输出、表达式结果、异常和请求的图像；机器人 API 返回测量及动作结果，模型据此检查目标、调整参数或重写下一段代码。

**关联：** [5. 训练与能力提升](#section-5)

<a id="work-2610-13862"></a>
<!-- stage3-record: {"id": "2610.13862", "scope": "Adjacent", "section": 1} -->

#### BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation

`2026-10-09` · Stanford University; University of California, Berkeley; NVIDIA

[完整书目](../README.zh-CN.md#paper-2610-13862) · [论文](https://arxiv.org/abs/2610.13862)

通过固定行为树 Skill 组织感知与物理动作工具，以结构化失败反馈重试或改变任务决策，本地 Guard 则监督经操作员批准的机载运动。

**验证：** 文本／Habitat 任务对齐 · 感知与运动失败 · 真机任务完成 · Guard 中断 · 接口／反馈消融。

<a id="work-2610-12457"></a>
<!-- stage3-record: {"id": "2610.12457", "scope": "Adjacent", "section": 1} -->

#### SpatialHarness: Test-Time Spatial Scaffolding for Fine Robotic Manipulation

`2026-10-08` · Fudan University; Singapore Management University

[论文](https://arxiv.org/abs/2610.12457) · [项目页](https://emilia113.github.io/SpatialHarness/)

维持与真实执行同步的模拟场景，按任务需要渲染补充视角，为冻结的多模态机器人策略提供空间支架。

**具体方法：** SpatialHarness 为操控中的模型维护一个随现实观测更新的数字场景。它先对齐对象与布局，再结合物理推进、视觉对照和程序约束纠正状态，并渲染任务需要的观察角度。特色是让数字模型服务当前动作判断，因此与现实重建交叉，但阅读重点仍是空间信息怎样改善操作决策。

**验证：** 动作后用新观测修正数字场景，向模型提供更新的物体位姿和补充视角；模型据此检查遮挡、空间关系与操作位置，再决定下一步。

<a id="work-2610-04929"></a>
<!-- stage3-record: {"id": "2610.04929", "scope": "Adjacent", "section": 1} -->

#### RobotUse: Allocating Computation, Context, and Decisions

`2026-10-04` · KAIST; Seoul National University

[论文](https://arxiv.org/abs/2610.04929) · [项目页](https://robotuse-team.github.io/)

围绕物理动作组织计算、上下文与决策，并用持久执行手册积累机器人 Agent 的任务经验。

**具体方法：** RobotUse 关注接口把哪些物理选择留给 Agent。例如抓杯子时，只调用内部自动选最高分抓取的函数，模型未必能决定抓哪里；它因此把候选与姿态显式交给 Agent 选择和修订。底层几何计算继续由后端完成，任务语义相关的选择则保留在模型一侧。

**验证：** 候选姿态与执行结果可供视觉检查；局部详细交互保存在子 Agent 上下文，主 Agent 接收任务结果、当前状态和仍未解决的约束。

**关联：** [5. 训练与能力提升](#section-5)

<a id="work-2610-02459"></a>
<!-- stage3-record: {"id": "2610.02459", "scope": "Core", "section": 1} -->

#### OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies

`2026-10-01` · University College London; Carnegie Mellon University

[论文](https://arxiv.org/abs/2610.02459) · [代码](https://github.com/terminalworld/OpenRUA)

仅向现成 Coding Agent 提供终端、ROS 2 文档与机器人工作区，检验直接编程使用原生机器人接口的零样本能力。

**具体方法：** OpenRUA 把机器人视作一个可探索的软件工作区：提供原生 ROS 2 接口、文档和可修改的起始工具，而不预先规定完整任务流程。模型既能复用已有脚本，也能编写新的反馈控制逻辑。它与固定工具菜单的区别在于，Agent 可以沿原生接口扩展自己的操作方法。

**验证：** 图像文件、传感器读数、命令输出和运行错误进入工作区与 Agent 上下文；Agent 可据此修改脚本，也可让脚本在运动中读取力或位置反馈。

<a id="work-2610-01939"></a>
<!-- stage3-record: {"id": "2610.01939", "scope": "Core", "section": 1} -->

#### Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens

`2026-10-01` · Peking University; National University of Singapore; NVIDIA; Impossible Research

[论文](https://arxiv.org/abs/2610.01939)

让 Agent 在 Python 单元中组合机器人原语、局部检查和重试，减少回传上下文，并探索小型编程模型的强化学习。

**具体方法：** PyRUA 同时改变执行粒度与观察粒度：可由程序处理的短循环在本地完成，需要模型重新判断时再回传证据。这样减少逐原语调用 LLM 和反复发送图像的开销。底层原语按配置可含学习式策略，因此核心比较点是程序组织与信息回传，而不只是“有没有写代码”。

**验证：** 中间动作结果可留在运行时供程序判断；只有选中的状态、文本和图像在代码块结束后进入 LLM 上下文，再用于整体重规划。

**关联：** [5. 训练与能力提升](#section-5)

<a id="work-2610-14018"></a>
<!-- stage3-record: {"id": "2610.14018", "scope": "Adjacent", "section": 1} -->

#### RoboHarness: A Simple Harness Outperforms VLA and World Action Models

`2026-09-29` · Zhejiang University

[论文](https://arxiv.org/abs/2610.14018)

给 LLM Agent 提供视觉几何控制面板，研究简单工具接口能否支持零样本机器人操作。

**验证：** 结果对应完整的 Harness 与模型配置，而非独立动作模型的能力。

<a id="work-2609-38078"></a>
<!-- stage3-record: {"id": "2609.38078", "scope": "Adjacent", "section": 1} -->

#### MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation

`2026-09-29` · University of Illinois Urbana-Champaign

[论文](https://arxiv.org/abs/2609.38078)

用中层动作、确定性控制和异步监测连接通用 VLM 与机械臂，考察推理频率与执行可靠性的关系。

**具体方法：** MotorMind 在顺序行动之外加入异步监测与记忆更新，使慢速模型推理期间也能跟踪执行进展。短程动作允许逐步纠正空间误差，完成判断与异常处理则避免把动作已发出等同任务已完成。它是冻结 VLM 的接口对照，不是代码生成系统。

**验证：** 相机图像、实际工具位姿和夹爪状态用于下一次决策；并行监测发现进展异常时可触发中断，子目标完成后还需要核验结果。

<a id="work-2609-29389"></a>
<!-- stage3-record: {"id": "2609.29389", "scope": "Adjacent", "section": 1} -->

#### Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation

`2026-09-24` · The Chinese University of Hong Kong; The Hong Kong University of Science and Technology (Guangzhou); Knowin AI

[论文](https://arxiv.org/abs/2609.29389)

把三维感知作为可调用工具提供给 Robot-Use Agent，增强几何定位能力而不重新训练视觉编码器。

**具体方法：** K1 把操作拆成“获取空间信息”和“实际运动”两类步骤：前者不改变环境，可连续查询后再行动。持续的对象标识、空间锚点与候选姿态投影帮助模型跨视角理解同一目标；模型接收易读的图像和工具结果，不必直接处理稠密深度或点云。论文还用这种工具交互轨迹训练小模型；报告的验证为仿真。

**验证：** 测量返回标注图像、三维位置和候选抓取姿态；动作后返回新图像、实际位姿及目标误差，模型据此补测、微调或检查抓取是否成功。

<a id="work-2609-20822"></a>
<!-- stage3-record: {"id": "2609.20822", "scope": "Core", "section": 1} -->

#### Coding Agents with an Obstacle-Aware Harness for Safe Robot Manipulation

`2026-09-17` · University of Southern California; University of Central Florida; University of California, Santa Barbara

[完整书目](../README.zh-CN.md#paper-2609-20822) · [论文](https://arxiv.org/abs/2609.20822)

为 Code-as-policy Agent 增加视觉定位的路径检查与接触约束，并在执行遭遇障碍或未建模物理限制时，根据观测到的停止位姿重新规划后续动作。

**具体方法：** SafeHarness 将问题分成两段：到目标的途中是否安全，以及靠近目标后的接触行为是否安全。路径检查需考虑夹爪及被抓物体的占据范围，接触阶段则使用单独的执行约束。两段分别处理，因为一条无碰撞到达路径并不能保证后面的推、拉或抓取也安全。

**验证：** 外部检查给出路径是否侵入障碍区域，执行阶段提供接触与动作结果；Agent 据此重规划或改变操作方式，不能把“提示过安全”当作已经验证。

<a id="work-2609-12541"></a>
<!-- stage3-record: {"id": "2609.12541", "scope": "Core", "section": 1} -->

#### Agent as Policy for Robotic Manipulation

`2026-09-11` · University of Notre Dame; University of California San Diego; San Diego State University

[论文](https://arxiv.org/abs/2609.12541)

让通用 Agent 持续读取视觉证据、编写程序并发出运动指令，根据物理执行结果调整下一步行动。

**验证：** 后续决策依赖物理执行结果，具体观测和动作接口决定评测设置。

<a id="work-2609-10522"></a>
<!-- stage3-record: {"id": "2609.10522", "scope": "Adjacent", "section": 1} -->

#### Show-Harness: Just a VLM Agent Can Play Robots

`2026-09-09` · Show Lab, National University of Singapore

[论文](https://arxiv.org/abs/2609.10522) · [项目页](https://showlab.github.io/Show-Harness)

以紧凑语义动作接口连接通用 VLM 与机器人解释器，研究将数字 Agent 式交互迁移到物理控制的条件。

**验证：** 接口将运动实现委派给下游模块；模型推理与底层控制承担不同职责。

<a id="work-chemautoagent"></a>
<!-- stage3-record: {"id": "chemautoagent", "scope": "Adjacent", "section": 1} -->

#### ChemAutoAgent: A Multi-Agent System for Evidence-Controlled Laboratory Instrument Driver Generation from Text-Based Manuals

`2026-08-20` · 单位未明确

[论文](https://www.mdpi.com/2076-3417/16/16/8291) · [论文](https://www.mdpi.com/2076-3417/16/16/8291/notes)

让 Agent 从带出处的设备手册生成驱动内容，在确定性协议骨架和硬件测试中修复错误，再把可复用接口提供给后续实验 Agent。

**验证：** §3.2、3.6：三种真实仪器测试，人工确认参与；直接生成基线未做同等硬件测试，不能把其命令检查与多 Agent 实测视为同一协议。文中代码开放承诺不等于已核实数据集发布。

<a id="work-2608-03924"></a>
<!-- stage3-record: {"id": "2608.03924", "scope": "Adjacent", "section": 1} -->

#### ETA: A New Agentic Paradigm for Embodied Tasks

`2026-08-04` · Shanghai Innovation Institute; Fudan University; Jilin University; Nanjing University; Zhejiang University

[论文](https://arxiv.org/abs/2608.03924)

通过 OpenETA 将观察、标记目标与运动能力接入 Codex 等数字 Agent，研究轻量接口如何支持物理任务。

**具体方法：** OpenETA 明确区分提出操作的 Agent、负责检查与派发的 Interface，以及实际执行的 World。最重要的运行约定是“一次改变世界的操作之后，先重新观察，再作依赖状态的决定”。完整系统与 Codex 轻量插件是不同配置，后者以少量观察、指点和运动工具接入现成 Agent。

**验证：** 每次改变环境后，执行回执与新观测必须先进入上下文，才能继续依赖当前状态的动作；观测失败或执行状态未知时，不能沿用旧画面盲目推进。

<a id="work-2607-16636"></a>
<!-- stage3-record: {"id": "2607.16636", "scope": "Adjacent", "section": 1} -->

#### PhyAgentOS: A Self-Evolving Operating System for Embodied Agents with Decoupled Cognitive Planning and Physical Execution

`2026-07-18` · X-Era Lab; Sun Yat-sen University; Peng Cheng Laboratory

[论文](https://arxiv.org/abs/2607.16636)

用文件化状态契约分离 Agent 推理与机器人执行，让工具调用、状态记录和经验更新能够跨运行层衔接。

**验证：** 需要明确哪些状态与经验跨越运行时边界，实际到达 Agent。

<a id="work-2607-05369"></a>
<!-- stage3-record: {"id": "2607.05369", "scope": "Adjacent", "section": 1} -->

#### GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks

`2026-07-06` · University of California, Berkeley; Bosch; NVIDIA

[论文](https://arxiv.org/abs/2607.05369) · [项目页](https://graph-robots.github.io/gap)

由多 Agent 编写连接感知、规划与控制节点的计算图，以可组合机器人技能库支持可变自动化任务。

**具体方法：** GaP 把策略表示为可检查、可修改的计算图，让技能之间的数据依赖与执行关系显式化。它面对的是已知工作单元及一定范围的对象和初始状态，希望得到可以反复运行的自动化方案。内部仿真用于排演和改图，不能据此认为它解决了任意未知现实环境的重建。

**验证：** 内部仿真执行图后返回任务结果与问题，Agent 在部署前据此修订；优化后的图由解释器在机器人上重复执行，不要求每次动作都调用 LLM。

<a id="work-2605-26637"></a>
<!-- stage3-record: {"id": "2605.26637", "scope": "Adjacent", "section": 1} -->

#### Enabling Extensible Embodied Capabilities with Tools

`2026-05-26` · Huazhong University of Science and Technology; Hebei University of Technology; Tianjin University; Lehigh University; Tsinghua University

[论文](https://arxiv.org/abs/2605.26637)

提出 Embodied Tool Protocol，将机器人感知、推理与执行能力统一为可注册、发现和调用的工具，支撑 Agent 组合现有能力。

**验证：** 协议暴露已有能力；任务是否成功仍取决于接入的 Agent 和工具。

<a id="work-2511-00917"></a>
<!-- stage3-record: {"id": "2511.00917", "scope": "Core", "section": 1} -->

#### MAESTRO: Orchestrating Robotics Modules with Coding Agents for Zero-Shot Generalist Robots

`2025-11-02` · University of Pennsylvania

[论文](https://arxiv.org/abs/2511.00917) · [项目页](https://maestro-robot.github.io) · [代码](https://github.com/penn-pal-lab/maestro)

让 VLM 编写机器人程序来组织感知、规划和控制模块，通过视觉与执行反馈验证结果及恢复失败。

**具体方法：** MAESTRO 研究的核心是工具增加后怎样仍然可靠使用：封装容易出错的模块链，提供组合示例，并加入可视化检查、缓存和执行监测。模型通过“计划—执行—检查—重规划”组织这些能力。主比较不调用 VLA；另有把 VLA 包装成可监测、可停止工具的扩展。

**验证：** 真实机器人测试覆盖 Franka／DROID 平台上的八项桌面任务，以及 Go2-W 搭载 PiPER 机械臂的四项移动操作任务，每项使用五种设置。人工评审独立于 Agent 监测器评分任务进展。桌面对照和工具／Harness 消融不调用 VLA 工具；移动测试没有竞争基线，跨回合改进另以案例研究展示。

<a id="work-2510-21302"></a>
<!-- stage3-record: {"id": "2510.21302", "scope": "Adjacent", "section": 1} -->

#### Towards Reliable Code-as-Policies: A Neuro-Symbolic Framework for Embodied Task Planning

`2025-10-24` · Sungkyunkwan University

[论文](https://arxiv.org/abs/2510.21302)

将机器人策略代码生成与符号验证结合，通过探索程序补全缺失观测并验证行动条件。

**验证：** 验证依赖建模所覆盖的条件和实际观测证据，不能保证所有物理执行结果。

<a id="work-2505-07532"></a>
<!-- stage3-record: {"id": "2505.07532", "scope": "Adjacent", "section": 1} -->

#### RAI: Flexible Agent Framework for Embodied AI

`2025-05-12` · Robotec.AI; Warsaw University of Technology

[论文](https://arxiv.org/abs/2505.07532)

以模块化工具接口把语言模型、多 Agent、ROS 与仿真连接起来，为机器人 Agent 提供可复用的运行基础。

**验证：** 理解演示结果时，需要结合实际接入的工具和机器人配置。

<a id="work-2503-21969"></a>
<!-- stage3-record: {"id": "2503.21969", "scope": "Core", "section": 1} -->

#### Robotic Long-Horizon Manipulation with Progressive In-Context Code Generation and Episodic Feedback

`2025-03-27` · Technical University of Munich; Ludwig Maximilian University of Munich; Beijing Academy of Artificial Intelligence; Nanjing University

[论文](https://arxiv.org/abs/2503.21969)

用递进式上下文生成机器人程序，再由视觉报告器在每轮执行后总结结果并指导重规划。

**验证：** 整段程序执行结束后才由 VLM 报告并修订，不能描述为每个动作都获得闭环反馈。

<a id="work-2412-04455"></a>
<!-- stage3-record: {"id": "2412.04455", "scope": "Adjacent", "section": 1} -->

#### Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection

`2024-12-05` · Beihang University; Peking University; Beijing Academy of Artificial Intelligence; Galbot

[论文](https://arxiv.org/abs/2412.04455) · [项目页](https://zhoues.github.io/Code-as-Monitor/)

让 VLM 编写可执行的时空约束监测程序，利用视觉跟踪检查机器人执行中的失败和潜在违规。

**具体方法：** Code-as-Monitor 把“不要让面包掉出锅”等语言要求转成可持续运行的时空约束检查。它连接约束生成、视觉定位和代码监测，使执行过程中的问题能被及时发现。生成的产物主要是监测器，因此可附加到不同动作执行路径，而不是第三种操控流程。

**验证：** 视觉模块把相关物体或部件定位为三维几何元素，跟踪结果进入监测器；检测到违反约束后，将失败原因交给上层重新规划。

<a id="work-bounded-motion"></a>
<!-- stage3-record: {"id": "bounded-motion", "scope": "Adjacent", "section": 1} -->

#### Language-guided Manipulator Motion Planning with Bounded Task Space

`2024-10-11` · 单位未明确

[项目页](https://proceedings.mlr.press/v270/oelerich25a.html) · [项目页](https://www.acin.tuwien.ac.at/42d2/)

让语言模型根据视觉信息编写 Python 调用受约束路径规划器，再由 BoundMPC 执行平滑轨迹，连接语义推理与机器人运动约束。

**验证：** 包含模拟和实体机械臂实验；路径与轨迹约束由规划器承担，不能归为模型自身学会底层动力学。

<a id="work-2410-06472"></a>
<!-- stage3-record: {"id": "2410.06472", "scope": "Adjacent", "section": 1} -->

#### Enabling Novel Mission Operations and Interactions with ROSA: The Robot Operating System Agent

`2024-10-09` · NASA Jet Propulsion Laboratory; California Institute of Technology

[论文](https://arxiv.org/abs/2410.06472)

将 ROS 查询、诊断与操作封装为语言 Agent 可调用的工具，支持不同机器人平台的自然语言任务交互。

**验证：** 能力范围取决于已接入工具和展示的任务；仅有 ROS 工具桥不能证明自主恢复能力。

<a id="work-2312-04474"></a>
<!-- stage3-record: {"id": "2312.04474", "scope": "Adjacent", "section": 1} -->

#### Chain of Code: Reasoning with a Language Model-Augmented Code Emulator

`2023-12-07` · Stanford University; Google DeepMind; University of California, Berkeley

[论文](https://arxiv.org/abs/2312.04474) · [项目页](https://chain-of-code.github.io)

用解释器执行明确的程序逻辑，并把未定义的语义计算交给语言模型模拟；机器人实验展示代码与模型调用的组合方式。

**验证：** 除通用推理实验外，附录有实体机器人任务；本目录只引用其机器人代码/API 使用贡献。

<a id="work-2306-09523"></a>
<!-- stage3-record: {"id": "2306.09523", "scope": "Adjacent", "section": 1} -->

#### Tell Me Where to Go: A Composable Framework for Context-Aware Embodied Robot Navigation

`2023-06-15` · University of Colorado Boulder

[论文](https://arxiv.org/abs/2306.09523)

用生成的 Python 中间层连接语言推理、视觉环境描述和移动机器人导航接口，支持依赖上下文的导航指令。

**验证：** 情境相关的导航任务检验的是组合系统，不表示 LLM 内部学习了底层运动控制。

<a id="work-2305-11176"></a>
<!-- stage3-record: {"id": "2305.11176", "scope": "Adjacent", "section": 1} -->

#### Instruct2Act: Mapping Multi-modality Instructions to Robotic Actions with Large Language Model

`2023-05-18` · Shanghai Jiao Tong University; Shanghai AI Laboratory; University of Chinese Academy of Sciences; Peking University; The Chinese University of Hong Kong

[论文](https://arxiv.org/abs/2305.11176) · [代码](https://github.com/OpenGVLab/Instruct2Act)

由 LLM 生成 Python 程序，调用 SAM、CLIP 与动作 API，把多模态指令组织成感知、规划和执行流程。

**具体方法：** Instruct2Act 用代码把多模态指令与已有机器人能力连接起来：视觉模块负责找到对象，程序负责组合处理步骤，控制器负责运动。其特色是利用现成模型与 API 完成感知到动作的衔接，无需为每条新指令重新训练整套操控策略。

**验证：** 在 PyBullet 中测试六项选定的 VIMABench 桌面元任务，覆盖 L1 摆放、L2 组合和 L3 新物体泛化。成功依据最终仿真状态判断，另比较指令模态、提示组成和感知模型。报告的实验仅限仿真并受所提供动作原语限制，不能据此证明行动后的视觉代码修复。

<a id="work-2306-17582"></a>
<!-- stage3-record: {"id": "2306.17582", "scope": "Adjacent", "section": 1} -->

#### ChatGPT for Robotics: Design Principles and Model Abilities

`2023-02-20` · Scaled Foundations; Microsoft Autonomous Systems and Robotics Research

[论文](https://arxiv.org/abs/2306.17582) · [项目页](https://www.microsoft.com/en-us/research/publication/chatgpt-for-robotics-design-principles-and-model-abilities/)

通过函数库、提示设计和人机对话，让 ChatGPT 为机械臂、无人机与移动机器人编写和修改任务程序。

**具体方法：** 这份早期技术报告探索怎样用清晰的机器人函数命名、接口文档和交互提示，让通用语言模型编写机器人程序。机械臂、无人机等案例展示了同一种编程式使用方式；其中人的检查与反馈是实际流程的一部分，不能省略成完全自主执行。

**验证：** 不同案例把用户纠正、仿真测试或机器人执行结果带回对话。需要逐例区分自动返回的状态与人工观察后给出的意见。

<a id="work-2209-11302"></a>
<!-- stage3-record: {"id": "2209.11302", "scope": "Adjacent", "section": 1} -->

#### ProgPrompt: Generating Situated Robot Task Plans using Large Language Models

`2022-09-22` · University of Southern California; NVIDIA

[论文](https://arxiv.org/abs/2209.11302) · [项目页](http://progprompt.github.io)

用可用动作、对象和断言组织程序式提示，使语言模型生成能够检查前置条件并恢复的机器人任务计划。

**具体方法：** 它把环境能做什么直接写进提示中的函数与对象定义，让生成的计划受实际接口约束。计划中的断言还能把“先确认前提，再执行动作”写成可执行逻辑。关键贡献是计划的落地与前提检查，恢复能力取决于生成计划覆盖了哪些情况。

**验证：** 执行时检查动作前提是否成立，例如抓取前是否已靠近目标；不成立时运行计划中的恢复步骤。论文也指出，动作成功反馈并未全面提供给 Agent。

<a id="work-2209-07753"></a>
<!-- stage3-record: {"id": "2209.07753", "scope": "Adjacent", "section": 1} -->

#### Code as Policies: Language Model Programs for Embodied Control

`2022-09-16` · Robotics at Google

[论文](https://arxiv.org/abs/2209.07753) · [项目页](https://code-as-policies.github.io)

用语言模型递归生成 Python 策略，组合感知结果、几何计算与控制 API，是机器人 Code-as-Policy 的早期基础；程序内反馈不等于写码模型根据执行结果重写程序。

**具体方法：** 核心是把机器人策略表示成可组合的程序：条件、循环、几何运算和函数调用共同表达任务逻辑。模型生成的代码连接语言意图与机器人已有能力，底层感知和运动执行仍由接口提供。它为后来的交互式 Coding Agent 提供了程序表示基础；不同实验使用的控制原语粒度并不相同。

**验证：** 生成程序读取感知模块返回的位置等信息，并据此计算下一条控制指令。这里主要是程序在使用反馈，不能等同于 LLM 每次行动后重新看图改代码。

### 委派已有策略

<a id="work-2611-03585"></a>
<!-- stage3-record: {"id": "2611.03585", "scope": "Adjacent", "section": 1} -->

#### Seeing Through the Illusion: Test-Time Scaling for World Action Models

`2026-11-02` · Huawei Technologies Canada; University of British Columbia

[完整书目](../README.zh-CN.md#paper-2611-03585) · [论文](https://arxiv.org/abs/2611.03585)

组合动作有效性、想象运动的逆动力学一致性与任务进度，为冻结世界—动作模型选择候选轨迹，执行动作块后依据新观测重规划。

**具体方法：** 组合动作有效性、逆动力学与想象运动的一致性、任务进度三类信号，为冻结的世界—动作模型选择候选轨迹。执行选定的动作块后获取新观测并重规划；改变的是推理时的选择过程，模型保持冻结。

**验证：** RoboLab：50仿真回合 · LIBERO：每方法2,000回合 · 同为四候选的比较 · 组件与运行耗时分析；相对同预算最强选择器的提升较小。

<a id="work-system-the-harness-corl2026"></a>
<!-- stage3-record: {"id": "system:the-harness-corl2026", "scope": "Adjacent", "section": 1} -->

#### The Harness: One Agent Harness for Anything that Acts

`2026-11` · University of Michigan; Nanyang Technological University; EPFL; Princeton University; University of Virginia; LMMs-Lab

[项目页](https://web.eecs.umich.edu/~stellayu/publication/2026harnessCoRLL.html) · [论文](https://web.eecs.umich.edu/~stellayu/publication/doc/2026harnessCoRLL.pdf)

把 Agent 编写的程序、有界 VLA 技能和快速反应守卫组合成共享控制层级。

**具体方法：** 程序组合解析工具和托管策略；生成的守卫在控制周期运行，无法处理的事件再返回模型，由固定检查层拒绝无效命令。

**验证：** 验证来自 RoboDojo 仿真与组件消融；短报告支持事件驱动的编排机制，尚不足以建立完整代码修复轨迹。

<a id="work-2610-42053"></a>
<!-- stage3-record: {"id": "2610.42053", "scope": "Adjacent", "section": 1} -->

#### REA: A Routed Embodied Agent Runtime for Asynchronous Brain-Cerebellum Control

`2026-10-30` · National University of Singapore, HPC-AI Lab; InfRec, Cardinal AI Lab; University of California, Berkeley; The University of Tokyo; Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences; Hong Kong University of Science and Technology

[完整书目](../README.zh-CN.md#paper-2610-42053) · [论文](https://arxiv.org/abs/2610.42053) · [项目页](https://mikeeeeeeeeeeeeee.github.io/REA/)

将快速机器人执行与异步模型判断、路径选择分离，在策略返回边界通过视觉结果检查协调固定代码策略和动作模型。

**具体方法：** REA 让快速策略按自身控制频率运行，避免每个动作都等待慢速大模型。REA-M 用路由记忆且没有在线上层模型；REA-A 调用 Agent 选择策略；REA-V 在策略返回时用视觉判断结果。三个配置的比较说明上层推理在哪里有用，不能把它们统一写成持续在线编程。

**验证：** 策略返回消耗的步数、耗时、异常与截断状态，视觉判断配置还检查结果图像；运行时据此结束任务或升级到下一种恢复策略。

<a id="work-2610-21453"></a>
<!-- stage3-record: {"id": "2610.21453", "scope": "Adjacent", "section": 1} -->

#### CarryOn: A Dual-Loop Harness for Personalized and Reliable Robot Assistance

`2026-10-15` · Hong Kong University of Science and Technology; The Chinese University of Hong Kong; SmartMore

[完整书目](../README.zh-CN.md#paper-2610-21453) · [论文](https://arxiv.org/abs/2610.21453) · [项目页](https://vincent2311.github.io/Projects/CarryOn/) · [代码](https://github.com/JIA-Lab-research/CarryOn)

协调持久用户／场景记忆、冻结 VLA、几何安全过滤与视觉失败恢复，并通过离线反思修订恢复策略和参数，供后续尝试复用。

**具体方法：** CarryOn 有两条互相配合的循环：规划循环判断“当前还应当做什么”，执行循环处理“这个操作怎样可靠完成”。恢复操作常用于把现场恢复到 VLA 能继续工作的条件。记忆改善以后的计划，失败经验改善恢复技能；两者都不等于训练底层 VLA 权重。

**验证：** 视觉 Judge 检查子任务结果，几何检查拦截危险动作；失败轨迹进入事后反思，分别更新用户／场景记忆和经过版本管理的恢复技能。

<a id="work-2609-29166"></a>
<!-- stage3-record: {"id": "2609.29166", "scope": "Core", "section": 1} -->

#### HarnessPAI: An Evolving Harness for Physical AI

`2026-09-24` · Xiaomi Inc.; Tsinghua University; Nanjing University; Shanghai Jiao Tong University; East China Normal University; University College London; King’s College London; Imperial College London; Institute of Automation, Chinese Academy of Sciences; Shanghai Innovation Institute; University of Oxford; University of Edinburgh; Nanyang Technological University

[论文](https://arxiv.org/abs/2609.29166) · [项目页](https://darwin-agent.github.io/HarnessPAI)

以可执行代码组织底层动作原语，并依据交互反馈演化机器人程序，使稳定程序还能生成下游策略训练数据。

**具体方法：** HarnessPAI 将两种时间尺度分开：一次 rollout 内运行固定程序，跨 rollout 再改进程序。这里的“固定”不代表没有传感器反馈，程序内部仍可检查物理状态。任务记忆、修复技能和可执行代码分别积累，使后续任务可以复用已验证的执行方法。

**验证：** 同一次执行中，程序根据观察检查抓取或放置是否成立，再决定是否推进；执行结束后的轨迹与失败信息才用于下一轮改程序和整理技能。

**关联：** [5. 训练与能力提升](#section-5)

<a id="work-2608-11246"></a>
<!-- stage3-record: {"id": "2608.11246", "scope": "Adjacent", "section": 1} -->

#### Towards the Harness of Embodied Agents

`2026-08-03` · Eastern Institute of Technology, Ningbo

[论文](https://arxiv.org/abs/2608.11246) · [项目页](https://eit-hai.github.io/thea)

用持久场景图和带成功、失败原因的执行返回值，将机器人能力组织为 Agent 可理解和调用的工具。

**具体方法：** Thea 把 Coding Agent 的工具、上下文、Skills 与记忆组织方式迁移到机器人，并补上物理执行需要的状态与结果语义。区别不只在统一函数名，而在让模型知道一次调用在世界里实际发生了什么。工具可以包装已有代码策略；知识型 Skill 与真正执行动作的策略需要分开理解。

**验证：** 模型每轮读取最新观测、持久场景信息和带语义的执行结果，判断是否成功、失败原因以及下一步；上下文和记忆管理控制哪些历史继续保留。

<a id="work-2607-08448"></a>
<!-- stage3-record: {"id": "2607.08448", "scope": "Adjacent", "section": 1} -->

#### Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents

`2026-07-09` · Tsinghua University; Striding AI; Purdue University; Institute of Automation, Chinese Academy of Sciences; Infinigence AI; Hong Kong University of Science and Technology; Zhongguancun Academy

[论文](https://arxiv.org/abs/2607.08448)

让 Coding Agent 编排冻结 VLA 与解析动作原语

**具体方法：** Harness VLA 把已有 VLA 封装成与其他运动原语并列的工具。Agent 可以先用解析操作准备场景，再把接触操作交给 VLA，失败后重新安排；任务记忆与通用经验支持后续选择。这里可直接用语言委派，不需要先生成新的控制程序，学习式动作能力仍来自冻结的下游策略。

**验证：** 工具返回后，上层得到图像、深度、机器人状态与执行诊断，决定继续、调整物体或重新设置条件；VLA 内部也用自己的观测持续控制。

### Agent 能力评测

<a id="work-2611-12177"></a>
<!-- stage3-record: {"id": "2611.12177", "scope": "Adjacent", "section": 1} -->

#### Embodied First Exam

`2026-11-09` · Northwestern University; Carnegie Mellon University; University of California Berkeley; University of Washington; Stanford University; UNC-Chapel Hill; Texas A&M University; University of Texas at Austin

[论文](https://arxiv.org/abs/2611.12177) · [论文](https://arxiv.org/html/2611.12177)

跨机器人形态检验通用 Agent 的具身任务能力，明确比较观测权限、重置预算和执行时钟不同的运行方式。

**具体方法：** 允许直接动作、控制程序或学习得到的策略。Standard 通过独立仿真服务提供 RGB-D、本体感知与动作块；Realtime 持续计时；Privileged 开放完整状态与不限次数重置，再由独立回放评测。

**验证：** Standard 不向 Agent 开放隐藏判定逻辑和场景源码，但大多数套件仍返回完成信号；去掉成功信号是单独消融。不同策略和信息权限须分开读，视觉反馈并不说明每条轨迹都发生代码修订。

**关联：** [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2611-08209"></a>
<!-- stage3-record: {"id": "2611.08209", "scope": "Adjacent", "section": 1} -->

#### RoboARCade: Benchmarking Agentic Robot Control

`2026-11-05` · Stanford University

[完整书目](../README.zh-CN.md#paper-2611-08209) · [论文](https://arxiv.org/abs/2611.08209) · [项目页](http://roboarcade.org)

在随机化长程 MuJoCo 任务上评测视觉机器人控制 Agent，分别比较接口、上下文示范和跨尝试文本工作流优化。

**验证：** 22 任务、三种机器人形态、隐藏任务判据、控制成本与误报成功分析，以及五任务适应实验；属于仿真控制和工作流更新。

<a id="work-2611-02497"></a>
<!-- stage3-record: {"id": "2611.02497", "scope": "Adjacent", "section": 1} -->

#### RoboColosseum: Evaluating Physical Intelligence at Scale In-The-Wild

`2026-11-02` · National University of Singapore; University of Washington; Stanford University; University of North Carolina at Chapel Hill; Allen Institute for AI; University of Oxford; Hugging Face; BitRobot; Singapore Embodied AI Centre

[完整书目](../README.zh-CN.md#paper-2611-02497) · [论文](https://arxiv.org/abs/2611.02497) · [项目页](https://robocolosseum.ai/) · [仓库](https://github.com/RoboColosseum)

通过跨站点、条件匹配的盲测实机试验比较冻结 Agent 与 VLA，并另设适配赛道分析不同机器人上的排名变化。

**验证：** 多地点实机操作协议与人为复位/评价需保留；Agent 和 VLA 的轨迹来源不可混成同一种训练数据。

<a id="work-2610-34649"></a>
<!-- stage3-record: {"id": "2610.34649", "scope": "Core", "section": 1} -->

#### RobotAgentBench: Towards Open-world Robot Autonomy

`2026-10-26` · Aether AI; University of California San Diego; University of California Davis

[完整书目](../README.zh-CN.md#paper-2610-34649) · [论文](https://arxiv.org/abs/2610.34649) · [项目页](https://aetherlabsai.github.io/RobotAgentBench/)

通过任务发现、情境推理、物理执行与恢复环节评估开放世界机器人 Agent，而不仅测试给定目标的动作成功率。

**验证：** 50 个仿真布局、五项任务能力与四类开放场景、配对仿真／实机子集及 Harness 消融；Coding Agent 与独立策略分轨评估，场景校准有人类协助。

<a id="work-2610-34527"></a>
<!-- stage3-record: {"id": "2610.34527", "scope": "Adjacent", "section": 1} -->

#### LLM4Robot-Bench: How Far Can GPT-6 Astra Go in Robotic Manipulation? A Hierarchical, Paired Sim-Real Benchmark

`2026-10-25` · Tuojing Intelligence; The University of Hong Kong; Chinese Academy of Sciences; Nanyang Technological University; University of Michigan, Ann Arbor; Southeast University; Sapient Intelligence; SimpleAI; Mohamed bin Zayed University of Artificial Intelligence; Stanford University; Imperial College London; Tsinghua University; Carnegie Mellon University

[完整书目](../README.zh-CN.md#paper-2610-34527) · [论文](https://arxiv.org/abs/2610.34527) · [代码](https://github.com/LLM4Robot/LLM4Robot-Bench) · [项目页](https://llm4robot.github.io/bench/)

在配对的仿真与真实双臂任务中，测量 GPT-6 Astra 在几何对齐、力调节和接触重配置中的表现，基准原名 PhysLadder。

**验证：** 配对仿真/实机任务；真实结果由人视觉判断且每任务试验数有限，不等同于自动可重复评分。

<a id="work-2610-30051"></a>
<!-- stage3-record: {"id": "2610.30051", "scope": "Adjacent", "section": 1} -->

#### From Reasoning to Action: Benchmarking Frontier AI Models on LIBERO-10 Robot Manipulation Tasks

`2026-10-21` · The University of Texas at Dallas

[论文](https://arxiv.org/abs/2610.30051) · [项目页](https://irvlutd.github.io/LLM-LIBERO/) · [代码](https://github.com/IRVLUTD/LLM_LIBERO)

在统一闭环与控制接口下比较前沿模型执行 LIBERO-10 操作任务的表现，避免把模型更换与接口更换混为一谈。

**验证：** 受控接口有助于区分模型差异与机器人 Harness 变化的影响。

<a id="work-2610-27039"></a>
<!-- stage3-record: {"id": "2610.27039", "scope": "Adjacent", "section": 1} -->

#### Embodied Playground: A Long-Horizon Agentic Robotics Benchmark for Physical, Strategic, and Spatial Reasoning

`2026-10-19` · The University of Hong Kong; Sharpa; Tsinghua University; Stanford University; University of North Carolina at Chapel Hill; Massachusetts Institute of Technology; Transcengram

[论文](https://arxiv.org/abs/2610.27039) · [项目页](https://winniechen2002.github.io/Agent-bench-website/)

以长时序机器人任务评测 Agent 如何协调物理、空间和策略推理，并在执行反馈下保持任务进度。

**验证：** 重点是任务进展与执行反馈；使用仿真环境不代表评测对象是模拟器质量。

<a id="work-2610-25287"></a>
<!-- stage3-record: {"id": "2610.25287", "scope": "Adjacent", "section": 1} -->

#### The Bitter Lesson Comes to Robotics

`2026-10-18` · Robocurve; University of Southern California; University of California, Irvine

[论文](https://arxiv.org/abs/2610.25287)

在物理机械臂上比较通用多模态模型通过控制接口执行任务的能力，观察模型、工具与执行设置对结果的影响。

**验证：** 在六项真实双臂 RoboDojo 任务上比较九个模型、15 种配置，每任务 20 次试验、每次最多 40 个动作。相机视频评分记录曾达到的最高累积子任务进展，即使后续被撤销也计入；耗时和 API 成本包含失败尝试。因此部分进展分不同于最终状态保持成功，预算内完整完成任务仍较困难。

<a id="work-2610-22471"></a>
<!-- stage3-record: {"id": "2610.22471", "scope": "Adjacent", "section": 1} -->

#### Has GPT-6-Astra Achieved Embodied Intelligence?

`2026-10-15` · SenseNova and Joint Research Team

[完整书目](../README.zh-CN.md#paper-2610-22471) · [论文](https://arxiv.org/abs/2610.22471) · [文章](https://sensenova.ai/has-gpt-6-astra-achieved-embodied-intelligence)

在十二项具身基准上研究示范辅助的直接控制与 VLA 动作审查，将扩大交互预算的收益与八种真实机器人配置上的零样本试验分别评估。

**验证：** 标准与最高十倍步数预算 · 冻结的上下文知识 · 动作接口与 token 成本消融 · 人类上下文／安全监督 · 实机接触、延迟与恢复限制。

<a id="work-2610-16238"></a>
<!-- stage3-record: {"id": "2610.16238", "scope": "Adjacent", "section": 1} -->

#### Embodied Skill Bench: Benchmarking How Well Agents with Embodied Skills Perform on Physical Tasks

`2026-10-12` · Shanghai Jiao Tong University; Shanghai Artificial Intelligence Laboratory; Sun Yat-Sen University; Jilin University; Beihang University

[论文](https://arxiv.org/abs/2610.16238) · [代码](https://github.com/HanZhi306/EmbodiedSkill-Bench)

在原生控制、仅用技能和 Agent 自主选择或修改技能三种条件下，评测具身 Skills 对物理任务的实际帮助。

**具体方法：** EmbodiedSkillBench 将“给 Agent 配什么能力”变成可比较的实验条件。技能包同时记录说明、脚本、参考知识和配置，模型、代码与经验可按需求组合。它比较不同 Agent 与 Skill 集合在相同任务协议下的表现，属于评测入口，不是单独提出一种动作控制算法。

**验证：** 统一观察与动作接口返回执行信息供 Agent 继续判断；评测器另记录任务成功、有效动作、token 和耗时，不能把所有评分信息当成 Agent 输入。

<a id="work-2610-10409"></a>
<!-- stage3-record: {"id": "2610.10409", "scope": "Adjacent", "section": 1} -->

#### RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments

`2026-10-07` · The Hong Kong University of Science and Technology; The Chinese University of Hong Kong; Peking University; Stanford University; University of California, Berkeley; National University of Singapore; Massachusetts Institute of Technology; Tsinghua University; Carnegie Mellon University; Fudan University; The University of Hong Kong

[完整书目](../README.zh-CN.md#paper-2610-10409) · [论文](https://arxiv.org/abs/2610.10409) · [代码](https://github.com/robotworldai/robotworld) · [项目页](https://robotworldai.github.io/)

在 84 项仿真任务和多种本体上评测图像、状态驱动的机器人工具使用，区分辅助计算与可选的环境侧控制代码。

**验证：** 隐藏验收任务成功率 · 行动／非行动预算 · 感知／控制失败 · 跨本体覆盖。

<a id="work-2610-07594"></a>
<!-- stage3-record: {"id": "2610.07594", "scope": "Adjacent", "section": 1} -->

#### BiGym 2.0: Benchmarking Learned and Agent-Developed Policies for Humanoid Household Manipulation

`2026-10-06` · Imperial College London

[论文](https://arxiv.org/abs/2610.07594) · [代码](https://github.com/swirl-uk/BiGym2)

在一致的机载观测和全身控制器下比较人形机器人学习策略与 Agent 开发的程序，并发布仿真中的人类 VR 示范。

**验证：** 本论文评测在仿真中进行；人类 VR 示范是仿真数据，不能列作真实机器人轨迹。

<a id="work-2610-00854"></a>
<!-- stage3-record: {"id": "2610.00854", "scope": "Adjacent", "section": 1} -->

#### Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena

`2026-10-01` · The Hong Kong University of Science and Technology (Guangzhou); The Chinese University of Hong Kong; Knowin AI

[论文](https://arxiv.org/abs/2610.00854) · [项目页](https://embodied-agent-arena.github.io/embodied-agent-arena/)

在统一预算与源任务接口下比较前沿 VLM Agent 的机器人通用性，并区分修复程序运行与完成物理任务。

**验证：** 将程序修复至可运行与完成物理任务分开评估。

<a id="work-2609-40325"></a>
<!-- stage3-record: {"id": "2609.40325", "scope": "Adjacent", "section": 1} -->

#### WorldAuditBench: Interactive 3D World Auditing with Multimodal Agents

`2026-09-30` · University of California Santa Barbara; MIT CSAIL; MIT-IBM Watson AI Lab

[完整书目](../README.zh-CN.md#paper-2609-40325) · [论文](https://arxiv.org/abs/2609.40325) · [论文](https://arxiv.org/html/2609.40325) · [项目页](https://ucsb-nlp-chang.github.io/WorldAuditBench/)

衡量 Agent 主动探索交互世界、发现异常并提供证据的能力，覆盖物理、空间、时间与语义问题。

**具体方法：** 比较由 VLM 选动作、检索观察并更新报告的交互审计，以及 VLA 探索后由 VLM 离线分析的两阶段流程；最终按 rubric 检查报告及其证据图像。

**验证：** 产物是审计报告而非修复后的场景代码。主设置含异常类型提示，两种流程使用不同探索预算；模型比较也包含所用 Harness 的影响。

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2609-39507"></a>
<!-- stage3-record: {"id": "2609.39507", "scope": "Adjacent", "section": 1} -->

#### LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation

`2026-09-30` · Fudan University; Shanghai Innovation Institute

[论文](https://arxiv.org/abs/2609.39507)

把 LIBERO 改造成通用 Agent 可主动检查观测、使用自己的工具并发出原生动作的交互测试环境。

**验证：** 在整合 200 项任务的框架中，30 项主要仿真任务区分感知、短程操作与长程组合。主实验提供完整观测、不提供示范，并设置 1,800 秒墙钟时限；Agent 组合有界原生动作序列，独立评测器保留私有任务判定。困难与长程任务表现下降，容易任务上的成功不代表广泛的操作可靠性。

<a id="work-2609-33807"></a>
<!-- stage3-record: {"id": "2609.33807", "scope": "Core", "section": 1} -->

#### CodeActionBench: Evaluating Agentic Code-as-Policy for Embodied Manipulation

`2026-09-27` · Nanyang Technological University

[完整书目](../README.zh-CN.md#paper-2609-33807) · [论文](https://arxiv.org/abs/2609.33807) · [代码](https://github.com/lyhkk/CodeActionBench) · [项目页](https://codeactionbench.org/)

在 RoboTwin 2.0 双臂仿真中，Agent 执行 Python 操控程序，根据相机画面、机器人状态和接触反馈修订策略。隐藏验收器独立核对最终状态和 Agent 的完成声明。

**具体方法：** CodeActionBench 同时检查代码能否执行、物理任务是否达到要求，以及完成声明是否可信。共享接口把观察、几何计算和受限运动提供给不同模型，任务仍需由模型自行组织。这里的“物理结果”来自仿真环境；固定初始场景的评测也不等同于验证广泛现实泛化。

**验证：** 动作结果、接触信息、机器人状态与新图像供 Agent 调整程序；隐藏验收器独立判断真实任务状态，并检查 Agent 是否错误地宣称完成。

<a id="work-2609-01404"></a>
<!-- stage3-record: {"id": "2609.01404", "scope": "Adjacent", "section": 1} -->

#### Evaluating Multimodal LLMs as Generalist Vision-Language-Action Agents for Drone Control: Commanding, Approaching, Tracking and Searching

`2026-09-01` · Drone AI Team, NAVER Cloud

[完整书目](../README.zh-CN.md#paper-2609-01404) · [论文](https://arxiv.org/abs/2609.01404) · [代码](https://github.com/naver-ai/DroneCATS) · [数据集](https://huggingface.co/datasets/naver-ai/DroneCATS-Pilot-54K)

在仿真器与真实 Tello 飞行中评测图像条件动作及指挥员—子 Agent 协作，分析延迟与到达声明失误。

**具体方法：** 测试多模态模型怎样根据视觉观察生成无人机动作，以及指挥员与子 Agent 如何协作。任务覆盖仿真和真实 Tello 飞行中的指令执行、接近、跟踪与搜索，并分别分析执行延迟和到达声明带来的失败。

**验证：** 十模型仿真评测、100次单机与18次双机实飞；每组样本较少，54K来自RGB-D的监督数据不等于真实飞行轨迹。

<a id="work-2607-04434"></a>
<!-- stage3-record: {"id": "2607.04434", "scope": "Resource", "section": 1} -->

#### RoboDojo: A Unified Sim-and-Real Benchmark for Comprehensive Evaluation of Generalist Robot Manipulation Policies

`2026-07-05` · MMLab@HKU; UC Berkeley; THU; PKU; Stanford; MIT; UNC; Princeton; CMU; NUS; NTU; CUHK; IC; SJTU; NU; HKUST (GZ); ZJU; Yale

[论文](https://arxiv.org/abs/2607.04434) · [项目页](http://robodojo-benchmark.com/) · [项目页](https://robodojo-benchmark.com/) · [代码](https://github.com/RoboDojo-Benchmark/RoboDojo) · [榜单](https://robodojo-benchmark.com/leaderboard)

提供统一仿真与实机操作评测协议，已被 CaPtain 等编程 Agent 研究用于检验跨任务和跨环境表现。

**验证：** 用于评估代码策略 Agent 的迁移表现；仿真分数与真实硬件成功率仍是不同指标。

<a id="work-2604-25788"></a>
<!-- stage3-record: {"id": "2604.25788", "scope": "Resource", "section": 1} -->

#### KinDER: A Physical Reasoning Benchmark for Robot Learning and Planning

`2026-04-28` · University of Cambridge; Georgia Institute of Technology; Princeton University; NVIDIA; Massachusetts Institute of Technology; Carnegie Mellon University

[论文](https://arxiv.org/abs/2604.25788) · [项目页](https://prpl-group.com/kinder-site/)

提供可重置的物理推理任务、参数化技能与统一评测接口，已被通用 Coding Agent 求解任务—运动规划的研究直接使用。

**验证：** 为 Coding Agent 的任务与运动规划研究提供评测支持，基准本身不是新的 Agent。

<a id="work-2603-22435"></a>
<!-- stage3-record: {"id": "2603.22435", "scope": "Core", "section": 1} -->

#### CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation

`2026-03-23` · NVIDIA; University of California, Berkeley; Stanford University; Carnegie Mellon University

[完整书目](../README.zh-CN.md#paper-2603-22435) · [论文](https://arxiv.org/abs/2603.22435)

评测并改进编写操作代码、执行、观察结果和修复失败行为的 Agent。

**验证：** 编译成功 · 稠密任务奖励 · 任务成功率 · 特权感知与 RGB-D 鲁棒性。

<a id="work-2601-20334"></a>
<!-- stage3-record: {"id": "2601.20334", "scope": "Adjacent", "section": 1} -->

#### Demonstration-Free Robotic Control via LLM Agents

`2026-01-28` · Independent researchers

[论文](https://arxiv.org/abs/2601.20334) · [代码](https://github.com/robiemusketeer/faea-sim)

将原用于软件工程的 Agent 框架直接接入机器人控制，在可读取特权环境状态的设置中评估免示范任务执行。

**验证：** 主要实验向 Agent 开放特权环境状态；不能直接与仅 RGB/RGB-D 的接口比较。

<a id="work-2601-19510"></a>
<!-- stage3-record: {"id": "2601.19510", "scope": "Adjacent", "section": 1} -->

#### ALRM: Agentic LLM for Robotic Manipulation

`2026-01-27` · Technology Innovation Institute; Dublin City University

[论文](https://arxiv.org/abs/2601.19510)

在同一 ReAct 框架下比较生成控制代码与逐步调用工具两种机器人执行模式，并提供语言多样化操作任务。

**验证：** 在语言表述变化的任务中比较执行接口；接口变化带来的影响不能完全归因于模型。

<a id="work-2402-14623"></a>
<!-- stage3-record: {"id": "2402.14623", "scope": "Adjacent", "section": 1} -->

#### RoboScript: Code Generation for Free-Form Manipulation Tasks across Real and Simulation

`2024-02-22` · OpenGVLab, Shanghai AI Laboratory; ETH Zurich; The University of Hong Kong; Shanghai Jiao Tong University; Tsinghua University; University of California, Berkeley

[论文](https://arxiv.org/abs/2402.14623)

把机器人代码生成接入 ROS、感知与运动工具，并以仿真和实机任务检验程序的可执行性与部署差距。

**具体方法：** RoboScript 把复杂机器人系统封装成面向对象的感知与运动 API。例如开抽屉时，程序先查询移动关节方向，再据此组织拉动路径；障碍处理和轨迹求解交给运动规划后端。特色是让 LLM 组合任务相关的几何信息，而不要求它重新实现底层机器人算法。

**验证：** 多视角 RGB-D 经工具转成三维对象信息，并更新规划场景；生成程序读取这些几何参数组织动作。执行验证与在线模型修订是需要分别判断的环节。

<a id="work-2311-11183"></a>
<!-- stage3-record: {"id": "2311.11183", "scope": "Adjacent", "section": 1} -->

#### Deploying and Evaluating LLMs to Program Service Mobile Robots

`2023-11-18` · The University of Texas at Austin; Northeastern University; Wellesley College

[论文](https://arxiv.org/abs/2311.11183) · [项目页](https://amrl.cs.utexas.edu/codebotler/)

提出 CodeBotler 与 RoboEval，用 Python 嵌入式领域语言生成服务机器人程序，并评测动作顺序、条件逻辑和任务执行。

**验证：** 程序有效性与真实物理执行成功是不同的结果。

<a id="work-2306-03310"></a>
<!-- stage3-record: {"id": "2306.03310", "scope": "Resource", "section": 1} -->

#### LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning

`2023-06-05` · The University of Texas at Austin; Sony AI; Tsinghua University

[论文](https://arxiv.org/abs/2306.03310) · [项目页](https://libero-project.github.io)

提供可重置的长期机器人学习任务、统一接口与示范，是 Code-as-Policy Agent 与后训练研究常用的执行和评测底座。

**验证：** 为代码策略 Agent 提供执行与评估环境；基准本身不是一种 Coding Agent 方法。

### Skills、工具桥与运行资源

<a id="work-kinex"></a>
<!-- stage3-record: {"id": "kinex", "scope": "Resource", "section": 1} -->

#### Kinex

`2026-10-15` · 单位未明确

[代码](https://github.com/stacx-lab/kinex)

把设备、工具、技能和会话执行组织成 Coding Agent 可使用的机器人运行层，并提供仿真与实机适配入口。

**验证：** 能力以适配器和已发布示例为边界；不把安装成功当作物理任务完成。

<a id="work-qwen-mhs"></a>
<!-- stage3-record: {"id": "qwen-mhs", "scope": "Resource", "section": 1} -->

#### Qwen-MM-Plugins — MHS

`2026-09-20` · 单位未明确

[代码](https://github.com/QwenLM/Qwen-MM-Plugins) · [项目页](https://qwenlm.github.io/qwen-mm-plugins-hub/plugins/mhs/cookbook/)

将物理硬件操作封装为多模态 Agent 插件，为 Qwen 等模型提供连接现实设备的能力入口。

**验证：** 这里只纳入 MHS 的物理硬件关联；不将整套通用多模态插件全部并入机器人目录。

<a id="work-safe-lab-agents"></a>
<!-- stage3-record: {"id": "safe-lab-agents", "scope": "Resource", "section": 1} -->

#### Safe Lab Agents

`2026-07` · 单位未明确

[代码](https://github.com/MaxNaeg/safe_lab_agents) · [项目页](https://safe-lab-agents.org/)

通过宿主机 MCP 与 Python 接口，让隔离环境中的 Coding Agent 编写扫描和分析脚本、调用实验工具，并保存结构化过程记录。

**验证：** README 和 example_setup/setup.py：公开光路示例的 measure_power 调用 simulate_experiment；这是可接入硬件的 Harness，不把此示例当实测。

<a id="work-2505-03728"></a>
<!-- stage3-record: {"id": "2505.03728", "scope": "Resource", "section": 1} -->

#### PyRoki: A Modular Toolkit for Robot Kinematic Optimization

`2025-05-06` · University of California, Berkeley

[论文](https://arxiv.org/abs/2505.03728) · [项目页](https://pyroki-toolkit.github.io)

以可组合的机器人运动学优化接口承接 Agent 生成的目标与程序，为部分 Coding Agent Harness 提供底层求解能力。

**验证：** 这是求解器资源；控制和优化能力不应归因于语言模型本身。

<a id="work-phys-0"></a>
<!-- stage3-record: {"id": "phys-0", "scope": "Resource", "section": 1} -->

#### phys-0

`首发日期未明确` · 单位未明确

[项目页](https://jvboid.dev/projects/phys-0) · [代码](https://github.com/JacobFV/chem-0)

用统一、带记录的工具接口连接 Coding Agent、可编辑物理场景、SO-101 机械臂和实验台观测，探索同一工作流中的虚拟与真实操作。

**验证：** 作者页区分录屏、真实相机帧和动画；仅 SO-101 为已验证硬件，虚拟模板仍有碰撞/CLI 问题；chem-0 试验方案还含人工预摆样品和揭晓步骤。

<a id="work-vbot-lab"></a>
<!-- stage3-record: {"id": "vbot-lab", "scope": "Resource", "section": 1} -->

#### VBOT Lab

`首发日期未明确` · 单位未明确

[代码](https://github.com/VitaDynamics/vbot-lab)

用 API、类型定义、程序样例与 Skills 为 Coding Agent 提供面向 VBOT 机器人的应用开发环境。

**验证：** 发布说明限定支持的 EDU 四足硬件和软件版本；不能外推到未发布的人形或轮足版本。

<a id="work-robotics-agent-skills"></a>
<!-- stage3-record: {"id": "robotics-agent-skills", "scope": "Resource", "section": 1} -->

#### Robotics Agent Skills

`首发日期未明确` · 单位未明确

[代码](https://github.com/arpitg1304/robotics-agent-skills)

以可复用技能文件提供 ROS 软件开发、诊断和机器人工作流知识，帮助 Coding Agent 组织工具与项目操作。

**验证：** 文档与技能内容可核查；不据单个提示示例宣称通用机器人性能提升。

<a id="work-robouse"></a>
<!-- stage3-record: {"id": "robouse", "scope": "Resource", "section": 1} -->

#### Robo Use

`首发日期未明确` · 单位未明确

[代码](https://github.com/benchflow-ai/robouse)

通过统一的命令行和 episode 服务，让 Coding Agent 访问机器人仿真任务、提交动作并读取结果。

**验证：** 当前接口与示例主要验证模拟任务；任务数量随仓库变化，不作为论文实验数引用。

<a id="work-rosclaw"></a>
<!-- stage3-record: {"id": "rosclaw", "scope": "Resource", "section": 1} -->

#### ROSClaw

`首发日期未明确` · 单位未明确

[代码](https://github.com/ros-claw/rosclaw)

把 Codex、Claude 等 Agent 接入 ROS 工作区，通过执行回执和状态接口组织机器人任务及程序运行。

**验证：** 项目处于 alpha 阶段；示例与已验证适配范围不能外推到所有实体机器人。

<a id="work-ros-mcp-server"></a>
<!-- stage3-record: {"id": "ros-mcp-server", "scope": "Resource", "section": 1} -->

#### ROS MCP Server

`首发日期未明确` · 单位未明确

[代码](https://github.com/robotmcp/ros-mcp-server)

向 Codex、Claude Code 等客户端开放 ROS 主题、服务、动作和传感图像，让 Agent 同时读取机器人状态并调用控制能力。

**验证：** 工具桥本身不等于自主完成任务；源代码、控制器和 Agent 各自承担的职责需区分。

<a id="work-nvidia-robot-skills"></a>
<!-- stage3-record: {"id": "nvidia-robot-skills", "scope": "Resource", "section": 1} -->

#### NVIDIA Agent Skills — Physical AI and Robotics

`首发日期未明确` · 单位未明确

[代码](https://github.com/NVIDIA/skills)

提供面向 Coding Agent 的机器人、仿真与 Isaac 工作流技能，将任务编写、数据管线、数字孪生和验证步骤组织为可调用过程知识。

**验证：** 引用相关机器人技能入口，不把整个 CUDA 或通用 Agent 技能目录算作本主题工作。

<a id="work-dimos"></a>
<!-- stage3-record: {"id": "dimos", "scope": "Resource", "section": 1} -->

#### DimOS

`首发日期未明确` · 单位未明确

[代码](https://github.com/dimensionalOS/dimos)

以 Python 模块、感知流和机器人控制接口构成 Agent 可编排的机器人软件底座，并提供 CLI 与工具调用入口。

**验证：** 按文档核对接口和示例；本轮未运行实体机器人。

### 跨章节阅读

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

[返回研究地图](#research-map)

---

<a id="section-2"></a>

## 2. Simulator 构建

本节关注 Agent 在执行和检验物理任务之前需要构建什么。产物可以是关节物体、完整场景、任务 API、面向当前任务的世界草图或动力学模型。这些产物提供不同保证：渲染逼真、能够重置执行、接触行为稳定，以及有助于策略训练，是需要分别验证的结果。

| 层面 | 构建内容 | 比较时关注什么 |
|---|---|---|
| 场景与资产 | 几何、物体身份、尺度、关节、摆放及支撑关系 | 可编辑结构、坐标系、碰撞几何，以及与观测的对应关系 |
| 物理属性 | 质量、惯量、摩擦、恢复系数、材料本构及接触参数 | 参数来自推断、测量还是交互拟合；能够解释哪些运动 |
| 任务接口 | 重置状态、观测、动作、奖励、成功检查与终止条件 | 任务能否重放，检查是否符合预期行为，以及依赖什么控制器假设 |
| 渲染与传感 | 相机、光照、材质、传感器输出及叠加视图 | 视觉一致性，以及渲染证据是否确实进入构建期决策 |
| 仿真器与求解器 | 场景格式、执行 API、积分、接触或形变求解 | 区分创作平台与物理后端；USD、URDF、MJCF 导出本身不是求解器 |

**Real-to-Sim** 以具体观测到的物体、场景或交互为参照，恢复其可执行表示；**生成式构建** 从需求、目标或设计条件出发，构造新资产、场景或任务。重建可以调用生成式 mesh 模型，生成式系统也可以检索真实资产：来源标签描述的是构建目标。有两条路线的明确证据时保留双标签。已有数字资产的物理化若既不复原具体观测场景，也不生成新环境，则单独说明其作用。

下文按最早可核实公开时间倒序排列，形成统一方法序列。来源、产物与引擎标记用于横向比较，不再切分为相互竞争的分类体系。可展开摘要是简要阅读解读，完整方法与结果见论文和官方项目。

早期 [GenSim](https://arxiv.org/abs/2310.01361)、[RoboGen](https://arxiv.org/abs/2311.01455) 等任务生成系统把环境程序连接到示范、奖励与策略学习；[Real2Code](https://arxiv.org/abs/2406.08474) 和 [Articulate Anything](https://arxiv.org/abs/2410.13882) 则将关节物体结构变为可执行产物。后续系统进一步结合场景编辑、物理检查和更有针对性的修复。这些是便于比较的研究联系，不表示所有新方法都沿用同一条流水线。

两个近期对照有助于阅读方法表：[WorldSketch](https://arxiv.org/abs/2611.00513) 只构造规划器需要的运动学结构，[CUE](https://arxiv.org/abs/2611.02691) 则主动收集交互证据拟合动力学。[Spatial Harness](https://arxiv.org/abs/2611.11344) 用可执行几何代理辅助空间推理；调用物理引擎不自动使代理成为经过校准的动态孪生。需要什么保真度，取决于后续要完成的计算。

构建反馈属于生成流程：渲染、编译报错、几何探针或失败 rollout 都可能触发编辑；最终质量评估则检查已接受环境在独立条件下是否仍然有用。第 3 节区分这两种作用，第 4、5 节进一步区分生成训练样本、更新下游控制器、积累外部技能与训练 Coding Agent 模型。一个核心开放问题是：哪些环境误差最影响 Agent 学习，哪些构建期检查能够可靠预测这种影响？

**可组合资源。** 以下已有资源提供外观生成、运行时接口或可复用流程，与构建方法数量分开统计。PBR 外观参数不能替代接触、惯量或材料本构校准。

| 资源 | 对构建流程的贡献 | 可用性与含义 |
|---|---|---|
| [UltraTex](../README.zh-CN.md#paper-res-ultratex-2k-multi-view-diffusion) · [论文](https://arxiv.org/abs/2609.23169) · [代码](https://github.com/YiboZ2001/UltraTex) | 参考图与 mesh 几何线索 → 2K 多视图纹理及 PBR 扩展 | 表面外观组件；方法附有代码与 G-buffer 数据 |
| [MIKU](../README.zh-CN.md#paper-res-miku) · [论文](https://arxiv.org/abs/2611.07354) | 参考图与几何 → 对齐的 albedo、metallic、roughness 贴图 | 论文描述的材质能力；尚未链接代码与权重，生成贴图不是测得的物理属性 |
| [WorldFoundry](../README.zh-CN.md#paper-res-worldfoundry) · [源码](https://github.com/OpenEnvision/WorldFoundry) | CLI、Studio 与适配器 → 模型执行、产物和评估流程 | 提供共享基础设施，区分模型依赖与就绪状态；本身不证明场景物理精度 |
| [Unreal Engine 5.9 MegaJam Preview](../README.zh-CN.md#paper-res-unreal-engine-5-9-megajam-preview) · [官方公告](https://forums.unrealengine.com/t/unreal-engine-5-9-megajam-preview/2852840) | Unreal MCP 与 Canvas → 编辑器操作、渲染／调试反馈及生成模型组合 | 实验性平台接口；属于集成公告，不是自主构建评测 |
| [blender-agent-skills](../README.zh-CN.md#paper-res-blender-agent-skills) · [源码](https://github.com/oh-ashen-one/blender-agent-skills) | 参考与场景 → 分阶段构建、视觉关卡、绑定及导出检查 | 五套社区专家流程；属于可复用外部技能，未证明模型学习 |

<a id="work-2611-11344"></a>
<!-- stage3-record: {"id": "2611.11344", "scope": "Adjacent", "section": 2} -->

#### Spatial Harness: Grounding Spatial Reasoning in Executable World States with Physics Engines

`2026-11-08` · Hong Kong Baptist University; ByteDance Seed

[完整书目](../README.zh-CN.md#paper-2611-11344) · [论文](https://arxiv.org/abs/2611.11344) · [代码](https://github.com/tmlr-group/Spatial-Harness) · [论文](https://arxiv.org/html/2611.11344v1)

可执行代理场景将空间推理落实到明确几何状态。

**具体方法：** 感知器融合语言约束与视觉估计，形成物体和相机位姿；推理器通过 Python 在 MuJoCo 中测量和改变视角，读取数值与渲染视图。

**构造流程：** 图像与问题 → 约束和视觉估计 → 共享代理世界 → 测量与视角变化 → 有几何依据的回答

**来源／产物／平台：** Real-to-Sim（任务专用空间代理） · 可执行物体与相机状态 · MuJoCo

**验证：** 四个空间评测包含相同真实标注布局对照及感知／反馈消融。代理尺寸不是实物测量；静态推理不证明动力学或机器人控制保真度。

<details>
<summary>摘要概述</summary>

可执行代理场景将空间推理落实到明确几何状态。感知器融合语言约束与视觉估计，形成物体和相机位姿；推理器通过 Python 在 MuJoCo 中测量和改变视角，读取数值与渲染视图。

</details>

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3)

<a id="work-2611-10602"></a>
<!-- stage3-record: {"id": "2611.10602", "scope": "Adjacent", "section": 2} -->

#### Agentic discrete-event simulation for manufacturing system design: an open 3D simulator, a benchmark and an industrial case

`2026-11-07` · Universidade da Coruña; CITENI; Grupo Integrado de Ingeniería

[论文](https://arxiv.org/abs/2611.10602) · [论文](https://arxiv.org/html/2611.10602v2)

SimuLean 为 Agent 提供经过验证的制造系统建模组件。

**具体方法：** 领域命令构造共享的 Unity 三维与无头模型，校准作业时长后加速重复研究；独立参考模型检查最终系统语义。

**构造流程：** 制造系统规范 → 领域命令 → 共享三维／无头模型 → 作业时长校准 → 参考模型对照

**来源／产物／平台：** 生成式任务模型构建 · 制造离散事件模型与实验报告 · Unity；离散事件仿真

**验证：** 18 项建模任务中，一个前沿 Agent 在 108 次尝试中构建 93 个有效模型。焊接车间案例与纠正后的参考结果相差 1% 内；残余错误可能通过构建／运行检查，未证明实机部署。

<details>
<summary>摘要概述</summary>

SimuLean 为 Agent 提供经过验证的制造系统建模组件。领域命令构造共享的 Unity 三维与无头模型，校准作业时长后加速重复研究；独立参考模型检查最终系统语义。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [6. 物理应用与实验](#section-6)

<a id="work-2611-02691"></a>
<!-- stage3-record: {"id": "2611.02691", "scope": "Core", "section": 2} -->

#### Closing the Dynamics Gap through Self-Directed Robotic Interaction

`2026-11-02` · Stanford University; ETH Zurich; NVIDIA Research; microagi

[论文](https://arxiv.org/abs/2611.02691) · [论文](https://arxiv.org/html/2611.02691v1) · [项目页](https://cue-dynamics.github.io/)

通过自主击球探索获取动力学证据，让 Agent 同时构建轨迹测量、拟合仿真参数并选择下一次实验。

**具体方法：** Agent 从初始图片写 MuJoCo 台球模型，自行选取重要参数与初值范围，再构建相机球轨迹跟踪。CMA-ES 重放已观察击球并拟合轨迹差异；Agent 根据残差选择模型最不准确的接触情形继续探索。

**构造流程：** 台球图像＋高层指令 → MuJoCo 场景与动力学先验 → 自主击球和相机轨迹 → CMA-ES 并行重放拟合 → 残差导向的新击球 → 校准后的预测仿真模型

**来源／产物／平台：** Real-to-Sim · 台球场景、跟踪／拟合代码与辨识后的物理参数 · MuJoCo

**验证：** 25 个隐藏物理条件、每条件最多 30 次击球的 sim-to-sim 测试中误差降至 0.91 cm（较最强基线降 72%），真实小台球桌另做部署展示，不能把该数值当作实机误差。

<details>
<summary>摘要概述</summary>

CUE 针对仅看图片难以恢复摩擦和恢复系数的动力学缺口，让 Agent 主动收集交互证据。系统自行构建场景、感知和参数拟合流程，并把新实验集中在模型预测不足之处。定量提升来自隐藏物理的仿真对照；真实部署则揭示了视觉、模型表达和实验管理的实际限制。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [6. 物理应用与实验](#section-6)

<a id="work-2611-00513"></a>
<!-- stage3-record: {"id": "2611.00513", "scope": "Core", "section": 2} -->

#### WorldSketch: Sketching World Models for Zero-Shot Mobile Manipulation

`2026-10-31` · 单位未明确

[完整书目](../README.zh-CN.md#paper-2611-00513) · [论文](https://arxiv.org/abs/2611.00513) · [论文](https://arxiv.org/html/2611.00513v1)

从 RGB-D 和任务构造可修订的最小运动学草图，让几何规划器据此选择接触与全身运动。

**具体方法：** VLM 请求点和局部视图，后端用深度测量尺寸和轴线，再将结构化草图投回图像检查。规划器在草图与碰撞体素上求解动作；执行后的环境观测接口更新关节假设，受挫时触发草图重建。

**构造流程：** 任务＋校准 RGB-D → VLM 点／视图请求 → 深度测量的部件与关节 → 叠加图检查和草图修订 → 接触与全身运动规划 → 执行反馈后的草图更新

**来源／产物／平台：** Real-to-Sim · 最小运动学世界草图（碰撞体素、任务实体、关节假设、目标） · 未明确；平台：WorldSketch 几何规划器；RoboCasa / LIBERO-PRO / R2R-CE 评测

**验证：** RoboCasa、LIBERO-PRO 和 R2R-CE 上零样本成功率约 91%、97% 和 76%，全部采用仿真深度和标定，不包括真机、柔体、关节链或动力学任务。

<details>
<summary>摘要概述</summary>

WorldSketch 让 VLM 决定任务需要哪些部件和机制，由深度测量提供几何量，再让规划器计算动作。世界草图保留任务相关实体与单关节运动学，其他物体仅作为障碍。叠加图与执行结果可以修订草图，但它不构建完整动力学仿真，已报告的实验也全部在仿真中。

</details>

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3) · [6. 物理应用与实验](#section-6)

<a id="work-2610-40565"></a>
<!-- stage3-record: {"id": "2610.40565", "scope": "Core", "section": 2} -->

#### Gym-Anything for Robotics: Scaling physical simulations with digital agents

`2026-10-29` · Carnegie Mellon University

[论文](https://arxiv.org/abs/2610.40565) · [论文](https://arxiv.org/html/2610.40565v1) · [项目页](https://gym-anything.github.io/robotics)

把仿真器本身作为 Coding Agent 任务，用独立物理审计反复修订场景、动力学和验证证据。

**具体方法：** 创建 Agent 根据工作活动研究设备和物理过程，写出场景、任务及运行证据；四类审计检查物理与可解性、性能配置、鲁棒性等。报告返回同一创建 Agent 修订代码，经过三轮后形成统一接口下的 RoboWorld 仿真和任务。

**构造流程：** 工作活动组与能力需求 → 物理过程研究和场景设计 → 仿真代码＋测量证据 → 四类独立审计 → 三轮代码与场景修订 → RoboWorld 环境与任务

**来源／产物／平台：** 生成式 · 可交互仿真代码、任务验证器与物理验证记录 · 多后端与自定义求解器；部分场景用 Newton / MuJoCo-Warp、Warp

**验证：** 构建 25 类 RoboWorld 仿真并评测物理检查、Agent 解题及代码示范训练的小型 VLA，学习与迁移结果在仿真内完成，不等于真机技能迁移。

<details>
<summary>摘要概述</summary>

Gym-Anything for Robotics 将构建与检验物理仿真转化为 Coding Agent 的工作流。创建 Agent 需要研究活动、编写场景和动力学，并提交视频与物理测量；独立审计通过运行和检查驱动修订。输出环境用于比较操作 Agent，也用于特权状态指导与示范生成的仿真内学习实验。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2610-40754"></a>
<!-- stage3-record: {"id": "2610.40754", "scope": "Core", "section": 2} -->

#### DyCraft: An Agentic System for Long-Horizon 4D Scene Generation

`2026-10-29` · Stanford University; University of Cambridge

[完整书目](../README.zh-CN.md#paper-2610-40754) · [论文](https://arxiv.org/abs/2610.40754) · [论文](https://arxiv.org/html/2610.40754v1) · [项目页](https://dy-craft.github.io/)

分镜与逐帧诊断引导程序修复，构建长时序动画场景。

**具体方法：** 编码 Agent 构建关节 CAD 场景，先验证关键姿态，再用动作捕捉、逆运动学及 Blender 仿真工具组合连续运动；渲染网格与穿插、支撑、关节限制诊断引导场景和运动程序修订。

**构造流程：** 提示词与扩展任务描述 → CAD 场景与关节 → 经验证的分镜姿态 → 运动工具与仿真 → 逐帧视觉和几何检查 → 修订后的 Blender 影片

**来源／产物／平台：** 生成式物理动画场景 · 可编辑 Blender 工程、动画影片、计划与任务描述 · Blender 原生仿真；具体后端未明确

**验证：** 24 个多镜头任务用于人类偏好、逐帧物理错误指标和工具消融。产物是渲染动画，未验证为机器人训练环境或实机试验，仍存在物理错误。

<details>
<summary>摘要概述</summary>

经验证的关键姿态将长动画拆为局部运动问题。Agent 根据渲染与空间诊断修订几何和运动；已发布影片资产便于检查，但不等同于完整训练轨迹。

</details>

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4)

<a id="work-2610-36592"></a>
<!-- stage3-record: {"id": "2610.36592", "scope": "Adjacent", "section": 2} -->

#### LabWorld: Learning Interactive 4D Worlds for Scientific Experimentation

`2026-10-27` · Princeton University; Stanford University; University of Chicago; New York University; Oregon State University; University of Illinois at Urbana-Champaign; University of Texas at Austin

[论文](https://arxiv.org/abs/2610.36592) · [论文](https://arxiv.org/html/2610.36592v1)

从实验视频构建可编辑的资产、场景、轨迹和事件，把操作事件转换为空间时间约束。

**具体方法：** VLM 从视频组织对象和事件，SAM3 与 MapAnything 提供掩码、度量几何和相机，生成或复用设备资产并装配场景。轨迹优化同时利用观测、几何、平滑、事件与非穿透约束，导出可重放、可独立编辑的 4D 状态。

**构造流程：** 单目实验操作视频 → 对象与事件清单 → 掩码、深度、相机和资产 → 度量场景与功能地标 → 事件约束下的轨迹优化 → 可编辑 4D 场景与程序事件

**来源／产物／平台：** Real-to-Sim · 可重放的 4D 世界状态与结构化事件；非完整动力学仿真 · 未明确；平台：显式资产／场景／相机／轨迹／事件表示与优化器

**验证：** 以真实移液与振荡视频评测 mask IoU 0.501、归一化 PCK-AUC 0.638 和 35 项建模约束通过率，未验证机器人部署、完整流体动力学或从原始视频全自动复现。

<details>
<summary>摘要概述</summary>

LabWorld 将实验室视频中的设备、空间布局和操作过程转为可编辑的世界表示。事件描述不只作为标签，还约束物体接近、进入、停留和退出等时空关系，以减少投影正确但交互不合理的重建。评测检验观测一致性和已建模约束，现有复现包从缓存输入开始，不能独立证明从原始视频完全自动化。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [6. 物理应用与实验](#section-6)

<a id="work-2610-34745"></a>
<!-- stage3-record: {"id": "2610.34745", "scope": "Core", "section": 2} -->

#### SceneAgent: An Agentic Pipeline from 3D and 4D Captures to Simulation Environments

`2026-10-26` · Harvard University

[完整书目](../README.zh-CN.md#paper-2610-34745) · [论文](https://arxiv.org/abs/2610.34745) · [论文](https://arxiv.org/html/2610.34745v1) · [项目页](https://computationalrobotics.seas.harvard.edu/SceneAgent/)

把 3D/4D 采集组织成可交互仿真，利用分步视觉检查与修订统一物体重建、关节及材料行为。

**具体方法：** Agent 规划、摄取采集并调用分割、补全、物理属性和关节工具，打包后在 Isaac Lab 检查场景。动态视频路线生成可重建整段时序的脚本，对照早中晚帧修改相机、静态几何、初态或物理参数，再生成场景变体与示范。

**构造流程：** 3DGS／扫描或动态视频 → 分割物体与补全网格 → 属性、关节与动态模型 → 仿真导出及多帧渲染 → 视觉诊断和局部修订 → 可交互场景与数字变体

**来源／产物／平台：** Real-to-Sim ＋ 生成式 · 可编辑仿真场景、4D 构建脚本与示范 · PhysX；NVIDIA Warp、Newton、Blast（依材料案例）

**验证：** 在单个厨房、单个杂乱料箱和三个合成动态场景评测重建，并做 Franka 抓放先导迁移，最终顺序微调方案在 50 次实机布局中成功 44 次，尚未校准真实材料参数或验证真实 4D 重建。

<details>
<summary>摘要概述</summary>

SceneAgent 从多类 3D 捕获和动态视频构建可交互场景，协调物体重建、结构补全、关节与可变形材料模型。Agent 通过仿真渲染检查中间产物并进行修订，同时生成物体和场景变化以合成训练示范。实验包含少量静态与合成动态场景，以及初步真机抓放；隐藏物理参数的实测校准仍是限制。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4)

<a id="work-2610-32978"></a>
<!-- stage3-record: {"id": "2610.32978", "scope": "Adjacent", "section": 2} -->

#### SceneBloom: Agentic Indoor Environment Generation with Realistic and Diverse Layouts for Embodied Learning

`2026-10-23` · New York University; University of California, San Diego

[完整书目](../README.zh-CN.md#paper-2610-32978) · [论文](https://arxiv.org/abs/2610.32978) · [论文](https://arxiv.org/pdf/2610.32978v1) · [项目页](https://tinaliu0123.github.io/scenebloom/)

先生成带资产身份的视觉布局提案，再用关系约束把它编译为几何可行的 3D 房间。

**具体方法：** VLM 根据房间需求和参考示例划分功能区，FLUX 配合资产专属 LoRA 为各区采样家具布局图。感知模型把图中物体提升到 3D，VLM 提取朝向、对齐和邻近等关系契约；编译器拟合分区并局部修正位姿，补充墙面和表面物体后导出场景。

**构造流程：** 房间描述与示例 → 功能分区和资产清单 → FLUX 视觉布局提案 → 3D 包围盒与关系契约 → 分层几何拟合／位姿修正 → 墙面和表面补全 → 布局 JSON 与 Habitat 场景

**来源／产物／平台：** 生成式 · scene_layout.json、材质配置、实例化 mesh 与 scene.glb · 未明确；平台：Python 场景编译；Habitat 导出；Isaac Gym 稳定性评测

**验证：** 在五类房间共 50 个生成场景上评估碰撞、越界、REST3D 稳定性、VLM 质量与真实布局分布，检测碰撞率为零、物体稳定率为 75.3%，并在 Habitat 中的留出真实扫描上报告导航成功率而非实机结果。

<details>
<summary>摘要概述</summary>

SceneBloom 将视觉生成模型提供的布局先验与几何编译结合，用来生成真实、多样且可部署的室内环境。分层采样器在功能区内生成家具布局，编译器则保留提案中的关系并修复数值位姿。实验比较视觉质量、物理稳定性和真实布局分布，并显示生成场景可用于提升留出真实扫描环境中的导航表现。

</details>

**关联：** [4. 数据](#section-4)

<a id="work-2610-31834"></a>
<!-- stage3-record: {"id": "2610.31834", "scope": "Core", "section": 2} -->

#### WorldMirror: Agentic Real-to-Sim Generation of Interactive Worlds from In-the-Wild Robot Demonstrations

`2026-10-22` · Xspark AI; Tsinghua University; The University of Hong Kong; University College London; Peking University

[完整书目](../README.zh-CN.md#paper-2610-31834) · [论文](https://arxiv.org/abs/2610.31834) · [论文](https://arxiv.org/html/2610.31834v1) · [项目页](https://worldmirror-page.github.io/)

把真实机器人视频与记录轨迹重建为相机对齐的可编辑世界，用逐阶段验证修订到原轨迹可直接重放。

**具体方法：** 路由 Agent 沿固定依赖图调用重建、校准、布局和重放 Agent，共享包含静态背景、交互资产与失败记录的世界状态。候选必须通过渲染、空间和物理检查才提交；失败会回退到对应阶段并重建受影响的下游组件。

**构造流程：** RGB 演示＋记录的机器人轨迹 → Gaussian 背景与交互资产 → 相机校准和统一坐标系 → 场景／机器人装配程序 → 原轨迹重放及分类失败 → 定向回退修订后的数字孪生

**来源／产物／平台：** Real-to-Sim · 相机锚定的可编辑世界程序与可直接重放的机器人场景 · 未明确；平台：Isaac Sim；Gaussian 背景＋Meshy / Articraft 资产

**验证：** 在 DROID 场景分别评测外观、17 个物体及 8 对关系的空间误差与轨迹重放，所测示范重放成功率 100% 对比基线 40%，这不是新策略的真机任务成功率。

<details>
<summary>摘要概述</summary>

WorldMirror 以真实机器人示范和相应轨迹构建数字孪生。固定构建图与共享世界状态组织多个专门 Agent，渲染和执行检查驱动局部修订或跨阶段回退。输出统一相机、物体与机器人坐标系，重点验证原轨迹无需重规划即可在重建世界中执行。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4)

<a id="work-system-plumb"></a>
<!-- stage3-record: {"id": "system:plumb", "scope": "Resource", "section": 2} -->

#### Plumb: Coding Agents with 3D Perception Rebuild Physical Scenes from Video

`2026-10-21` · Westlake University; The University of Hong Kong

[项目页](https://yubel426.github.io/Plumb/) · [代码](https://github.com/Inception3D/Plumb)

把视频中的跟踪、深度和相机测量交给 Coding Agent，用可重放的 MuJoCo 模型重建动态场景。

**具体方法：** Agent 调用 SAM3 与 Pi3X 得到物体轨迹、深度和相机姿态，用测量工具估计支撑平面、坡度、尺寸及三维路径。它编写 MJCF、初态、参数和拟合程序，官方流程提供仿真重放及图像／深度轨迹比较，最终交付可被动运行的场景。

**构造流程：** 动态视频＋任务要求 → SAM3 轨迹与 Pi3X 深度／相机 → 支撑面、尺寸和三维路径 → MJCF＋初态＋物理参数 → 重放、overlay 和轨迹差异 → 可被动执行的 MuJoCo 世界

**来源／产物／平台：** Real-to-Sim · scene.xml、initial_state.json、parameters.json、拟合代码与 preview · MuJoCo

**验证：** 在 50 个筛选后的 PhysInOne／Physion 视频上评测 2D/3D 轨迹、输入及未见视角 mask 和 279 项物理量，物理精度为 34.8% 对比 Codex 30.8%，未报告真机控制迁移。

<details>
<summary>摘要概述</summary>

Plumb 探讨 Coding Agent 如何从视频恢复可执行的物理场景，以 3D 感知工具减少单视图外观匹配带来的几何歧义。Agent 自行编写场景和拟合程序，并可将仿真与观测轨迹比较。官方项目报告受控的 50 视频对照，但尚未发布 arXiv 论文，物理参数恢复仍明显不完备。

</details>

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3)

<a id="work-2610-33060"></a>
<!-- stage3-record: {"id": "2610.33060", "scope": "Core", "section": 2} -->

#### MARC: Mechanism-Aware Reflective Correction for Articulated Object Code Generation

`2026-10-19` · Shanghai Jiao Tong University; Meituan

[完整书目](../README.zh-CN.md#paper-2610-33060) · [论文](https://arxiv.org/abs/2610.33060) · [论文](https://arxiv.org/html/2610.33060v1) · [项目页](https://demianmusk.github.io/MARC-Home/)

让关节机构代码共享运动学图，用连接级数值诊断定位闭链和耦合运动错误，再按原路径重测修订。

**具体方法：** Agent 将参考图、文字和目标运动范围写成几何及 socket 绑定连接程序；数值求解器固定驱动坐标并解从动坐标。渲染和图关联诊断交给 Judge 探测原因，Executor 改连接或几何，Reviewer 检查后重新求解整段运动。

**构造流程：** 参考图＋文字＋目标运动域 → 几何、socket 与连接程序 → 可执行运动学图 → 驱动路径求解与碰撞诊断 → 探测→修订→复核 → 可执行关节机构程序

**来源／产物／平台：** 生成式 · 带闭链、socket 连接和坐标耦合的可执行机构程序 · 未明确；平台：MARC mechanism-authoring SDK＋数值运动学求解

**验证：** 在 20 个复杂机构上评测可执行率、结构正确性、有效运动覆盖与耦合动作，Kimi-K3 配置覆盖率为 67.8%、总体成功率为 60%，属于数值运动学验证而非完整动力学或真机验证。

<details>
<summary>摘要概述</summary>

MARC 面向闭链与耦合机构中“能加载但不能按预期运动”的问题。程序、运动求解和修订共享运动学图，使错误可对应到特定连接和配置。Agent 利用数值诊断选择探测和协调编辑，并通过重复原运动路径检验修订效果。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2610-21498"></a>
<!-- stage3-record: {"id": "2610.21498", "scope": "Core", "section": 2} -->

#### GRASE: Geometry-native Real-to-sim Agentic Scene Modeling from Video

`2026-10-15` · Xi’an Jiaotong University; Fuzhou University; Adobe Systems; Westlake University

[完整书目](../README.zh-CN.md#paper-2610-21498) · [论文](https://arxiv.org/abs/2610.21498) · [论文](https://arxiv.org/html/2610.21498v1)

持续对照输入视频，逐层修订房间外壳、物体位姿和局部部件，重建可编辑静态几何。

**具体方法：** 先以多视角深度和共享边界拟合房间外壳，再按支撑关系放置物体：大型物体优先用 Blender 几何基元，小物体及难以表达的形状使用 TRELLIS.2。Agent 将源视频、渲染和几何测量对照，定位到具体物体或部件，只保留改善差异且不破坏已对齐区域的修改。

**构造流程：** 单目室内视频 → 多视角深度与相机 → 闭合房间外壳 → 程序化几何／生成 mesh → 配准与支撑布局 → 渲染对照和局部修订 → 可编辑静态 Blender 场景

**来源／产物／平台：** Real-to-Sim · 房间结构、对象与部件可编辑的静态 3D 场景 · 未明确；平台：Blender / MCP

**验证：** 在 8 个 Replica 与 15 个 Imaginarium 场景上测量 CD、法向一致性、F-score、实例 mIoU 与渲染指标，场景 CD 分别为 5.80 cm、3.14 cm，未评测机器人动态任务。

<details>
<summary>摘要概述</summary>

GRASE 将输入视频作为整个重建过程的持续参照，避免一次性估计中的误差向后传播。它连接外壳拟合、资产放置与部件级精修，通过多视角视觉和几何反馈定位并修正结构差异。实验主要验证几何与渲染一致性；当前方法假设静态场景，尚不恢复关节、完整材质与物理参数。

</details>

<a id="work-2610-18835"></a>
<!-- stage3-record: {"id": "2610.18835", "scope": "Core", "section": 2} -->

#### RoboSimStudio: An Interactive Toolkit for Human and Agent Rapid Real2Sim of Robot Manipulation Tasks

`2026-10-13` · University of California, Berkeley; NVIDIA

[论文](https://arxiv.org/abs/2610.18835) · [论文](https://arxiv.org/html/2610.18835v2) · [项目页](https://robosimstudio.github.io)

以可编辑求解器、接触模型和参数支撑视频驱动的多物理构建，并展示真实失败反推场景约束修订。

**具体方法：** Agent 观看任务视频后建立机器人、刚体和柔体场景，RSS 把执行结果整理为空间时间事件与视觉观测供其修订。双臂擦拭案例以 Newton 连接 MuJoCo-Warp 与 SuperDex，真实支架被推倒的失败又促使 Agent 将固定支架改为自由刚体。

**构造流程：** 手机任务视频 → 场景代码与求解器选择 → Newton 多物理执行 → 视觉＋接触／滑移事件 → 几何、动作或物理参数修订 → 可交互仿真与失败驱动模型更新

**来源／产物／平台：** Real-to-Sim · 可编辑多物理场景、机器人行为与交互反馈 · Newton / MuJoCo-Warp；SuperDex FEM（擦拭软体）；VBD（布与线缆）

**验证：** 展示 18 个接触丰富的仿真与双臂擦拭先导实验，其中 Agent 约一小时构建场景、策略经 14 次仿真迭代完成擦拭后上真机，但不构成大规模 sim-to-real 成功率统计。

<details>
<summary>摘要概述</summary>

RoboSimStudio 暴露求解器、接触模型和物理参数，让人和 Coding Agent 都能构建、执行、观察并修订仿真。论文的方法案例说明视频到多物理场景以及仿真反馈下的策略开发。真实部署失败进一步揭示了不正确的固定约束，Agent 据此修订模型；本页保留这一构建与校准贡献。

</details>

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2610-17114"></a>
<!-- stage3-record: {"id": "2610.17114", "scope": "Core", "section": 2} -->

#### D-World: An Explicit World-Language-Action Model with Recursive Self-Improvement under Dual Control

`2026-10-12` · Geek+

[论文](https://arxiv.org/abs/2610.17114) · [论文](https://arxiv.org/html/2610.17114v1)

让机器人一边行动一边用真实测量校正自己编写的显式数字孪生。

**具体方法：** Sense 用视觉与几何程序重建可执行孪生，Plan 在孪生中搜索动作并分段交给机器人。每段真实执行后，对比深度、夹爪和末端运动等测量，修订状态或命名物理参数；参数修改需通过回放一致性检查，结构错误则返回 Sense 重建。

**构造流程：** 相机与机器人观测 → 视觉／几何程序 → 可执行数字孪生 → 仿真中的动作段 → 真实机器人执行与测量 → 回放检查和孪生修订 → 更新后的世界模型与动作

**来源／产物／平台：** Real-to-Sim · 版本化可执行孪生、参数／状态修订、动作与测量记录 · 未明确；平台：定制 Sense–Plan–Act harness；可导出 MuJoCo 场景

**验证：** 真实双臂机器人的毛巾和烤面包机案例以深度残差、夹爪闭合与末端运动评估孪生修订，其中面包深度残差由 22.4 mm 降至 1.5 mm，尚无系统性成功率和基线对比。

<details>
<summary>摘要概述</summary>

D-World 把世界模型表示为 Agent 可直接检查和修订的数字孪生，而非只存于网络权重或预测视频中。机器人在模拟规划与真实执行之间交替，以实际测量检验局部修订，并在必要时重建结构。论文用双臂操作案例展示这种校准过程，推理延迟、局部验证范围和缺少系统对比仍限制结论。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2610-13947"></a>
<!-- stage3-record: {"id": "2610.13947", "scope": "Core", "section": 2} -->

#### Towards Physically Grounded Articulated 3D Assets: A Multi-Agent Pipeline and Benchmark

`2026-10-09` · Nanyang Technological University; ETH Zurich; Microsoft; University of Cambridge; University of Oxford

[完整书目](../README.zh-CN.md#paper-2610-13947) · [论文](https://arxiv.org/abs/2610.13947) · [论文](https://arxiv.org/html/2610.13947v3) · [项目页](https://physicalvision.github.io/artisan/)

以设计、编码和审阅 Agent 联合 MuJoCo 检查，修订能运动、站稳且保留目标功能的关节资产。

**具体方法：** 设计 Agent 给出结构蓝图与设计图，编码 Agent 用 Python 和 Articraft SDK 构建部件、标准连接件及物理属性。系统将多视图渲染与运动碰撞、重力稳定性报告交给审阅 Agent，形成具体问题清单，再交回编码 Agent 修订。

**构造流程：** 文本＋可选参考图 → 结构蓝图与设计图 → Python 资产程序 → Blender 视图＋MuJoCo 检查 → 功能审阅与代码修订 → 有关节的可交互资产

**来源／产物／平台：** 生成式 · Python 定义的有关节资产及物理属性 · MuJoCo

**验证：** 评测 100 个参考资产、50 个稳定性提示和 50 个有质量标注的 ABO 物体，另测仿真机器人下游任务与人工交互偏好，未报告这些下游任务的真机迁移成功率。

<details>
<summary>摘要概述</summary>

Artisan 将资产生成目标从几何外观扩展到碰撞、稳定性、质量和材质。多 Agent 流程借助物理仿真报告对程序化资产进行修订，同时检查目标运动功能是否被保留。论文还建立统一评测，分别衡量空间保真、物理合理性、下游仿真任务和人工质量判断。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2610-11322"></a>
<!-- stage3-record: {"id": "2610.11322", "scope": "Core", "section": 2} -->

#### USDCraft: Geometrically Grounded Programmatic Modeling of Articulated 3D Assets for Simulation

`2026-10-08` · NVIDIA; Nanyang Technological University; Peking University

[完整书目](../README.zh-CN.md#paper-2610-11322) · [论文](https://arxiv.org/abs/2610.11322) · [论文](https://arxiv.org/html/2610.11322v1) · [项目页](https://xingyoujun.github.io/usdcraft/)

用可执行程序重建有关节的 USD 资产，把缺失的已观测表面与尚未观测的空间分开处理。

**具体方法：** 系统把部分源网格编码为度量切片和局部几何查询，Agent 结合参考图规划部件并编写参数化资产程序。候选在同一度量表示中与源几何复查，再以多视图及关节状态渲染补充外观和功能检查，最终编译为带物理属性的 USD。

**构造流程：** 源网格＋参考图／文本 → 度量切片与部件计划 → 参数化资产程序 → 候选表面差异与运动渲染 → 部件／关节程序修订 → 可直接载入 Isaac Sim 的 USD

**来源／产物／平台：** Real-to-Sim · 含刚体、关节、碰撞及物理属性的 USD 资产与源程序 · NVIDIA PhysX

**验证：** 在两个资产基准评测部件、几何与关节恢复，并用三项真机操作测试仿真训练策略，USDCraft 的仿真到现实成功率下降均不超过 10 个百分点，柔体动力学未验证。

<details>
<summary>摘要概述</summary>

USDCraft 将关节资产重建写成以部分几何证据为依据的程序建模问题。度量源几何约束已观测表面，参考图和功能知识支持对未知区域的合理补全。Agent 反复编译、几何复查和视觉检查，生成可在 Isaac Sim 直接使用的资产，并以机器人策略迁移验证用途。

</details>

**关联：** [4. 数据](#section-4)

<a id="work-2610-10479"></a>
<!-- stage3-record: {"id": "2610.10479", "scope": "Core", "section": 2} -->

#### Agentic RSR: Real-to-Sim-to-Real through Scene Reconstruction and Execution-Grounded Robot Policies

`2026-10-07` · Sun Yat-sen University; The Hong Kong University of Science and Technology (Guangzhou)

[完整书目](../README.zh-CN.md#paper-2610-10479) · [论文](https://arxiv.org/abs/2610.10479) · [论文](https://arxiv.org/html/2610.10479v2)

把参考视频的场景修订与操作策略开发串在同一任务中，形成可从仿真迁移到真机的程序。

**具体方法：** Agent 根据工作台视频、任务与机器人模型恢复尺度，在 Blender 中对照多视图修订外观与布局，再在 MuJoCo 检查支撑和抓取等交互。策略开发从特权状态逐步转向视觉观测和随机化环境，执行反馈用于续写、重试或改写策略。

**构造流程：** 视频＋任务＋机器人模型 → 尺度与多视图重建 → Blender 场景修订 → MuJoCo 物理探测与最小修复 → 观测驱动策略程序 → 固定策略的真机迁移测试

**来源／产物／平台：** Real-to-Sim · 尺度对齐的场景、MJCF 与可执行机器人策略 · MuJoCo

**验证：** 18 个场景、两类机器人均通过联合视觉检查，报告深度 MAE 0.0808 m，并在真机取得相当于仿真成功率 80% 的聚合表现，物理合理性探测不能当作真实参数辨识。

<details>
<summary>摘要概述</summary>

Agentic RSR 将场景重建、策略开发和真机执行连接到同一个操作任务。重建阶段恢复尺度、检查多视图和任务相关物理交互；策略阶段逐步减少对特权状态的依赖。共同任务接口支持真机执行，但模拟中的稳定性或抓取探测只验证建模先验，不能替代实测动力学校准。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2610-02274"></a>
<!-- stage3-record: {"id": "2610.02274", "scope": "Core", "section": 2} -->

#### Awomo-SimDataEngine: Agentic Simulation-Ready World Generation

`2026-10-01` · 单位未明确

[完整书目](../README.zh-CN.md#paper-2610-02274) · [论文](https://arxiv.org/abs/2610.02274) · [论文](https://arxiv.org/html/2610.02274v1)

把资产生成、单图重建、文本场景规划和可重放示范连接起来，以模块级验证和有限修订获得可仿真的世界。

**具体方法：** ISArt 先规划部件与运动树，再生成网格、绑定 URDF 并观看关节运动进行修订；Unravel 逐层移除图中物体，融合点图后逆序重组，SimForge 则从文本规划房间。图式执行框架记录依赖和失败归属，回到对应资产、几何、关节或布局步骤，最后绑定机器人与任务合成示范。

**构造流程：** 文本／单张场景图＋可选任务 → ISArt 资产与 URDF → Unravel 重组或 SimForge 布局 → 支撑、碰撞与运动检查 → 模块定向修订与导出 → Isaac Sim 世界及可重放示范

**来源／产物／平台：** Real-to-Sim ＋ 生成式 · 可交互资产、独立可编辑场景及带 reset/task 契约的示范 · 未明确；平台：Isaac Sim；下游 LIBERO / LIBERO-Plus

**验证：** 分别评测资产、场景及策略共训练，在 MuJoCo LIBERO-Plus 中 WAM 成功率从 77.17% 升至 89.43%，这是 Isaac Sim 生成数据的跨仿真训练结果，未据此证明真机收益。

<details>
<summary>摘要概述</summary>

Awomo-SimDataEngine 把仿真资产、世界构建和机器人示范合成整合为可追踪流程。单图路线使用已验证的图像移除和点图重组，文本路线直接规划室内布局，资产路线处理几何与关节。系统以几何、物理、任务及导出检查控制接受与修订，策略实验则单独衡量生成数据的训练价值。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2609-36593"></a>
<!-- stage3-record: {"id": "2609.36593", "scope": "Core", "section": 2} -->

#### Text2Sim: Agentic Physics-Based Simulation Generation with Distilled Expertise

`2026-09-29` · Tsinghua University; Carnegie Mellon University; Genesis AI; Shanghai Qi Zhi Institute

[完整书目](../README.zh-CN.md#paper-2609-36593) · [论文](https://arxiv.org/abs/2609.36593) · [论文](https://arxiv.org/html/2609.36593v2)

把物理过程需求拆成场景、物体、动作和渲染程序，并按执行证据定向修复。

**具体方法：** Planner 维护全局计划，调用四类 Writer 编写接口明确的代码模块，按需获取 mesh 或关节资产。Genesis 执行后，Critic 综合视频、代码和数值记录诊断问题，Planner 再将修改交给对应 Writer，并从 Debug Cards 中检索物理仿真经验。

**构造流程：** 文字物理过程需求 → 全局计划与 Debug Cards → mesh／关节资产清单 → Scene／Body／Action／Render 程序 → Genesis 执行与记录 → Critic 诊断和局部修复 → 可编辑动态案例

**来源／产物／平台：** 生成式 · 可执行程序、资产、物理参数、控制、状态轨迹与渲染视频 · Genesis

**验证：** 在 42 个留出提示的刚体、可变形体和布料模拟上，独立评估器给出物理／视觉分数 95.32／70.23，并辅以盲测人类偏好与消融；没有实机机器人实验。

<details>
<summary>摘要概述</summary>

Text2Sim 将文字描述转成可执行且可编辑的物理动态案例，协调资产、布局、物理参数、控制和渲染。系统以分工明确的 Agent 结构与从图形学示例提炼的 Debug Cards 支持执行驱动的修复。论文在独立物理／视觉评分和人类偏好中验证效果，并展示生成数据集及多模态输入扩展。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2609-37089"></a>
<!-- stage3-record: {"id": "2609.37089", "scope": "Core", "section": 2} -->

#### Real2Gym: Building Gyms from Videos, Bringing Skills to Robots

`2026-09-29` · Shanghai Artificial Intelligence Laboratory; Shanghai Jiao Tong University; Zhejiang University; University of Science and Technology of China; The Chinese University of Hong Kong; The University of Hong Kong

[论文](https://arxiv.org/abs/2609.37089) · [论文](https://arxiv.org/html/2609.37089v1) · [项目页](https://real2gym.github.io/)

把人类或机器人演示变成视觉对齐、物理可执行的 Gym，并以执行结果修订场景与动作。

**具体方法：** Agent 用深度、分割和多视图线索重建物体、相机及机器人，在接触与抓取变化的关键帧检查差异。随后在 MuJoCo 中执行或重定向示范，修订场景及动作，并只保留通过物理执行检查的场景变体。

**构造流程：** 演示视频＋机器人 URDF → 物体网格、相机与尺度 → 接触事件关键帧 → MuJoCo 示范执行 → 差异定位与场景／动作修订 → 可执行 Gym 与任务变体

**来源／产物／平台：** Real-to-Sim ＋ 生成式 · 配套 Blender 场景、MuJoCo 模型和可执行操作阶段程序 · MuJoCo 3.3.7

**验证：** 在 24 个重建环境上评测视觉保真、任务成功与 token 开销，技能 Agent 仿真成功率为 87.5%，并在四类 Franka 实机任务测试迁移，实机覆盖仅限平行夹爪。

<details>
<summary>摘要概述</summary>

真实演示提供任务与接触信息，Real2Gym 将其重建为可编辑、可执行的交互环境。系统以原生物理执行验证示范与场景变化，再让 Agent 在环境中编写操作阶段程序。成功与失败记录形成可复用技能，底层模型权重不更新；技能随后通过共同感知控制接口用于真机。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2609-37067"></a>
<!-- stage3-record: {"id": "2609.37067", "scope": "Adjacent", "section": 2} -->

#### FACT: Fidelity-Aware Construction of Articulated Twins

`2026-09-29` · ShanghaiTech University

[论文](https://arxiv.org/abs/2609.37067) · [论文](https://arxiv.org/html/2609.37067v2)

把关节孪生分为几何、接触和动态保真三阶段，用局部测量与仿真残差驱动 Agent 修改模型。

**具体方法：** Agent 根据图片生成的网格规划特征、选择测量并编写部件程序，视觉和表面诊断引导重新测量或改写。随后在固定几何上修订碰撞分区、压缩代理，再从被动响应视频构造动力学形式并以仿真残差指导参数拟合和模型修订。

**构造流程：** 物体图片＋被动响应视频 → 特征计划与度量几何程序 → 关节和功能补全 → 任务相关碰撞代理修订 → 响应模型构造与参数拟合 → 验证后的关节数字孪生

**来源／产物／平台：** Real-to-Sim · 几何程序、关节图、碰撞代理与校准响应模型 · MuJoCo（动态预测实验）

**验证：** 评测 21 物体几何、仿真交互与真实物体留出被动视频预测，碰撞阶段 ISR 为 99.47%，动态 TMSE 为 0.0252，但未验证主动机器人真机操作且只覆盖采样姿态与所观测响应。

<details>
<summary>摘要概述</summary>

FACT 以共享部件身份和坐标系逐阶段构建关节数字孪生。Agent 决定需要什么测量和模型修改，数值工具执行几何、碰撞与动态拟合并返回可定位诊断。它在保真约束下简化碰撞代理，并以留出真实视频评测动态预测；后续阶段固定前级结构，也限制了跨阶段纠错。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2609-36024"></a>
<!-- stage3-record: {"id": "2609.36024", "scope": "Core", "section": 2} -->

#### CoDimRecon: Agentic Reconstruction of Sim-Ready 3D Scenes with Deformable Curves, Surfaces, and Volumes

`2026-09-28` · Tsinghua University; Carnegie Mellon University; Genesis AI

[完整书目](../README.zh-CN.md#paper-2609-36024) · [论文](https://arxiv.org/abs/2609.36024) · [论文](https://arxiv.org/html/2609.36024v3) · [项目页](https://shuzhaoxie.github.io/CoDimRecon/)

用几何与生成参考指导可编辑场景重建，并分别构造可仿真的线、面、体软物体。

**具体方法：** VGGT-Omega 提供场景几何，SAM3D 等生成物体形状参考，Agent 在 Blender 中重建紧凑可编辑几何并通过渲染修订外观与位姿。曲线、曲面和体积分别生成 rod、shell、solid 表示，再以机器人行为测试诊断动作、几何、数值或材料模型。

**构造流程：** 多视图 RGB → 场景几何和物体 mesh 参考 → Blender 可编辑重建 → 渲染修订与 MuJoCo 沉降 → rod／shell／solid 物理表示 → 机器人行为诊断与修订 → 刚体、关节及软体场景

**来源／产物／平台：** Real-to-Sim · 可编辑场景、显式关节、曲线中心线／薄壳／体积网格与物理配置 · MuJoCo；IPC-family 接触及 rod/shell/solid 求解器

**验证：** 在 3 个 Replica 与 3 个 ScanNet++ 场景上比较 CD、F1、法向、输入视图渲染与刚体稳定性，软体以行为演示和纸折叠控制实验验证，参数为有效仿真值而非真实辨识。

<details>
<summary>摘要概述</summary>

CoDimRecon 将可组合场景重建扩展到具有不同几何维度的可变形物体，避免把所有对象都简化成刚体或体积 mesh。其构建流程用参考几何、视觉修订与行为验证结合，既输出可编辑场景，也输出能够由对应求解器处理的物理资产。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2609-33208"></a>
<!-- stage3-record: {"id": "2609.33208", "scope": "Core", "section": 2} -->

#### WorldAgent: Verification-Guided Agentic Physical World Construction

`2026-09-27` · University of British Columbia; VAST; Zhejiang University; University of Utah; The University of Texas at Austin; University of California, Los Angeles

[完整书目](../README.zh-CN.md#paper-2609-33208) · [论文](https://arxiv.org/abs/2609.33208) · [论文](https://arxiv.org/html/2609.33208v1)

将故事、实体、空间关系和镜头写成世界规格，以几何和仿真检查持续修订物理世界。

**具体方法：** Agent 从单条语言提示生成 JSON 规格，利用地形、水文、场景与分类物理技能在 Blender 中构建和仿真。验证层检查尺度、穿透、支撑、通行、因果、类别行为、数值稳定和接触，失败定位到对象和帧并回写规格，重跑受影响步骤。

**构造流程：** 自然语言世界要求 → 故事／实体／场景图／镜头规格 → Blender 场景与求解器配置 → 短仿真和渲染 → 八类几何／物理检查 → 规格修订与重执行 → 可编辑可重模拟世界

**来源／产物／平台：** 生成式 · JSON 世界规格、Blender 可编辑场景、仿真配置和缓存、渲染序列 · Bullet 刚体；Mantaflow 流体／气体；Blender Soft Body、Cloth 与粒子系统

**验证：** 13 条 AgenticSimBench 长提示用穿透、因果、构图、对齐和视频质量七指标及 26 人研究比较，同骨干 Agent 对比中五项最佳，均是数字仿真且部分多物理过程采用近似。

<details>
<summary>摘要概述</summary>

WorldAgent 将复杂世界构建看作规格与验证共同驱动的过程，要求场景结构及物理事件都符合提示。与仅检查最终视频不同，它检查可执行场景和仿真状态；可靠性仍受 Blender 求解器、参数推断和全轨迹检查成本限制。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2609-23103"></a>
<!-- stage3-record: {"id": "2609.23103", "scope": "Core", "section": 2} -->

#### DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation

`2026-09-19` · University of British Columbia; National University of Singapore; University of Cambridge; Friedrich-Alexander-Universität Erlangen-Nürnberg; University of Wisconsin–Madison

[完整书目](../README.zh-CN.md#paper-2609-23103) · [论文](https://arxiv.org/abs/2609.23103) · [论文](https://arxiv.org/html/2609.23103v1) · [项目页](https://diaggen.github.io/)

让诊断 Agent 主动抓取和扰动生成资产，把行为异常回送给负责的生成阶段。

**具体方法：** 单张照片先经清理、部件分割、OmniPart 几何和分部件材料推断，合并成可加载的 Genesis 资产。诊断 Agent 选语义锚点并预览抓取框，在重置后执行接触、位移、释放，利用多视图和日志把问题路由到分割、材料或 mesh 处理，再重跑相应下游阶段。

**构造流程：** 真实照片 → 清理与部件分割 → OmniPart 几何及材料 → Genesis 候选资产 → 锚点探测与 RGB／状态观察 → 上游路由修复 → 冻结资产包和诊断谱系

**来源／产物／平台：** Real-to-Sim · 带部件语义、mesh、材料、尺度和诊断记录的可变形资产包 · Genesis 隐式 FEM；SAP 摩擦接触

**验证：** 40 个资产中 14 个被诊断为需修复，PMSC 从 2.14 升到 3.43，动态配对比较为 9 胜／4 负／1 平，三项操控及实机记录到孪生示例不构成大规模真实策略验证。

<details>
<summary>摘要概述</summary>

DiagGen 将生成后的物理响应变成可行动的诊断信号，弥补仅静态评审资产的不足。受控探测帮助定位并修复分割、材料或几何错误，但修复并非每次改善交互，材料与分割的相似症状也会造成误判。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2609-18620"></a>
<!-- stage3-record: {"id": "2609.18620", "scope": "Core", "section": 2} -->

#### DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation

`2026-09-16` · Nankai University; Rightly Robotics, A4x

[完整书目](../README.zh-CN.md#paper-2609-18620) · [论文](https://arxiv.org/abs/2609.18620) · [论文](https://arxiv.org/html/2609.18620v2) · [项目页](https://can-lee.github.io/DeformSmith_web/)

分层建立几何、物理模型和材料，再用受约束物理探测与机器人交互修订可变形资产。

**具体方法：** L0 从图像恢复 mesh、粒子和高斯外观，L1 建立尺度、质量、体积及接触条件，L2 用 MPM 探测选择材料参数。L3 运行抓取运输释放，Planner、Designer 和 Critic 在固定测试条件与力预算下选择动作、数值或材料修订，材料修改须返回 L2 复验。

**构造流程：** 文本／单张图像 → mesh、粒子与高斯对齐 → 质量体积及接触模型 → MPM 材料探测 → 机器人抓取测试 → 分层诊断与复验 → 可变形资产和交互记录

**来源／产物／平台：** 生成式 · 粒子物理表示、高斯外观、材料配置、诊断与交互数据 · Warp MPM（集成 DeformMaster 后端）；机器人使用 SAPIEN

**验证：** 39 个案例以匿名 VLM 评分、40 人偏好及物理测试消融评估生成质量，真实机器人材料辨识仅列潜在应用，未验证恢复真实材料参数。

<details>
<summary>摘要概述</summary>

DeformSmith 面向可抓取的体积软物体，把几何、物理条件、材料和交互按层构造，利用共享物理 harness 保持反馈可比较。实验改善视觉与感知物理可信度，但假设均匀各向同性材料，文本／图像推断的参数尚需真实验证。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2609-05927"></a>
<!-- stage3-record: {"id": "2609.05927", "scope": "Adjacent", "section": 2} -->

#### GIF: Agentic Generation of Interactive and Functional Object Compositions for Robot Learning

`2026-09-05` · Galbot; Peking University; Zhejiang University; The University of Hong Kong; Tsinghua University; Beijing Academy of Artificial Intelligence

[论文](https://arxiv.org/abs/2609.05927) · [项目页](https://fufumeichi.github.io/gif-project-page/) · [论文](https://fufumeichi.github.io/gif-project-page/assets/paper.pdf)

用图像与 3D 模型生成独立物体，再修正精细接触关系，构成可以用于机器人训练的操作场景。

**具体方法：** 先生成参考图和对象规格；CoGen 同时保留直接重建与擦除遮挡后补全两路 mesh。GPRM 依次对齐几何、去除碰撞，并在 MuJoCo 中搜索稳定姿态；VLM 查看仿真多视图，筛选关系正确的组合。相比房间级布局，它关注盖合、挂接、插入等物体间接触。

**构造流程：** 文字／参考图 → 生成参考图＋对象规格 → 两路 mesh 候选（直接重建／擦除遮挡后补全） → 几何对齐与碰撞消除 → 仿真稳定化＋VLM 检查 → 可交互物体组合 → 训练轨迹

**来源／产物／平台：** 生成式 · 具有目标接触关系的刚体场景、示范轨迹 · MuJoCo

**验证：** 以 120 个场景检查外观、接触关系、碰撞和人工偏好，并测试合成数据训练策略后的仿真及实机操作；主体范围是刚体物体组合。

<details>
<summary>摘要概述</summary>

GIF 将精确物体组合分解为独立资产重建和相对位姿恢复。互补的生成路径缓解遮挡，几何与物理优化保证接触，视觉验证选择可用组合。所生成场景用于合成训练数据并验证真实操作；关节物体、可变形体和房间尺度布局仍不在主体范围。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2609-05594"></a>
<!-- stage3-record: {"id": "2609.05594", "scope": "Adjacent", "section": 2} -->

#### SceneMosaic: Efficient and Diverse Simulation-Ready Scene Generation via Hybrid Agentic Layout Evolution

`2026-09-04` · The University of Hong Kong; University of Electronic Science and Technology of China

[论文](https://arxiv.org/abs/2609.05594) · [论文](https://arxiv.org/html/2609.05594) · [代码](https://github.com/rxjfighting/SceneMosaic) · [项目页](https://rxjfighting.github.io/SceneMosaic/)

先从一张图快速重建，再让 Agent 分块调整布局，组合出多个可仿真的场景。

**具体方法：** SAM3 分割与 SAM3D 逐物体重建先给出 mesh 和粗布局，再按支撑、包含关系拆成局部单元。Agent 依据正交视图和仿真诊断修正局部位置与朝向，最后组合通过检查的局部变体；重点是降低逐物体迭代成本，同时保留多样性。

**构造流程：** 参考图／文字生成的图 → 分割物体 → 逐物体 mesh → 推断支撑关系与局部单元 → 重力稳定化 → 局部布局修订 → 组合并筛选局部变体 → 可仿真场景及多样布局

**来源／产物／平台：** Real-to-Sim ＋ 生成式 · 可仿真室内场景及变体 · 未明确；平台：刚体仿真与 GLB 场景导出

**验证：** 在 SceneEval-100 上评估语义位置与朝向、碰撞／越界／可导航性、生成耗时和布局多样性，并辅以人工评分；不是实机任务验证。

<details>
<summary>摘要概述</summary>

该工作将快速图像到三维重建与较慢但可纠错的 Agent 构建结合起来。系统对局部单元独立修订并记录历史，再组合场景变体，以减少反复全局布局的开销。实验关注生成效率、场景合理性与多样性，未将这些指标等同于真实机器人表现。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2608-30821"></a>
<!-- stage3-record: {"id": "2608.30821", "scope": "Adjacent", "section": 2} -->

#### Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling

`2026-08-31` · ByteDance Seed; Peking University; Zhejiang University

[论文](https://arxiv.org/abs/2608.30821) · [论文](https://arxiv.org/html/2608.30821v1) · [项目页](https://lucida-r2s.github.io/)

先聚合每个物体的多视图证据，再由 GizmoAct 反复看图并编辑姿态完成场景对齐。

**具体方法：** 系统从有位姿 RGB-D 观测构建带掩码、点云、3D 框和空间关系的对象图，经多视图补全图像生成完整资产。GizmoAct 把定位视为多轮 GUI 交互，观察资产与点云叠加及局部轴视图，在局部坐标系修改平移、旋转、缩放，直到主动停止。

**构造流程：** 有位姿 RGB-D 序列 → 对象多视图证据图 → 遮挡补全图像 → 完整独立 3D 资产 → gizmo 多视图观察 → 姿态／尺度增量编辑 → 可组合场景图

**来源／产物／平台：** Real-to-Sim · 独立物体资产、9-DoF 位姿、尺度和空间关系场景图 · 未明确；平台：自定义 GizmoAct 3D 图形交互环境

**验证：** 论文在 R2S、CA-1M 与 ADT 上比较 3D 检测、ADD-SB 位姿和场景 F-score 等，CA-1M ADD-SB@0.05 达 83.4%，未验证物理交互或实机迁移。

<details>
<summary>摘要概述</summary>

Lucida 按解析、生成和放置三步重建可编辑真实场景，将准确对齐放到最后的闭环阶段而非依赖完美上游几何。GizmoAct 经过合成纠错轨迹监督训练与 RL，学习从图形观察进行连续局部编辑；这是构建子策略的训练，与机器人下游 RL 有别。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2608-27549"></a>
<!-- stage3-record: {"id": "2608.27549", "scope": "Core", "section": 2} -->

#### Code as Worlds: Agentic Discovery of Executable World Representations for Physical Reasoning

`2026-08-27` · MirroS; Tsinghua University; Peking University; Nanyang Technological University

[完整书目](../README.zh-CN.md#paper-2608-27549) · [论文](https://arxiv.org/abs/2608.27549) · [论文](https://arxiv.org/html/2608.27549v2) · [项目页](https://mirros-lab.github.io/code-as-world)

将文字或视频解释成可执行世界程序，通过投影与观测差异迭代修订物体、状态和外观。

**具体方法：** 模态适配器从文字提取语义约束，或从视频取得深度、分割、轨迹和生成物体 mesh。Agent 提议包含物理组成、动态演化和视觉外观的 EWR，实例化、执行并渲染后比较关键帧证据，将差异定位到相关成分作局部修改。

**构造流程：** 文字／真实视频 → 语义或深度／掩码／轨迹证据 → EWR 可执行世界假设 → MuJoCo 接口实例化与执行 → 渲染／投影对比 → 局部程序修订 → 已验证 EWR 与状态轨迹

**来源／产物／平台：** Real-to-Sim ＋ 生成式 · EWR 程序、对象／接触／事件轨迹、验证记录与物理标注视频 · MuJoCo（可选动力学后端）；主文 reconstruction 使用运动学 animation engine

**验证：** 视频重建以最多五轮和同预算 Best-of-5 比较视觉对齐、对象 IoU、轨迹／速度误差等，主文用运动学 animation engine，视频真实感转换和 QuantiPhy 提升不等同于实机物理验证。

<details>
<summary>摘要概述</summary>

Code as Worlds 把世界分成可独立编辑的组成、动态和外观，并用 Agent 的假设—执行—验证过程从观测寻找紧凑表示。已验证世界可提供定量物理推理训练数据；本次版本的主重建结果使用运动学轨迹执行，其 sim-to-real 指视频真实感重渲染。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2608-18840"></a>
<!-- stage3-record: {"id": "2608.18840", "scope": "Adjacent", "section": 2} -->

#### Beyond Placement and Articulation: Usage-Driven Code Scenes for Embodied Interaction

`2026-08-19` · Shanghai Jiao Tong University; Meituan

[论文](https://arxiv.org/abs/2608.18840) · [论文](https://arxiv.org/html/2608.18840)

用程序同时构建房间、可动资产和使用规则，让“按按钮开灯”等跨部件交互真正发生。

**具体方法：** 先按房间用途补全必需物体、支撑关系和交互图，再用 ArtiCraft 编写可动资产，将交互边编译成“触发—条件—效果”规则。FLUX.2 负责墙面等平面的贴图；几何求解器与视觉 Critic 完成布局，并通过仿真检查修订。

**构造流程：** 房间描述与使用要求 → 规划房间／对象／交互图 → 代码生成可动资产与关节 → 编译交互规则；生成表面贴图 → 约束布局 → 视觉与物理修订 → 可触发交互的完整场景

**来源／产物／平台：** 生成式 · 带关节及状态变化规则的任务场景 · 未明确；平台：Isaac Sim／OmniGibson

**验证：** 用28个房间提示评估空间与语义约束、可交互对象和协调行为数量，并展示仿真机器人关门、按键；未报告实机验证。

<details>
<summary>摘要概述</summary>

RoomWright 将代码场景的目标从“摆放和关节”扩展到物体如何被使用。它将对象间因果关系表达为可执行规则，并保留部件语义以帮助确定操作朝向。结果包括程序化房间、资产和交互运行时，实验验证了场景质量与仿真中的功能交互。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2610-01863"></a>
<!-- stage3-record: {"id": "2610.01863", "scope": "Core", "section": 2} -->

#### LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction

`2026-08-04` · University of Cambridge; Imperial College London; Independent Researcher

官方项目文章：2026-08-04；arXiv v1：2026-10-01。

[完整书目](../README.zh-CN.md#paper-2610-01863) · [论文](https://arxiv.org/abs/2610.01863) · [论文](https://arxiv.org/html/2610.01863v1) · [项目页](https://litereality.github.io/agent/)

把 RGB-D 房间重建写成可执行的 Room.py，并通过观察、编辑和检查持续完善。

**具体方法：** 扫描布局先经过几何修正，再将物体分为程序化／关节资产与图像到 3D 资产两路，装配为初始 Room.py。Coding Agent 利用校准视图、点云、测量和渲染比较修改场景程序，经几何、支撑和碰撞检查后导出带物理信息的场景。

**构造流程：** RGB-D 扫描与检测 → 修正布局和物体框 → 程序资产／TRELLIS mesh → 初始 Room.py → 观察、编辑与验证 → 可编辑房间与 MuJoCo 导出

**来源／产物／平台：** Real-to-Sim · Room.py、可编辑场景、独立物体／关节与 MuJoCo 模型 · MuJoCo（导出后的交互演示）

**验证：** 在 10 个真实室内扫描、620 个捕获视角上评估视觉重建，并在 611 个深度帧上得到 10.50 cm 深度 MAE、零检测到的家具表面相交，MuJoCo 交互仅作演示而非实机任务成功率实验。

<details>
<summary>摘要概述</summary>

LiteReality-Agent 从 RGB-D 扫描构建真实、带关节且可交互的室内场景，将重建表述为持续编辑 Python 场景程序。专用工具、分阶段工作流和质量检查支持 Agent 收集证据并逐步改善场景。论文以真实扫描的视觉与几何重建质量为主要证据，同时展示导出场景在 MuJoCo 中的互动。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2607-21522"></a>
<!-- stage3-record: {"id": "2607.21522", "scope": "Adjacent", "section": 2} -->

#### GS-Agent: Creating 4D Physical Worlds With Generative Simulation

`2026-07-23` · University of Massachusetts Amherst; Genesis AI

[论文](https://arxiv.org/abs/2607.21522) · [论文](https://arxiv.org/html/2607.21522) · [项目页](https://umass-embodied-agi.github.io/gs-agent/)

Agent 编写物体、材料、运动与镜头程序，在物理引擎中运行并修订动态世界。

**具体方法：** 系统先检索合适资产，缺失时调用 Meshy，仍失败才用几何基本体替代；随后编程设置材料、位置和运动控制。它在 Genesis 中推进或重置仿真，依据画面、状态和错误反馈修改世界，同时编写相机和灯光控制。

**构造流程：** 自然语言动态场景描述 → 拆解实体／运动／镜头要求 → 检索资产 → 按需生成或基本体 → 编写材料、控制与渲染程序 → 运行 Genesis 并修订 → 可执行4D世界与渲染视频

**来源／产物／平台：** 生成式 · 物理仿真程序与动态4D世界 · Genesis

**验证：** 在物理规律与复杂交互场景上比较视频／状态物理不变量、图文对齐、美学及人工评分；未评估机器人策略训练或实机迁移。

<details>
<summary>摘要概述</summary>

GS-Agent 将实体构建、物理参数与拍摄过程交给能够编程和互相协作的 Agent。世界以可执行代码保留，并通过引擎反馈反复修改，覆盖刚体、液体和可变形材料。它为物理仿真世界构建提供直接基础，但论文的主要结果是动态世界生成而非机器人学习。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2607-19190"></a>
<!-- stage3-record: {"id": "2607.19190", "scope": "Core", "section": 2} -->

#### Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents

`2026-07-21` · University of British Columbia; National University of Singapore; Johns Hopkins University; Friedrich-Alexander-Universität Erlangen-Nürnberg; University of Cambridge; Columbia University; University of California, Los Angeles; Style3D

[论文](https://arxiv.org/abs/2607.19190) · [论文](https://arxiv.org/html/2607.19190v5) · [项目页](https://agentic-real2sim.github.io/)

由视觉语言 Agent 编排感知、物理先验与重放优化，把真实机器人交互变成可运行孪生。

**具体方法：** 视觉 Agent 选择帧、分割对象、恢复和缩放 mesh 并追踪位姿，物理 Agent 估计材料和接触属性；场景 Agent 校准相机、机械臂和地面。MuJoCo 重放真实轨迹，以抓取位移扫描或接收渲染反馈的 Agent 循环优化物体放置，背景采用注册后的高斯场景合成。

**构造流程：** RGB-D、标定与机器人轨迹 → 对象／帧选择和分割 → mesh、尺度与位姿轨迹 → 材料先验与坐标校准 → MuJoCo 重放及抓取优化 → 可执行 episode 孪生

**来源／产物／平台：** Real-to-Sim · 包含资产、相机、轨迹、物理配置和重放接口的 episode 孪生 · MuJoCo（刚体 episode）

**验证：** 500 条 DROID episode 的重放成功率为 48.4%，349 条可测样本另报 PSNR、SSIM、ADD-S，外加六个实机任务的仿真评估代理验证，失败样本保留在成功率分母内。

<details>
<summary>摘要概述</summary>

Agentic Real2Sim 将真实交互记录转换成能够再次执行而非仅观看的物理场景，整合感知资产恢复、物理推断、标定和仿真优化。它支持数据增强及策略测试，并扩展到可变形和人形记录；大规模刚体转换仍有明显分割、位姿与抓取失败。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2607-13586"></a>
<!-- stage3-record: {"id": "2607.13586", "scope": "Adjacent", "section": 2} -->

#### UniPhysGen: Unified Physical Grounding for Simulation-Ready 3D Assets

`2026-07-15` · Zhejiang University; Manycore Tech; University of Electronic Science and Technology of China

[完整书目](../README.zh-CN.md#paper-2607-13586) · [论文](https://arxiv.org/abs/2607.13586) · [代码](https://github.com/breezexian/UniPhysGen) · [数据集](https://huggingface.co/datasets/spatialverse/UniPhys-Bench)

资产分解与物理语义学习生成可仿真的关节资产。

**具体方法：** UniPhys 结合感知部件分组、多模态物理属性估计与几何约束关节候选，通过一致性检查筛选或修订标注；UniPhysGen 使用旋转鲁棒关节监督学习物理语义。

**构造流程：** 已有三维资产 → 感知分解 → 物理属性与关节假设 → 一致性筛选 → 物理语义学习

**来源／产物／平台：** 资产物理化（已有合成／CAD／艺术家模型） · 关节资产、物理标注与学习模型 · Isaac Sim 验证；后端未明确

**验证：** UniPhys-40K 与含 1,927 个物体的 UniPhys-Bench 支持属性、关节及分布变化测试。Isaac Sim 交互案例检验合理性，不代表真实物理参数达到测量精度。

<details>
<summary>摘要概述</summary>

资产分解与物理语义学习生成可仿真的关节资产。UniPhys 结合感知部件分组、多模态物理属性估计与几何约束关节候选，通过一致性检查筛选或修订标注；UniPhysGen 使用旋转鲁棒关节监督学习物理语义。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2607-07459"></a>
<!-- stage3-record: {"id": "2607.07459", "scope": "Resource", "section": 2} -->

#### EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI

`2026-07-08` · Horizon Robotics; WuwenAI

[论文](https://arxiv.org/abs/2607.07459) · [论文](https://arxiv.org/html/2607.07459v3) · [项目页](https://horizonrobotics.github.io/EmbodiedGen/)

以统一物理资产表示、场景图放置和有状态编辑，把任务意图变成可执行 3D 世界。

**具体方法：** 资产流水线补齐尺度、质量、摩擦和碰撞代理，任务分解器生成角色化场景图，再按 BFS 关系采样位置并在 SAPIEN 中沉降。Agent–skill 编辑层维护场景、资产、位姿和历史，以有边界的增量完成自然语言修改并输出跨仿真器配置。

**构造流程：** 文本／图像／任务 → 统一物理资产 → 角色与空间关系场景图 → BFS 放置与物理沉降 → 有状态增量编辑 → 跨仿真器资产和布局

**来源／产物／平台：** 生成式 · 物理资产 URDF/XML/USD、场景图、布局、affordance 与编辑状态 · 未明确；平台：SAPIEN 放置与抓取；导出到 Genesis、Isaac Gym、Isaac Sim、MuJoCo、PyBullet、SAPIEN

**验证：** 200 个资产上人工接纳率为 96.5%、SAPIEN 脚本抓取抬升成功率为 98.6%，另有布局实验，论文汇总的实机提升来自独立下游 VLA 研究。

<details>
<summary>摘要概述</summary>

EmbodiedGen V2 联合仿真资产加工、交互 affordance、任务世界、多房间场景和自然语言编辑，使生成结果可复用与跨平台部署。其论文包含具体生成和放置算法及消融，适合方法页阅读；不能把下游强化学习当作构建者训练。

</details>

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4)

<a id="work-2607-01766"></a>
<!-- stage3-record: {"id": "2607.01766", "scope": "Adjacent", "section": 2} -->

#### SimWorlds: A Multi-Agent System for Dynamic 3D Scene Creation

`2026-07-02` · Carnegie Mellon University; Harvard University; University of California, Merced

[论文](https://arxiv.org/abs/2607.01766) · [论文](https://arxiv.org/html/2607.01766v1) · [项目页](https://dynsimworlds.github.io/)

以固定构建阶段和场景协议约束 Blender 编程，联合渲染评审与引擎状态检查修复动态世界。

**具体方法：** 规划器先提交不变的全局场景计划，编码器按建模、UV、材质、形变、运动、相机和灯光阶段执行 bpy 脚本。确定性 verifier 检查对象层级、接触、关系及求解器状态，reviewer 读取预览与运行数据，失败时局部重试或修改战术计划，最终交付 .blend 和序列。

**构造流程：** 文本场景要求 → 全局场景／关系／运动计划 → 分阶段 bpy 编码 → 引擎状态和几何验证 → 预览／运动分镜评审 → 局部修订与检查点 → 动态 .blend 与渲染视频

**来源／产物／平台：** 生成式 · 可编辑动态 .blend、场景计划、求解器缓存、检查点和渲染帧序列 · Blender 内置 cloth、fluid、rigid body、particle、soft-body 求解器；正文未逐项标底层库

**验证：** 50 场景 4DBuildBench 的独立引擎审计 MPR 达 0.87、结构 SPR 0.89，并以 VLM 逐项评分和 BlenderBench 编辑比较验证，属于数字内容实验且 SPR 有分组公平性限制。

<details>
<summary>摘要概述</summary>

SimWorlds 针对看起来运动正确却使用错误机制的动态场景，加入可检查的场景协议、固定阶段及直接运行状态读取。它把视觉交付与真实引擎机制分开验证，使代码修订能够纠正隐藏的组装和仿真错误；生成主设置从文本开始。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2606-28276"></a>
<!-- stage3-record: {"id": "2606.28276", "scope": "Adjacent", "section": 2} -->

#### SimFoundry: Modular and Automated Scene Generation for Policy Learning and Evaluation

`2026-06-26` · NVIDIA; Georgia Institute of Technology; Stanford University; The University of Texas at Austin; University of Toronto

[论文](https://arxiv.org/abs/2606.28276) · [论文](https://arxiv.org/html/2606.28276v4) · [项目页](https://research.nvidia.com/labs/gear/simfoundry/) · [代码](https://github.com/NVlabs/SimFoundry)

把一段现实视频转成可交互数字孪生，再沿物体、布局和任务三个维度生成可训练的变体。

**具体方法：** 系统从视频中提取物体、深度与语义，逐个生成 mesh 并对齐尺度和位姿，再补充关节、碰撞几何及物理属性。装配场景经过 PyBullet 去穿透与稳定化后，可扩展为保留任务功能的 digital cousins；关节子模块以代码 Actor–Critic 检查和修订运动。

**构造流程：** 真实场景视频 → 物体分割、深度与语义 → 逐物体生成 mesh → 尺度／位姿配准 → 关节与碰撞属性 → 稳定数字孪生 → 物体、布局与任务变体

**来源／产物／平台：** Real-to-Sim ＋ 生成式 · 带关节和物理属性的数字孪生、场景变体及任务规格 · PyBullet（去穿透与稳定化）；下游引擎依导出平台

**验证：** 在 7 个操作任务、5 类策略及 DROID／YAM 真实机器人上比较仿真与实测成功率，平均 Pearson 相关系数为 0.911、MMRV 为 0.018，并报告数字变体训练的实机泛化收益。

<details>
<summary>摘要概述</summary>

SimFoundry 从单段现实视频自动重建可模拟场景，同时支持物体、场景和任务编辑。它生成保留可操作功能的多种数字变体，为机器人训练和评估提供数据。论文展示模拟评估与现实策略表现的较强相关性，并通过真实机器人实验检验模拟数据及变体带来的迁移收益。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2606-14168"></a>
<!-- stage3-record: {"id": "2606.14168", "scope": "Adjacent", "section": 2} -->

#### MUSE: Agentic 3D Scene Authoring via Memory-Grounded Incremental Requirement Satisfaction

`2026-06-12` · East China Normal University; Fudan University; Shanghai Jiao Tong University

[论文](https://arxiv.org/abs/2606.14168) · [论文](https://arxiv.org/html/2606.14168) · [项目页](https://xujay111.github.io/muse_githubio/)

把场景要求拆成逐项可验证的目标，在局部编辑时保护已经正确的内容。

**具体方法：** Architect 将指令变成需求程序，Sculptor 检索资产并执行放置、移动等局部操作，Inspector 用几何规则和渲染视图检查完成情况。已满足的对象和关系进入保护集合，下一轮只修复未完成的要求；其验证重点是结构化场景与导航代理指标。

**构造流程：** 指令＋空房间／已有场景 → 编译需求程序与保护范围 → 检索资产 → 执行局部编辑 → 几何与视图逐项验证 → 更新需求状态及场景记忆 → 导出满足要求的结构化场景

**来源／产物／平台：** 生成式 · 可编辑室内场景（导航环境构建基础） · 未明确；平台：结构化场景与 AuthorBench 导出

**验证：** 在 AuthorBench 上评估需求满足率、编辑保留率、碰撞／越界与人工偏好，并用占用栅格检查导航课程连续性；不是动力学或实机评测。

<details>
<summary>摘要概述</summary>

MUSE 研究如何在持续构建中保留已经完成的工作。它用需求程序、场景记忆和逐步验证协调局部操作，减少新增要求对原场景的破坏。实验支持约束满足与保留式编辑的改进，下游证据限于导航代理测试，未建立完整动态交互环境的结论。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2606-04226"></a>
<!-- stage3-record: {"id": "2606.04226", "scope": "Adjacent", "section": 2} -->

#### PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification

`2026-06-02` · Université de Montréal; Mila – Quebec AI Institute

[论文](https://arxiv.org/abs/2606.04226) · [论文](https://arxiv.org/html/2606.04226v1) · [项目页](https://percept-twin.github.io/)

把机器人感知得到的开放词汇地图转成可操作的场景，用于审查和修订任务计划。

**具体方法：** 输入地图包含每个对象的描述、分割视图和点云，系统检索 Objaverse 或用 TRELLIS 生成资产，并以受约束 ICP 放置。LLM 为物体分配已实现的 affordance，预条件和状态变化构成可执行交互语义，独立 judge 再审查规划执行前后的状态差异。

**构造流程：** 语义地图、分割图与点云 → 检索／生成 3D 资产 → 约束 ICP 放置 → 物体 affordance 与技能预条件 → 交互仿真场景 → 计划执行状态差异

**来源／产物／平台：** Real-to-Sim · 带 3D 资产、位姿、affordance 和技能状态转移的交互场景 · 未明确；平台：ConceptGraphs、TRELLIS、Objaverse；AI2-THOR 相关场景组件

**验证：** 通过可视化对比、93 人计划可解释性研究及三种 LLM 的计划成功／错误／安全判定评测，约 39% 的计划成功提升来自模拟验证，不是实机动作执行验证。

<details>
<summary>摘要概述</summary>

PerceptTwin 从机器人感知地图自动构造一个可解释、可交互的场景表示，补足静态语义地图缺乏行为结果的问题。它利用技能预条件和独立 LLM judge 帮助规划器修改计划；反馈作用于计划，并未证明场景构建本身的视觉迭代修复。

</details>

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3)

<a id="work-2605-21572"></a>
<!-- stage3-record: {"id": "2605.21572", "scope": "Adjacent", "section": 2} -->

#### PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects

`2026-05-20` · Nanyang Technological University; ACE Robotics

[论文](https://arxiv.org/abs/2605.21572) · [论文](https://arxiv.org/html/2605.21572v1) · [项目页](https://physx-omni.github.io/)

以模板游程编码让 VLM 直接预测高分辨几何与物理属性，统一生成多类可仿真资产。

**具体方法：** Qwen2.5-VL 从完整或遮挡图像推断类别、尺度、部件层级和物理属性，再用跨切片模板共享的 RLE 文本表示生成部件体素。TRELLIS 解码得到 mesh，结合关节与材料属性输出资产，也可接入深度和分割提供的场景布局。

**构造流程：** 物体图像 → 全局尺度、层级与物理先验 → 部件几何模板 RLE → 体素与属性预测 → TRELLIS mesh 解码 → 刚体／软体／关节资产

**来源／产物／平台：** Real-to-Sim · 带尺度、材料、affordance、关节和几何的物理 3D 资产 · 未明确；平台：应用仿真器未明确命名；生成模块使用 Qwen2.5-VL / TRELLIS

**验证：** 在 PhysXVerse、PhysX-Mobility 上比较几何和物理属性并用六维 PhysX-Bench 评估，机器人与场景应用主要为仿真展示，正文未给实机策略验证。

<details>
<summary>摘要概述</summary>

PhysX-Omni 的独立方法贡献是面向 VLM 的模板 RLE 几何表示及全局到部件的生成机制，可同时覆盖刚体、软体和关节对象。它配套构建 PhysXVerse 数据和 PhysX-Bench，提供场景与机器人仿真的资产基础，但没有 Agent 的执行后修复环。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2605-19587"></a>
<!-- stage3-record: {"id": "2605.19587", "scope": "Adjacent", "section": 2} -->

#### SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects

`2026-05-19` · The Chinese University of Hong Kong; Shanghai Jiao Tong University; Shanghai AI Laboratory; Microsoft; University of Oxford

[论文](https://arxiv.org/abs/2605.19587) · [论文](https://arxiv.org/html/2605.19587v1) · [项目页](https://scene-code.github.io/) · [代码](https://github.com/wangpuyi/SceneCode)

把房间里的每个物体继续拆成可执行的部件程序，再编译为带关节和物理属性的场景。

**具体方法：** 房间 Agent 先给出布局和逐物体 AssetRequest，路由器按物体类型选择构建策略，用参考图和 ObjectPlan 驱动部件级 Blender Python 生成。程序经过执行修复与渲染检查后，编译出质量、惯量、碰撞体和关节，并用场景注册表关联代码、mesh 与模拟资产。

**构造流程：** 自然语言房间需求 → 布局与 AssetRequest → 参考图和 ObjectPlan → 逐部件 Blender Python → 执行修复与渲染精修 → 关节／物理属性编译 → 场景注册表与 SDF 资产

**来源／产物／平台：** 生成式 · 逐部件 Blender Python、SceneObject 注册表、SDF 与关节资产 · MuJoCo（下游交互演示）

**验证：** 在六类房间的 30 个提示上做 SceneEval 与九人用户研究，并比较物体拓扑、UV 和 PBR 指标；MuJoCo 的开门／滑动操作是模拟交互演示，未报告实机或策略成功率。

<details>
<summary>摘要概述</summary>

SceneCode 将可交互室内场景生成表述为程序化世界构建，以显式物体程序代替不可解释的静态 mesh 集合。房间级规划产生资产需求，物体级生成通过分策略编码、执行修复和视觉精修创建独立部件，并编译关节与物理信息。论文评估场景语义、资产结构和人类偏好，并展示生成资产在 MuJoCo 中的接触交互。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2605-14398"></a>
<!-- stage3-record: {"id": "2605.14398", "scope": "Core", "section": 2} -->

#### ChronoAgentic: A Code-based Multi-Agent World Simulator for Physically Grounded Simulation Construction

`2026-05-14` · University of Wisconsin–Madison

[完整书目](../README.zh-CN.md#paper-2605-14398) · [论文](https://arxiv.org/abs/2605.14398) · [论文](https://arxiv.org/html/2605.14398v3) · [项目页](https://uwsbel.github.io/chrono-agentic-website/)

从人可审阅的物理仿真计划出发，生成、执行并逐步修复独立 PyChrono 程序。

**具体方法：** Plan Agent 将文字与可选参考图转为用户审阅的场景计划，Code Agent 据此调用技能、资产目录和源码检索编写程序。系统依次检查物理运行、首帧和完整视频，再由视觉分析与数值物理检查形成审查报告，驱动同一程序的定向补丁。

**构造流程：** 文字／可选参考图 → 用户审阅的仿真计划 → 技能、资产与源码检索 → 独立 PyChrono 程序 → 分阶段执行和记录 → 视觉／物理审查与补丁 → 可运行物理世界

**来源／产物／平台：** 生成式 · 独立 PyChrono 程序、计划、轨迹、视频与审查记录 · Project Chrono

**验证：** 在 PhyWorldBench 选出的 80 个可支持场景上评估语义遵循与物理正确性，联合通过率为 82.5%，另展示生成城市中的 ROS 驾驶交互，均属模拟环境证据。

<details>
<summary>摘要概述</summary>

ChronoAgentic 通过可执行代码构建显式物理世界，让专门角色处理计划、程序、视觉分析和审查。用户确认计划后，系统运行程序并结合视频和确定性轨迹检查迭代修复。论文在物理视频基准的受支持子集上评价生成世界，并展示其作为实时机器人交互模拟环境的用法。

</details>

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3)

<a id="work-2605-15187"></a>
<!-- stage3-record: {"id": "2605.15187", "scope": "Adjacent", "section": 2} -->

#### Articraft: An Agentic System for Scalable Articulated 3D Asset Generation

`2026-05-14` · University of Cambridge; University of Oxford; Nanyang Technological University

[论文](https://arxiv.org/abs/2605.15187) · [论文](https://arxiv.org/html/2605.15187v1) · [项目页](https://articraft3d.github.io/)

用受限 SDK 编写可执行关节资产程序，并通过结构检查与几何探针迭代修复。

**具体方法：** Agent 在唯一可写的 model.py 中定义部件几何、关节轴限位和对象特定测试，SDK 支持基本体、CadQuery 和程序化构件。Harness 执行并返回 failure/warning/note，Agent 可继续查询距离、穿透、包含和部件姿态，修改同一程序后导出 URDF。

**构造流程：** 文字／可选参考图 → 部件、几何和关节程序 → 编译与对象特定测试 → 距离／穿透／包含探针 → model.py 局部修订 → 关节 mesh 与 URDF

**来源／产物／平台：** 生成式 · model.py、带语义部件和关节的 URDF／mesh、对象测试及验证记录 · 未明确；平台：Articraft Python SDK、CadQuery；Isaac Sim 为下游演示

**验证：** 46 类各五条提示的生成结果由 125 人完成约 5000 次偏好比较，另测关节模型数据增益并展示 Isaac Sim 操作，未提供实机控制成功率。

<details>
<summary>摘要概述</summary>

Articraft 将关节 3D 资产生成写成小而专用的程序编写问题，通过结构化检查和几何测量帮助通用编码模型修复结果。方法支持文本和图像条件，并构建 245 类、超过一万项的筛选资产集；轻量检查不能保证所有姿态下的功能正确或全局外观质量。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4)

<a id="work-2605-09423"></a>
<!-- stage3-record: {"id": "2605.09423", "scope": "Core", "section": 2} -->

#### SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning

`2026-05-10` · UC San Diego; New York University

[论文](https://arxiv.org/abs/2605.09423) · [论文](https://arxiv.org/html/2605.09423v2) · [代码](https://github.com/SimWorld-AI/SimWorld-Studio)

让 Coding Agent 在 UE5 中持续开发任务环境，并根据学习者表现调整后续训练场景。

**具体方法：** SimCoder 通过 Python、MCP 工具和可复用 Skills 编写、执行并验证 UE5 环境，接收编译、几何及视觉反馈后修改。环境通过 Gymnasium 接口供具身 Agent 学习；外层将学习结果送回 SimCoder，调整任务难度和环境分布，并积累工具与技能。

**构造流程：** 文字／图像需求 → 工具与 Skills 检索 → UE5 环境代码 → 编译、几何与视觉检查 → 可交互 Gymnasium 任务 → 学习者表现反馈 → 后续课程环境

**来源／产物／平台：** 生成式 · 引擎环境、任务／奖励配置、Gymnasium 接口与可复用工具技能 · 未明确；平台：SimWorld / Unreal Engine 5；Gymnasium

**验证：** 三组模拟导航案例评估生成有效性及 SR、SPL、SoftSPL、nDTW，共同演化的成功率比固定环境学习高 18 个百分点、比未训练 Agent 高 40 个百分点，未报告实机迁移。

<details>
<summary>摘要概述</summary>

SimWorld Studio 用工具和技能增强的 Coding Agent 自动构建可供具身学习的 UE5 环境，强调可验证任务和标准交互接口。生成器根据编译、物理和视觉反馈修订场景，并把有效操作整理为工具或技能。论文进一步将学习者表现接回生成过程，以自适应课程提高模拟导航表现。

</details>

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2605-09586"></a>
<!-- stage3-record: {"id": "2605.09586", "scope": "Adjacent", "section": 2} -->

#### DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos

`2026-05-10` · Nankai University; Zhejiang University; Southern University of Science and Technology; Rightly Robotics, A4X; University of Science and Technology of China

[论文](https://arxiv.org/abs/2605.09586) · [论文](https://arxiv.org/html/2605.09586v2) · [项目页](https://can-lee.github.io/deformmaster-web/)

从真实交互视频优化可执行软体动力学，将物理滚动、神经残差和高斯外观耦合。

**具体方法：** 视频提供点云、3D 轨迹和手部驱动，MPM 先进行物理推进，再用受限神经速度残差补偿模型缺失。分布式柔顺驱动器把稀疏手轨迹传给物体，混合本构专家描述空间变化材料，粒子运动通过蒙皮驱动高斯外观并联合优化。

**构造流程：** 交互 RGB-D 视频 → 点云、3D 轨迹与手部锚点 → MPM＋神经残差动力学 → 柔顺驱动和混合本构 → 粒子驱动高斯外观 → 可按新动作执行的软体模型

**来源／产物／平台：** Real-to-Sim · 动作条件软体动力学、空间材料场、神经残差和动态高斯外观 · 可微 MPM（NVIDIA Warp）

**验证：** 20 段真实 PhysTwin 序列按未来帧的 Chamfer、Track、IoU、PSNR、SSIM、LPIPS 评测，整体 Chamfer 为 0.011、Track 为 0.024，薄片 Track 仍落后 PhysTwin且不是实机控制实验。

<details>
<summary>摘要概述</summary>

DeformMaster 从真实物体交互建立可响应新动作、材料设置和视角的物理神经世界模型，解决理想物理近似、稀疏接触和外观联动的问题。它是参数优化型重建方法而非 Coding Agent，且 DeformSmith 明确复用其 Warp MPM 后端，因此属于直接技术基础。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2604-10992"></a>
<!-- stage3-record: {"id": "2604.10992", "scope": "Core", "section": 2} -->

#### ArtiCAD: Articulated CAD Assembly Design via Multi-Agent Code Generation

`2026-04-13` · Beihang University; Zhejiang University; The University of Hong Kong

[完整书目](../README.zh-CN.md#paper-2604-10992) · [论文](https://arxiv.org/abs/2604.10992) · [论文](https://arxiv.org/html/2604.10992v2) · [项目页](https://shui-yuan.github.io/articad/)

预先约定部件连接器，再通过多 Agent 代码生成、装配和回滚构造可动 CAD。

**具体方法：** 设计 Agent 从文字或图片给出部件、连接器局部坐标系、关节类型及限位，生成 Agent 独立编写 FreeCAD Python。确定性装配器对齐连接器，VLM 检查多视图与运动关键帧，错误路由器按代码或设计原因只回滚受影响阶段。

**构造流程：** 文字／参考图片 → 部件与连接器契约 → 逐部件 FreeCAD Python → 执行与局部视觉核验 → 关节装配 → 全局运动核验／回滚 → 参数化 CAD 与 URDF

**来源／产物／平台：** 生成式 · 参数化关节 CAD 装配、FreeCAD Python、URDF · 未明确；平台：FreeCAD；Robot Viewer 用于 URDF 验证

**验证：** 120 项 ArtiCAD-Bench 以几何、细节、运动评分和有效成功率评测，并展示 3D 打印及 URDF 关节可视化，未报告机器人策略迁移基准。

<details>
<summary>摘要概述</summary>

ArtiCAD 将多部件可动模型生成拆成设计、部件代码、确定性装配和审查，提前定义连接器以降低后期匹配的不确定性。跨阶段回滚和经验检索改善生成质量，其仿真关联在于可导出的关节资产，而非完整机器人环境生成。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [6. 物理应用与实验](#section-6)

<a id="work-2602-10116"></a>
<!-- stage3-record: {"id": "2602.10116", "scope": "Adjacent", "section": 2} -->

#### SAGE: Scalable Agentic 3D Scene Generation for Embodied AI

`2026-02-10` · NVIDIA; University of Illinois Urbana-Champaign; Cornell University; Stanford University

[论文](https://arxiv.org/abs/2602.10116) · [论文](https://arxiv.org/html/2602.10116v2) · [项目页](https://research.nvidia.com/labs/dir/sage/)

用可组合的场景工具和双重 critic，把机器人任务变为稳定的可交互 3D 场景。

**具体方法：** Agent 选择房间初始化、资产生成放置、移动和删除工具，TRELLIS 生成物体，VLM 提议尺度和物理属性。视觉 critic 检查俯视及四角渲染，物理 critic 在 Isaac Sim 中测量位姿变化并拒绝不稳定放置，二者共同指导后续工具动作。

**构造流程：** 机器人任务／场景要求 → 房间与物体清单 → TRELLIS 资产与物理属性 → 约束放置 → 多视图与仿真稳定性检查 → 移动／增删修订 → 仿真就绪场景

**来源／产物／平台：** 生成式 · 带物理属性的场景、SAGE-10k 场景与合成机器人示范 · 未明确；平台：MCP 工具编排、Isaac Sim

**验证：** 论文以视觉评分、碰撞率和仿真稳定性及下游模仿策略成功率评测，完整 critic 配置稳定性达 99.6%，没有对应实机泛化实验。

<details>
<summary>摘要概述</summary>

SAGE 从用户任务自动组织布局、物体组合和场景校验工具，以渲染和仿真反馈修订生成场景。论文展示多风格场景、1 万场景生成及模拟数据驱动的具身学习；下游策略学习与构建者的推理修订是不同环节。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2602-09153"></a>
<!-- stage3-record: {"id": "2602.09153", "scope": "Core", "section": 2} -->

#### SceneSmith: Agentic Generation of Simulation-Ready Indoor Scenes

`2026-02-09` · Massachusetts Institute of Technology; Toyota Research Institute

[论文](https://arxiv.org/abs/2602.09153) · [论文](https://arxiv.org/html/2602.09153v2) · [项目页](https://scenesmith.github.io/)

从建筑到家具再到小物体，逐层生成可直接进入物理模拟的密集室内场景。

**具体方法：** 每个层级由 Designer 编辑场景，Critic 观察并评估，Orchestrator 决定继续修改或回退。静态资产由参考图、分割与 3D 重建生成，关节资产从库中检索，再补充碰撞几何和物理属性，最后通过去穿透与重力沉降形成稳定场景。

**构造流程：** 自然语言场景需求 → 建筑与房间布局 → 家具、墙面与顶面物体 → 生成／检索带物理属性的资产 → 支撑面上的可操作小物体 → 去穿透与重力沉降 → 可模拟室内场景

**来源／产物／平台：** 生成式 · 独立物体、碰撞几何、质量／惯量／摩擦与关节齐备的室内场景 · Drake

**验证：** 在 210 个场景提示上结合 205 人用户研究、SceneEval 与 Drake 物理检查评估，179 个房间场景的物体碰撞率为 1.2%、稳定率为 95.6%，机器人应用也在仿真中评测。

<details>
<summary>摘要概述</summary>

SceneSmith 面向家庭机器人训练和评估，生成包含密集杂物、可动家具和物理属性的室内环境。它以分层 Agent 交互组织建筑、家具和小物体构建，并整合按需资产生成与关节资产检索。场景在真实性、提示遵循与物理稳定性评估中表现较好，论文还演示了自动生成任务场景并评估机器人策略的流程。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2509-20414"></a>
<!-- stage3-record: {"id": "2509.20414", "scope": "Adjacent", "section": 2} -->

#### SceneWeaver: All-in-One 3D Scene Synthesis with an Extensible and Self-Reflective Agent

`2025-09-24` · State Key Laboratory of General Artificial Intelligence, BIGAI; Tsinghua University

[论文](https://arxiv.org/abs/2509.20414) · [论文](https://arxiv.org/html/2509.20414v2) · [项目页](https://scene-weaver.github.io/) · [代码](https://github.com/Scene-Weaver/SceneWeaver) · [论文](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd2b3c429c8a2ca57656970e010b4b60-Abstract-Conference.html)

按当前场景最需要解决的问题选择构建工具，在渲染与几何反馈中逐步完善室内环境。

**具体方法：** Planner 依据文字需求、历史场景和反馈，从整屋初始化、小场景补全、局部修改等工具中逐轮选择操作。Blender／Infinigen 执行器把布局草案替换成真实 mesh，落实空间关系并减少碰撞；评价器再读取俯视渲染与场景状态，给出下轮修改建议。

**构造流程：** 文字需求 → 工具卡与初始场景 → 单步工具选择 → 布局修改与资产实例化 → 几何约束优化 → 渲染／状态反馈 → 可导出 USD 的室内场景

**来源／产物／平台：** 生成式 · 持续编辑的场景布局、实例化资产及 USD 场景 · 未明确；平台：OpenManus Planner；Blender / Infinigen Executor；Isaac Sim 导出应用

**验证：** 在常见房间和八类开放词汇房间上评估碰撞、越界、VLM 视觉语义分数与用户偏好，并展示 USD 导入 Isaac Sim 后的虚拟 Unitree G1 交互，没有证明真实机器人迁移。

<details>
<summary>摘要概述</summary>

SceneWeaver 以可扩展工具接口统一多种场景合成方式，让语言模型根据场景反馈选择后续操作。整屋生成、局部细节补全和编辑工具结合几何约束执行器，形成反复推理、行动和检查的流程。论文在多类室内场景中评价物理可行性、视觉与语义质量，并展示模拟机器人交互。

</details>

**关联：** [3. Simulator 质量评估](#section-3)

<a id="work-2411-01775"></a>
<!-- stage3-record: {"id": "2411.01775", "scope": "Adjacent", "section": 2} -->

#### Eurekaverse: Environment Curriculum Generation via Large Language Models

`2024-11-04` · University of Pennsylvania

[论文](https://arxiv.org/abs/2411.01775) · [论文](https://arxiv.org/html/2411.01775v1) · [项目页](https://eureka-research.github.io/eurekaverse/)

根据四足策略的学习表现迭代生成可执行地形代码，形成适应能力的跑酷课程。

**具体方法：** LLM 生成含高度场与八个目标点的 Python 地形函数，系统检查可执行性及高度阈值并修正部分几何错误。多组 PPO 策略分别训练后选出泛化最好的策略，再把地形统计、奖励项和成功率交给 LLM 演化下一轮地形。

**构造流程：** 任务说明与地形示例 → 高度场和目标点代码 → 执行／可行性检查 → 多策略 PPO 训练 → 地形与成功率统计 → LLM 演化课程地形

**来源／产物／平台：** 生成式 · Python 高度场／目标点函数与渐进地形课程 · 未明确；平台：Extreme Parkour 训练框架；Unitree Go1

**验证：** 论文在 20 类多难度仿真跑酷障碍及 Unitree Go1 的爬箱、越沟、斜坡、楼梯实机任务上比较成功率，验证的是课程对策略的作用。

<details>
<summary>摘要概述</summary>

Eurekaverse 将无监督环境设计写成 LLM 可编辑的地形程序，并让环境与机器人策略交替演化。自动课程提升了仿真跑酷与实机迁移表现，但被训练的是运动策略，LLM 构建者通过提示上下文得到反馈而非参数更新。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2410-15536"></a>
<!-- stage3-record: {"id": "2410.15536", "scope": "Adjacent", "section": 2} -->

#### GRS: Generating Robotic Simulation Tasks from Real-World Images

`2024-10-20` · NVIDIA; Stanford University

[论文](https://arxiv.org/abs/2410.15536) · [论文](https://openaccess.thecvf.com/content/CVPR2025W/CV2/papers/Zook_GRS_Generating_Robotic_Simulation_Tasks_from_Real-World_Images_CVPRW_2025_paper.pdf)

从单张 RGB-D 图生成可运行的机器人任务与测试，再由错误路由选择修订仿真或测试。

**具体方法：** SAM2 分割和 VLM 描述配合深度得到候选物体及三维包围盒，再从资产库匹配模型。VLM 生成任务、CLIPort 仿真程序和 unittest 测试；oracle 执行和运行错误驱动 router 选择改写仿真或补充测试诊断。

**构造流程：** 单张 RGB-D 场景图 → 分割、物体描述和三维框 → 资产匹配与任务定义 → CLIPort 程序＋测试 → oracle 执行与错误路由 → 修订后的可解任务环境

**来源／产物／平台：** Real-to-Sim · Python 任务仿真代码、URDF 资产布局与测试套件 · 未明确；平台：CLIPort / GenSim task framework

**验证：** 在 10 个场景、每场景 30 次任务生成中评测 oracle 平均奖励（运行错误案例被排除），完整流程为 0.71 对比无 router 0.65，未验证训练策略的真机迁移。

<details>
<summary>摘要概述</summary>

GRS 将单幅 RGB-D 观测转化为包含可解任务的仿真。系统先理解物体并匹配资产，再生成任务程序与自动测试，利用路由机制选择修改失败的仿真或测试。该方法关注任务可执行性及定义对齐，数值反馈修订不应被写成视觉修复闭环。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4)

<a id="work-2410-13882"></a>
<!-- stage3-record: {"id": "2410.13882", "scope": "Core", "section": 2} -->

#### Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model

`2024-10-03` · University of Pennsylvania

[论文](https://arxiv.org/abs/2410.13882) · [论文](https://arxiv.org/html/2410.13882v4) · [项目页](https://articulate-anything.github.io/) · [代码](https://github.com/vlongle/articulate-anything)

让 VLM 编写可编译为 URDF 的 Python，并对照参考与模拟运动反复修正关节资产。

**具体方法：** 先从资产库检索各部件的 mesh，再由 Actor 编写 Python 安排部件位置并定义关节类型、轴线和范围。Critic 对比参考图像或视频与模拟结果，指出装配或运动错误，Actor 据此改写代码。

**构造流程：** 文字、图像或运动视频 → 检索各部件 mesh → Python 部件装配 → Python 关节定义 → URDF 编译与运动渲染 → 修订后的可交互资产

**来源／产物／平台：** Real-to-Sim ＋ 生成式 · Python 装配／关节程序、URDF 和部件 mesh · PyBullet（辅助几何处理）；MuJoCo（Robosuite 策略训练）

**验证：** 在 PartNet-Mobility 上报告约 75% 的关节构建成功率，并将四个生成资产上的模拟训练策略部署到真实 Franka，报告四项任务均为 100% 成功。

<details>
<summary>摘要概述</summary>

Articulate-Anything 从文字、图像或视频构建带关节的交互物体，降低人工标注部件运动结构的成本。系统结合 mesh 检索与 Actor–Critic 程序生成，反复比较模拟结果和输入证据来纠错。论文在关节重建上优于对比方法，并展示了利用生成资产训练机器人策略后迁移到实机的应用。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2409-17652"></a>
<!-- stage3-record: {"id": "2409.17652", "scope": "Adjacent", "section": 2} -->

#### FactorSim: Generative Simulation via Factorized Representation

`2024-09-26` · Stanford University; NVIDIA

[论文](https://arxiv.org/abs/2409.17652) · [论文](https://arxiv.org/html/2409.17652v2) · [项目页](https://cs.stanford.edu/~sunfanyun/factorsim/)

用因子化 POMDP 限制每步需要的代码上下文，从语言规格生成完整仿真。

**具体方法：** 系统先把需求拆成逐步子任务，再用状态变量和局部转移／奖励因子组织仿真代码。每次只取与当前需求相关的状态及函数，按控制、模型和视图更新，减少无关代码干扰。

**构造流程：** 语言任务规格 → 子任务序列 → 相关状态变量 → 局部转移与奖励因子 → 模型／控制／视图代码 → 完整可运行仿真

**来源／产物／平台：** 生成式 · 游戏仿真代码；机器人对象状态与奖励任务代码 · 未明确；平台：PyGame Learning Environment；CLIPort 机器人任务

**验证：** 在八种 2D 游戏和 GenSim 的 50 项机器人任务上检验代码正确性、人工规格符合度及 RL 零样本迁移，均为模拟环境且机器人 oracle 完成率受控制器能力限制。

<details>
<summary>摘要概述</summary>

FactorSim 针对长规格下语言模型容易遗漏条件或修改无关代码的问题，提出因子化状态和功能依赖表示。方法能同时构造环境动态与奖励，在游戏和机器人任务生成实验中改善规格符合度；其贡献是生成结构，而非视觉反馈修复。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2409-02920"></a>
<!-- stage3-record: {"id": "2409.02920", "scope": "Adjacent", "section": 2} -->

#### RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins

`2024-09-04` · The University of Hong Kong; Shanghai AI Laboratory; Shenzhen University; AgileX Robotics; Institute of Automation, Chinese Academy of Sciences

[论文](https://arxiv.org/abs/2409.02920) · [论文](https://arxiv.org/html/2409.02920v3) · [项目页](https://robotwin-benchmark.github.io/early-version/)

以单张真实图像生成物体数字孪生，并围绕功能坐标系生成双臂专家轨迹程序。

**具体方法：** Rodin 将 RGB 物体图像变成带纹理的 3D mesh，再为功能部位指定接触和接近方向。GPT-4V 根据任务与功能坐标轴编写关键姿态关系代码，GPT-4 进一步生成调用轨迹规划工具的程序，用于合成专家数据。

**构造流程：** 真实物体 RGB 图像 → Rodin mesh 与纹理 → 功能点和坐标轴 → 关键姿态序列代码 → 规划器调用 → 双臂专家轨迹与孪生任务

**来源／产物／平台：** Real-to-Sim · 对象数字孪生、任务姿态／规划程序、专家示范 · 未明确；平台：Rodin、COBOT Magic；早期正文未明确命名仿真后端

**验证：** 早期版以六项任务上由 10／20／50 条专家示范训练的 DP3 成功率验证数据效用，结果不能单独证明自动构建的物理精度或视觉修复闭环。

<details>
<summary>摘要概述</summary>

RoboTwin 早期版把真实遥操作数据与生成式数字孪生中的合成数据结合，用于双臂工具使用和协作任务。除基准本身外，它提出低成本图像建模与语言模型辅助专家程序构造流程，因而可作为任务构建基础阅读。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2406-08474"></a>
<!-- stage3-record: {"id": "2406.08474", "scope": "Adjacent", "section": 2} -->

#### Real2Code: Reconstruct Articulated Objects via Code Generation

`2024-06-12` · Stanford University; Columbia University

[论文](https://arxiv.org/abs/2406.08474) · [论文](https://arxiv.org/html/2406.08474v2) · [项目页](https://real2code.github.io/)

用部件包围盒连接视觉重建与代码生成，预测可以直接模拟的对象关节结构。

**具体方法：** 模型从多视角图像分割部件并补全 mesh，将每个部件表示为中心、朝向和尺寸明确的定向包围盒。微调后的 CodeLlama 依据包围盒选择关节轴和位置，生成 Python／MJCF 描述并在 MuJoCo 中实例化。

**构造流程：** 多视角 RGB／RGB-D 图像 → 一致部件分割与点云 → 形状补全后的部件 mesh → 定向包围盒 OBB → CodeLlama 关节代码 → MuJoCo 可交互物体

**来源／产物／平台：** Real-to-Sim · 部件 mesh、Python／MJCF 关节模型 · MuJoCo

**验证：** 在 PartNet-Mobility 未见物体上评估 mesh Chamfer Distance 及关节类型、轴向和位置误差，并展示最多 10 个关节部件与真实多视角图像的重建，不包含实机策略迁移实验。

<details>
<summary>摘要概述</summary>

Real2Code 从视觉观测重建物体的部件几何，再用定向包围盒把空间结构交给代码语言模型预测关节。它通过预训练视觉模型与微调代码模型结合，处理不同数量的部件并从合成数据泛化到现实图像。方法产出可执行模拟模型，实验主要检验几何和关节重建准确性。

</details>

**关联：** [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2405-15568"></a>
<!-- stage3-record: {"id": "2405.15568", "scope": "Adjacent", "section": 2} -->

#### OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code

`2024-05-24` · Imperial College London; University of British Columbia; Vector Institute

[论文](https://arxiv.org/abs/2405.15568) · [论文](https://arxiv.org/html/2405.15568v3) · [项目页](https://dub.sh/omniepic)

借助任务档案和学习反馈持续编写新的环境、奖励与成功判定代码。

**具体方法：** 任务生成器从已成功和失败的档案中检索相关例子，提出有新意且难度适当的任务；环境生成器把它写成 Gymnasium 风格的 Python 环境。编译错误和机器人未学会的结果触发代码修改，兴趣评审决定是否进入训练与档案。

**构造流程：** 成功／失败任务档案 → 新任务描述 → Python 环境与奖励 → 编译检查 → DreamerV3 学习 → 程序成功检测 → 修改环境或入档

**来源／产物／平台：** 生成式 · Python 环境 reset/step/reward/terminated/get_success 与任务档案 · Bullet（通过 PyBullet）

**验证：** 以任务嵌入覆盖度和 ANNECS-OMNI 衡量多样性与累计新任务学习进展，长运行采用模拟学习、短运行实际训练 RL，验证范围均为仿真。

<details>
<summary>摘要概述</summary>

OMNI-EPIC 将开放式探索扩展到以代码定义环境，联合生成场景、动态规则和奖励。它利用历史任务与学习结果调节后续挑战，展示持续的新任务产生；主要证据不依赖 VLM 对渲染视频的自动成功判断。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2312-09067"></a>
<!-- stage3-record: {"id": "2312.09067", "scope": "Adjacent", "section": 2} -->

#### Holodeck: Language Guided Generation of 3D Embodied AI Environments

`2023-12-14` · University of Pennsylvania; Stanford University; Allen Institute for Artificial Intelligence; University of Washington

[论文](https://arxiv.org/abs/2312.09067) · [论文](https://arxiv.org/html/2312.09067v2) · [项目页](https://yueyang1996.github.io/holodeck/) · [代码](https://github.com/allenai/Holodeck)

把文字里的房间需求拆成建筑结构、物体清单和空间约束，组装为可导航的室内环境。

**具体方法：** GPT-4 依次设计地板与墙体、门窗、物体及相对位置关系，并从 Objaverse 与 ProcTHOR 资产中检索模型。布局求解器先放置锚点物体，再搜索满足边界、碰撞和相对关系约束的位置，最终导入 AI2-THOR。

**构造流程：** 房间文字需求 → 平面、墙体与门窗 → 物体描述与检索 mesh → 物体间空间关系 → 约束求解后的布局 → AI2-THOR 室内场景

**来源／产物／平台：** 生成式 · 房屋结构、实例化 3D 资产与布局组成的可交互环境 · Unity Physics（AI2-THOR）

**验证：** 通过 680 人参与的人类偏好评测和模拟环境 NoveltyTHOR 的 ObjectNav 成功率、SPL 评估，Holodeck 微调后的平均成功率为 20.40%，未报告实机导航。

<details>
<summary>摘要概述</summary>

Holodeck 根据自然语言自动构建多样化的具身 AI 室内环境，利用大语言模型的常识选择场景结构和物体。它从大型 3D 资产库检索物体，以空间关系约束和布局优化完成装配。人类评估与新场景中的模拟导航实验表明，这些环境能够提升场景多样性和下游训练效果。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2311-01455"></a>
<!-- stage3-record: {"id": "2311.01455", "scope": "Adjacent", "section": 2} -->

#### RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation

`2023-11-02` · Carnegie Mellon University; Tsinghua University; Massachusetts Institute of Technology; University of Massachusetts Amherst; MIT-IBM AI Lab

[论文](https://arxiv.org/abs/2311.01455) · [论文](https://arxiv.org/html/2311.01455v3) · [项目页](https://robogen-ai.github.io/)

让 LLM 提议任务、组合场景并选择学习算法，批量形成机器人技能训练问题。

**具体方法：** GPT-4 从机器人和种子对象提出任务，检索或生成相关资产，再设置尺寸、关节初态和空间关系。系统为子任务选择强化学习、运动规划或可微轨迹优化，分别生成奖励、目标形状或动作原语参数。

**构造流程：** 机器人与种子对象 → 任务及相关物体 → 检索／生成资产 → 尺寸、关节和场景配置 → 子任务与算法选择 → 监督程序及可执行任务

**来源／产物／平台：** 生成式 · 场景配置、任务分解、奖励／目标形状、技能示范 · Genesis 多材料仿真求解器

**验证：** 106 个生成任务用于多样性比较，69 个任务的技能学习平均成功率为 77.4%，均为仿真结果，不能等同于构建者学习或实机泛化。

<details>
<summary>摘要概述</summary>

RoboGen 将基础模型用于生成机器人学习所需的任务、场景和监督，而非直接预测低层动作。它通过任务相关的资产组合与多种学习算法覆盖刚体、关节、软体操控和运动任务，主要验证生成问题的多样性及其仿真可学习性。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2310-18308"></a>
<!-- stage3-record: {"id": "2310.18308", "scope": "Adjacent", "section": 2} -->

#### Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models

`2023-10-27` · Carnegie Mellon University

[论文](https://arxiv.org/abs/2310.18308) · [论文](https://arxiv.org/html/2310.18308v1) · [项目页](https://gen2sim.github.io/)

把物体图像转成带物理属性的资产，再由 LLM 生成任务分解与奖励程序。

**具体方法：** Zero-1-to-3 先验和两阶段 SDS 从单张物体图像重建纹理 mesh，GPT-4 提议尺寸、质量，MeshLab 计算惯量并封装 URDF。LLM 读取资产关节和部件信息，输出可串联的子任务与 Python 奖励函数，PPO 随后学习执行策略。

**构造流程：** 物体图像 → 图像到纹理 mesh → 尺寸、质量与惯量 → URDF 场景资产 → 子任务与 Python 奖励 → 可训练仿真任务

**来源／产物／平台：** Real-to-Sim · 纹理 mesh、URDF、任务描述、子任务和 Python 奖励函数 · 未明确；平台：Isaac Gym

**验证：** 论文比较资产多视图外观并展示 Isaac Gym 长时序任务学习及实机执行，但实机仅回放仿真优化的开环轨迹，未验证闭环视觉策略迁移。

<details>
<summary>摘要概述</summary>

Gen2Sim 用预训练视觉与语言生成模型减少人工制作机器人训练环境的工作量，联合生成物体资产、任务描述、时间分解与奖励。它展示了多类操控任务的仿真学习与数字孪生中的轨迹迁移；关节物体主要取自既有资产库，生成器尚不覆盖复杂可变形对象。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2310-01361"></a>
<!-- stage3-record: {"id": "2310.01361", "scope": "Adjacent", "section": 2} -->

#### GenSim: Generating Robotic Simulation Tasks via Large Language Models

`2023-10-02` · MIT CSAIL; UC San Diego; University of Washington; CMU; Tsinghua University; Shanghai Jiao Tong University

[论文](https://arxiv.org/abs/2310.01361) · [论文](https://arxiv.org/html/2310.01361v2) · [项目页](https://liruiw.github.io/gensim) · [代码](https://github.com/liruiw/GenSim)

把任务描述变成可执行的机器人任务类，扩展模拟任务库与示范数据。

**具体方法：** LLM 先提出任务名称、资产与目标，再检索已有任务代码作为示例，生成 Ravens／CLIPort 任务类中的初始化和目标定义。程序运行后生成专家演示，并通过执行、LLM 任务质量检查和人工审阅筛选，合格任务进入任务库用于后续生成与策略训练。

**构造流程：** 目标任务／探索要求 → 任务文字规格 → 检索参考任务代码 → 生成 reset 与目标定义 → 模拟执行与专家演示 → 任务筛选与入库 → 多任务策略训练数据

**来源／产物／平台：** 生成式 · 任务类程序、任务库、专家示范与训练后的策略 · PyBullet

**验证：** 评估任务代码生成、模拟策略成功率及真实桌面操作迁移，使用 70 个 GPT-4 任务预训练后的策略在 12 个真实任务上达到平均 62.5% 成功率。

<details>
<summary>摘要概述</summary>

GenSim 利用 LLM 的推理和代码能力自动扩展机器人模拟任务，而不只改变同类场景的资产与姿态。系统支持给定目标的任务生成和从既有任务库探索新任务，并将生成程序转成专家演示。论文研究代码模型微调与多任务策略训练，展示生成任务数据对未见模拟任务和现实操作迁移的帮助。

</details>

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-mujoco-workbench"></a>
<!-- stage3-record: {"id": "mujoco-workbench", "scope": "Resource", "section": 2} -->

#### mujoco-workbench

`首发日期未明确` · Hebbian Robotics

[代码](https://github.com/Hebbian-Robotics/mujoco-workbench)

CLI 与 Agent Skills 支持快速构建和检查 MuJoCo 场景。

**具体方法：** mwb 接口统一运行场景、渲染帧、检查阶段契约和导出多相机视频，Skills 将这些操作组织成迭代编辑工作流。

**构造流程：** 需求与 Skills → 场景代码 → MuJoCo 执行 → 图像与契约诊断 → 场景修订

**来源／产物／平台：** 生成式构建工具 · 场景程序与检查产物 · MuJoCo

**验证：** 官方示例与诊断说明工具接口能力，不构成经校准的数字孪生精度或受控 Agent 评测。

<details>
<summary>摘要概述</summary>

CLI 与 Agent Skills 支持快速构建和检查 MuJoCo 场景。mwb 接口统一运行场景、渲染帧、检查阶段契约和导出多相机视频，Skills 将这些操作组织成迭代编辑工作流。

</details>

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4)

### 跨章节阅读

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

[返回研究地图](#research-map)

---

<a id="section-3"></a>

## 3. Simulator 质量评估

先明确**评估对象**，再区分观测一致性、交互响应、未见条件表现和下游效用。这些问题相互补充：看起来像真实场景的重建可能无法正确接触；控制器也可能通过补偿误差，在不准确的世界中完成任务。

| 评估对象 | 实际交付物 | 代表性检查 |
|---|---|---|
| 物体与场景 | 几何、布局、材质与关节资产 | 外观、尺寸、支撑、碰撞、语义约束与关节运动 |
| 任务环境 | 带动作、观测、重置和成功判定接口的世界 | 接口一致性、固定策略结果与实机评估一致性 |
| 动态仿真案例 | 可执行场景及其时间演化，有时同时生成控制器 | 运动、物理事件、任务完成与改变条件后的执行 |
| 动力学模型与求解器 | 参数、支配规律或数值状态更新 | 测量参数、守恒、稳定性、可辨识性与外推 |

**明确证据边界。** 静态支撑检查不能验证求解器；独立评测器重新渲染，也不能证明构建 Agent 使用了视觉反馈。原生状态检查、隐藏测试和反事实干预提供不同证据，需交代适用范围、预算和失败分母。操作世界、审计世界等 Agent 能力评测归入第 1 部分。

**分开环境误差与控制器误差。** 固定动作或策略，设置已能成功工作的参照环境，并报告执行条件。交叉执行能够诊断兼容性，但不自动构成因果分解。Video2World 的主要结果属于提交的环境—行为组合，补充的控制器迁移测试仅覆盖满足条件的子集。[Video2World 协议](https://arxiv.org/html/2610.04432#S10.SS1)

**写清参照来源。** 实测机器人运动、命令目标和仿真执行轨迹是不同量。Video2World 按来源组合真实观测、拟合几何／运动以及原生仿真状态；人工辅助参照（HAR）是利用额外信息构造的执行结果，不等于观测真值，也不是性能上界。其补充末端运动分析读取实际执行的连杆位姿，并按来源处理跨形态对应关系。[数据与参照协议](https://arxiv.org/html/2610.04432#S8.SS1)

仍需研究：哪些质量检查能够预测未见控制器或干预条件下的成功？如何根据真实误差及其不确定性校准验收阈值？“环境—经验—Coding Agent 能力提升”的完整闭环，需要为每一段联系提供独立证据。

<a id="work-2611-13576"></a>
<!-- stage3-record: {"id": "2611.13576", "scope": "Adjacent", "section": 3} -->

#### PhyRubric: Rubric-Grounded Diagnostic Evaluation of Physical Commonsense in Text-to-Video Generation

`2026-11-10` · University of Illinois Chicago

[完整书目](../README.zh-CN.md#paper-2611-13576) · [论文](https://arxiv.org/abs/2611.13576) · [代码](https://github.com/chenyil6/phyRubric) · [数据集](https://huggingface.co/datasets/kittyhy/PhyRubric-Bench)

以针对描述预先制定的 rubric，逐项诊断生成视频中可见的物理常识错误。

**具体方法：** 在观看视频前固定语义和物理要求，用带时间戳的证据支持逐项判定，再由判定计算分数；已发布的评测与训练视频用于微调 VLM 评审模型。

**评估对象：** 生成视频中可见的物理现象；相邻诊断参照

**验证：** 通过与人工判定的一致性及未见生成器／领域测试评估评审器。对象是非交互视频的物理合理性，不是可执行动力学；训练更新评审模型权重，而非 Coding Agent。评测标签经人工核验，训练标签来自 Agent 标注器。

**关联：** [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2611-09017"></a>
<!-- stage3-record: {"id": "2611.09017", "scope": "Adjacent", "section": 3} -->

#### Frontier3DBench: Benchmarking Coding Agents for 3D Creation across Objects, Scenes, and Interactive Open Worlds

`2026-11-06` · Navers Lab; Einsia.AI; Tsinghua University

[完整书目](../README.zh-CN.md#paper-2611-09017) · [论文](https://arxiv.org/abs/2611.09017) · [论文](https://arxiv.org/html/2611.09017)

跨 Blender 与 Unreal Engine 评测代码生成的物体、场景和交互世界，连接可视化产物与可执行任务要求。

**具体方法：** 按任务产物要求，结合渲染证据与原生场景结构；交互世界还通过运行时检查验证交互契约和持久状态。

**评估对象：** 物体、场景与交互任务环境

**验证：** 覆盖范围是广义 3D 创作，其中包含功能性世界检查；视觉或交互任务成功仍不等于物理参数已校准。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2611-05802"></a>
<!-- stage3-record: {"id": "2611.05802", "scope": "Adjacent", "section": 3} -->

#### GREP: Grounding Generated Room Evaluation in Principles

`2026-11-04` · University of Washington; Tencent AI Lab; HKUST; USTC; Shanghai Jiao Tong University

[论文](https://arxiv.org/abs/2611.05802) · [论文](https://arxiv.org/html/2611.05802)

提出一个检查生成房间的评估 Agent：根据具体场景主动寻找问题，调用几何工具并选择观察视角，从物理有效性、视觉协调和日常使用逻辑三个方面给出分数与诊断报告。报告还能作为反馈，帮助生成系统修订场景。

**具体方法：** 将物理有效性、视觉协调和人的使用逻辑落实为场景专属检查，结合几何工具与主动选取的渲染视角生成诊断。

**评估对象：** 物体与场景

**验证：** 碰撞、支撑、边界与通行等主要是静态检查；不能据此断言动力学模拟正确。评估器的主动观察也不等于构建 Agent 的修复闭环。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2610-37326"></a>
<!-- stage3-record: {"id": "2610.37326", "scope": "Adjacent", "section": 3} -->

#### ScIntBench: Physical Interaction Plausibility in 3D Scene Generation

`2026-10-27` · University of Western Australia; University of British Columbia

[完整书目](../README.zh-CN.md#paper-2610-37326) · [论文](https://arxiv.org/abs/2610.37326) · [论文](https://arxiv.org/html/2610.37326)

把文字生成的室内场景放进物理仿真，按统一协议执行推、开合和表面探测等动作，检查场景是否真的支持交互。它要揭示的是：物体摆得合理、静止时没有明显错误，并不保证动起来以后仍然可用。

**具体方法：** 对生成场景执行推、开合与表面探测等标准交互，结合语义、静态有效性和动态响应检查交互合理性。

**评估对象：** 物体与场景

**验证：** 主要衡量需求与交互合理性，不要求重建唯一真实现场；部分动态判断使用视频评审，控制器自身失败须单独处理。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-system-blenderworld"></a>
<!-- stage3-record: {"id": "system:blenderworld", "scope": "Core", "section": 3} -->

#### BlenderWorld: Benchmarking Visual Agents for 3D Creation from Real-World References

`2026-10-14` · Zhejiang University; Alibaba Token Hub, Alibaba Group; The Chinese University of Hong Kong; Fudan University; National University of Singapore

[完整书目](../README.zh-CN.md#paper-system-blenderworld) · [论文](https://arxiv.org/abs/2610.23986) · [论文](https://arxiv.org/html/2610.23986) · [项目页](https://blenderworld.github.io/)

提供来自建筑、产品、自然环境和科学可视化的 3D 创作任务，让 Agent 根据文字、图片、视频或规格文件，用 Blender 创建或编辑可复用的场景。评估时结合多视角渲染、原生场景检查和逐任务要求，判断最终作品是否完成创作意图。

**具体方法：** 结合重新渲染与原生场景检查，对照创作需求评价功能、几何、外观及产物质量。

**评估对象：** 物体与场景

**验证：** 与 Coding Agent 直接相关，但大部分任务不等于物理模拟器重建；引用适合的评估维度，不把整套任务归为物理仿真。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2610-17521"></a>
<!-- stage3-record: {"id": "2610.17521", "scope": "Adjacent", "section": 3} -->

#### YUBI-Real2Sim: 3DGS Scene Verification for Reliable Policy Evaluation

`2026-10-13` · AI Robot Association (AIRoA); Waseda University

[论文](https://arxiv.org/abs/2610.17521) · [论文](https://arxiv.org/html/2610.17521) · [项目页](https://research.airoa.io/publications/yubi-real2sim/) · [数据集](https://huggingface.co/datasets/airoa-org/yubi-real2sim-assets) · [代码](https://github.com/airoa-org/yubi-real2sim)

把真实机器人场景重建为 3D 高斯视觉场景，并接入 MuJoCo 进行策略测试；通过真实与仿真的配对实验，研究重建中的孔洞、漂浮伪影等缺陷会怎样改变策略表现和排名。重点是判断这样的数字场景能否可靠地替代部分实机评测。

**具体方法：** 组合标定的腕部相机视图与 MuJoCo，比较同一策略的实机／仿真排名；仅改变背景伪影，固定物体、物理与 rollout 条件，分析重建质量的影响。

**评估对象：** 任务环境

**验证：** 视觉分数不足以可靠识别策略排名失败；仍需物理／控制对齐。已发布的资产和策略覆盖明确的配置，资产需申请访问，并非无条件开放下载。

**关联：** [2. Simulator 构建](#section-2) · [4. 数据](#section-4)

<a id="work-2610-17288"></a>
<!-- stage3-record: {"id": "2610.17288", "scope": "Core", "section": 3} -->

#### PhysCodeGym: Benchmarking Coding Agents for Physically Verifiable 4D Reconstruction

`2026-10-12` · Shanghai Jiao Tong University; Sun Yat-sen University; Shanghai Innovation Institute; Southeast University; Nanyang Technological University; Carnegie Mellon University

[完整书目](../README.zh-CN.md#paper-2610-17288) · [论文](https://arxiv.org/abs/2610.17288) · [论文](https://arxiv.org/html/2610.17288)

让 Coding Agent 观察物理过程的视频，自主编写、运行和修订 Blender 场景程序，重建刚体、液体、可变形物体及风驱动现象。除了比较重建画面，还检查程序和场景中的物理机制，并在部分任务中改变条件后重新仿真。

**具体方法：** 检查 Coding Agent 交付的可执行场景、视觉与运动一致性、物理有效性，并对部分任务施加反事实干预后重新仿真。

**评估对象：** 动态世界与仿真案例

**验证：** 要求主要运动由物理机制产生；并非每个样例都有同样的干预测试，也不要求不可辨识的隐藏参数逐一精确恢复。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2610-15166"></a>
<!-- stage3-record: {"id": "2610.15166", "scope": "Adjacent", "section": 3} -->

#### ExeWorldBench: Benchmarking Code-Based Executable 3D World Modeling

`2026-10-10` · University of Science and Technology of China; The Chinese University of Hong Kong

[完整书目](../README.zh-CN.md#paper-2610-15166) · [论文](https://arxiv.org/abs/2610.15166) · [论文](https://arxiv.org/html/2610.15166)

让 Coding Agent 从视觉参考或高层目标出发，编写一个能够运行的 3D 世界；任务从单个机械机制逐步扩展到多阶段联动系统和目标驱动的世界设计。它研究模型能否把对结构、运动和因果关系的理解落实为可执行产物。

**具体方法：** 评价代码生成世界的视觉结构、机械运动、因果过程与目标达成，区分可运行产物和满足要求的世界。

**评估对象：** 动态世界与仿真案例

**验证：** 主要根据采样渲染帧进行多模态评审；“因果”评分不能直接当成原生物理状态审计或反事实因果验证。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2610-08720"></a>
<!-- stage3-record: {"id": "2610.08720", "scope": "Adjacent", "section": 3} -->

#### WorldSolver: Can LLM Agents Simulate the Physical Dynamics via Solver Generation?

`2026-10-06` · NLPR & MAIS, CASIA; Peking University; Huawei Noah’s Ark Lab

[完整书目](../README.zh-CN.md#paper-2610-08720) · [论文](https://arxiv.org/abs/2610.08720) · [论文](https://arxiv.org/html/2610.08720)

把经典物理模拟问题变成编程任务：给 Agent 一个已经准备好场景和执行接口的代码框架，让它补全决定系统如何随时间演化的求解器。随后运行程序，分别检查执行成功、目标现象的再现程度和物理合理性。

**具体方法：** 在给定场景和执行框架中让 Coding Agent 编写求解器，分别检查可运行性、视觉事件和物理行为。

**评估对象：** 动力学模型与求解器

**验证：** 主要改写动力学求解程序，几何、参数与框架有预设；不是从零搭建完整通用仿真引擎。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2610-04432"></a>
<!-- stage3-record: {"id": "2610.04432", "scope": "Core", "section": 3} -->

#### Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos

`2026-10-03` · Aether AI; University of California San Diego

[完整书目](../README.zh-CN.md#paper-2610-04432) · [论文](https://arxiv.org/abs/2610.04432) · [论文](https://arxiv.org/html/2610.04432) · [文档](https://github.com/AetherLabsAI/Video2World/blob/main/docs/benchmark.md)

把机器人或人类示范视频转化为一项端到端软件工程任务：Agent 既要重建模拟环境，也要编写对应的机器人行为，并根据执行反馈反复修改。最终检查空间结构、动态过程和交互任务能否在生成世界中重现。

**具体方法：** 执行提交的环境—行为程序组合，比较几何、物体轨迹和任务结果；补充交叉执行用来诊断控制器与场景的兼容性。

**评估对象：** 动态世界与仿真案例

**验证：** 任务成功是环境与行为的共同结果。参照几何／运动可能来自测量、拟合或仿真；人工辅助重建（HAR）的执行轨迹独立于这些评价目标，也不构成性能上界。

**关联：** [2. Simulator 构建](#section-2) · [4. 数据](#section-4)

<a id="work-2610-03715"></a>
<!-- stage3-record: {"id": "2610.03715", "scope": "Adjacent", "section": 3} -->

#### 4DCodeBench: Benchmarking Agents on Inverse Graphics of Dynamic Scenes

`2026-10-02` · Johns Hopkins University; Stanford University; Max Planck Institute for Intelligent Systems; Massachusetts Institute of Technology

[完整书目](../README.zh-CN.md#paper-2610-03715) · [论文](https://arxiv.org/abs/2610.03715) · [论文](https://arxiv.org/html/2610.03715)

要求 Agent 将真实或合成的动态视频重建成可执行图形程序，恢复场景的三维结构及其随时间发生的变化。基准同时比较画面和运动，并利用合成场景的三维真值作更直接的检查；实现方式可以是关键帧、解析轨迹或物理模拟。

**具体方法：** 从参考视频重建可执行 4D 场景，联合评价外观、2D 运动、2.5D 几何，以及合成子集上的 3D 几何和运动。

**评估对象：** 动态世界与仿真案例

**验证：** 允许关键帧、规定轨迹或物理模拟；高重建分数不保证学到正确物理机制。真实视频的深度／运动参照部分来自估计模型。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2609-36777"></a>
<!-- stage3-record: {"id": "2609.36777", "scope": "Core", "section": 3} -->

#### Code4Scene: Benchmarking Coding Agents for Constructing and Editing 3D Scenes

`2026-09-29` · University of California San Diego; University of California Berkeley

[完整书目](../README.zh-CN.md#paper-2609-36777) · [论文](https://arxiv.org/abs/2609.36777) · [论文](https://arxiv.org/html/2609.36777)

在统一 Unreal Engine 接口下研究两类任务：根据文字构建新场景，以及根据参考图精确修改已有场景。它直接检查引擎中的场景状态，特别关注目标是否实现、资产是否完整，以及修改一个地方时有没有破坏其他内容。

**具体方法：** 检查构建产物满足任务要求的程度、场景完整性和静态物理有效性，编辑任务还关注目标修改与无关内容保留。

**评估对象：** 物体与场景

**验证：** 适合检查场景构建结果；不应把静态有效性直接等同于动态物理或真实参数校准。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2611-02659"></a>
<!-- stage3-record: {"id": "2611.02659", "scope": "Adjacent", "section": 3} -->

#### Parametric CAD Bench v3: Evaluating Agentic Parametric CAD Authoring from Text and Engineering Drawings

`2026-09-21` · gNucleus AI, Inc.

官方基准首发：2026-09-21；arXiv v1：2026-11-02。

[完整书目](../README.zh-CN.md#paper-2611-02659) · [论文](https://arxiv.org/abs/2611.02659) · [文章](https://cadbench.ai/news/cad-bench-v3) · [数据集](https://huggingface.co/datasets/gnucleus-ai/cad-gen-freecad-bench-v3)

评测根据文字、先创建再编辑的要求和工程图纸，构建原生参数化 CAD 产物的能力。

**具体方法：** 在固定 FreeCAD／Harbor 环境中运行 Agent，由隔离评测器分别检查原生几何和规格一致性；版本化任务另配已发布的运行记录、轨迹与 CAD 产物。

**评估对象：** 物体与原生参数化 CAD 几何

**验证：** 连续奖励不等于二元任务成功率。这里检查参数化物体和特征结构，不验证动力学或制造认证；先创建再编辑的得分也不证明复用了基础模型的特征历史。已发布运行资料是实验产物，不是另行验证的训练数据集。

**关联：** [4. 数据](#section-4) · [6. 物理应用与实验](#section-6)

<a id="work-2609-15478"></a>
<!-- stage3-record: {"id": "2609.15478", "scope": "Adjacent", "section": 3} -->

#### BVB: Benchmarking Agentic Video Understanding via Programmatic Reconstruction in Blender

`2026-09-14` · University of Rochester; Sony Group Corporation; Carnegie Mellon University; University of Washington

[完整书目](../README.zh-CN.md#paper-2609-15478) · [论文](https://arxiv.org/abs/2609.15478) · [论文](https://arxiv.org/html/2609.15478)

让多模态 Agent 在统一预算和运行环境中，把真实视频重新写成带动画的 Blender 场景。通过渲染相似性以及原视频和重建视频中的时空事实是否一致，检验模型能否把视频理解转化为可复现的程序表达。

**具体方法：** 用 Blender 程序表达视频内容，通过重建表征的相似性和视频问答中的信息保留检查理解与重建。

**评估对象：** 动态世界与仿真案例

**验证：** 其重建评估不能保证真实物理机制；需要区别静态场景随相机运动的变化与物体本身的动力学。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2606-01869"></a>
<!-- stage3-record: {"id": "2606.01869", "scope": "Adjacent", "section": 3} -->

#### WorldCoder-Bench: Benchmarking Physically Grounded 3D World Synthesis

`2026-06-01` · NLPR & MAIS, CASIA; Huawei Noah’s Ark Lab

[论文](https://arxiv.org/abs/2606.01869) · [论文](https://arxiv.org/html/2606.01869)

要求模型根据自然语言生成浏览器中的交互式 3D 程序，任务包括模拟、渲染和应用。其 StateProbe 评估器会实际运行程序、执行动作并检查隐藏的状态要求，用来发现画面正常但交互逻辑或状态变化错误的产物。

**具体方法：** 通过 StateProbe 在预设动作后读取运行状态和状态变化，检查生成世界是否满足任务契约。

**评估对象：** 动态世界与仿真案例

**验证：** 这里只关注其物理模拟相关任务；整套基准还覆盖渲染和应用，运行状态满足契约不等于真实世界参数已校准。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2606-01538"></a>
<!-- stage3-record: {"id": "2606.01538", "scope": "Adjacent", "section": 3} -->

#### MPMWorlds: Material-Point-Method Simulations for Inferring and Extrapolating Physical Dynamics

`2026-06-01` · Cornell University

[论文](https://arxiv.org/abs/2606.01538) · [论文](https://arxiv.org/html/2606.01538)

构建包含可变形体、流体和多种材料的二维 MPM 模拟数据，让模型根据一段已观测视频及不同程度的场景信息预测后续过程。它对比两条路线：生成并运行模拟程序，或者直接生成未来视频，研究两者在物理推断和长时外推上的差别。

**具体方法：** 根据观测前缀生成 MPM 程序并向未来运行，在留出的后续时间段比较运动、空间重合、物体保留和时间稳定性。

**评估对象：** 动态世界与仿真案例

**验证：** 评测阶段主要比较输出视频，未直接使用粒子轨迹或物理状态；限于合成 2D MPM 世界。此处引用评测贡献，数据资源不重复计为独立论文。

**关联：** [2. Simulator 构建](#section-2) · [4. 数据](#section-4)

<a id="work-2605-20576"></a>
<!-- stage3-record: {"id": "2605.20576", "scope": "Adjacent", "section": 3} -->

#### Δynamics: Language-Based Representation for Inferring Rigid-Body Dynamics From Videos

`2026-05-20` · Cornell University; Amazon

[论文](https://arxiv.org/abs/2605.20576) · [论文](https://arxiv.org/html/2605.20576)

训练视觉语言模型从视频运动线索中推断物体形状、初始状态、物理属性和相机参数，并以结构化文本输出完整场景配置。配置交给物理引擎重新模拟，再通过采样和搜索改进匹配，研究语言表示能否连接视频理解与刚体动力学重建。

**具体方法：** 生成供模拟器执行的结构化场景配置，比较重仿真与参考的物体组成、掩码 IoU、光流误差及有真值时的参数误差。

**评估对象：** 动力学模型与求解器

**验证：** 输出主要是结构化配置，不等同于通用 Coding Agent；真实视频使用模型生成的伪标注，不能当作直接测得的全部物理真值。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2604-23580"></a>
<!-- stage3-record: {"id": "2604.23580", "scope": "Adjacent", "section": 3} -->

#### PhysCodeBench: Benchmarking Physics-Aware Symbolic Simulation of 3D Scenes via Self-Corrective Multi-Agent Refinement

`2026-04-26` · Nanjing University; Skywork AI; Jilin University; Great Wall Motor; Tianjin University

[论文](https://arxiv.org/abs/2604.23580) · [论文](https://arxiv.org/html/2604.23580)

将自然语言描述的物理现象转化为模拟代码生成任务，检查程序是否运行、画面是否符合要求以及物理断言是否成立。论文还提出专门负责生成与物理纠错的多 Agent 流程，研究有针对性的错误修正能否提升模拟的物理准确性。

**具体方法：** 检查生成程序的执行与产物、渲染外观和运动，并另外使用专家物理断言及适用场景的守恒检查。

**评估对象：** 动态世界与仿真案例

**验证：** 综合分中的视觉指标与另行报告的物理断言不是同一件事；不能只看总分就宣称物理正确。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2604-13035"></a>
<!-- stage3-record: {"id": "2604.13035", "scope": "Adjacent", "section": 3} -->

#### SceneCritic: A Symbolic Evaluator for 3D Indoor Scene Synthesis

`2026-04-14` · Stony Brook University

[论文](https://arxiv.org/abs/2604.13035) · [论文](https://arxiv.org/html/2604.13035)

从已有室内数据中整理空间常识和约束，建立直接检查布局与物体关系的符号评估器，指出具体哪些摆放合理、哪些关系违规。论文还比较规则、文本模型和视觉模型提供的反馈，研究不同反馈怎样影响场景修订。

**具体方法：** 使用符号化场景信息检查尺度、物体搭配、邻近关系、朝向、完整性与重叠，形成可解释的布局质量判断。

**评估对象：** 物体与场景

**验证：** 偏静态语义和几何质量，不直接验证物理时间演化；并非仅针对 Coding Agent。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2603-29798"></a>
<!-- stage3-record: {"id": "2603.29798", "scope": "Adjacent", "section": 3} -->

#### SceneTeract: Probing and Improving Agent-Aware Activity Reasoning in 3D Indoor Scenes

`2026-03-31` · École Polytechnique; Dassault Systèmes; Stanford University; Università della Svizzera italiana

[论文](https://arxiv.org/abs/2603.29798) · [论文](https://arxiv.org/html/2603.29798)

输入一个室内场景、一项活动以及执行者的身体条件，把活动拆成针对物体的具体动作，再检查可达范围、操作空间和路径是否允许这些动作。系统返回失败原因，并利用这些验证反馈训练视觉语言模型，使其更准确判断场景能否支持活动。

**具体方法：** 根据活动与使用者条件检查可达、操作空间和路径等几何条件，判断场景是否支持相应活动。

**评估对象：** 物体与场景

**验证：** 用于场景的功能可用性检查，同时评测模型判断可行性的能力；不是机器人真实动力学执行验证。

**关联：** [2. Simulator 构建](#section-2) · [5. 训练与能力提升](#section-5)

<a id="work-2603-16432"></a>
<!-- stage3-record: {"id": "2603.16432", "scope": "Adjacent", "section": 3} -->

#### IRIS: A Real-World Benchmark for Inverse Recovery and Identification of Physical Dynamic Systems from Monocular Video

`2026-03-17` · Hamad Bin Khalifa University; Texas A&M University

[论文](https://arxiv.org/abs/2603.16432) · [论文](https://arxiv.org/html/2603.16432)

提供带独立物理测量和不确定性标注的真实动态视频，要求方法从视频推断系统的物理参数或支配方程。它建立统一协议，检查推断是否准确、参数能否辨认，以及恢复的模型能否解释后续时间和不同条件下的运动。

**具体方法：** 用独立测量的物理参照检查系统与参数恢复，并考察可辨识性、鲁棒性和时间外推。

**评估对象：** 动力学模型与求解器

**验证：** 提供带不确定性的独立物理测量参照，但不是专门面向 Coding Agent 的整场景构建基准。

**关联：** [2. Simulator 构建](#section-2) · [4. 数据](#section-4)

<a id="work-2602-10840"></a>
<!-- stage3-record: {"id": "2602.10840", "scope": "Adjacent", "section": 3} -->

#### Training and Benchmarking Code Generation for Physics-Inspired Animations

`2026-02-11` · Mohamed bin Zayed University of Artificial Intelligence; Sun Yat-sen University

[论文](https://arxiv.org/abs/2602.10840) · [论文](https://arxiv.org/html/2602.10840)

围绕多种物理概念收集动画场景描述，训练和评测 LLM 编写可执行代码，把这些现象表现为动画。论文还让视觉语言模型检查生成视频，并把视觉奖励用于强化学习；目标是物理启发动画的表达质量，而非严格验证动力学求解。

**具体方法：** 检查生成代码是否可执行及动画是否表现指定现象，并利用视觉验证反馈训练生成模型。

**评估对象：** 动态世界与仿真案例

**验证：** 目标是物理启发动画的可执行性和定性表现；视觉上呈现物理现象不等于数值上正确求解其动力学。

**关联：** [2. Simulator 构建](#section-2) · [5. 训练与能力提升](#section-5)

<a id="work-2602-13294"></a>
<!-- stage3-record: {"id": "2602.13294", "scope": "Adjacent", "section": 3} -->

#### VisPhyWorld: Probing Physical Reasoning via Code-Driven Video Reconstruction

`2026-02-09` · University of Waterloo; Autodesk AI Lab; independent researcher

[论文](https://arxiv.org/abs/2602.13294) · [论文](https://arxiv.org/html/2602.13294)

要求多模态模型把看到的物理视频写成能够运行的模拟器代码，使其对世界的理解变成可检查、可修改的程序。配套 VisPhyBench 用受控场景比较重建的外观与运动，研究模型能否从视觉线索恢复合理的物理过程。

**具体方法：** 让模型以程序重建视频中的世界，用画面、运动和整体物理合理性评审比较重建表现。

**评估对象：** 动态世界与仿真案例

**验证：** 主要指标是视觉／运动及评审代理量，不是全面的真实物理参数恢复；输入还可含首帧结构信息。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2511-03001"></a>
<!-- stage3-record: {"id": "2511.03001", "scope": "Adjacent", "section": 3} -->

#### Apples on the Table? Evaluating Text-Guided 3D Scene Synthesis via Fine-Grained Constraint Verification

`2025-11-04` · Yonsei University; POSTECH

[论文](https://arxiv.org/abs/2511.03001) · [论文](https://arxiv.org/html/2511.03001)

针对文字生成 3D 场景，提供带人工约束标注和参考场景的 LEGO 数据，并提出 LEGO-Eval。评估器把一句描述拆成物体、属性和相对位置等具体要求，再调用工具逐项核对，从而说明生成场景到底满足或遗漏了什么。

**具体方法：** 把场景要求分解成细粒度约束，借助工具、视角与空间信息逐项验证布局、物体选择及位置关系。

**评估对象：** 物体与场景

**验证：** 侧重需求符合度和空间关系，不能替代动态物理测试；LEGO 和 LEGO-Eval 为同一论文的相关贡献。

**关联：** [2. Simulator 构建](#section-2) · [4. 数据](#section-4)

<a id="work-2506-23329"></a>
<!-- stage3-record: {"id": "2506.23329", "scope": "Adjacent", "section": 3} -->

#### IR3D-Bench: Evaluating Vision-Language Model Scene Understanding as Agentic Inverse Rendering

`2025-06-29` · The Chinese University of Hong Kong; Tianjin University; EPFL; HKUST; Xiamen University; Massachusetts Institute of Technology

[论文](https://arxiv.org/abs/2506.23329) · [论文](https://arxiv.org/html/2506.23329)

给视觉语言 Agent 一张输入图，要求它主动使用编程和渲染工具，重新构造图像背后的三维场景。通过位置、数量、空间关系和外观等指标检查重建结果，研究模型是否能用实际创作展示场景理解，而不只是回答描述性问题。

**具体方法：** 通过重建场景检查物体定位、数量、空间关系、外观和语义，提供从图像到程序化场景的较早评测参照。

**评估对象：** 物体与场景

**验证：** 没有动态物理校准；定位、掩码等指标要区分图像空间与真正的三维物理真值。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2504-01786"></a>
<!-- stage3-record: {"id": "2504.01786", "scope": "Adjacent", "section": 3} -->

#### BlenderGym: Benchmarking Foundational Model Systems for Graphics Editing

`2025-04-02` · Stanford University

[论文](https://arxiv.org/abs/2504.01786) · [论文](https://arxiv.org/html/2504.01786)

给 Agent 起始场景和目标效果，让它通过修改 Blender Python 程序完成几何、材质、光照、位置或形变编辑。基准量化编辑结果，并进一步研究如何在生成候选与验证候选之间分配推理计算，以提高图形编辑质量。

**具体方法：** 让 Agent 修改 Blender 程序以匹配目标场景，使用多视角图像指标和相应三维距离评估编辑结果。

**评估对象：** 物体与场景

**验证：** 作者明确指出这些距离未必捕捉物理合理性；适合补充视觉／几何质量评估，不能替代模拟器验证。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2503-14756"></a>
<!-- stage3-record: {"id": "2503.14756", "scope": "Adjacent", "section": 3} -->

#### SceneEval: Evaluating Semantic Coherence in Text-Conditioned 3D Indoor Scene Synthesis

`2025-03-18` · Simon Fraser University; Amii

[论文](https://arxiv.org/abs/2503.14756) · [论文](https://arxiv.org/html/2503.14756)

为文字条件的室内场景生成建立一套细粒度评估框架和标注测试集。它同时核对文字明确提出的物体、属性与关系，以及用户通常不会写出的支撑、碰撞和通行要求，提供可解释的场景质量诊断。

**具体方法：** 同时检查物体、属性、空间关系等显式要求，以及碰撞、支撑、通行和开合空间等隐式合理性。

**评估对象：** 物体与场景

**验证：** 主要检查静态场景的语义和几何一致性，不能据此断言动态物理模拟正确。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2405-05941"></a>
<!-- stage3-record: {"id": "2405.05941", "scope": "Adjacent", "section": 3} -->

#### Evaluating Real-World Robot Manipulation Policies in Simulation

`2024-05-09` · University of California San Diego; Stanford University; University of California Berkeley; Google DeepMind

[论文](https://arxiv.org/abs/2405.05941) · [论文](https://arxiv.org/html/2405.05941)

针对实机策略评测昂贵且难复现的问题，构建与常见真实机器人设置对应的仿真环境，并减少视觉与控制差异。通过同一策略在仿真和实机中的配对测试，检查仿真能否反映真实表现及其对环境变化的敏感性。

**具体方法：** 研究仿真中的策略表现能否反映真实机器人的表现，为“构建的世界是否有评估用途”提供较早参照。

**评估对象：** 任务环境

**验证：** 评测对象主要是策略评估的可信度，不是 Coding Agent 重建；结果也受视觉、控制与动力学对齐影响。

**关联：** [1. 具身 Harness](#section-1) · [2. Simulator 构建](#section-2) · [5. 训练与能力提升](#section-5)

<a id="work-real2sim-benchmark"></a>
<!-- stage3-record: {"id": "real2sim-benchmark", "scope": "Adjacent", "section": 3} -->

#### Real2Sim Benchmark

`首发日期未明确` · Momentum Research Labs

[项目页](https://www.real2sim.bot/)

给 Coding Agent 真实机器人片段、相机标定和动作记录，让它重建对应的仿真场景。提交后冻结场景，再分别比较渲染结果、重放真实动作的结果和固定机器人策略的闭环表现，以检查重建世界的外观及使用价值。

**具体方法：** 根据真实片段构建并冻结场景，比较渲染匹配、固定动作重放及固定策略闭环执行的结果。

**评估对象：** 动态世界与仿真案例

**验证：** 当前版本用 LPIPS 与整图 DINOv2 相似度；开放环结果由知晓系统身份的人工评审判断，闭环尚无成功且缺少 known-good 场景对照，因此失败不能完全归因于重建。

**关联：** [2. Simulator 构建](#section-2)

### 跨章节阅读

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

[返回研究地图](#research-map)

---

<a id="section-4"></a>

## 4. 数据

数据把物理经验连接到学习，但需要分别说明观测、标签、执行检查与训练对象。真实观测可以配合合成标签，仿真轨迹也可以渲染成接近真实的视频；这些来源组合本身不能把仿真回合变成实机执行。

| 数据形式 | 观测与标签来源 | 执行检查及用途 |
|---|---|---|
| 真实观测 | [DROID](#work-2403-12945) 配对遥操作机器人观测与动作；[Open-HumanWAM](#work-2611-06817) 对齐跨来源的人类视频、语言与手部运动，其中含生成片段。 | 机器人执行或人类记录提供观测，下游策略／WAM 评估衡量用途；人类手部运动不等于实测机器人动作。 |
| 合成环境与示范 | [RoboTwin 2.0](#work-2506-18088)、[EmbodiedSmith](#work-2610-07969) 与 [CoDA](#work-2610-22362) 构建任务，并用可执行控制器生成轨迹。 | 仿真成功谓词与轨迹审查筛选回合，策略训练检验数据是否有助于生成案例之外的任务。 |
| 程序与工具轨迹 | [RAX](#work-2610-22496) 发布实机会话文本、工具调用、机器人状态、视频及生成技能；[CaPtain](#work-2610-40799) 使用教师交互轨迹进行后训练。 | 保存的程序须对应实际执行证据；公开日志档案与经整理的训练集承担不同角色。 |
| 失败与修复 | [LabRobFail](#work-2607-23704) 结合仿真失败注入、元数据标签、LLM 标注、规则及人工抽样。 | 诊断准确率、未见失败与执行恢复分别回答不同问题；监督用于训练失败分析 VLM。 |
| 配对与受控数据 | [DataFarm](#work-2611-05320) 将仿真动作与图像条件化视频配对；[PhysOPSD](#work-2611-12411) 对齐程序、物理变体与视觉草稿；[TactileLab](#work-2611-07881) 对齐真实与仿真触觉。 | 保持动作／视频对齐，控制改变的变量，并分别评估所得机器人策略、视频模型或触觉转换器。 |

**发布状态与训练角色。** 数据集、构造方法与实验轨迹分别标注。BlenderFORGE 和 PhysOPSD 描述的训练材料仍待发布，Open-HumanWAM 提供有访问条件的语料。程序轨迹可以监督 Coding Agent，示范动作通常训练下游动作策略；同一仿真器支持两者，并不意味着两种实验相同。

**研究问题。** 固定仿真器、控制器、监督与评测预算后，成功回合、失败尝试及经过验证的修复如何配比，才能提升 Coding Agent 在未见物理任务上的能力？

### 真实观测与交互记录

<a id="work-2611-06817"></a>
<!-- stage3-record: {"id": "2611.06817", "scope": "Adjacent", "section": 4} -->

#### Open-HumanWAM: An Open Recipe for Scaling Human and Robot Experience for Embodied Foundation Models

`2026-11-04` · Peking University; National University of Singapore; Massachusetts Institute of Technology; University of California, Santa Barbara; NVIDIA

[完整书目](../README.zh-CN.md#paper-2611-06817) · [论文](https://arxiv.org/abs/2611.06817) · [项目页](https://dagroup-pku.github.io/open-humanwam/) · [代码](https://github.com/DAGroup-PKU/HumanNet/tree/Open-HumanWAM)

整理人类操作经验及对齐动作，用于世界—动作模型预训练与机器人适配。

**具体方法：** Open-HumanWAM-50K 汇合五类来源（含生成式第一视角数据），筛选手部可见性、运动和静止片段，对齐相机坐标、腕轴及夹爪开合，将视频与语言、手部运动配对。纯人类及人机混合训练更新 WAM 参数。

**验证：** 包含 RoboTwin／RoboDojo 规模与对齐研究、20 项真实零样本任务，以及另行开展的任务专属后训练。目标图像审查检查可见一致性，不证明物理可行性。开放语料的访问需同意数据使用条件。

**关联：** [1. 具身 Harness](#section-1) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2406-18915"></a>
<!-- stage3-record: {"id": "2406.18915", "scope": "Adjacent", "section": 4} -->

#### Manipulate-Anything: Automating Real-World Robots using Vision-Language Models

`2024-06-27` · University of Washington; Universidad Católica San Pablo; Allen Institute for Artificial Intelligence; NVIDIA

[论文](https://arxiv.org/abs/2406.18915) · [项目页](https://robot-ma.github.io/)

用视觉语言反馈自动采集真实示范。

**具体方法：** 通过视觉语言反馈自动生成真实机器人操作示范，并检验这些真实执行轨迹能否训练更稳健的下游行为克隆策略。

**验证：** 真实轨迹训练下游策略，初始化包含人工提供的代码例子。

<a id="work-2403-12945"></a>
<!-- stage3-record: {"id": "2403.12945", "scope": "Resource", "section": 4} -->

#### DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset

`2024-03-19` · Stanford University; University of California, Berkeley; Toyota Research Institute; Carnegie Mellon University; University of Texas at Austin; University of Montreal; University of Edinburgh; Princeton University; University of Washington; KAIST; University of California, San Diego; Google DeepMind; University of California, Davis; University of Pennsylvania; Columbia University; Yonsei University

[论文](https://arxiv.org/abs/2403.12945) · [项目页](https://droid-dataset.github.io/)

提供机器人学习所需的真实观测来源。

**具体方法：** 提供跨场景的真实机器人遥操作轨迹；RoboPro 将其中视频用作合成策略代码标签的真实观测来源。

**验证：** 开放遥操作数据本身不包含 Agent 推理、工具调用或代码修复轨迹。

### 合成数据与构造方法

<a id="work-2611-12411"></a>
<!-- stage3-record: {"id": "2611.12411", "scope": "Core", "section": 4} -->

#### PhysOPSD: Code as Privilege for Physically Plausible Video Generation

`2026-11-09` · Hong Kong University of Science and Technology; Alibaba Token Hub; Alibaba Group

[完整书目](../README.zh-CN.md#paper-2611-12411) · [论文](https://arxiv.org/abs/2611.12411) · [项目页](https://haroldchen19.github.io/PhysOPSD-site/)

构建可执行物理场景及配对视觉监督，用于视频生成器后训练。

**具体方法：** Coding Agent 依据参考构建 MuJoCo／Genesis／Blender 程序，通过执行日志、运动学诊断与预览关键帧修复；冻结轨迹后生成不同抽象程度的草稿和受控参数变体。共享噪声蒸馏更新视频模型权重，而非 Coding Agent。

**验证：** 在 VideoPhy-2、PhyGround、VBench 上评估并消融特权信息和参数变体。PhysOPSD-3K 合计约 3,000 个基础场景／变体条目，尚待发布。修复循环位于数据构造阶段，部署的视频生成无需仿真。

**关联：** [2. Simulator 构建](#section-2) · [3. Simulator 质量评估](#section-3) · [5. 训练与能力提升](#section-5)

<a id="work-2611-05320"></a>
<!-- stage3-record: {"id": "2611.05320", "scope": "Adjacent", "section": 4} -->

#### PyRUA-DataFarm: LLM Agent as a Cost-Efficient Teleoperator for Real-Ready Robot Data

`2026-11-03` · Peking University; NVIDIA

[完整书目](../README.zh-CN.md#paper-2611-05320) · [论文](https://arxiv.org/abs/2611.05320) · [项目页](https://dagroup-pku.github.io/PyRUA-Lean/DataFarm) · [代码](https://github.com/DAGroup-PKU/PyRUA-Lean/tree/DataFarm)

组合代码与视频模型生成动作标注数据。

**具体方法：** 编排 Agent 编写的仿真任务、专家控制器与真实图像条件视频模型，生成带动作标签的多视角训练轨迹并迁移到实体机器人。

**验证：** 五类 PiPER 任务比较匹配数据量与外观迁移，发布的是流程而非数据集。

<a id="work-2610-22362"></a>
<!-- stage3-record: {"id": "2610.22362", "scope": "Core", "section": 4} -->

#### CoDA: Co-Evolution of Data Engines and Action Policies

`2026-10-15` · University of Illinois Urbana-Champaign; Chinese University of Hong Kong, Shenzhen; Amazon

[完整书目](../README.zh-CN.md#paper-2610-22362) · [论文](https://arxiv.org/abs/2610.22362) · [项目页](https://plan-lab.github.io/projects/coda/)

共同演化数据生成程序与机器人策略。

**具体方法：** 将基于视频的机器人失败诊断转化为可复用的场景生成程序与训练势函数程序，再通过仿真中测得的学习进展持续修订程序和动作策略。

**验证：** 生成器修改场景和成功判据，下游策略使用独立训练信号。

**关联：** [2. Simulator 构建](#section-2) · [5. 训练与能力提升](#section-5)

<a id="work-2610-07969"></a>
<!-- stage3-record: {"id": "2610.07969", "scope": "Core", "section": 4} -->

#### EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation

`2026-10-06` · HKUST (Guangzhou); Xiaomi Robotics; Southeastern University; Tsinghua University; Zhejiang University; Westlake University; Symbiosis Robotics; Peking University; Xi’an Jiaotong University; Beijing Academy of Artificial Intelligence

[论文](https://arxiv.org/abs/2610.07969)

构建可自改进的仿真数据引擎。

**具体方法：** 把资产、场景、任务和求解程序组织成自改进数据引擎，在仿真中生成经执行验证的机器人学习数据。

**验证：** 数据引擎改进与下游策略提升是不同结果。

<a id="work-2609-35318"></a>
<!-- stage3-record: {"id": "2609.35318", "scope": "Core", "section": 4} -->

#### DexAgent: An Agentic Human2Sim2Robot Framework for Dexterous Manipulation with Self-Evolving Tool Library

`2026-09-28` · Stanford University; Columbia University

[论文](https://arxiv.org/abs/2609.35318) · [项目页](https://dexagent1.github.io/) · [项目页](https://dexagent123.github.io/)

把人类视频转为仿真灵巧操作监督。

**具体方法：** 让 Agent 从人类视频重建任务并自我改进工具库，将仿真中的物理校验结果转成灵巧机器人轨迹与策略监督。

**验证：** 真实输入视频与合成输出示范具有不同来源。

**关联：** [2. Simulator 构建](#section-2) · [5. 训练与能力提升](#section-5)

<a id="work-2609-27308"></a>
<!-- stage3-record: {"id": "2609.27308", "scope": "Core", "section": 4} -->

#### EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics

`2026-09-23` · ByteDance Seed; Yale University; Princeton University; Carnegie Mellon University; Stanford University; University of California, Los Angeles; University of Washington

[论文](https://arxiv.org/abs/2609.27308)

把验证过的机器人程序扩展为合成示范。

**具体方法：** 让 Coding Agent 解长时序灵巧操作任务，再把经验证的程序解扩展成多样仿真轨迹以训练机器人策略。

**验证：** 主体在仿真中开发与生成数据，另以合成数据训练策略完成一项实机长任务。

**关联：** [1. 具身 Harness](#section-1) · [2. Simulator 构建](#section-2) · [5. 训练与能力提升](#section-5)

<a id="work-2607-23704"></a>
<!-- stage3-record: {"id": "2607.23704", "scope": "Adjacent", "section": 4} -->

#### LabRobFail: A Benchmark for Robotic Failure Analysis in Chemical Self-driving Laboratory

`2026-07-26` · Dalian University of Technology; Shenzhen Loop Area Institute; Harbin Institute of Technology; Shanghai AI Laboratory; HKUST; Chinese University of Hong Kong

[论文](https://arxiv.org/abs/2607.23704) · [代码](https://github.com/Su-ISE-2001/LabRobFail)

构建带有结构化诊断及纠正标签的仿真实验室失败轨迹。

**具体方法：** 在 LabUtopia 中扰动控制关键帧、物理参数与任务语义并执行轨迹；LLM 依据仿真元数据生成问答，经规则过滤与人工抽样检查。混合微调训练失败分析 VLM，固定动作字典执行其纠正建议。

**验证：** 报告超过 2 万条轨迹、六类诊断任务及未见物体／场景划分，并测试 OpenVLA／ACT 下游恢复。文本纠正分数与仿真恢复不等于真实实验室安全验证，也不是 Coding Agent 后训练。

**关联：** [1. 具身 Harness](#section-1) · [5. 训练与能力提升](#section-5) · [6. 物理应用与实验](#section-6)

<a id="work-2506-18088"></a>
<!-- stage3-record: {"id": "2506.18088", "scope": "Adjacent", "section": 4} -->

#### RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation

`2025-06-22` · Lumina EAI; Shanghai AI Lab; Shenzhen University; Nanjing University; TeleAI; Fudan University; Sun Yat-sen University; USTC; Central South University; SUSTech; Tsinghua University; D-Robotics; Shanghai Jiao Tong University; HKU; Northeastern University

[论文](https://arxiv.org/abs/2506.18088) · [项目页](https://robotwin-platform.github.io/) · [代码](https://github.com/robotwin-Platform/robotwin/) · [代码](https://github.com/robotwin-Platform/robotwin) · [项目页](https://robotwin-platform.github.io/doc/) · [代码](https://github.com/RoboTwin-Platform/RoboTwin)

生成多样化双臂操作训练轨迹。

**具体方法：** 用多模态模型生成双臂任务执行代码并在仿真中修订，结合域随机化批量生成轨迹，支持策略训练与统一评测。

**验证：** 仿真修订、数据生成和实机策略实验各提供不同证据。

**关联：** [1. 具身 Harness](#section-1) · [2. Simulator 构建](#section-2)

<a id="work-2410-03645"></a>
<!-- stage3-record: {"id": "2410.03645", "scope": "Adjacent", "section": 4} -->

#### GenSim2: Scaling Robot Data Generation with Multi-modal and Reasoning LLMs

`2024-10-04` · Tsinghua University; University of California, San Diego; Shanghai Jiao Tong University; MIT CSAIL

[论文](https://arxiv.org/abs/2410.03645) · [项目页](https://gensim2.github.io/)

通过生成任务与求解器扩大机器人示范。

**具体方法：** 用多模态编码模型生成关节操作任务，并以规划和强化学习求解器批量获得示范，训练可迁移的下游机器人策略。

**验证：** 任务、求解器与示范支持下游策略学习，不是任务生成 LLM 后训练。

**关联：** [2. Simulator 构建](#section-2) · [5. 训练与能力提升](#section-5)

<a id="work-2307-14535"></a>
<!-- stage3-record: {"id": "2307.14535", "scope": "Adjacent", "section": 4} -->

#### Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition

`2023-07-26` · Columbia University; Google DeepMind

[论文](https://arxiv.org/abs/2307.14535) · [项目页](https://www.cs.columbia.edu/~huy/scalingup/)

将语言组织的机器人经验蒸馏为动作策略。

**具体方法：** 让 LLM 组织机器人技能与成功判定代码，批量生成带语言标签的仿真轨迹，再蒸馏为下游视觉运动策略。

**验证：** 生成示范训练的是视觉运动策略，不是写码 LLM。

### 跨章节阅读

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

[返回研究地图](#research-map)

---

<a id="section-5"></a>

## 5. 训练与能力提升

本节的组织问题是：**获得经验后，实际改变了什么？** 机器人表现改善可能来自代码优化、动作策略训练、技能库积累、上下文增加或 Agent 参数更新。以下三条线保留这些区别。

| 路线 | 更新对象 | 代表性证据 |
|---|---|---|
| 程序与下游策略研发 | 奖励／控制器／源码、训练流程或下游机器人策略。 | [Eureka](#work-2310-12931) 搜索奖励程序，再训练策略；[ENPIRE](#work-2606-19980) 通过物理执行改进策略及其学习流程。Agent 编写训练代码，不等于 Agent 自身接受训练。 |
| 经验、记忆与技能学习 | 可执行技能、检索／路由、笔记或推理上下文。 | [ASPIRE](#work-2607-00272) 积累经过验证的技能；[WICL](#work-2611-12885) 在排练后冻结任务记忆；[PyRUA-REAL](#work-2611-06768) 将实机经验保存在程序和技能中。 |
| Coding Agent 模型后训练 | 负责选择工具或生成可执行程序的模型参数。 | [CaPtain](#work-2610-40799) 结合教师 SFT 与物理 critic 辅助 RL；[BlenderFORGE](#work-2611-10768) 通过沙箱交互训练场景编辑 MLLM。测试时代码修复与参数更新是不同步骤。 |

混合系统需要按组件阅读更新机制。[TinyAstral](#work-2610-41216) 先演化教师 Harness，再训练小型 Agent；[Agentic World Action Models](#work-2610-30136) 联合学习程序、视频及动作输出；[One Policy for 100 Household Tasks](#work-2611-14432) 将 VLA 训练与复用冻结练习上下文的 Agent 路线结合。[PhysOPSD](#work-2611-12411) 训练视频生成器，[Open-HumanWAM](#work-2611-06817) 训练世界—动作模型；它们连接物理数据与学习，但不能因使用 Agent 或仿真就归为 Coding Agent 后训练。

验证应将开发反馈与最终留出执行分开，并按协议重置或冻结上下文。[123 轮技能发现个案](#work-2609-31760) 说明，通过局部测试并积累技能，仍可能无法改善完整任务。

**研究问题。** 能否用经过验证的仿真经验提升 Agent 参数，同时保留有用的可执行技能与记忆，并将收益迁移到独立评测的实机任务？已有组件级结果尚不能证明这一完整循环。

### 程序与策略研发

<a id="work-2610-36533"></a>
<!-- stage3-record: {"id": "2610.36533", "scope": "Core", "section": 5} -->

#### RoboAuto: Autonomous Robot Program Search through Multi-Level Physical Understanding

`2026-10-27` · Washington University in St. Louis

[完整书目](../README.zh-CN.md#paper-2610-36533) · [论文](https://arxiv.org/abs/2610.36533) · [项目页](https://roboauto-ai.github.io/)

通过分阶段物理诊断搜索程序。

**具体方法：** 结合对象物理知识、视觉场景定位与自主设计的诊断实验，根据同步执行视频的审核结果修订分阶段机器人程序。

**验证：** 仿真到实机对照保留物理实验中的人工成功判定和复位。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-23288"></a>
<!-- stage3-record: {"id": "2610.23288", "scope": "Core", "section": 5} -->

#### CoEvolve: Self-Evolving Code Policies from Skills to Strategies for Humanoid Robots

`2026-10-16` · Peking University; Renmin University of China; Beijing XYZ Embodied AI Co., Ltd.; Beijing Academy of Artificial Intelligence (BAAI)

[论文](https://arxiv.org/abs/2610.23288)

在固定人形技能上演化团队策略。

**具体方法：** 在固定机器人运动技能上生成并演化团队策略代码，把技能组合和多机器人协调纳入可执行程序搜索。

**验证：** 策略代码改进不能归因为学会了底层运动技能。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-18792"></a>
<!-- stage3-record: {"id": "2610.18792", "scope": "Core", "section": 5} -->

#### SEAR: Self-Evolving Agentic Robotics

`2026-10-13` · Luma AI

[论文](https://arxiv.org/abs/2610.18792)

比较多种机器人自改进模式。

**具体方法：** 在写程序作为策略、在线 Agent 控制和自动策略研发三种模式下研究机器人自改进，区分可迁移例程与任务专用代码。

**验证：** 七个模型在 330 项仿真任务及五项实机任务上比较保留技能库、重新尝试、留出状态与迁移。每项实机任务最多练习 12 小时，冻结代码策略再测十个操作者布置场景，在线 Agent 策略测五个。练习连胜可能高估留出表现；实机评分包含部分完成分与塔高。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-12369"></a>
<!-- stage3-record: {"id": "2610.12369", "scope": "Core", "section": 5} -->

#### Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement

`2026-10-08` · Nanyang Technological University; Ropedia

[完整书目](../README.zh-CN.md#paper-2610-12369) · [论文](https://arxiv.org/abs/2610.12369)

开发带显式状态的程序并部署执行。

**具体方法：** 在离线开发中检查失败执行的视频与显式状态，修订感知／控制代码，并保留经独立验证的修改，将共享的纯代码机器人策略用于无需模型推理的在线执行。

**验证：** 留出任务、状态估计、回归和部署成本检验导出策略，在线执行无需模型推理。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-09588"></a>
<!-- stage3-record: {"id": "2610.09588", "scope": "Core", "section": 5} -->

#### Adaptive Code Generation for Controlling Robots

`2026-10-07` · Technische Universität Berlin, Germany; logsight.ai, Berlin, Germany

[完整书目](../README.zh-CN.md#paper-2610-09588) · [论文](https://arxiv.org/abs/2610.09588)

在世界状态变化后热更新机器人工作流。

**具体方法：** 根据融合 RGB／LiDAR 的世界状态变化触发重规划，修订 Python 机器人工作流，并保留虚拟机指令与变量快照以热加载后继续执行。

**验证：** 通过 Gazebo 探索、语法有效性、适应频率和决策延迟评估系统。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-38982"></a>
<!-- stage3-record: {"id": "2609.38982", "scope": "Core", "section": 5} -->

#### SimEX: Simulation-Integrated Robotics AutoResearch

`2026-09-30` · Amazon FAR (Frontier AI & Robotics); The University of Texas at Austin; Carnegie Mellon University

[论文](https://arxiv.org/abs/2609.38982) · [项目页](https://robo-simex.github.io/)

结合仿真研发与少量实机反馈。

**具体方法：** 把仿真试验与少量真实机器人反馈接入 Coding Agent，帮助其编写、调试和搜索复杂操作策略。

**验证：** 检验仿真间迁移，以及实机餐盘收纳、毛巾折叠和条码扫描。每项实机任务用五次适配试验、约十分钟机器人交互，期间人工复位；随后 30 次评测成功 26 次，各基线最多成功 3 次。仿真能力发现与沙箱指导修复分别消融。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-30594"></a>
<!-- stage3-record: {"id": "2609.30594", "scope": "Core", "section": 5} -->

#### HuGo: LLMs as Whole-Body Policy Code Designers for Humanoid Loco-Manipulation

`2026-09-24` · University of California, Berkeley; ShanghaiTech University; Google DeepMind; Nomagic

[完整书目](../README.zh-CN.md#paper-2609-30594) · [论文](https://arxiv.org/abs/2609.30594) · [项目页](https://iconlab.negarmehr.com/HuGo/)

设计人形机器人的高层策略程序。

**具体方法：** 在冻结的全身控制策略上编写高层策略代码，依据执行录像与数值轨迹修订，并验证仿真到实机迁移及真实机器人代码改进。

**验证：** 留出仿真、真实迁移与实机反馈修订分别报告，结论受底层控制器能力约束。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-30233"></a>
<!-- stage3-record: {"id": "2609.30233", "scope": "Adjacent", "section": 5} -->

#### Coding Agents for Generalized Task and Motion Planning Problems

`2026-09-24` · Fondazione Bruno Kessler; Carnegie Mellon University; Princeton University

[论文](https://arxiv.org/abs/2609.30233)

编写任务与运动规划求解程序。

**具体方法：** 让 Claude Code 与 Codex 为任务—运动规划问题编写求解程序，在 KinDER 和 PDDLStream 环境中评测泛化。

**验证：** KinDER 与 PDDLStream 实验检验求解器行为和泛化，不等于通用学习式机器人策略。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-24145"></a>
<!-- stage3-record: {"id": "2609.24145", "scope": "Adjacent", "section": 5} -->

#### MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation

`2026-09-21` · Carnegie Mellon University

[论文](https://arxiv.org/abs/2609.24145) · [项目页](https://luckykantnayak.github.io/mimic-agent/)

为四足策略训练生成参考运动。

**具体方法：** 让 Coding Agent 根据技能描述生成四足机器人参考轨迹，再训练跟踪策略，比较参考运动与奖励代码两种研发路径。

**验证：** 运动学生成的参考不保证动力学可行，RL 负责学习可执行跟踪。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2608-07555"></a>
<!-- stage3-record: {"id": "2608.07555", "scope": "Adjacent", "section": 5} -->

#### You Don't Need To Stay in The Loop: An Agentic Robotics Loop for Robot-Policy Improvement

`2026-08-02` · Independent Researcher, United States

[论文](https://arxiv.org/abs/2608.07555)

组织可重复的机器人策略研发循环。

**具体方法：** 将主 Agent、分析工具和机器人试验组织成研发循环，通过可检查的程序修改持续改进下游机器人策略。

**验证：** 研发协议的描述本身不能证明完整无人值守调度已经实现。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2606-19980"></a>
<!-- stage3-record: {"id": "2606.19980", "scope": "Core", "section": 5} -->

#### ENPIRE: Agentic Robot Policy Self-Improvement in the Real World

`2026-06-18` · NVIDIA; Carnegie Mellon University; University of California, Berkeley

[完整书目](../README.zh-CN.md#paper-2606-19980) · [论文](https://arxiv.org/abs/2606.19980) · [项目页](https://research.nvidia.com/labs/gear/enpire/)

利用真实试验证据研发机器人策略。

**具体方法：** 让 Coding Agent 使用视频、力、Proprioception 和自动执行反馈修改机器人策略与训练代码。

**验证：** 真实试验支持策略研发结论，写码 LLM 本身未必更新权重。

**关联：** [1. 具身 Harness](#section-1) · [6. 物理应用与实验](#section-6)

<a id="work-2606-16458"></a>
<!-- stage3-record: {"id": "2606.16458", "scope": "Core", "section": 5} -->

#### RHO: Your Coding Agent is Secretly a Roboticist

`2026-06-15` · University of California, Berkeley; Embodied Science; AMD

[论文](https://arxiv.org/abs/2606.16458) · [项目页](https://rho-robotics.github.io)

在部署前搜索可复用机器人策略代码库。

**具体方法：** 让 Coding Agent 在开发期搜索可解释的多文件机器人策略仓库，使部署期由合成程序直接组织感知、规划和控制。

**验证：** 开发期搜索与部署期程序执行具有不同计算和反馈条件。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2606-08610"></a>
<!-- stage3-record: {"id": "2606.08610", "scope": "Core", "section": 5} -->

#### HARBOR: A Harness Framework for Agentic Robot Reinforcement Learning

`2026-06-07` · TU Darmstadt; Honda Research Institute Europe; Columbia University; Tongji University; Shanghai Research Institute for Intelligent Autonomous Systems; University of Würzburg; Hessian.AI

[论文](https://arxiv.org/abs/2606.08610)

把机器人 RL 研发组织为 Agent 工作环境。

**具体方法：** 将机器人强化学习研发组织成 Coding Agent Harness，让 Agent 从模拟器代码和任务说明出发配置环境、训练与检查策略。

**验证：** 检查研发阶段产物及策略效果，策略学习器与编程 Agent 职责分开。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2603-04466"></a>
<!-- stage3-record: {"id": "2603.04466", "scope": "Core", "section": 5} -->

#### Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation

`2026-03-03` · General Bionix

[完整书目](../README.zh-CN.md#paper-2603-04466) · [论文](https://arxiv.org/abs/2603.04466)

依据执行与视觉反馈改写控制程序。

**具体方法：** 执行生成的控制器、视觉观察机器人，并依据所得证据重写策略代码。

**验证：** 通过编译、重复试验成功率和失败恢复检验程序改进。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2508-02629"></a>
<!-- stage3-record: {"id": "2508.02629", "scope": "Core", "section": 5} -->

#### HyCodePolicy: Hybrid Language Controllers for Multimodal Monitoring and Decision in Embodied Agents

`2025-08-04` · Northeastern University; D-Robotics; HKU MMLab; Shanghai AI Lab; Shenzhen University; SUSTech; Shanghai Jiao Tong University; Tsinghua University

[完整书目](../README.zh-CN.md#paper-2508-02629) · [论文](https://arxiv.org/abs/2508.02629)

结合可执行策略与多模态监控。

**具体方法：** 将可执行策略代码与多模态监控结合，使具身行为能被在线诊断与修改。

**验证：** 通过任务与子目标成功率、完成判断和修复效率评估系统。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2503-13660"></a>
<!-- stage3-record: {"id": "2503.13660", "scope": "Adjacent", "section": 5} -->

#### INPROVF: Leveraging Large Language Models to Repair High-level Robot Controllers from Assumption Violations

`2025-03-17` · Cornell University

[论文](https://arxiv.org/abs/2503.13660)

用形式验证反例修复机器人控制器。

**具体方法：** 让语言模型提出高层机器人控制器的修复候选，再用形式化验证的反例反馈推动下一轮程序修订。

**验证：** 形式正确性与物理任务表现是不同结果，各需对应验证。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2410-18893"></a>
<!-- stage3-record: {"id": "2410.18893", "scope": "Adjacent", "section": 5} -->

#### Creating and Repairing Robot Programs in Open-World Domains

`2024-10-24` · Northeastern University; University of Texas at Austin

[论文](https://arxiv.org/abs/2410.18893)

修复程序时复用已经完成的任务步骤。

**具体方法：** 跟踪机器人程序失败前的执行状态，再生成尽量复用已完成步骤的恢复程序，减少修复时重复执行动作。

**验证：** 修复质量包括完成效果与重复动作成本，改进对象是程序。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2409-01652"></a>
<!-- stage3-record: {"id": "2409.01652", "scope": "Adjacent", "section": 5} -->

#### ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation

`2024-09-03` · Stanford University; Columbia University

[论文](https://arxiv.org/abs/2409.01652) · [项目页](https://rekep-robot.github.io/)

用程序化几何约束指导在线操作。

**具体方法：** 从 RGB-D 观测与语言指令生成表达关键点关系的 Python 约束函数，再由分层优化器在感知—动作循环中求解机器人运动。

**验证：** 执行实验检验约束控制；优化器重算、约束重写和 LLM 训练应区分。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2406-01967"></a>
<!-- stage3-record: {"id": "2406.01967", "scope": "Adjacent", "section": 5} -->

#### DrEureka: Language Model Guided Sim-To-Real Transfer

`2024-06-04` · University of Pennsylvania; NVIDIA; University of Texas, Austin

[论文](https://arxiv.org/abs/2406.01967) · [项目页](https://eureka-research.github.io/dr-eureka/)

用生成奖励和域随机化支持真实迁移。

**具体方法：** 让语言模型结合机器人任务与训练结果设计奖励和域随机化配置，以降低下游策略的仿真到实机迁移成本。

**验证：** 仿真与实机对照衡量策略迁移，不是编程模型后训练。

**关联：** [1. 具身 Harness](#section-1) · [2. Simulator 构建](#section-2)

<a id="work-2402-04764"></a>
<!-- stage3-record: {"id": "2402.04764", "scope": "Adjacent", "section": 5} -->

#### Code as Reward: Empowering Reinforcement Learning with VLMs

`2024-02-07` · Mila; McGill University; Google DeepMind; University of California, Berkeley

[论文](https://arxiv.org/abs/2402.04764)

把视觉任务理解编译为奖励代码。

**具体方法：** 将 VLM 对任务和视觉状态的理解编译为奖励程序，减少在线模型查询并支持机器人强化学习。

**验证：** 奖励程序减少重复模型调用，动作策略仍通过独立优化过程学习。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2310-12931"></a>
<!-- stage3-record: {"id": "2310.12931", "scope": "Adjacent", "section": 5} -->

#### Eureka: Human-Level Reward Design via Coding Large Language Models

`2023-10-19` · University of Pennsylvania; Caltech; NVIDIA; University of Texas at Austin

[论文](https://arxiv.org/abs/2310.12931) · [项目页](https://eureka-research.github.io/)

用策略训练反馈搜索奖励程序。

**具体方法：** 利用编码 LLM 搜索与改进奖励程序，再用强化学习训练机器人策略，改进目标是奖励代码和动作策略而非 LLM 权重。

**验证：** 奖励搜索与机器人策略优化不等于 LLM 权重学习。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2309-11489"></a>
<!-- stage3-record: {"id": "2309.11489", "scope": "Adjacent", "section": 5} -->

#### Text2Reward: Reward Shaping with Language Models for Reinforcement Learning

`2023-09-20` · The University of Hong Kong; Carnegie Mellon University; Nanjing University; Microsoft Research; University of Waterloo

[论文](https://arxiv.org/abs/2309.11489) · [项目页](https://text-to-reward.github.io/)

把奖励塑形变成代码生成任务。

**具体方法：** 由 LLM 生成可执行的稠密奖励代码，结合环境表示和人工反馈迭代调整下游强化学习策略的训练目标。

**验证：** 部分反馈由人观看 rollout 提供，训练对象是下游 RL 策略。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2306-08647"></a>
<!-- stage3-record: {"id": "2306.08647", "scope": "Adjacent", "section": 5} -->

#### Language to Rewards for Robotic Skill Synthesis

`2023-06-14` · Google DeepMind

[论文](https://arxiv.org/abs/2306.08647) · [项目页](https://language-to-reward.github.io/)

用生成奖励表达机器人技能目标。

**具体方法：** 让 LLM 根据语言指令编写奖励参数，通过实时优化器合成机器人行为，并接受用户对执行效果的修正。

**验证：** 行为优化和用户纠正改变控制目标，不是 LLM 后训练。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-autoresearch-robotics"></a>
<!-- stage3-record: {"id": "autoresearch-robotics", "scope": "Resource", "section": 5} -->

#### autoresearch-robotics

`首发日期未明确` · 未明确

[代码](https://github.com/jellyheadandrew/autoresearch-robotics)

提供社区机器人 RL 研发实例。

**具体方法：** 让 Coding Agent 修改机器人强化学习训练脚本，并利用固定评估、学习曲线和视频反馈继续试验。

**验证：** 这是社区仿真流程，不是经同行评议的实机结果。

**关联：** [1. 具身 Harness](#section-1)

### 经验、记忆与技能学习

<a id="work-2611-14432"></a>
<!-- stage3-record: {"id": "2611.14432", "scope": "Core", "section": 5} -->

#### One Policy for 100 Household Tasks: Our Solution for the 2026 BEHAVIOR Challenge

`2026-11-10` · 独立团队

[论文](https://arxiv.org/abs/2611.14432)

将家庭任务 VLA 与任务专属的 Coding Agent 练习会话结合，并在评测前冻结会话。

**具体方法：** Agent 编写调用图像／深度观察及运动工具的短程序，在训练实例上练习，并在上下文中积累笔记与操作配方。14 项任务整回合交给该 Agent，其余使用 VLA；上下文学习与 VLA 参数训练是两种独立机制。

**验证：** BEHAVIOR／OmniGibson 评测的每个 Agent 回合从冻结练习会话重新开始，移除训练期特权工具，回合间不更新。练习图像反馈指导后续程序；结果来自仿真，未证明实体部署。

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4) · [6. 物理应用与实验](#section-6)

<a id="work-2611-12885"></a>
<!-- stage3-record: {"id": "2611.12885", "scope": "Adjacent", "section": 5} -->

#### World In-Context Learning for Agentic Robot Manipulation

`2026-11-09` · Huazhong University of Science and Technology; ArcheOne AI

[完整书目](../README.zh-CN.md#paper-2611-12885) · [论文](https://arxiv.org/abs/2611.12885) · [项目页](https://archeone-ai.github.io/RoboScript/) · [代码](https://github.com/ArcheOne-AI/RoboScript)

利用仿真排练形成可迁移的任务记忆，基础模型参数保持冻结。

**具体方法：** RoboScript 从一次演示出发，在仿真变体中探索，将反馈整理成语义 Task Memory；部署前冻结记忆。积累的是上下文与程序知识，而非模型参数。

**验证：** 在 50 项 RoboTwin 2.0 任务上分离排练与部署，并测试四项真实 PiPER 任务。实机执行预先规划的动作序列，无在线重规划；仿真适应本身不等于实机纠错编程。

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4) · [6. 物理应用与实验](#section-6)

<a id="work-2611-06768"></a>
<!-- stage3-record: {"id": "2611.06768", "scope": "Core", "section": 5} -->

#### PyRUA-REAL: Robot Exploration and Adaptive Learning through RSI in the Real World

`2026-11-04` · Peking University; EngineAI; National University of Singapore

[完整书目](../README.zh-CN.md#paper-2611-06768) · [论文](https://arxiv.org/abs/2611.06768) · [项目页](https://dagroup-pku.github.io/PyRUA-Lean/real/) · [代码](https://github.com/DAGroup-PKU/PyRUA-Lean/tree/REAL)

从真实机器人探索学习可复用代码。

**具体方法：** 通过研究者与工程师 Agent 协作，将真实机器人执行证据转成修订后的程序与可复用技能，再以实时观测运行感知和控制代码。

**验证：** 八项实机与 42 项 RoboDojo 任务含反馈及迁移消融，需协助插接区别于冻结程序可靠性。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-42141"></a>
<!-- stage3-record: {"id": "2610.42141", "scope": "Core", "section": 5} -->

#### RoboArchitect: Automating the Design of Robotic Agents with Persistent Memory

`2026-10-30` · Stanford University

[完整书目](../README.zh-CN.md#paper-2610-42141) · [论文](https://arxiv.org/abs/2610.42141) · [代码](https://github.com/roboarchitect-ai/RoboArchitect) · [项目页](https://roboarchitect-ai.github.io/)

演化持久记忆与机器人控制代码。

**具体方法：** 依据执行视频和工具输出，迭代改写冻结机器人策略外的控制程序与持续记忆，并在留出的仿真场景和任务上评估。

**验证：** 留出场景和任务及消融检验迁移，已报告验证限于仿真。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-29560"></a>
<!-- stage3-record: {"id": "2610.29560", "scope": "Core", "section": 5} -->

#### From VLM Planners to Robotic Agents: Self-Evolving Harnesses for History-Dependent Manipulation

`2026-10-21` · University of Science and Technology of China; Shanghai Artificial Intelligence Laboratory; Shanghai Jiao Tong University; Mohamed bin Zayed University of Artificial Intelligence; Zhejiang University

[论文](https://arxiv.org/abs/2610.29560)

为依赖历史的任务改进 Harness 上下文。

**具体方法：** 根据历史依赖操作任务的轨迹修改高层 VLM 的上下文和 Harness，在固定配置下检验留出任务表现。

**验证：** 留出任务评估最终固定 Harness，改动位于动作策略之外。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-25114"></a>
<!-- stage3-record: {"id": "2610.25114", "scope": "Core", "section": 5} -->

#### Compile Once, Run Cheap: Frozen, Portable Skills for Embodied Agents, and What Recursive Self-Improvement Adds

`2026-10-18` · Beijing Ou Rui Ling Shi Technology; ChangingTek Robotics Technology (Suzhou); Shanghai Yunfan Intelligent Control Robot Technology

[论文](https://arxiv.org/abs/2610.25114) · [代码](https://github.com/Orillusion/embodied-skill-rsi)

离线构造技能并冻结复用。

**具体方法：** 让强模型离线编写、运行和修复机器人技能，通过冻结后抽样考试再交由低成本调用器复用。

**验证：** 开发与部署预算分开，冻结技能测试检验优化结束后保留的能力。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-23098"></a>
<!-- stage3-record: {"id": "2610.23098", "scope": "Core", "section": 5} -->

#### InstAgent: A Recursively Self-Improving Agent Operating System for Heterogeneous Robot Collaboration

`2026-10-16` · ShanghaiTech University, Shanghai, China.; InstAdapt, Shanghai, China.

[论文](https://arxiv.org/abs/2610.23098)

为异构机器人团队保留修复后的协作程序。

**具体方法：** 以 Agent 生成的行为树组织异构机器人协作，将执行修复保存为可复用协作程序，并用共享时空记忆检查任务交接。

**验证：** 协作与交接检查评估系统，保留程序是外部学习产物。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-22736"></a>
<!-- stage3-record: {"id": "2610.22736", "scope": "Adjacent", "section": 5} -->

#### Spatial Memory by Agents, for Agents

`2026-10-15` · Nanjing University; Princeton University; Carnegie Mellon University; Johns Hopkins University; Mondo Robotics

[论文](https://arxiv.org/abs/2610.22736) · [项目页](https://ba-fa-3344.github.io/)

编写供另一 Agent 使用的空间记忆。

**具体方法：** 由设计 Agent 编写和修订空间记忆的构建、检索代码，再以固定查询 Agent 的机器人空间任务反馈评估记忆方案。

**验证：** 留出评测前冻结记忆实现，设计 Agent 与查询 Agent 职责分开。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-22496"></a>
<!-- stage3-record: {"id": "2610.22496", "scope": "Core", "section": 5} -->

#### Scaling Online Exploration for Robot Agents

`2026-10-15` · Harvard University; NVIDIA; University of California, Berkeley; Massachusetts Institute of Technology; Stanford University

[论文](https://arxiv.org/abs/2610.22496) · [项目页](https://robot-agent-exploration.com/) · [数据集](https://huggingface.co/datasets/robot-agent-exploration/robot-session-logs) · [代码](https://github.com/robot-agent-exploration/skills-lib) · [代码](https://github.com/robot-agent-exploration/rax)

研究探索预算如何转化为机器人经验。

**具体方法：** 用通用 Coding Agent 自主探索多种机器人，生成控制程序并记录真实与仿真交互，研究探索预算如何转化为可复用技能与经验。

**验证：** 公开日志混含实机、仿真、代码、传感输出与人工指令，使用时需按来源拆分。 官方另发布 12 个实机会话的工具回执、视频与生成技能日志。

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4)

<a id="work-2610-18867"></a>
<!-- stage3-record: {"id": "2610.18867", "scope": "Core", "section": 5} -->

#### EmbodiedEvo: Self-Evolving Coding Agent For Physical Intelligence

`2026-10-13` · Navers Lab, Einsia.AI, Tsinghua University

[论文](https://arxiv.org/abs/2610.18867)

将可执行技能与诊断经验分别积累。

**具体方法：** 将物理执行反馈分别提炼为可执行 Skills 和诊断 Lessons，支持 Coding Agent 的持续机器人能力积累。

**验证：** 持久技能与经验复用不同于同回合的临时修复。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-18874"></a>
<!-- stage3-record: {"id": "2610.18874", "scope": "Adjacent", "section": 5} -->

#### ChunkAct: Action Chunking for Agentic Robotics

`2026-10-13` · University of Southern California; University of Central Florida; Stony Brook University

[论文](https://arxiv.org/abs/2610.18874)

把外部记忆编译成自主执行的动作块。

**具体方法：** 将机器人 Agent 的外部记忆编译为可自主运行的动作块，仅在失败时返回高层模型，降低重复推理开销。

**验证：** 执行成本与成功率需联合分析，减少推理也会改变恢复机会。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-14224"></a>
<!-- stage3-record: {"id": "2610.14224", "scope": "Adjacent", "section": 5} -->

#### Harness^2: Recursive Agent Harnessing for an Open World

`2026-10-09` · Google Cloud AI Research; Northwestern University

[论文](https://arxiv.org/abs/2610.14224)

在任务内和跨任务层面演化 Harness。

**具体方法：** 在任务和跨任务两层递归更新 Agent Harness，通过验证筛选可复用修改并研究开放任务中的泛化。

**验证：** 递归更新叙述本身不足以证明完整多模态代码修复链。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-10498"></a>
<!-- stage3-record: {"id": "2610.10498", "scope": "Core", "section": 5} -->

#### EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution

`2026-10-07` · Columbia University; Princeton University

[论文](https://arxiv.org/abs/2610.10498)

通过显式假设选择机器人探索。

**具体方法：** 用假设图选择下一次机器人探索，将交互结果用于共同改进代码和技能，避免盲目反复试错。

**验证：** 探索选择与技能保留收益需区别于单纯增加试验次数。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-08995"></a>
<!-- stage3-record: {"id": "2610.08995", "scope": "Core", "section": 5} -->

#### PhysEvo: Astra Can Act, Let It

`2026-10-06` · University of Chinese Academy of Sciences; Institute of Automation, Chinese Academy of Sciences; Tsinghua University; Independent researcher

[完整书目](../README.zh-CN.md#paper-2610-08995) · [论文](https://arxiv.org/abs/2610.08995)

保持模型冻结并改进机器人工具。

**具体方法：** 根据对齐的机器人图像、状态与执行轨迹，围绕冻结模型修改行动和诊断工具代码，在开发回合间测试并保留改进，再用固定版本评测。

**验证：** 留出布局、接口消融和冻结版本测试区分开发适应与最终评测。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-01178"></a>
<!-- stage3-record: {"id": "2610.01178", "scope": "Core", "section": 5} -->

#### Recova: Agent-Guided Failure Recovery for Autonomous Robotic Manipulation

`2026-10-01` · University of California, San Diego; University of Texas at Austin; NVIDIA

[论文](https://arxiv.org/abs/2610.01178) · [项目页](https://www.liuisabella.com/Recova)

先在数字孪生中练习恢复再执行实机任务。

**具体方法：** 让 Agent 在重建数字孪生中测试恢复程序，再通过真实执行改进任务和恢复能力，并保留不同策略的职责。

**验证：** 孪生质量、恢复程序质量与基础动作策略应分别分析。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-02204"></a>
<!-- stage3-record: {"id": "2610.02204", "scope": "Adjacent", "section": 5} -->

#### Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents

`2026-10-01` · UC Berkeley; MIT; Amazon FAR; University of Chicago

[论文](https://arxiv.org/abs/2610.02204) · [项目页](https://rpg-robot.github.io/)

利用重建练习环境改进具身 Agent。

**具体方法：** 从离线任务材料构造仿真练习，用执行反馈改进可复用机器人系统，并在部署前区分特权诊断与常规观测。

**验证：** 开发期特权诊断与部署 Agent 可用观测必须分开。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-39304"></a>
<!-- stage3-record: {"id": "2609.39304", "scope": "Core", "section": 5} -->

#### Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents

`2026-09-30` · 未明确

[论文](https://arxiv.org/abs/2609.39304)

研究 Harness 优化中的规模与筛选。

**具体方法：** 由优化 Coding Agent 根据机器人轨迹修改另一 Agent 的提示、工具和控制规则，研究试验规模与选择方式对 Harness 演化的作用。

**验证：** 实验区分搜索预算、候选筛选和执行模型的影响。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-39018"></a>
<!-- stage3-record: {"id": "2609.39018", "scope": "Core", "section": 5} -->

#### Make Code as Policy Great Again: Frontier Agents Write, Call, and Evolve Robot Tools

`2026-09-30` · HexaFuture; Peking University; Beijing Institute of Technology; Tsinghua University

[论文](https://arxiv.org/abs/2609.39018)

让 Agent 编写并演化自己的执行工具。

**具体方法：** 让前沿 Agent 编写并演化机器人工具，由程序承载多阶段动作、模型承担策略选择和结果检查。

**验证：** 工具演化区别于选择固定工具，也区别于更新模型参数。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-40306"></a>
<!-- stage3-record: {"id": "2609.40306", "scope": "Adjacent", "section": 5} -->

#### DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents

`2026-09-30` · Nanyang Technological University; Nanjing University

[论文](https://arxiv.org/abs/2609.40306) · [项目页](https://denghaoyuan123.github.io/Dynaharness_page/)

用物理执行契约约束 Harness 演化。

**具体方法：** 用共享执行契约连接语义推理与物理约束，将失败证据转成经验证的机器人能力和 Harness 修订。

**验证：** 经验证的代码变化是学习单元，不能仅靠反思文本证明提升。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-39207"></a>
<!-- stage3-record: {"id": "2609.39207", "scope": "Core", "section": 5} -->

#### ASENA: Self-evolving Agents for Embodied Navigation

`2026-09-30` · NVIDIA; University of California, San Diego; The University of Texas at Austin

[论文](https://arxiv.org/abs/2609.39207) · [项目页](https://research.nvidia.com/labs/gear/asena)

把导航修复用于后续环境。

**具体方法：** 让导航 Agent 读取传感器、编写程序、检查执行记录，并把修复后的例程与经验用于后续环境。

**验证：** 后续环境表现检验复用，单次重试不能代表持续学习。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-37583"></a>
<!-- stage3-record: {"id": "2609.37583", "scope": "Adjacent", "section": 5} -->

#### RoboHarn-Evo: Evolving Hierarchical Physical Knowledge for Self-Improving Robotic Manipulation

`2026-09-29` · Renmin University of China; XYZ Embodied AI; Tsinghua University

[论文](https://arxiv.org/abs/2609.37583)

从物理交互积累分层知识。

**具体方法：** 用双循环 Harness 从物理交互中提炼分层知识，检验这些外部知识如何改进后续机器人操作。

**验证：** 持久知识位于基模之外，其作用由后续任务检验。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-35432"></a>
<!-- stage3-record: {"id": "2609.35432", "scope": "Core", "section": 5} -->

#### Self-Evolving Coding Agents: From Digital Programs to Physical-World Intelligence

`2026-09-28` · 未明确

[完整书目](../README.zh-CN.md#paper-2609-35432) · [论文](https://arxiv.org/abs/2609.35432)

用显式世界与策略代码改进机器人工具。

**具体方法：** 通过显式世界程序与策略程序组织感知和学习式动作工具，根据机器人执行证据修改可复用工具代码，并保留轨迹用于独立模型更新。

**验证：** 版本化重放、留出种子和受约束实机实验区分工具更新与独立模型训练。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-33378"></a>
<!-- stage3-record: {"id": "2609.33378", "scope": "Adjacent", "section": 5} -->

#### Recursive Harness Distillation across Agents for Robot Manipulation

`2026-09-27` · Seoul National University; Korea Advanced Institute of Science and Technology

[论文](https://arxiv.org/abs/2609.33378)

在 Agent 间迁移外部 Harness 指导。

**具体方法：** 把不同 Agent 的干预和修复经验提炼成可迁移 Harness 指导，并用后续机器人执行验证其收益。

**验证：** 强弱模型与动作模型冻结，此处蒸馏迁移指导材料而非权重。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-32862"></a>
<!-- stage3-record: {"id": "2609.32862", "scope": "Core", "section": 5} -->

#### RoboFoundry: System-as-Policy Evolution for Self-Learning Embodied Agents

`2026-09-26` · Nanyang Technological University; Beihang University; National University of Singapore; Cloud Butterfly Technology; Shanghai Jiao Tong University

[论文](https://arxiv.org/abs/2609.32862) · [项目页](https://jingsongliang.com/robofoundry)

把机器人支持系统作为可演化策略。

**具体方法：** 把机器人支持系统本身视为可演化策略，将执行经验转换为经过验证的代码、记忆和接口更新。

**验证：** 能力提升属于组合系统，外部代码修改不能写成模型权重学习。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-29394"></a>
<!-- stage3-record: {"id": "2609.29394", "scope": "Core", "section": 5} -->

#### RACaP: Agentic Reasoning, Acting, and Coding as Policies for Evolvable Robot Learning

`2026-09-24` · Chinese University of Hong Kong; HKUST (Guangzhou); Knowin AI

[论文](https://arxiv.org/abs/2609.29394)

将在线决策与可演化机器人 API 分开。

**具体方法：** 将可复用机器人 API 与在线 ReAct 决策分离，并通过课程与交互经验更新 API、Harness 和长期记忆。

**验证：** API 与记忆演化应区别于单回合控制进行评估。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2609-31760"></a>
<!-- stage3-record: {"id": "2609.31760", "scope": "Core", "section": 5} -->

#### What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery

`2026-09-23` · National University of Singapore

[论文](https://arxiv.org/abs/2609.31760)

分析反复修改代码与技能为何仍可能无法形成累积的任务成功。

**具体方法：** Coding Agent 检查失败关键帧与诊断，修改类型化 Python 技能、安装外部模型，并据日志重拟合路由；回放与配对仿真试验决定是否接受修改。评估器及记忆框架由人维护，LLM 参数不训练。

**验证：** 123 轮 RoboCasa 个案在目标冰箱任务上始终未成功，分析了弱测试、记忆污染与早期步骤瓶颈。期间更换模型及人工修复框架，因此不能将其视为受控对比或全自动端到端自我改进。

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3) · [6. 物理应用与实验](#section-6)

<a id="work-2608-16590"></a>
<!-- stage3-record: {"id": "2608.16590", "scope": "Core", "section": 5} -->

#### Zetta $ζ$: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence

`2026-08-17` · Institute for AI Industry Research (AIR), Tsinghua University; Z-Trans AI

[论文](https://arxiv.org/abs/2608.16590)

围绕冻结动作策略演化监控器与恢复技能。

**具体方法：** 在冻结动作策略外演化代码化运行时评判器和恢复技能，使失败诊断能够影响正在进行的物理执行。

**验证：** 在线监控与离线代码演化是不同循环，动作策略保持冻结。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2608-11350"></a>
<!-- stage3-record: {"id": "2608.11350", "scope": "Adjacent", "section": 5} -->

#### Self-Evolving Embodied Agents via Skill-Harness Evolution

`2026-08-11` · Northeastern University; Microsoft Research

[论文](https://arxiv.org/abs/2608.11350)

共同演化技能与执行 Harness。

**具体方法：** 通过执行经验共同更新技能与 Harness，研究固定动作接口下无需更新底座权重的具身能力积累。

**验证：** 外部系统改进不同于训练基础模型。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2608-09410"></a>
<!-- stage3-record: {"id": "2608.09410", "scope": "Core", "section": 5} -->

#### Skills in Weights, Memory in Code: Hybrid Learning for Memory-Dependent Robot Manipulation

`2026-08-10` · Northwestern University; University of Minnesota; Stanford University

[完整书目](../README.zh-CN.md#paper-2608-09410) · [论文](https://arxiv.org/abs/2608.09410)

结合学习式技能与程序化记忆。

**具体方法：** 根据机器人 Rollout 迭代更新可执行记忆管理启发式，并用多模态阶段验证闭合执行。

**验证：** 任务与累积阶段成功率区别于本体感知或视觉完成检测。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2607-23784"></a>
<!-- stage3-record: {"id": "2607.23784", "scope": "Adjacent", "section": 5} -->

#### A Few Words Go a Long Way: Language Guided Robot Policy Synthesis

`2026-07-26` · University of Washington; Microsoft Research; Massachusetts Institute of Technology

[论文](https://arxiv.org/abs/2607.23784) · [项目页](https://robo-architect.github.io/)

用语言纠正改进机器人程序。

**具体方法：** 让 Coding Agent 根据执行轨迹和人类语言纠正重新合成机器人程序，将纠正沉淀为后续任务可复用的技能。

**验证：** Franka 实验允许最多五轮专家纠正，自动 VLM 纠正属于独立消融。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2607-00272"></a>
<!-- stage3-record: {"id": "2607.00272", "scope": "Core", "section": 5} -->

#### ASPIRE: Agentic /Skills Discovery for Robotics

`2026-06-30` · NVIDIA; Carnegie Mellon University; University of California, Berkeley; University of Michigan; University of Illinois Urbana-Champaign

[完整书目](../README.zh-CN.md#paper-2607-00272) · [论文](https://arxiv.org/abs/2607.00272) · [代码](https://github.com/NVlabs/ASPIRE) · [项目页](https://research.nvidia.com/labs/gear/aspire/)

把经过验证的代码修复提炼为技能。

**具体方法：** 根据细粒度多模态 Rollout Trace 编写和修复 Code-as-policy，经重新执行验证，并把成功修复提炼为可复用 Skill。

**验证：** 通过重执行、留出任务与迁移检验技能库，底座模型保持冻结。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2606-19419"></a>
<!-- stage3-record: {"id": "2606.19419", "scope": "Core", "section": 5} -->

#### Playful Agentic Robot Learning

`2026-06-17` · University of California, Berkeley  Impossible Research

[论文](https://arxiv.org/abs/2606.19419) · [项目页](https://playful-rats.github.io/)

把无任务探索转化为持久代码技能。

**具体方法：** 让机器人在无具体任务指派的探索中提出可学目标、编写和修复程序，再把成功执行提炼为持久代码技能。

**验证：** 技能发现与当前回合重试应区分，后续执行衡量能力是否保留。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2605-10332"></a>
<!-- stage3-record: {"id": "2605.10332", "scope": "Adjacent", "section": 5} -->

#### EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents

`2026-05-11` · Huazhong University of Science and Technology; University of Science and Technology of China; Microsoft Research; Institute for AI Industry Research (AIR), Tsinghua University

[论文](https://arxiv.org/abs/2605.10332)

将反思对应到导致失败的具体技能。

**具体方法：** 按技能与执行失败的关系组织反思，使具身任务经验进入更有针对性的技能更新过程。

**验证：** 学习对象是技能经验，改进需由后续执行验证而非仅凭反思文本。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2603-02623"></a>
<!-- stage3-record: {"id": "2603.02623", "scope": "Adjacent", "section": 5} -->

#### Uni-Skill: Building Self-Evolving Skill Repository for Generalizable Robotic Manipulation

`2026-03-03` · Institute of Computing Technology, Chinese Academy of Sciences; University of Chinese Academy of Sciences

[论文](https://arxiv.org/abs/2603.02623)

维护可持续演化的机器人技能仓库。

**具体方法：** 以统一技能仓库连接技能感知规划与自动演化，研究机器人操作经验如何转化为后续任务可复用的技能。

**验证：** 技能迁移通过仓库使用检验，持久技能不自动等于模型权重学习。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2509-18597"></a>
<!-- stage3-record: {"id": "2509.18597", "scope": "Core", "section": 5} -->

#### Robotic Ultra-Long-Horizon Manipulation Skills via Human-guided Lifelong Code Generation

`2025-09-23` · Beijing Academy of Artificial Intelligence; XYZ Embodied AI

[完整书目](../README.zh-CN.md#paper-2509-18597) · [论文](https://arxiv.org/abs/2509.18597) · [代码](https://github.com/Ghiara/LYRA) · [项目页](https://ghiara.github.io/LYRA/)

把人工纠错积累为长时序代码技能。

**具体方法：** 将人类纠错保留为可继承、可检索的机器人技能代码，并独立评测根据 RGB-D 反馈诊断执行结果、迭代修订计划的配置。

**验证：** 人工指导与视觉反馈配置分别评测，并检查记忆消融和长时实机执行。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2406-18746"></a>
<!-- stage3-record: {"id": "2406.18746", "scope": "Adjacent", "section": 5} -->

#### Lifelong Robot Library Learning: Bootstrapping Composable and Generalizable Skills for Embodied Control with Language Models

`2024-06-26` · University of Groningen

[论文](https://arxiv.org/abs/2406.18746) · [项目页](https://gtziafas.github.io/LRLL_project)

持续积累可组合的机器人控制程序库。

**具体方法：** 从机器人执行中积累可组合的程序库，使语言模型通过复用已学例程逐步获得更广的控制能力。

**验证：** 通过跨任务程序复用检验迁移，程序库与模型权重是不同学习载体。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2406-03757"></a>
<!-- stage3-record: {"id": "2406.03757", "scope": "Adjacent", "section": 5} -->

#### RoboCoder: Robotic Learning from Basic Skills to General Tasks with Large Language Models

`2024-06-06` · CUHK; SmartMore

[论文](https://arxiv.org/abs/2406.03757)

通过复用基础技能组合复杂机器人任务。

**具体方法：** 利用 LLM 将基本机器人技能组合成更复杂任务程序，并通过技能库支持后续任务复用。

**验证：** 任务执行检验技能组合；技能库复用与基模训练分别理解。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2405-19758"></a>
<!-- stage3-record: {"id": "2405.19758", "scope": "Adjacent", "section": 5} -->

#### InterPreT: Interactive Predicate Learning from Language Feedback for Generalizable Task Planning

`2024-05-30` · University of California, Los Angeles; University of Texas at Austin

[论文](https://arxiv.org/abs/2405.19758) · [项目页](https://interpret-robot.github.io)

从语言纠正中学习可执行规划谓词。

**具体方法：** 根据人类语言反馈学习可执行的状态谓词与符号操作规则，再将其编译为 PDDL 来泛化到更复杂的机器人任务。

**验证：** 泛化针对谓词与规划模型，人工反馈是学习配置的一部分。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2305-16744"></a>
<!-- stage3-record: {"id": "2305.16744", "scope": "Adjacent", "section": 5} -->

#### Demo2Code: From Summarizing Demonstrations to Synthesizing Code via Extended Chain-of-Thought

`2023-05-26` · Cornell University

[论文](https://arxiv.org/abs/2305.16744) · [项目页](https://portal-cornell.github.io/demo2code/)

从示范总结任务，再合成机器人程序。

**具体方法：** 先将示范递归压缩为任务规格，再展开为机器人可执行代码，研究从观察到程序与技能的转换。

**验证：** 通过程序合成与任务执行检验示范到代码的转换，不等于更新基模权重。

**关联：** [1. 具身 Harness](#section-1)

### Coding Agent 后训练

<a id="work-2611-10768"></a>
<!-- stage3-record: {"id": "2611.10768", "scope": "Core", "section": 5} -->

#### BlenderFORGE: Framework for Optimizing Reactive 3D-Graphics Editing Ability of MLLMs

`2026-11-07` · Hong Kong University of Science and Technology; SenseTime Research

[完整书目](../README.zh-CN.md#paper-2611-10768) · [论文](https://arxiv.org/abs/2611.10768) · [项目页](https://sensetime-fvg.github.io/BlenderFORGE/)

通过可执行编辑与渲染反馈，训练开放权重 Coding Agent 修订显式 Blender 场景。

**具体方法：** 扰动资产产生起点／目标场景、图像和状态目标；教师轨迹用于 SFT 冷启动，沙箱奖励用于多轮 AgentLoop-RL。Agent 在 bpy 编辑之间请求预览；训练更新编辑 MLLM 参数，场景状态指标提供监督。

**验证：** 覆盖四类编辑、SFT／RL 消融和跨相机／BlenderGym 迁移；指标排除超时及服务失败。报告 9,000 个训练、800 个测试任务。官方仓库仍将代码、沙箱、数据和权重列为待发布，不能标为已发布训练集。

**关联：** [1. 具身 Harness](#section-1) · [2. Simulator 构建](#section-2) · [4. 数据](#section-4)

<a id="work-2610-41216"></a>
<!-- stage3-record: {"id": "2610.41216", "scope": "Adjacent", "section": 5} -->

#### TinyAstral: Transferring Self-Evolving Harnesses to Tiny Generalist Manipulation Agents

`2026-10-30` · Huawei Technologies Co., Ltd; Huawei Noah Research Institute

[论文](https://arxiv.org/abs/2610.41216) · [项目页](https://garfield-kh.github.io/TinyAstral/)

将改进后的教师 Harness 用于小模型训练。

**具体方法：** 先通过配对试验演化冻结教师的 Harness，再用固定 Harness 中的教师轨迹训练更小的机器人 Agent。

**验证：** Harness 演化与学生模型权重学习分为两个阶段。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2610-40799"></a>
<!-- stage3-record: {"id": "2610.40799", "scope": "Core", "section": 5} -->

#### CaPtain: A Pipeline for Post-Training Code-as-Policy Robot Agents

`2026-10-29` · MMLab, The Chinese University of Hong Kong; NovaXBot

[完整书目](../README.zh-CN.md#paper-2610-40799) · [论文](https://arxiv.org/abs/2610.40799) · [代码](https://github.com/waltstephen/CaPtain) · [代码](https://github.com/waltstephen/CaPtain-Harness)

训练小模型通过机器人代码行动。

**具体方法：** 通过 SFT 与物理 critic 辅助 RL，训练小型视觉语言模型依据摄像图像和低层动作回执迭代编写机器人控制程序，再经仿真适配迁移到实机。

**验证：** 更新的是编程 Agent 权重；测试去除 critic 特权状态，实机迁移经过仿真适配。

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4)

<a id="work-2610-30136"></a>
<!-- stage3-record: {"id": "2610.30136", "scope": "Adjacent", "section": 5} -->

#### Agentic World Action Models

`2026-10-21` · University of California, Berkeley; NVIDIA; University of Pennsylvania

[完整书目](../README.zh-CN.md#paper-2610-30136) · [论文](https://arxiv.org/abs/2610.30136) · [项目页](https://agentic-wam.github.io/)

联合建模程序、预测视频与机器人动作。

**具体方法：** 联合生成技能程序计划、未来视频与机器人动作，并以可选混合模式在有效程序片段和模型动作块之间切换，当前不进行在线技能库学习。

**验证：** 联合学习输出不同于冻结 Agent 调外部动作模型，不宣称在线技能库学习。

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4)

<a id="work-2610-28589"></a>
<!-- stage3-record: {"id": "2610.28589", "scope": "Core", "section": 5} -->

#### AgenticRoboRL: Bringing Coding-Agent Post-Training to Agentic Robotics

`2026-10-20` · University of Central Florida; University of Southern California; Michigan State University

[论文](https://arxiv.org/abs/2610.28589)

跨不同 Harness 后训练机器人规划模型。

**具体方法：** 将编程 Agent 的多轮后训练方法接入不同机器人 Harness，同时处理控制代码生成和动作技能调用两类执行机制。

**验证：** 规划模型权重更新区别于 Harness 改进，不同接口结果不能概括为同一种控制机制。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2606-18363"></a>
<!-- stage3-record: {"id": "2606.18363", "scope": "Adjacent", "section": 5} -->

#### Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness

`2026-06-16` · University of Maryland College Park; University of Illinois Urbana-Champaign; University of Waterloo; Mohamed bin Zayed University of Artificial Intelligence; University of Pennsylvania; Amazon FAR

[论文](https://arxiv.org/abs/2606.18363)

通过机器人 Harness 蒸馏前沿模型能力。

**具体方法：** 先研究具身工具 Harness 的设计，再将前沿模型在该接口中的机器人轨迹蒸馏到较小的 Agent。

**验证：** Harness 改动与学生模型训练是两个不同的改进来源。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2501-04268"></a>
<!-- stage3-record: {"id": "2501.04268", "scope": "Adjacent", "section": 5} -->

#### Robotic Programmer: Video Instructed Policy Code Generation for Robotic Manipulation

`2025-01-08` · Institute of Computing Technology, Chinese Academy of Sciences; University of Chinese Academy of Sciences

[论文](https://arxiv.org/abs/2501.04268)

用真实视频合成代码监督并训练机器人编程模型。

**具体方法：** 用 Video2Code 为真实机器人视频合成策略代码标签，再训练能从视觉和指令生成机器人程序的 RoboPro。

**验证：** 视频真实不代表合成代码曾在对应实机轨迹中执行。

**关联：** [1. 具身 Harness](#section-1) · [4. 数据](#section-4)

<a id="work-2402-16117"></a>
<!-- stage3-record: {"id": "2402.16117", "scope": "Adjacent", "section": 5} -->

#### RoboCodeX: Multimodal Code Generation for Robotic Behavior Synthesis

`2024-02-25` · University of Hong Kong; OpenGVLab, Shanghai AI Laboratory; ETH Zurich; Shanghai Jiao Tong University; Chinese University of Hong Kong; Tsinghua University; University of California, Berkeley

[论文](https://arxiv.org/abs/2402.16117)

训练多模态模型生成机器人行为程序。

**具体方法：** 通过多模态机器人代码数据训练模型，把视觉信息、物理偏好与任务推理转换为机器人行为程序。

**验证：** 训练改变代码生成模型；行为执行与迁移需区别于训练数据质量。

**关联：** [1. 具身 Harness](#section-1)

### 跨章节阅读

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

[返回研究地图](#research-map)

---

<a id="section-6"></a>

## 6. 物理应用与实验

物理应用检验生成程序、模型与设计能否达到外部目标。操作任务仍是本专题的重点；实验室操作、仪器与制造提供互补场景，其中标定、测量和材料约束会改变成功的含义。

| 应用 | 产物与接口 | 实验需要证明什么 |
|---|---|---|
| 机器人操作 | 运动程序、控制策略、力／触觉接口及可执行技能。 | 在姿态、物体和接触条件变化下的任务成功与恢复；分别说明仿真、实机及人工协助。[RAPID](#work-2609-30249) 检验演示推导程序，[FORCA](#work-2610-31841) 研究力感知编程。 |
| 科学实验与测量 | 仪器驱动、实验室布局、机器人实验流程与分析程序。 | 仪器调试、经标定的测量及可复核实验结果。[Self-Building Labs](#work-2610-23826) 连接实验室配置与可执行流程；物理观测既须支持工具执行，也须支持科学结论。 |
| 设计、制造与验证 | CAD、机器人形态、驱动程序、PCB 布线及制造方案。 | 几何／求解器检查、可制造性和实体试验是逐级证据。[PneuGen](#work-2611-13344) 制作选定的仿真设计；[PCBRouteAgent](#work-2611-08175) 报告布线检查，未开展制板实测。 |

每项结果分别识别 **Agent 的贡献**、**控制器或求解器的贡献**，以及**用于修订的反馈**。实体展示可以验证冻结设计或程序，而硬件未必参与其优化循环；通过真实试验开发的策略，也仍需要开发结束后的独立可靠性测试。

**研究问题。** 将经过验证的仿真结果迁移到新物理装置，需要哪些充分证据？哪些失败要求修改环境模型、控制器、程序或实验规格？

### 机器人交互与操作

<a id="work-2611-07881"></a>
<!-- stage3-record: {"id": "2611.07881", "scope": "Adjacent", "section": 6} -->

#### TactileLab: Sim-to-Real Dexterous Robot Manipulation with Efficient Shear-Sensitive Tactile Simulation

`2026-11-05` · Beijing Institute of Technology; University of Bristol; Xi’an Jiaotong-Liverpool University

[完整书目](../README.zh-CN.md#paper-2611-07881) · [论文](https://arxiv.org/abs/2611.07881) · [项目页](https://yijionglin.github.io/tactilelab/)

利用真实／仿真配对的触觉表示迁移仿真训练的操作策略。

**具体方法：** IsaacLab 刚体接触产生深度与切向流场，PETS-Net 将其与本体状态历史融合；真实触觉图像流用于训练映射到仿真表示的转换器。更新对象是触觉转换模型与控制策略，而非 Coding Agent。

**验证：** 验证包括仿真模态／架构消融、配对触觉标定、真实双臂物体跟随与 LEAP 手旋转。切向流建模采用黏着接触假设；该结果支持策略迁移，不代表自主构建仿真器。

**关联：** [2. Simulator 构建](#section-2) · [3. Simulator 质量评估](#section-3) · [4. 数据](#section-4) · [5. 训练与能力提升](#section-5)

<a id="work-2611-08321"></a>
<!-- stage3-record: {"id": "2611.08321", "scope": "Adjacent", "section": 6} -->

#### ControlAnything: Generative UI and On-Demand Device Integration for Mixed-Reality Hand Interaction by a Coding Agent

`2026-11-05` · 未明确

[完整书目](../README.zh-CN.md#paper-2611-08321) · [论文](https://arxiv.org/abs/2611.08321) · [代码](https://github.com/Apolotary/controlanything)

生成连接手势与设备的交互接口。

**具体方法：** 将视觉选物和语言请求交给 Coding Agent，基于已有传输层生成设备连接器、AR 控件与手势映射程序。

**验证：** 单作者技术评估验证到通信确认层，不等于目标物理效果已验证。

<a id="work-2610-31841"></a>
<!-- stage3-record: {"id": "2610.31841", "scope": "Core", "section": 6} -->

#### FORCA: A Force-Aware Coding Agent for Contact-Rich Robot Manipulation

`2026-10-22` · University of Illinois Urbana-Champaign; Tsinghua University

[完整书目](../README.zh-CN.md#paper-2610-31841) · [论文](https://arxiv.org/abs/2610.31841) · [项目页](https://tanoom.github.io/forca/)

联合视觉和力轨迹修复接触操作代码。

**具体方法：** 联合实机视觉结果与力／力矩轨迹修订 Python 接触控制代码，将执行反馈用于接触判断、动作顺序和恢复逻辑。

**验证：** 五类 UR5e 任务评估固定控制器成功率、力限制与真实修订成本。

<a id="work-2610-20998"></a>
<!-- stage3-record: {"id": "2610.20998", "scope": "Core", "section": 6} -->

#### MoCaP: Mobile Code-as-Policies for Zero-Shot Mobile Manipulation from Passive Human Videos

`2026-10-14` · New York University; Fudan University; NYU Shanghai

[完整书目](../README.zh-CN.md#paper-2610-20998) · [论文](https://arxiv.org/abs/2610.20998) · [项目页](https://mocap-7.github.io/MoCAP-page/)

把人类视频先验用于移动机器人程序。

**具体方法：** 从被动人类视频提取空间与接近方向先验，再依据实时 RGB-D 和执行反馈修订短 Python 机器人程序，由感知与运动工具落实机器人自身的约束。

**验证：** YOR 导航与两项抓取检验单环境可行性，不代表广泛跨家庭泛化。

<a id="work-2610-12549"></a>
<!-- stage3-record: {"id": "2610.12549", "scope": "Core", "section": 6} -->

#### Fly-by-Code: Embodied Coding Agents for Aerial Manipulation with Active Visual and Physical Feedback

`2026-10-08` · Seoul National University; Carnegie Mellon University; University of Maryland, College Park; All Purpose AI; Kyung Hee University

[论文](https://arxiv.org/abs/2610.12549) · [项目页](https://fly-by-code.github.io/)

用主动观测和物理探测编写空中操作程序。

**具体方法：** 让空中操作 Coding Agent 主动选择视角并实施物理探测，利用视觉和动作反馈修订可迁移到实机的任务程序。

**验证：** 仿真与实机证据分开，说明观测与物理探测分别贡献什么。

<a id="work-2609-30249"></a>
<!-- stage3-record: {"id": "2609.30249", "scope": "Adjacent", "section": 6} -->

#### RAPID: Robot Agentic Programming from Demonstrations

`2026-09-24` · Massachusetts Institute of Technology; National University of Singapore; University of Pennsylvania; NVIDIA

[完整书目](../README.zh-CN.md#paper-2609-30249) · [论文](https://arxiv.org/abs/2609.30249) · [项目页](https://yuyaoliu.me/projects/rapid)

从单次视觉演示推导可复用的关系式机器人程序与验证环境。

**具体方法：** 从视觉演示推导关系式机器人程序、成功谓词和重建仿真环境，在场景变体中细化原语及组合方式后，以固定程序部署。

**验证：** 在仿真中评估八项接触丰富的非抓取任务和 LIBERO-Pro，并在真实 Franka 上测试八项非抓取任务；部署验证所得程序，而非在线模型学习。

<a id="work-2609-23133"></a>
<!-- stage3-record: {"id": "2609.23133", "scope": "Core", "section": 6} -->

#### AquaCap: A Training-Free Underwater Embodied Agent with Code-as-Policy

`2026-09-19` · Sun Yat-sen University; Dalian University of Technology; BIXOCEAN; Southern Marine Science and Engineering Guangdong Laboratory

[完整书目](../README.zh-CN.md#paper-2609-23133) · [论文](https://arxiv.org/abs/2609.23133)

依据执行反馈调整水下机器人程序。

**具体方法：** 用传感器衍生的目标几何与可靠性检查水下动作结果，将抓取失败纠正传入后续 Python 程序与重规划。

**验证：** 仿真效率与消融另配泳池抓取和搬运结果，恢复与超时需单列。

<a id="work-2503-23875"></a>
<!-- stage3-record: {"id": "2503.23875", "scope": "Core", "section": 6} -->

#### GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models

`2025-03-31` · Department of Artificial Intelligence, Westlake University, Hangzhou, China; School of Automation Science and Electrical Engineering, Beihang University, Beijing, China; Institute of Engineering and Technology, University of Groningen, Groningen, Netherlands; Department of Computer Science, Technical University of Darmstadt, Darmstadt, Germany; School of Electrical and Electronic Engineering, The University of Sheffield, Sheffield, UK

[论文](https://arxiv.org/abs/2503.23875) · [代码](https://github.com/WindyLab/GenSwarm) · [论文](https://www.nature.com/articles/s44182-025-00065-w)

生成、修订并部署多机器人程序策略。

**具体方法：** 由语言模型分解多机器人任务并生成分层控制代码，通过仿真、视频分析与人工反馈修订后部署到实体机器人。

**验证：** 仿真优化与实体部署分开报告，人工纠正应明确保留。

<a id="work-2403-07832"></a>
<!-- stage3-record: {"id": "2403.07832", "scope": "Adjacent", "section": 6} -->

#### DeliGrasp: Inferring Object Properties with LLMs for Adaptive Grasp Policies

`2024-03-12` · University of Colorado Boulder

[论文](https://arxiv.org/abs/2403.07832) · [项目页](https://deligrasp.github.io)

把物体属性估计用于自适应抓取。

**具体方法：** 让 LLM 推断物体质量、摩擦和刚度并写成自适应抓取策略，将常识估计与反馈控制结合以操作易损物体。

**验证：** 抓取使用推断属性，操作成功不能证明物理参数被准确恢复。

<a id="work-2310-13065"></a>
<!-- stage3-record: {"id": "2310.13065", "scope": "Adjacent", "section": 6} -->

#### Creative Robot Tool Use with Large Language Models

`2023-10-19` · Carnegie Mellon University; Google DeepMind

[论文](https://arxiv.org/abs/2310.13065) · [项目页](https://creative-robotool.github.io/)

通过程序组织机器人的物理工具使用。

**具体方法：** 由分析、规划、参数计算和编码模块生成机器人 Python 程序，研究机器人怎样借助工具解决带隐含物理约束的操作任务。

**验证：** 执行实验检验工具使用，物理推理结论限于所测对象与任务。

<a id="work-2307-05973"></a>
<!-- stage3-record: {"id": "2307.05973", "scope": "Adjacent", "section": 6} -->

#### VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models

`2023-07-12` · Stanford University; University of Illinois Urbana-Champaign

[论文](https://arxiv.org/abs/2307.05973) · [项目页](https://voxposer.github.io)

用代码组合三维价值图来规划操作。

**具体方法：** 让语言模型编写组合视觉工具的程序以形成三维价值图，再由模型式规划器生成机器人轨迹；重算价值图与重写代码应区分。

**验证：** 根据新观测重算价值图与 LLM 重写代码应分开。

### 实验、测量与发现

<a id="work-2610-41717"></a>
<!-- stage3-record: {"id": "2610.41717", "scope": "Adjacent", "section": 6} -->

#### Evaluating Instrument-Centered AI Agents for Table-Top Science Experiments

`2026-10-30` · Massachusetts Institute of Technology; Boston College; University of Washington

[论文](https://arxiv.org/abs/2610.41717) · [代码](https://github.com/caidish/instrMCP) · [代码](https://github.com/caidish/qdevbench)

通过可编程仪器工具检验实验推理。

**具体方法：** 以 instrMCP 给 Coding Agent 提供仪器接口，并用 q-devBench 的虚拟台式实验检查测量、诊断和分析能力。

**验证：** 虚拟仪器结果区别于真实设备接入、权限与人工批准机制。

<a id="work-2610-41383"></a>
<!-- stage3-record: {"id": "2610.41383", "scope": "Adjacent", "section": 6} -->

#### BioAgent: Self-Directed Skill Acquisition and Capability Growth for Long-Horizon Laboratory Protocols

`2026-10-30` · Shanghai Jiao Tong University; University of Sussex

[论文](https://arxiv.org/abs/2610.41383)

通过教学与实现补齐实验室技能。

**具体方法：** 让实验室机器人识别协议中的能力缺口，通过工具实现与人类教学获得技能，并验证其在长时序实验中的有效性。

**验证：** 人工教学、实现审阅和验证限制了自主技能发现的表述。

<a id="work-2610-37649"></a>
<!-- stage3-record: {"id": "2610.37649", "scope": "Core", "section": 6} -->

#### Can LLMs Uncover Hidden Physical Laws through Free Exploration?

`2026-10-27` · HKUST(GZ); ZJU; Alibaba Group; HKUST

[完整书目](../README.zh-CN.md#paper-2610-37649) · [论文](https://arxiv.org/abs/2610.37649) · [项目页](https://zhenyangcs.github.io/LongChang-website/) · [代码](https://github.com/EnVision-Research/LongChang)

检验对模拟物理规律的开放探索。

**具体方法：** 在改变物理规律的 MuJoCo 世界中评测无指定任务的物理探究，包括探索者发现球滑离秤盘后依据空间观测重新设计测量装置的轨迹。

**验证：** 发现针对修改后的模拟世界，不是经真实实验确立的新物理规律。

<a id="work-2610-35385"></a>
<!-- stage3-record: {"id": "2610.35385", "scope": "Adjacent", "section": 6} -->

#### EmbodiedLab: Benchmarking Embodied Agents That Act to Know

`2026-10-26` · HexaFuture; Tsinghua University; National University of Singapore; Peking University

[论文](https://arxiv.org/abs/2610.35385) · [代码](https://github.com/HexaFuture/EmbodiedLab) · [项目页](https://hexafuture.ai/benchmarks/embodiedlab/)

评测通过行动获取科学证据的 Agent。

**具体方法：** 在模拟实验室中评测 Coding Agent 如何安排操作、读取仪表并提交有执行证据支持的结论，而非只完成动作目标。

**验证：** 仪表读数与答案检查来自仿真，不是实机科学发现。

<a id="work-2610-23826"></a>
<!-- stage3-record: {"id": "2610.23826", "scope": "Adjacent", "section": 6} -->

#### Self-Building Labs

`2026-10-16` · University of Toronto; Vector Institute; Acceleration Consortium; University of Amsterdam; CIFAR; NVIDIA

[论文](https://arxiv.org/abs/2610.23826) · [项目页](https://self-building-labs.github.io/)

将实验装置纳入可编程研究对象。

**具体方法：** 让 Agent 围绕科学目标设计、配置并操作实验装置，研究实验室从固定流程执行向可编程重构扩展的条件。

**验证：** 装置构建、配置与实验结果各需对应物理执行证据。

<a id="work-2609-18435"></a>
<!-- stage3-record: {"id": "2609.18435", "scope": "Adjacent", "section": 6} -->

#### WetRobo: A Reproducible Robot Kit for Coding Agents in Biological Laboratories

`2026-09-16` · University of Tokyo; RIKEN; New York University; Google DeepMind; National Institute for Materials Science

[论文](https://arxiv.org/abs/2609.18435) · [代码](https://github.com/tsudalab/WetRobo)

提供编程 Agent 可用的实验室机器人套件。

**具体方法：** 提供机械臂、实验室器具、示范和 Skill 文件，使 Codex 能在真实实验台上编写和调整基础操作程序。

**验证：** 人工标定、设备准备与技能示教仍是实验配置的一部分。

<a id="work-2608-01690"></a>
<!-- stage3-record: {"id": "2608.01690", "scope": "Adjacent", "section": 6} -->

#### ProtoAct: Turning Wet-Lab Protocols into Embodied Robotic Actions

`2026-08-03` · East China University of Science and Technology; Ruijin Hospital, Shanghai Jiao Tong University School of Medicine; Shanghai AI Laboratory

[论文](https://arxiv.org/abs/2608.01690)

把实验协议编译为机器人动作。

**具体方法：** 将实验协议解析为可检查的条件与函数序列，通过检索和修订补齐隐含步骤，并连接机器人演示采集与策略训练。

**验证：** 协议编译、示范采集和学习策略执行分别验证。

<a id="work-2607-23045"></a>
<!-- stage3-record: {"id": "2607.23045", "scope": "Adjacent", "section": 6} -->

#### Stress-testing large language model agents in a robotic chemistry laboratory

`2026-07-25` · University of Science and Technology of China; Center for Scientific Intelligence Innovation, Hefei; University of Birmingham

[论文](https://arxiv.org/abs/2607.23045)

在机器人实验室流程中检验编程 Agent。

**具体方法：** 将实验室工作站封装为机器可读 Skills，让 Codex、Claude Code 等 Agent 生成和提交实验流程，评测可执行性与物理反馈下的修订能力。

**验证：** 大规模可执行性评分不等于全部实机运行；多轮实机实验包含人工科学判断。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-bespoke-instrument"></a>
<!-- stage3-record: {"id": "bespoke-instrument", "scope": "Resource", "section": 6} -->

#### AI-designed and AI-implemented control systems for bespoke scientific instrumentation: application to scanning microscopy

`2026-05-08` · University of Cambridge

[项目页](https://pubs.rsc.org/en/content/articlelanding/2026/dd/d6dd00177g) · [论文](https://www.repository.cam.ac.uk/items/cb2e6fef-94c4-4fe9-903a-aaa198da8f4f)

在人类监督下开发仪器控制代码。

**具体方法：** 由研究者与通用 LLM 协作开发显微镜控制代码和数字沙盒，经模拟检查、另一模型交叉审阅及人工审核后部署到真实仪器。

**验证：** 真实 SHeM 成像与衍射验证仪器，开发、审阅和部署仍由人主导。

**关联：** [2. Simulator 构建](#section-2)

<a id="work-2509-25651"></a>
<!-- stage3-record: {"id": "2509.25651", "scope": "Adjacent", "section": 6} -->

#### AutoLabs: cognitive multi-agent systems with self-correction for autonomous chemical experimentation

`2025-09-30` · Pacific Northwest National Laboratory, Richland, Washington, WA, USA

[论文](https://arxiv.org/abs/2509.25651) · [代码](https://github.com/pnnl/autolabs) · [论文](https://doi.org/10.1038/s41598-026-45593-z)

生成经过检查的实验室可执行协议。

**具体方法：** 将实验目标分解为液体处理器可执行协议，通过多 Agent 计算、检查和修订，评测硬件就绪文件的有效性。

**验证：** 硬件就绪文件有效性不同于逐条协议均已实机执行。

<a id="work-2509-24978"></a>
<!-- stage3-record: {"id": "2509.24978", "scope": "Core", "section": 6} -->

#### Agentic Exploration of Physics Models

`2025-09-29` · Max Planck Institute for the Science of Light, Staudtstraße 2, 91058 Erlangen, Germany; Department of Physics, Friedrich-Alexander Universität Erlangen-Nürnberg, Staudtstraße 5, 91058 Erlangen, Germany

[论文](https://arxiv.org/abs/2509.24978) · [代码](https://github.com/MaxNaeg/SciExplorer) · [论文](https://journals.aps.org/prx/abstract/10.1103/xnqc-q6nt)

通过程序化数值实验探索物理模型。

**具体方法：** 让多模态 Agent 编写分析与绘图代码、主动选择数值实验，并根据观测持续修订未知物理系统的模型与解释。

**验证：** 实验来自数值模拟，不是实机机器人实验或现实新规律发现。

<a id="work-chemagents"></a>
<!-- stage3-record: {"id": "chemagents", "scope": "Adjacent", "section": 6} -->

#### A Multiagent-Driven Robotic AI Chemist Enabling Autonomous Chemical Research On Demand

`2024-07-30` · 未明确

[论文](https://doi.org/10.1021/jacs.4c17738) · [论文](https://www.cambridge.org/engage/chemrxiv/article-details/66a8c11bc9c6a5c07a7a59c0)

通过生成 API 程序协调机器人化学研究。

**具体方法：** 以分工协作的 Agent 将实验意图转化为机器人 API 程序，结合代码审查、设备执行与实验数据分析开展多步骤化学研究。

**验证：** 预印本支持代码生成与执行，期刊全文受限，研究者参与目标和设计。

**关联：** [1. 具身 Harness](#section-1)

<a id="work-2304-05332"></a>
<!-- stage3-record: {"id": "2304.05332", "scope": "Adjacent", "section": 6} -->

#### Autonomous chemical research with large language models

`2023-04-11` · 未明确

[论文](https://arxiv.org/abs/2304.05332) · [论文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10733136/) · [代码](https://github.com/gomesgroup/coscientist)

用语言模型组织自动化化学实验。

**具体方法：** 让语言模型调用文献、Python 和实验设备接口，生成并执行化学实验程序，在人类配置的实验系统中开展自动研究。

**验证：** 真实化学实验依赖人工配置设备；简化发布代码不等于完整实验系统。

<a id="work-xray-scientist"></a>
<!-- stage3-record: {"id": "xray-scientist", "scope": "Adjacent", "section": 6} -->

#### An agentic artificially intelligent X-ray scientist

`首发日期未明确` · Stanford University; SLAC National Accelerator Laboratory; University of Texas at Austin; Carnegie Mellon University; Northeastern University; Howard University; Massachusetts Institute of Technology

[论文](https://www.nature.com/articles/s42256-026-01261-5) · [代码](https://github.com/zhantaochen/llm4xray)

把实验 Agent 接入 X 射线仪器。

**具体方法：** 让 Agent 调用 Python 与 MCP 实验接口，在虚拟光束线中准备流程，再结合真实仪器测量完成单晶样品定向。

**验证：** 真实命令由人转交作为固定中介，虚拟光束线由研究者构建。

**关联：** [1. 具身 Harness](#section-1)

### 物理设计、制造与验证

<a id="work-2611-13344"></a>
<!-- stage3-record: {"id": "2611.13344", "scope": "Core", "section": 6} -->

#### PneuGen: Task-Driven Agentic Co-Design of Soft Pneumatic Robots

`2026-11-09` · Oxford Robotics Institute, University of Oxford

[完整书目](../README.zh-CN.md#paper-2611-13344) · [论文](https://arxiv.org/abs/2611.13344)

通过可执行设计程序与仿真批评，迭代联合设计软体气动机器人的形态及驱动。

**具体方法：** 设计 Agent 依据拟合的模块响应先验选择参数化模块；类型化程序经结构检查后生成 CAD 与四面体网格，并运行 SOFA 有限元仿真。批评 Agent 根据空间诊断修改形态和驱动。

**验证：** 开展限预算抓取、二维／三维形状匹配、批评器与响应先验消融，并制作实体机器人展示。实物实验验证选定设计，硬件反馈未进入所报告的优化循环。

**关联：** [2. Simulator 构建](#section-2) · [3. Simulator 质量评估](#section-3) · [5. 训练与能力提升](#section-5)

<a id="work-2611-08175"></a>
<!-- stage3-record: {"id": "2611.08175", "scope": "Core", "section": 6} -->

#### PCBRouteAgent: How Close Are LLM Agents to Becoming PCB Routing Engineers?

`2026-11-05` · University of Texas at Dallas; Texas Instruments; Iowa State University

[完整书目](../README.zh-CN.md#paper-2611-08175) · [论文](https://arxiv.org/abs/2611.08175) · [项目页](https://chip-ai-agent.github.io/research/pcbrouteagent)

依据 KiCad 原生执行反馈修订 PCB 布线指引，以改善电路板连通性。

**具体方法：** 多模态全局规划器结合固定的初始板图和更新的障碍／连通性报告，修改布线顺序、走廊与换层方案；KiCad 负责细部几何布线及有限恢复，并保留已接受的走线。

**验证：** 在 247 块 PCBWorld 电路板上按连通性及零错误级设计规则违规评估，并比较重规划策略；部分 D3-B 结果含恢复步骤。未报告制板实测、信号完整性验证或完整制造认证。

**关联：** [1. 具身 Harness](#section-1) · [3. Simulator 质量评估](#section-3) · [5. 训练与能力提升](#section-5)

<a id="work-2610-31651"></a>
<!-- stage3-record: {"id": "2610.31651", "scope": "Core", "section": 6} -->

#### BrickWright: Agentic Creation of Physically Feasible Brick Builds

`2026-10-22` · Carnegie Mellon University; Independent Researcher; Stanford University

[完整书目](../README.zh-CN.md#paper-2610-31651) · [论文](https://arxiv.org/abs/2610.31651) · [代码](https://github.com/avalovelace1/brickwright) · [项目页](https://avalovelace1.github.io/brickwright/)

检查程序化积木设计的结构可行性。

**具体方法：** 通过类型化连接、碰撞与悬空检查及渲染观察修复 Python 积木模型；其物理可行性定义不包含稳定性和可执行装配顺序保证。

**验证：** 可行性覆盖连接、碰撞和悬空，不保证承载稳定性或可执行装配顺序。

<a id="work-2610-17881"></a>
<!-- stage3-record: {"id": "2610.17881", "scope": "Core", "section": 6} -->

#### Agentic Robot Creation through Generation, Verification, and Revision

`2026-10-13` · ShanghaiTech University

[完整书目](../README.zh-CN.md#paper-2610-17881) · [论文](https://arxiv.org/abs/2610.17881) · [项目页](https://roboforge-project.github.io/)

联合开发机器人形态和可执行行为。

**具体方法：** 提出 RoboForge，依据仿真中的身体、关节和接触反馈修订程序化参考运动与奖励配置，再将学得策略部署到经过人工设计修正并制造的机器人上。

**验证：** Gorilla 实体验证包含制造前的人工机械设计修正。

**关联：** [5. 训练与能力提升](#section-5)

<a id="work-2609-08220"></a>
<!-- stage3-record: {"id": "2609.08220", "scope": "Core", "section": 6} -->

#### Bridging Language and Physics: Automated Design of Continuum Robots with Large Language Models

`2026-09-08` · University of Science and Technology of China; University of North Carolina at Chapel Hill; University of Central Florida

[完整书目](../README.zh-CN.md#paper-2609-08220) · [论文](https://arxiv.org/abs/2609.08220) · [代码](https://github.com/UNITES-Lab/AID-SR)

用物理反馈改进连续体机器人设计。

**具体方法：** 生成可执行的 MuJoCo XML 机器人设计，观察其仿真物理状态，并把结构化诊断返回 Coding Agent，迭代修复机器人形态。

**验证：** XML 有效性、稳定性、下游任务与仿真实体一致性分别检查。

<a id="work-2605-17448"></a>
<!-- stage3-record: {"id": "2605.17448", "scope": "Core", "section": 6} -->

#### Self-Improving CAD Generation Agents with Finite Element Analysis as Feedback

`2026-05-17` · Seoul National University; OneLineAI; Sungkyunkwan University; Ewha Womans University

[完整书目](../README.zh-CN.md#paper-2605-17448) · [论文](https://arxiv.org/abs/2605.17448)

用视觉和有限元反馈改进 CAD 设计。

**具体方法：** 让 Coding Agent 编写 CadQuery 装配程序，依据多视图图像和有限元反馈修改设计，以结构与物理约束检查生成的工程产物。

**验证：** Hephaestus-CCX 检验工程仿真，部分提升涉及检查器契约修复，不等同实体制造。

**关联：** [5. 训练与能力提升](#section-5)

<a id="work-2408-14307"></a>
<!-- stage3-record: {"id": "2408.14307", "scope": "Adjacent", "section": 6} -->

#### LLM-3D Print: Large Language Models To Monitor and Control 3D Printing

`2024-08-26` · Carnegie Mellon University

[论文](https://arxiv.org/abs/2408.14307) · [代码](https://github.com/BaratiLab/LLM-3D-Print-Large-Language-Models-To-Monitor-and-Control-3D-Printing)

将打印图像反馈接入真实制造控制。

**具体方法：** 让视觉语言模型逐层检查打印图像、查询设备参数并调用控制工具修正打印过程，将 Agent 接入真实制造反馈。

**验证：** 诊断使用真实打印图像与参数，设备文档和平台配置由人准备。

<a id="work-ai-cad"></a>
<!-- stage3-record: {"id": "ai-cad", "scope": "Resource", "section": 6} -->

#### ai-cad

`首发日期未明确` · 未明确

[代码](https://github.com/BorjaLL/ai-cad) · [结果](https://github.com/BorjaLL/ai-cad/blob/1ef2bf72de799006d069498d3ee146dae2e4f075/data/fits-measured.json)

连接参数化 CAD 与人工打印试配。

**具体方法：** 以参数化 CAD 程序、打印试配照片和人工反馈迭代实体零件，提供代码设计走向制造验证的社区记录。

**验证：** 试配由人操作与判断，名义间隙不是自动精密测量结果。

<a id="work-agentic-fdm-printing"></a>
<!-- stage3-record: {"id": "agentic-fdm-printing", "scope": "Resource", "section": 6} -->

#### Agentic AI for FDM 3D Printing Process Control

`首发日期未明确` · 未明确

[代码](https://github.com/jabarkle/AgenticAI-FDM-Printing) · [代码](https://github.com/BaratiLab/LLM-3D-Print-Large-Language-Models-To-Monitor-and-Control-3D-Printing)

记录复用式 Agent 打印工作流。

**具体方法：** 复用 LLM-3D-Print 的图像检查和 G-code 控制工作流，记录不同提示对缺陷诊断、打印参数修正与恢复的影响。

**验证：** 公开七次运行，其中一次图像处理失败导致幻觉评分，上游已明确注明。

### 跨章节阅读

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

[返回研究地图](#research-map)
