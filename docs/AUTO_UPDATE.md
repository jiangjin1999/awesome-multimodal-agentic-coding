# Automated update rules

[Maintenance contract](./MAINTENANCE.md) · [Contribution guide](../CONTRIBUTING.md) · [Collection](../README.md)

These rules are for the agent that keeps the collection current. They cover what to search, how to decide, what to write, what to record and what to leave alone. Entry fields and checks are defined in the [maintenance contract](./MAINTENANCE.md), and scope identities in the [contribution guide](../CONTRIBUTING.md#suggest-a-work). If those files conflict with this one, they take precedence. This file governs the update run itself.

## 0. Start here

You need no context beyond this repository.

```sh
python3 -m pip install -r scripts/requirements.txt
python3 scripts/build_readme.py --check
```

Read these files, in this order:

1. this file;
2. the [contribution guide](../CONTRIBUTING.md#suggest-a-work), for scope;
3. the [maintenance contract](./MAINTENANCE.md), for fields;
4. `data/triage.yaml`, the decision log. Its `pending` candidates are your queue.

`data/works.yaml` is the catalog. Never edit the three root READMEs by hand. They are generated.

## 1. One run, in order

1. Start from the latest `main`.
2. Work through the `pending` candidates in `data/triage.yaml`, oldest first.
3. Sweep for new candidates over the window in §2.
4. Remove duplicates of existing entries (§3).
5. Read each candidate and decide (§4).
6. Write or update entries (§5).
7. Record the run and every decision in `data/triage.yaml` (§7).
8. Rebuild and check (§6). Commit only when every check passes.

If you cannot finish the queue, leave the rest as `pending`. A run with no new entries still commits its log update.

## 2. Discovery

**Window.** Cover everything announced since the previous run's date in `data/triage.yaml`, and re-scan the trailing 14 days. Works are cross-listed late, revised under new titles, or announced on a different day from the one their ID suggests.

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
- **Citation chasing.** For each work added in this run, read its references and check every work from the last six months against the catalog. A missing work becomes a candidate only if its title or abstract could fit a scope identity. Cited VLA models, VLA evaluations and general RL methods usually do not.
- **Leaderboards and benchmarks.** Check the submissions to benchmarks that are already in the catalog, such as RoboLab-120 and RoboDojo.
- Official lab blogs and project pages that announce agent, robotics or generation releases. A blog post that only announces a release is not added (see the contribution guide).

## 3. Duplicates

Before reading a candidate, search `data/works.yaml` and `data/triage.yaml` for:

- the arXiv ID without its version suffix, including every `aliases` entry;
- the title, ignoring case and punctuation;
- the project page and code repository URLs. These catch works that were renamed, for example PhysLadder, which became LLM4Robot-Bench, and PROBE, which became MG-VQA.

If the work is already in the catalog, update the existing entry: add new sources, an alias or a corrected title. Never create a second entry for the same work. If it is already in the log, continue from its recorded decision instead of starting over.

## 4. Reading and deciding

- Read the full text (arXiv HTML, or the PDF), not only the abstract. For every number you will write, note its section, table or figure.
- Assign one scope identity from the contribution guide. Ask:
  1. Does an agent or model produce code or another programmatic representation, and run it?
  2. After execution, does a multimodal observation (image, render, video, sensor reading, physical outcome) change a later code or tool action in the same trajectory?

  If both are yes, the work is Core. If it is related work with a different feedback setup, it is Adjacent. A reusable model, tool, skill or engine is a Resource.
- **Follow precedent.** Find the two or three closest existing entries in the same subgroup, and match their section, `sub` and scope unless the paper gives a reason not to. Record those entries as `precedent`. In 3.1 and 3.5, the catalog marks agents that write programs or Python cells as Core, and agents that only issue tool calls, such as poses, motion commands or skill calls, as Adjacent. Examples are Agent as Policy (Core) and Robo-Harness K1, Guava, TinyAstral and ZAP (Adjacent).
- **Exclude** a work only when no scope identity fits, and record the reason. Two examples: code generation evaluated only on text output with no visual or physical observation, and robot learning with no agent, code, tool use or reusable model contribution.
- **Defer** a work when the evidence cannot be read yet (no full text, broken links). Defer it rather than guessing, record what is missing, and re-check it in the next run.

## 5. Writing entries

- **Placement.** One `section` and one allowed `sub` from `data/site.yaml`. Use `see_also` only where the paper supports the link.
- **Date.** The month of the first version (`v1`), not of the latest revision.
- **`tldr`.** One sentence per language saying what the work does. Match the length of the neighbouring entries in the same subgroup. Recent 3.5 entries run about 6–12 English words, and other subgroups stay under about 30. Results and trial counts go in `verification`. The Chinese and Japanese versions carry the same meaning and the same limitations as the English one, and must not be word-for-word machine translations.
- **`verification`.** Use `·` to separate the evidence: the base model, the training or evaluation scale, the observation the agent receives, the headline results with their baselines, and trial counts. Separate simulation from hardware results, and name what is only qualitative. Required in English and Chinese for Core, and recommended for every paper.
- **`setup`.** Stage 3 only. Follow the engine and robot naming rules in the maintenance contract, such as RoboLab → `Isaac Lab` and a make-only robot → `Franka`.
- **`sources`.** The arXiv abstract, then the work's own project page, code, weights, dataset and demo. Open each code link and confirm it holds implementation files. Do not add third-party tools that the project page merely cites, such as a simulator or a training framework.

## 6. Build, check, commit

```sh
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`--check` also validates `data/triage.yaml` against the catalog:

- a candidate marked `added` or `updated` must exist in `data/works.yaml`;
- a candidate marked `pending`, `excluded` or `deferred` must not exist there;
- `excluded` and `deferred` need a `reason`;
- every `precedent` must be a catalog ID.

A run may change:

- `data/works.yaml`, `data/triage.yaml`, and the generated READMEs and figures, including `robotics/` and `assets/robotics/`;
- `updated` in `data/site.yaml`, set to the run date, but only when an entry was added or changed;
- `source_kind_overrides` and `paper_url_aliases` in `data/site.yaml`, when a new source needs them.

A run must not change:

- News, the version or `CITATION.cff`;
- the section structure;
- the hand-maintained guides: `stage3/README*.md` (which have their own literature cutoff), `stage3/simulator-evaluation*.md`, `eval_ladder` and `engine_map`.

New works that belong in those guides are flagged in the run's `note` for the maintainer.

A Stage 3 or 2.6 entry is published twice: in this repository and in the robotics repository, which is generated from the same data. The build regenerates both, so commit `robotics/` and `assets/robotics/` with the data; there is nothing to edit by hand. After the commit reaches `main`, the robotics repository syncs within an hour.

Make one commit per run. Name the topics it adds, in the existing style, for example `Add embodied harness and simulator fidelity research`. Commit on the branch your environment gives you. If that branch is not `main`, open a pull request.

## 7. Decision log

`data/triage.yaml` is the record of every decision. Its header comment documents the fields.

- **One `runs` row per run.** It gives the date, the trigger (`sweep`, `report`, `citations` or `issue`), and what was covered: the window, the listings and the queries. Put anything the maintainer should review in `note`.
- **One `candidates` row per work.** Each row has `found`, `via` and a `decision`:

  | Decision | Meaning and required fields |
  |---|---|
  | `pending` | Queued, not yet read. |
  | `added` or `updated` | Give `decided` and `precedent`, and `entry` if the catalog ID differs from `id`. |
  | `excluded` | Give `decided` and a `reason`. |
  | `deferred` | Give `decided` and a `reason` saying what is missing. |

- Update a candidate's row when its decision changes. Never delete rows, so that a later question can still be answered.

**Answering "why is X not in the collection?"**

1. Search `data/works.yaml` by ID, alias, title and URLs (§3). The work may be there under another name.
2. Search `data/triage.yaml`. The `reason` or `pending` status is the answer.
3. If it is in neither, it was never found. Log a `report` run, decide the work, and add a row to the known misses below.

## 8. Known misses

When a missed work is reported, add it here. Record the gap that let it through and the rule above that now catches it.

| Work | Reported | Listing | Gap → rule |
|---|---|---|---|
| [ZAP (2610.35817)](../README.md#paper-2610-35817), v1 2026-10-26 | 2026-11-15 | `cs.RO` primary | No decision was recorded, so the cause is unknown. → Read every title in `cs.RO` (§2), chase citations (§2), and log every decision (§7). The citation chase of ZAP queued 22 more candidates. |
| [ACE-CaP-0 (2611.16872)](../README.md#paper-2611-16872), v1 2026-11-12 | 2026-11-18 | `cs.RO` primary, announced 2026-11-13 | The backfill retrieved and screened the paper, but the lead did not reach triage. → When resuming a partial sweep, reconcile saved `cs.RO` title leads with the catalog and triage before advancing the listing checkpoint. Keep plausible leads as `pending` even when a keyword ranking puts them below the current review batch (§2, §7). |
