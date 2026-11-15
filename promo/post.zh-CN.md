# 多模态视角下的 Coding｜Awesome Multimodal Agentic Coding

> 宣传稿草稿。图片在 [`images/`](images/)，由 [`gen.js`](gen.js) 生成；改了图里的文字后重新运行即可。

## 一、精要介绍（帖子正文）

### 中文完整版（X Premium、即刻、小红书、朋友圈）

```text
多模态视角下的 Coding

GPT-6 之后，Computer Use Agent 火了。但我们一直从 Coding、而不是 CUA 的角度看多模态 Agent：
CUA 关心 Agent 怎么「用」现成的软件；我们关心 Agent 怎么用代码「造」东西，看见结果，再把它改好。

我们把这条路分成三个逐层叠加的阶段：
1️⃣ Visual as Feedback：看见自己造出的东西，coding loop 闭合起来
2️⃣ Agent Orchestrates Models：把生成、感知、动作模型当作工具调用
3️⃣ Bridging Digital & Physical：用代码构建仿真、驱动机器人，Real2Sim2Real

扩展 Agent 的能力边界，最终通向物理 AGI。
我们把相关工作整理成了 Awesome Multimodal Agentic Coding：664 项工作，中 / 英 / 日三语，持续更新 👇
https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
```

### 中文短版（X 免费账号，280 字符限制内）

X 上一个汉字算 2 个字符，链接固定算 23 个。这一版约 230 / 280。

```text
多模态视角下的 Coding：
不从 Computer Use，而从 Coding 看多模态 Agent，分三个阶段：
1 视觉反馈，让 coding loop 闭合
2 编排模型，把模型当作工具
3 用代码打通仿真与现实
扩展 Agent 能力边界，最终通向物理 AGI 👇
https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
```

### English（X，约 272 / 280）

```text
Coding, seen through a multimodal lens:
agents that write code, see what it builds, and improve it.
01 Visual as feedback
02 Orchestrating models as tools
03 Bridging digital & physical worlds
Toward physical AGI. 664 works, updated continuously 👇
https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
```

## 二、图片

| 顺序 | 文件 | 内容 |
|---|---|---|
| 1 | [`00-cover.png`](images/00-cover.png) | 封面：大字「多模态视角下的 Coding」、仓库头图、三阶段、链接与二维码 |
| 2 | [`01-why-coding.png`](images/01-why-coding.png) | 出发点：不是 Computer Use，而是 Coding |
| 3 | [`02-stage1-visual-feedback.png`](images/02-stage1-visual-feedback.png) | 01 Visual as Feedback |
| 4 | [`03-stage2-orchestrate-models.png`](images/03-stage2-orchestrate-models.png) | 02 Agent Orchestrates Models |
| 5 | [`04-stage3-digital-physical.png`](images/04-stage3-digital-physical.png) | 03 Bridging Digital & Physical Worlds |

尺寸都是 2160 × 2880（3:4）。小红书、即刻可以 5 张全发。X 每条最多 4 张：主帖放 1、3、4、5，第 2 张的内容已经写进正文；也可以把第 2 张放进回复。

## 三、正文（详细思路）

图里的文字是下面这版的压缩版。下面这版可以直接用于公众号、知乎或长帖。

### 多模态视角下的 Coding｜Awesome Multimodal Agentic Coding

**扩展 Agent 的能力边界，最终通向物理 AGI**

最近和几位大佬交流，大家觉得我们看问题的角度还挺有意思，所以整理出来分享一下。

我们从 6 月开始做多模态 coding 相关的任务。GPT-6 发布后，Computer Use Agent（CUA）迅速火了起来，我们之前贴着模型能力边界做的不少研究，也一下子失去了意义。

但我们一直是从 **Coding**、而不是 CUA 的角度来看多模态 Agent：

- **CUA 视角**：Agent 像人一样「用」现成的软件，看屏幕、点按钮，完成软件里已有的操作；
- **Coding 视角**：Agent 用代码「造」东西，看见运行的结果，再把它改好。造出的可以是网页、3D，也可以是仿真世界。

沿着这条线，我们把多模态 Agentic Coding 理解为三个逐层叠加的阶段。

#### 01 Visual as Feedback：视觉反馈，让 coding loop 跑起来

相比一般的 coding agent，多模态 coding agent 的关键是有**视觉反馈**：写代码 → 渲染或运行 → 观察结果 → 决定下一步怎么改。这一点极大地扩展了 Agent 的能力边界：网页与 UI、图表、文档与幻灯片、3D 与 CAD、游戏……凡是运行出来能被看见的东西，都可以进入这个闭环。

其中，perception、grounding、diff 等原子多模态能力是基础：看得准、定位得准、比得出差异，反馈才精准，coding loop 才能稳定地跑起来。

在此之前，通过各种 workflow 也能引入视觉反馈；但在 Agent 场景下，模型不再只是做 VQA，而是能自主地对比、定位问题，并对整个「多模态 repo」（代码 + 素材 + 渲染结果）持续优化。

#### 02 Agent Orchestrates Models：编排模型，进一步扩展能力边界

视觉反馈让 Agent 拥有了巨大的多模态任务空间。但如果 Agent 只能自己看、自己做，不仅会有长上下文带来的幻觉，还可能需要极大量的计算。把其他模型当作工具调用，可以有效改善这两点。

Orchestration 同时体现在输入和输出两端：

- **输入端**：调用更擅长的模型（检测、分割、深度、重建等感知模型），从不同维度提供观察；
- **输出端**：调用生成模型做 mask 重绘、基于白模给出构图，或生成视频、3D 与可交互的世界；也可以调用 action model 来操控机械臂。

代码在这里是胶水：Agent 用代码选择、组合这些模型，并根据反馈修改整个工作流。这既扩展了能力边界，也提高了效率。

#### 03 Bridging Digital & Physical Worlds：用代码打通数字世界与物理世界

前两个阶段不断扩展 coding agent 在数字世界里的能力边界；到第三个阶段，这个闭环走进了物理世界。这也是我们仓库目前最大、增长最快的部分：664 项工作中有 318 项属于这一阶段，2026 年下半年新增的就有 200 项。

我们看到三条主线：

**① 代码驱动行动（Digital → Physical）。** 从 Code as Policies 开始，Agent 就在用代码调用感知与运动接口来操控机器人。最近一批 robot-use agent 和 embodied harness 让通用 coding agent 直接写 Python、调 ROS，观察相机画面与力反馈，再修改下一步动作。阶段一的「看结果改代码」，在这里变成了「看动作结果改策略」。同样的闭环也延伸到 PCB 布线、软体机器人设计和科学实验。

**② 代码构建仿真（Real → Sim）。** Agent 从真实视频和观测出发，把场景、物体、关节和物理参数写成可执行的仿真器。仿真器本身就是一个「多模态 repo」：可以和真实录像对照，也可以改变条件重新跑。为此我们整理了一套仿真器质量的检验层级：从「看起来像」「静止时合理」「能交互」「动起来对」，一直到「在仿真里排第一的策略，到真机上是否仍排第一」，每一层拆穿一种「假仿真」。

**③ 在仿真里练，回到现实用（Sim → Real）。** 有了可验证的环境，Agent 就能自己造数据，积累经验、记忆与 skills，在数字孪生里先预演失败恢复，甚至只靠仿真里的成功轨迹给小模型做后训练，再把能力带回真机。

从代码的角度看，这三条线是同一个闭环：**构建可验证的环境 → 收集交互经验 → 提升 Agent**。代码可执行、可检查、可编辑、可组合，因此能成为连接感知、生成、行动与仿真的共同语言。

#### 结语

三个阶段是逐层叠加的：

- **01** 看见自己造出的东西；
- **02** + 把模型当作工具调用；
- **03** + 在仿真与现实中行动和学习。

我们相信，这条「写代码 → 看结果 → 再改进」的路径，会一步步把 Agent 从屏幕里带到真实世界，最终通向物理 AGI。

我们把相关工作整理成了 **Awesome Multimodal Agentic Coding**：目前收录 664 项工作（论文、工具、数据集与 Demo），按三个阶段、19 个方向组织，提供中 / 英 / 日三语，并持续更新。欢迎 star、提 issue 推荐工作，也欢迎直接来找我们交流。

🔗 https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
