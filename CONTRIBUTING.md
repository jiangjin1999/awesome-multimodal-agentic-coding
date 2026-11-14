# Contributing

[简体中文](./CONTRIBUTING.zh-CN.md) · [日本語](./CONTRIBUTING.ja.md) · [Back to the collection](./README.md)

Suggest a paper, tool, demo, or correction through the [issue forms](https://github.com/jiangjin1999/awesome-multimodal-agentic-coding/issues/new/choose). Submissions in English, Chinese, or Japanese are welcome. You may contribute in one language; maintainers can help with translation and placement.

## Suggest a work

Provide the official title, an original author or project link, and a sentence explaining the contribution. Include the paper, source repository, or demo when available. For a feedback-driven system, explain **what the agent observes after execution and how this changes its next code or tool action**, with a paper section, figure, code location, or timestamp. If evidence is unavailable, say so.

- **Core:** code or a programmatic representation constructs an artifact, and a post-execution multimodal observation changes a later code or tool action in the same trajectory. For a benchmark, identify the configuration using this loop.
- **Adjacent:** related generation, evaluation, interaction, model orchestration, or embodied work with a different feedback setup.
- **Resource:** a reusable generation, perception, prediction, action, or verification model; a skill, tool bridge, or engine. Describe inputs, outputs, practical use, and available code or weights. The resource need not implement an agent or feedback loop itself.
- **Survey, Demo, Reading:** overviews, attributed demonstrations, and commentary retain their own roles. Resources, demos, and readings do not count as research papers.

These are scope identities, not rankings. Inclusion is independent of whether authors share or star this repository. Distinguish simulation, real hardware, generated video, and final evaluation from feedback received by the agent.

## Submit a pull request

The three stages organize **visual feedback**, **models as tools**, and **bridging digital and physical worlds**. Choose one main section for a work; link other relevant sections to its stable entry rather than repeating the bibliography. Stage placement does not determine Core or Adjacent status.

Edit [data/works.yaml](./data/works.yaml) for entries and [data/site.yaml](./data/site.yaml) for shared navigation and text. Preserve canonical IDs, first-publication dates, source URLs, existing scope, and compatibility anchors. Keep a concise summary in each language and retain English/Chinese verification evidence for Core works. An official report can use a stable non-arXiv ID; record a later arXiv ID as an explicit alias.

The three root READMEs are generated. From the public repository, run:

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
```

If you can supply only one translation, describe the gap in your draft PR. Publication requires all three summaries; an English fallback is not a completed Japanese translation. See the [maintenance contract](./docs/MAINTENANCE.md) for fields and checks.

Do not add release announcements or change News, the version, or CITATION as part of a routine entry update. Small corrections are welcome; discuss a new category or major reorganization in an issue first.
