# 参与贡献

[English](./CONTRIBUTING.md) · [日本語](./CONTRIBUTING.ja.md) · [返回合集](./README.zh-CN.md)

欢迎通过 [Issue 表单](https://github.com/jiangjin1999/awesome-multimodal-agentic-coding/issues/new/choose)推荐论文、工具、Demo 或更正。中英日文提交均可；只贡献一种语言也可以，维护者会协助翻译与定位。

## 推荐一项工作

请提供官方标题、原作者或项目链接，以及一句贡献说明。如有论文、源码或 Demo，请一并附上。对于利用反馈的系统，请说明**执行后 Agent 观察到了什么，这如何改变下一次代码或工具动作**，并附论文章节、图号、代码位置或时间戳。证据尚不清楚时直接注明。

- **Core：** 代码或程序化表示构建产物；同一轨迹中，执行后的多模态观测改变后续代码或工具动作。基准请指出使用这一闭环的配置。
- **Adjacent：** 相关的生成、评估、交互、模型编排或具身研究，采用不同的反馈设置。
- **Resource：** 可复用的生成、感知、预测、动作或验证模型，以及 Skill、工具桥、引擎。请说明输入、输出、具体用途及代码或权重的可用性；资源本身无需实现 Agent 或反馈闭环。
- **Survey、Demo、Reading：** 综述、署名演示和观点阅读保留各自角色。资源、Demo 和阅读材料不计作研究论文。

这些是范围身份，不是排名。收录与作者是否分享仓库或点 star 无关。请区分仿真、真实硬件、生成视频，以及最终评估与 Agent 在过程中收到的反馈。

## 提交 Pull Request

三阶段分别组织**视觉反馈**、**模型作为工具**与**连接数字与物理世界**。每项工作选择一个主入口，其他相关位置链接到稳定条目，避免重复完整书目。阶段位置不决定 Core 或 Adjacent 身份。

条目编辑 [data/works.yaml](./data/works.yaml)，共享导航与文案编辑 [data/site.yaml](./data/site.yaml)。保留规范 ID、首次发布日期、来源 URL、已有范围身份及兼容锚点。每种语言写一句简洁摘要，Core 工作还须保留中英文验证证据。官方报告可使用稳定的非 arXiv ID，后续论文 ID 作为明确别名记录。

三个根目录 README 均由数据生成。在公开仓库中运行：

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
```

若只能提供一种语言，请在草稿 PR 说明缺口；发布前需补齐三语摘要，英文回退不算完成日文翻译。字段与校验见[维护约定](./docs/MAINTENANCE.md)。

日常条目更新不新增发布公告，也不修改 News、版本号或 CITATION。欢迎小幅更正；新增分类或大范围重组前，请先开 Issue 讨论。
