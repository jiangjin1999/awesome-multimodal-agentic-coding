# Automated update rules

[Maintenance contract](./MAINTENANCE.md) · [Contribution guide](../CONTRIBUTING.md) · [Collection](../README.md)

These rules are for the agent that keeps the collection current. They cover what to search, how to decide, what to write and what to leave alone. Entry fields and checks are defined in the [maintenance contract](./MAINTENANCE.md), and scope identities in the [contribution guide](../CONTRIBUTING.md#suggest-a-work). If those files conflict with this one, they take precedence. This file governs the update run itself.

## 1. One run, in order

1. Start from the latest `main`.
2. Sweep for candidates over the window in §2.
3. Remove duplicates of existing entries (§3).
4. Read each remaining candidate and record a decision (§4).
5. Write or update entries (§5).
6. Rebuild and check (§6). Commit only when every check passes.
7. Write the run note (§7).

A run with no qualifying works makes no commit, but it still writes the run note.

## 2. Discovery

**Window.** Cover everything announced since the previous run, and re-scan the trailing 14 days. Works are cross-listed late, revised under new titles, or announced on a different day from the one their ID suggests.

**arXiv listings.** Include cross-lists in every category.

| Category | How |
|---|---|
| `cs.RO` | Read every title in the listing. Stage 3 depends on it, and keyword searches miss papers whose titles say "policy", "harness" or a model name instead of "agent". |
| `cs.CV`, `cs.GR`, `cs.AI`, `cs.LG`, `cs.CL`, `cs.SE`, `cs.HC`, `cs.MM` | Search titles and abstracts with the queries below. |

**Queries by stage.** Combine terms within a row. A hit is only a candidate.

| Stage | Query terms |
|---|---|
| 1 Visual feedback | code + render / screenshot / visual feedback / self-correction; webpage, UI, GUI, SVG, TikZ, chart-to-code, slides, poster, document, CAD, Blender, 3D program, shader, game generation; visual critic or judge for generated code |
| 2 Models as tools | agent or code calling image, video, 3D or world generation models; perception or segmentation models as tools; VLA or action model as a callable tool |
| 3 Digital–physical | agent, harness, tool calling or code-as-policy with a robot; a frontier model name together with robot or manipulation; post-training, SFT, RL or GRPO of robot agents; simulation, scene or asset generation for robots; real-to-sim, digital twin and simulator fidelity; robot agent benchmarks; lab automation and fabrication agents |

**Other sources, every run.**

- Open issues created from the [suggestion form](../.github/ISSUE_TEMPLATE/suggest-work.yml).
- **Citation chasing.** For each work added in this run, read its related-work section. Check every cited work from the last six months against the catalog, and treat each one missing from it as a candidate.
- **Leaderboards and benchmarks.** Check the submissions to benchmarks that are already in the catalog, such as RoboLab-120.
- Official lab blogs and project pages that announce agent, robotics or generation releases. A blog post that only announces a release is not added (see the contribution guide).

## 3. Duplicates

Before reading a candidate, search `data/works.yaml` for:

- the arXiv ID without its version suffix, including every `aliases` entry;
- the title, ignoring case and punctuation;
- the project page and code repository URLs, which catch works that were renamed (for example, PhysLadder became LLM4Robot-Bench).

If the work is already there, update the existing entry: add new sources, an alias or a corrected title. Never create a second entry for the same work.

## 4. Reading and deciding

- Read the full text (arXiv HTML, or the PDF), not only the abstract. For every number you will write, note its section, table or figure.
- Assign one scope identity from the contribution guide. Ask:
  1. Does an agent or model produce code or another programmatic representation, and run it?
  2. After execution, does a multimodal observation (image, render, video, sensor reading, physical outcome) change a later code or tool action in the same trajectory?

  If both are yes, the work is Core. If it is related work with a different feedback setup, it is Adjacent. A reusable model, tool, skill or engine is a Resource.
- Follow precedent. Find the two or three closest existing entries in the same subgroup, and match their section, `sub` and scope unless the paper gives a reason not to. Name those entries in the run note. For example, a small model trained to issue pose tool calls without writing code is Adjacent in 3.5 `post-training`, like Guava, TinyAstral and ZAP.
- Exclude a work only when no scope identity fits, and write the reason down. Two examples: code generation evaluated only on text output with no visual or physical observation, and robot learning with no agent, code, tool use or reusable model contribution.
- Defer a work when the evidence cannot be read yet (no full text, broken links). Defer it rather than guessing, and re-check it in the next run.

## 5. Writing entries

- **Placement.** One `section` and one allowed `sub` from `data/site.yaml`. Use `see_also` only where the paper supports the link.
- **Date.** The month of the first version (`v1`), not of the latest revision.
- **`tldr`.** One sentence per language saying what the work does and how. Keep it under about 30 English words. Results and trial counts go in `verification`. The Chinese and Japanese versions carry the same meaning and the same limitations as the English one, and must not be word-for-word machine translations.
- **`verification`.** Use `·` to separate the evidence: the base model, the training or evaluation scale, the observation the agent receives, the headline results with their baselines, and trial counts. Separate simulation from hardware results, and name what is only qualitative. Required in English and Chinese for Core, and recommended for every paper.
- **`setup`.** Stage 3 only. Follow the engine and robot naming rules in the maintenance contract, such as RoboLab → `Isaac Lab` and a make-only robot → `Franka`.
- **`sources`.** The arXiv abstract, then the work's own project page, code, weights, dataset and demo. Open each code link and confirm it holds implementation files. Do not add third-party tools that the project page merely cites, such as a simulator or a training framework.

## 6. Build, check, commit

```sh
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
```

A run may change:

- `data/works.yaml`, and the generated READMEs and figures;
- `updated` in `data/site.yaml`, set to the run date, but only when an entry was added or changed;
- `source_kind_overrides` and `paper_url_aliases` in `data/site.yaml`, when a new source needs them.

A run must not change:

- News, the version or `CITATION.cff`;
- the section structure;
- the hand-maintained guides: `stage3/README*.md` (which have their own literature cutoff), `stage3/simulator-evaluation*.md`, `eval_ladder` and `engine_map`.

New works that belong in those guides go in the run note for the maintainer.

Make one commit per run. Name the topics it adds, in the existing style, for example `Add embodied harness and simulator fidelity research`.

## 7. Run note

Every run leaves a note in the research workspace's daily record. It lists:

- the window covered and the listings and queries used;
- each candidate and its decision: added, updated, excluded (with the reason) or deferred (with what is missing);
- the precedent entries used for each placement;
- works that belong in the hand-maintained guides.

When the maintainer asks why a work is not in the collection, this note is the answer.

## 8. Known misses

When a missed work is reported, add it here. Record the gap that let it through and the rule above that now catches it.

| Work | Reported | Listing | Gap → rule |
|---|---|---|---|
| [ZAP (2610.35817)](../README.md#paper-2610-35817), v1 2026-10-26 | 2026-11-15 | `cs.RO` primary | No decision was recorded, so the cause is unknown. → Read every title in `cs.RO` (§2), chase citations (§2), and write run notes (§7). |
