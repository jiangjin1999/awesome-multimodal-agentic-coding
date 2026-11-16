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

可以直接用于公众号、知乎或长帖。下面的文字也做成了 4 张图（3:4，2160 × 2880），文字与这里一致，只加了重点标注：

| 顺序 | 文件 | 内容 |
|---|---|---|
| 1 | [`post-1-intro.png`](images/post-1-intro.png) | 开头与三个阶段 |
| 2 | [`post-2-visual-feedback.png`](images/post-2-visual-feedback.png) | 1 - Visual as Feedback |
| 3 | [`post-3-orchestrate-models.png`](images/post-3-orchestrate-models.png) | 2 - Agent Orchestrates Models，以及通向第三阶段的过渡 |
| 4 | [`post-4-digital-physical.png`](images/post-4-digital-physical.png) | 3 - Bridging Digital World & Physical World，以及最后 |

### 多模态视角下的 Coding｜Awesome Multimodal Agentic Coding

**扩展 Agent 能力边界，最终通向物理 AGI**

最近和一些同学交流，感觉我们的角度还挺有意思的，所以分享下我们的思考。

我们从六月份开始做多模态 agentic coding 相关的任务。GPT-6 发布后，Computer Use Agent 一下子火了，也让我们之前摸着能力边界做的一些研究显得不那么前沿了（一个人做也确实比较慢）。

但我们一直是从 coding 的角度、而不是 CUA 的角度来看这件事。最近 Robot Use Agent 也越来越多：让 Agent 直接写代码控制机器人，再加上 Real2Sim2Real，这些都是多模态 coding 这条线往物理世界的延伸。其实从 coding 的角度来看，这个发展是很自然的。

我们主要从下面三个阶段来理解：

1️⃣ Visual as Feedback：有了视觉反馈，模型才能真正 loop 起来

2️⃣ Agent Orchestrates Models：让 Agent 去调生成、感知、动作模型，能力边界进一步扩展

3️⃣ Bridging Digital & Physical：用代码搭仿真、控机器人，从屏幕走到真实世界

#### 1 - Visual as Feedback：有了视觉反馈，模型才能 loop 起来

视觉反馈和 perception 能力的提升，让模型可以真正 loop 起来。

相比于一般的 coding agent，多模态 coding agent 的关键就是有视觉反馈，这一点极大地扩展了 agent 的能力边界。网页、图表、PPT、3D/CAD、游戏……只要能跑出来、看得见，就能放进这个 loop 里。

其中，perception、grounding 以及 diff 这些原子多模态能力是基础：看得准、找得到、比得出差别。反馈够精准，coding loop 才能更好地跑起来。

当然，在这之前通过各种 workflow 也能带来 visual feedback；但在 agent 场景下，模型不只是做 VQA 了，它可以自主地去对比，并且对整个「多模态 repo」进行优化。

#### 2 - Agent Orchestrates Models：让 Agent 去调别的模型

Agent 去 orchestrate 各种模型（其他 VLM、生成模型、action model 等），进一步扩展了能力边界，也提高了效率。

视觉反馈让 agent 拥有了极大的多模态任务空间。但如果 agent 只能自己看、自己做，不仅会有长上下文带来的幻觉，也可能需要极大量的计算；把其他模型当作工具来调，就能有效改善效率和效果。

orchestration 既体现在输入，也体现在输出：

- **输入**：用更擅长的模型，从不同维度给 agent 提供观察，比如检测、分割、深度、重建；
- **输出**：调生成模型来做 mask 重绘、基于白模给出构图；也可以调 action model 来操控机械臂。

上面两个阶段为第三个阶段打下了扎实的基础：视觉反馈让 agent 能看清每一步的结果，把模型当工具来调，又让它能借用感知、生成和动作模型的能力。走进物理世界，靠的正是这两样。

#### 3 - Bridging Digital World & Physical World：把 loop 带进物理世界

前两个阶段不断扩展着 coding agent 的能力边界，但都还在 digital world 里。很自然地，我们想把这个 loop 带进 physical world。这也是我们仓库里现在最大、涨得最快的一块。

Agentic Loop 是一切想法的开始。coding控制的就是一台机器人，「看结果改代码」变成了「看动作结果改策略」。最近的 Robot Use Agent 做的正是这件事：不用专门训练一个策略，只给现成的 coding agent 一个终端和机器人的感知、运动接口，它就能自己写 Python 让机器人干活，看相机画面和执行结果，失败了就改代码再试。但真机上的 loop 又慢又贵，于是很自然地想先把真实世界「搬」进代码里，而前两个阶段的发展为 Real2Sim 提供了可能；再在仿真里把 loop 转得又快又多，造数据、攒经验，最后把能力带回真机。这一切又是基模的故事了

#### 最后

三个阶段是层层叠上去的。我们相信，沿着「写代码 → 看结果 → 再改」这条路，agent 会一步步从屏幕走向物理世界。

## 四、评论（第一条评论）

```text
相关工作都整理在了 Awesome Multimodal Agentic Coding 里，其中 Stage 3（Robot Use Agent）的内容和结构是我们最近主要的思考，未来也还有很多可做的空间。仓库会持续更新，欢迎 star、提 issue 推荐工作，也欢迎来找我们聊～

🔗 https://github.com/jiangjin1999/awesome-multimodal-agentic-coding
```
