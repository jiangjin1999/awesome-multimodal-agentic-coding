# A guide to multimodal agentic coding

[Back to the collection](../README.md) · [简体中文](./READING_GUIDE.zh-CN.md)

An agent writes code, runs it, observes the result, and uses that observation to choose its next edit or action. This guide connects examples across interfaces, CAD, 3D, and games through that shared loop.

## Five starting points

These examples illustrate different mechanisms; they are not a ranking.

| Start with | Follow the feedback | What it helps you understand |
|---|---|---|
| [Programming with Pixels](https://programmingwithpixels.com/) — UI Development demo | The agent edits HTML inside an IDE, looks at its live preview beside the reference image, and edits again. | How screen observations can guide implementation inside a general computer-use environment. |
| [CAD-Assistant](https://cadassistant.github.io/) | FreeCAD actions change a model; the evolving CAD state informs later actions. | Why the environment needs to expose geometry and useful views alongside code execution. |
| [Procedura](https://spatiaos.github.io/projects/procedura/) | A procedural assembly grows part by part; rendered views and a separate visual critic guide revisions, alongside compile and mate checks. | How the program representation and acceptance checks shape the repair loop. |
| [Play2Code](https://continual-game-generation.vercel.app/) | A GUI agent plays a generated HTML game and returns a report and fix list to the coding agent. | Why interaction trajectories reveal failures that a still image can miss. |
| [Text-to-CAD Evaluation with CADTests](https://arxiv.org/html/2605.07807v1) — §6 and Appendix C | Compare four-view visual ReAct with test-based code refinement and geometric logs. | Why the choice of feedback needs an experiment: added visual feedback did not improve performance in this study. |

## Choose a reading path

- **Understand the field:** watch the PwP UI demo, explore CAD-Assistant and Play2Code, then use the [topic map](../README.md#topic-map) to find your artifact type.
- **Build a system:** choose an [execution engine](../README.md#execution-and-rendering-engines), inspect its [skills and tool bridges](../README.md#skills-and-tool-bridges), and compare a method with a similar artifact and observation channel. A tool's screenshot capability alone does not establish that an agent uses it to improve code.
- **Design a research study:** compare the feedback paths in Procedura and CADTests, then read the relevant [benchmarks and methods](../README.md#paper-and-project-list) and [research frontiers](../README.md#research-frontiers).

## Compare the loop, not just the final artifact

Use these five questions when reading a paper or designing an experiment.

| Question | Record | Why it matters |
|---|---|---|
| What can be edited? | HTML/CSS, a CAD program, a scene graph, game code, slide objects, or a robot policy. | The representation determines what can be changed locally and what must be rebuilt. |
| What is actually observed? | A rendered view, a video segment, an interaction trace, spatial measurements, or a rollout. | The feedback must expose the failure you want to fix. |
| Who sees it, and when? | The coding model, a separate critic, a human, or a final evaluator; before or after execution. | A visual critic can relay a text diagnosis to a coding model; a final evaluation alone does not guide a later edit. |
| What changes next? | A code patch, camera view, interaction, parameter, or another test. | A concrete next action connects observation to improvement. |
| What establishes progress? | Visual fidelity, functionality, geometry, physical behavior, content accuracy, cost, or regression checks. | A visually plausible artifact can still fail its intended task. |

For a compact comparison note, write:

```text
Task → editable representation → runtime → observation → recipient → next action
Acceptance check / stopping rule:
Final evaluation:
Cost and failure cases:
```

## Three lessons to carry into an experiment

**Match the check to the requirement.** A render can expose missing objects or poor layout; a CAD kernel can test dimensions and topology; playing a game can expose a broken win condition. CADTests provides a concrete comparison between visual and test-based feedback ([§6](https://arxiv.org/html/2605.07807v1#S6)).

**Inspect the whole system.** A separate visual critic may observe the artifact and send a diagnosis to a text-based coder. Procedura makes this division explicit ([paper, §3.4](https://arxiv.org/html/2608.26238v1#S3.SS4)).

**Measure the value of another round.** Compare revisions with a matched one-shot or execution-only baseline, account for extra tokens and runtime, and examine regressions. Treat an unsuccessful refinement result as useful evidence about the feedback design.

## Find the right part of the collection

**Core** works document code, execution, multimodal observation, and a subsequent action within a trajectory or a named benchmark configuration. **Adjacent** works contribute related generation, evaluation, or interaction foundations. **Resources** provide tools, skills, engines, and demos. These describe different roles, not a quality ranking.

For any benchmark, check which evaluated configuration uses feedback. For any demo, distinguish the behavior shown from a measured benchmark result.

Have a useful example or a correction? [Suggest it here](https://github.com/jiangjin1999/awesome-multimodal-agentic-coding/issues/new/choose). Contributions in English or Chinese are welcome.
