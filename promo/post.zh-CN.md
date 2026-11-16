# 多模态视角下的 Coding｜Awesome Multimodal Agentic Coding

> 宣传稿。封面图（定版）是 [`images/cover.png`](images/cover.png)，由 [`gen.js`](gen.js) 生成；改了图里的文字后重新运行即可。

## 一、精要介绍（帖子正文）

### 中文版（定版）

适合 X Premium、即刻、小红书、朋友圈；X 免费账号有 280 字符限制，发不下。

```text
多模态视角下的 Coding

最近和一些同学交流，感觉我们的角度还挺有意思，分享一下～

GPT6 Astra 之后 Computer Use Agent 火了，但我们更多是从 coding 而不是 CUA 的角度来看多模态的发展，最近 Robot Use Agent 也开始多起来了：让 Agent 直接写代码控制机器人，这也是多模态 coding 这条线往物理世界的延伸；

我们把这条路分成三步：
1️⃣ Visual as Feedback：有了视觉反馈，模型才能真正 loop 起来
2️⃣ Agent Orchestrates Models：让 Agent 去调生成、感知、动作模型，能力边界进一步扩展
3️⃣ Bridging Digital & Physical：用代码搭仿真、控机器人，从屏幕走到真实世界

扩展 Agent 能力边界，最终通向物理 AGI👇
https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
```

以下两个版本是早先的草稿，没有按定版更新。

### 中文短版（X 免费账号，280 字符限制内）

X 上一个汉字算 2 个字符，链接固定算 23 个。这一版约 209 / 280。

```text
多模态视角下的 Coding：
我们一直从 coding 而不是 CUA 的角度看多模态 Agent，分三步：
1 有了视觉反馈，模型才能 loop 起来
2 让 Agent 去调别的模型
3 用代码打通仿真和现实
最终通向物理 AGI 👇
https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
```

### English（X，约 278 / 280）

```text
We look at multimodal agents from a coding angle, not computer use:
agents write code, see what it builds, and fix it.
01 Visual as feedback
02 Orchestrating models as tools
03 Bridging digital & physical worlds
Toward physical AGI. 664 works, growing 👇
https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
```

## 二、封面图（定版）

[`images/cover.png`](images/cover.png)：2160 × 2880（3:4）。大字「多模态视角下的 Coding」，加上仓库头图、三个阶段和仓库链接。

## 三、正文（详细思路）

可以直接用于公众号、知乎或长帖。

### 多模态视角下的 Coding｜Awesome Multimodal Agentic Coding

**扩展 Agent 能力边界，最终通向物理 AGI**

最近和一些大佬交流，感觉我们的角度还挺有意思的，所以分享下我们的思考。

我们从六月份开始做多模态 coding 相关的任务。GPT-6 发布后，Computer Use Agent 一下子火了，也让我们之前摸着能力边界做的一些研究失去了意义。

但我们一直是从 coding 的角度、而不是 CUA 的角度来看这件事。说白了，CUA 关心的是 Agent 怎么去「用」现成的软件；我们更关心的是 Agent 怎么用代码把东西「造」出来，自己看结果，再自己改好。

我们主要从下面三个阶段来理解。

#### 1 - Visual as Feedback：有了视觉反馈，模型才能 loop 起来

视觉反馈和 perception 能力的提升，让模型可以真正 loop 起来。

相比于一般的 coding agent，多模态 coding agent 的关键就是有视觉反馈，这一点极大地扩展了 agent 的能力边界。网页、图表、PPT、3D/CAD、游戏……只要能跑出来、看得见，就能放进这个 loop 里。

其中，perception、grounding 以及 diff 这些原子多模态能力是基础：看得准、找得到、比得出差别。反馈够精准，coding loop 才能更好地跑起来。

当然，在这之前通过各种 workflow 也能带来 visual feedback；但在 agent 场景下，模型不只是做 VQA 了，它可以自主地去对比，并且对整个「多模态 repo」进行优化。

#### 2 - Agent Orchestrates Models：让 Agent 去调别的模型

Agent 去 orchestrate 各种模型（生成模型、action model 等），进一步扩展了能力边界，也提高了效率。

视觉反馈让 agent 拥有了极大的多模态任务空间。但如果 agent 只能自己看、自己做，不仅会有长上下文带来的幻觉，也可能需要极大量的计算；把其他模型当作工具来调，就能有效改善。

orchestration 既体现在输入，也体现在输出：

- **输入**：用更擅长的模型，从不同维度给 agent 提供观察，比如检测、分割、深度、重建；
- **输出**：调生成模型来做 mask 重绘、基于白模给出构图；也可以调 action model 来操控机械臂。

一句话：agent 负责想和写代码，专业的「看」和「做」交给更擅长的模型。

#### 3 - Bridging Digital World & Physical World：把 loop 带进物理世界

前两个阶段不断扩展着 coding agent 的能力边界，但都还在数字世界里。第三个阶段，我们想把这个 loop 带进物理世界。这也是我们仓库里现在最大、涨得最快的一块：664 项工作里有 318 项在这个阶段，光 2026 年下半年就新增了 200 项。

我们觉得大概有三件事在同时发生：

**一是用代码去动手（Digital → Physical）。** 从 Code as Policies 开始，大家就在用代码调感知和运动接口来控制机器人。最近一批 robot-use agent 更直接，让通用 coding agent 自己写 Python、调 ROS，看相机画面和力反馈，再改下一步动作。第一阶段的「看结果改代码」，到这里就变成了「看动作结果改策略」。PCB 布线、软体机器人设计、科学实验，也都开始用上了这套 loop。

**二是用代码把真实世界「搬」进仿真（Real → Sim）。** 拿一段真实视频，让 agent 把场景、物体、关节、物理参数写成能跑的仿真器。仿真器本身就是一个「多模态 repo」：能拿来和真实录像对比，也能改改条件再跑一遍。不过仿真到底像不像，是个大问题。所以我们在仓库里整理了一套检验层级：从「看起来像」，到「放着不动合理」「碰一下有反应」「动起来对」，最后到「在仿真里最好的策略，到真机上是不是也最好」。每一层拆穿一种「假仿真」。

**三是在仿真里练，再回到现实（Sim → Real）。** 有了能验证的环境，agent 就可以自己造数据，攒经验和 skills，先在数字孪生里把失败恢复练一遍，甚至只靠仿真里的成功轨迹给小模型做后训练，再把能力带回真机。

这三件事其实是同一个 loop：搭一个能验证的环境 → 在里面收集交互经验 → 让 agent 变强。代码能跑、能检查、能改、能组合，刚好可以把感知、生成、行动和仿真串起来。

#### 最后

三个阶段是一层层叠上去的：先看见自己造的东西，再学会调别的模型，最后在仿真和现实里动手、学习。我们相信，沿着「写代码 → 看结果 → 再改」这条路，agent 会一步步从屏幕走进真实世界，最终通向物理 AGI。

我们把相关的工作都整理在了 **Awesome Multimodal Agentic Coding** 里，目前 664 项（论文、工具、数据集、Demo），按三个阶段、19 个方向组织，中英日三语，会持续更新。欢迎 star、提 issue 推荐工作，也欢迎来找我们聊～

🔗 https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
