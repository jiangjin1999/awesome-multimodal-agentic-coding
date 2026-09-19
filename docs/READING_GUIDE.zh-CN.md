# 多模态智能体编程导读

[返回合集](../README.zh-CN.md) · [English](./READING_GUIDE.md)

Agent 编写代码、执行、观察结果，再依据观测选择下一次修改或动作。本导读用这条共同的闭环，连接界面、CAD、3D 与游戏中的具体案例。

## 五个阅读起点

以下案例展示不同机制，不代表排名。

| 从哪里开始 | 跟随反馈路径 | 帮助理解什么 |
|---|---|---|
| [Programming with Pixels](https://programmingwithpixels.com/) — UI Development Demo | Agent 在 IDE 内修改 HTML，将实时预览与参考图并排查看，再继续编辑。 | 屏幕观测如何在通用计算机操作环境中指导实现。 |
| [CAD-Assistant](https://cadassistant.github.io/) | FreeCAD 动作改变模型，不断变化的 CAD 状态影响后续动作。 | 为什么环境除了执行代码，还需要暴露几何信息与合适的视图。 |
| [Procedura](https://spatiaos.github.io/projects/procedura/) | 程序化装配逐部件构建；渲染视图与独立视觉 Critic 指导修订，编译与配合检查共同把关。 | 程序表示和验收检查如何影响修复循环。 |
| [Play2Code](https://continual-game-generation.vercel.app/) | GUI Agent 实际游玩生成的 HTML 游戏，将体验报告与修复清单返回给 Coding Agent。 | 为什么交互轨迹能暴露单张图片难以发现的问题。 |
| [Text-to-CAD Evaluation with CADTests](https://arxiv.org/html/2605.07807v1) — §6 与附录 C | 对比四视图视觉 ReAct、测试驱动代码修订与几何日志。 | 为什么反馈方式需要实验验证：该研究中额外的视觉反馈没有提高性能。 |

## 选择阅读路线

- **了解领域：** 先看 PwP 的 UI Demo，再看 CAD-Assistant 与 Play2Code，随后通过[主题地图](../README.zh-CN.md#topic-map)寻找关心的产物类型。
- **搭建系统：** 先选[执行引擎](../README.zh-CN.md#execution-and-rendering-engines)，再查看对应的 [Skills 与工具桥](../README.zh-CN.md#skills-and-tool-bridges)，比较产物与观测通路相近的方法。工具能截图，并不等于 Agent 已经利用截图改进代码。
- **设计研究：** 对比 Procedura 与 CADTests 的反馈路径，再阅读相应的[基准与方法](../README.zh-CN.md#paper-and-project-list)以及[研究前沿](../README.zh-CN.md#research-frontiers)。

## 比较闭环，而不只看最终产物

阅读论文或设计实验时，可以使用以下五个问题。

| 问题 | 记录什么 | 为什么有用 |
|---|---|---|
| 什么可以被修改？ | HTML/CSS、CAD 程序、场景图、游戏代码、幻灯片对象或机器人策略。 | 表示方式决定哪些内容能局部修改，哪些需要重新构建。 |
| 实际观察到了什么？ | 渲染视图、视频片段、交互轨迹、空间测量或 Rollout。 | 反馈需要能暴露希望修复的错误。 |
| 谁看到了它，何时看到？ | Coding 模型、独立 Critic、人或最终评估者；执行前还是执行后。 | 视觉 Critic 可以向 Coding 模型传递文本诊断；只有最终评估并不能指导后续修改。 |
| 下一步改变了什么？ | 代码补丁、相机视角、交互动作、参数或另一项测试。 | 具体的后续动作把观测与改进连接起来。 |
| 如何确认进展？ | 视觉保真度、功能、几何、物理行为、内容准确性、成本或回归检查。 | 视觉上合理的产物仍可能无法完成预期任务。 |

可以用这个简短格式记录比较结果：

```text
任务 → 可编辑表示 → 运行环境 → 观测 → 接收者 → 后续动作
验收检查／停止规则：
最终评估：
成本与失败案例：
```

## 实验中值得带走的三个问题

**检查方式是否对应需求？** 渲染能暴露缺失对象或布局问题；CAD 内核能检查尺寸与拓扑；实际游玩能暴露无法触发的胜利条件。CADTests 提供了视觉反馈与测试反馈的具体比较（[§6](https://arxiv.org/html/2605.07807v1#S6)）。

**是否看到了完整系统？** 独立视觉 Critic 可以观察产物，再向文本 Coding 模型传递诊断。Procedura 明确展示了这种分工（[论文 §3.4](https://arxiv.org/html/2608.26238v1#S3.SS4)）。

**多一轮反馈是否值得？** 与条件匹配的单次生成或仅执行反馈基线比较，计入额外 Token 与运行成本，并检查回归。修订没有成功的结果，同样能帮助理解反馈设计。

## 找到合适的收录区域

**Core** 工作在同一轨迹或明确的基准配置中包含代码、执行、多模态观测与后续动作。**Adjacent** 工作提供相关的生成、评估或交互基础。**Resource** 提供工具、Skills、引擎与 Demo。这些身份表示不同作用，不是质量排名。

阅读基准时，确认具体哪种评估配置使用反馈；观看 Demo 时，区分展示的行为与经过测量的基准结果。

有合适的案例或更正？欢迎[在这里提交](https://github.com/jiangjin1999/awesome-multimodal-agentic-coding/issues/new/choose)，中英文均可。
