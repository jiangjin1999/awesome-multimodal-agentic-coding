Describe the addition or correction, with an original source link.
请简述新增或更正的内容，并附上原始来源。

For a feedback-driven system: what is executed, what does the agent observe, and what changes next?
对于反馈驱动系统：执行了什么、Agent 观察到什么、下一步如何改变？

If translation help is needed, say which language is ready.
如需翻译帮助，请注明已完成的语言版本。

For catalog changes, edit `data/works.yaml` (and shared text in `data/site.yaml`), then regenerate all three READMEs. Preserve IDs, scope, source URLs, and old anchors. Publication checks require complete English, Chinese, and Japanese summaries.
条目修改请编辑 YAML 后生成三语 README，保留 ID、范围身份、来源和旧锚点；发布校验要求中英日摘要完整。

Validation / 校验：`python3 scripts/build_readme.py --check` and `python3 -m unittest discover -s scripts -p 'test_*.py'`.
