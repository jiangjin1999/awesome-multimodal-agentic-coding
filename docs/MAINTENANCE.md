# Maintaining the three-stage collection

[Contribution guide](../CONTRIBUTING.md) · [Collection](../README.md)

`data/works.yaml` and `data/site.yaml` are the canonical public sources. `scripts/build_readme.py` generates the English, Chinese, and Japanese root READMEs. Do not edit generated entries directly. The public layout identifier is `three-stages-v1`: 19 numbered sections across three stages, plus the Survey entry `SV`.

## Entry contract

| Field | Meaning |
|---|---|
| `id` | Stable, unique identity; arXiv IDs omit version suffixes. Official reports may use a non-arXiv ID. |
| `aliases` | Explicit alternative identities, such as a later arXiv ID for an existing report. Never create a second entry for the same work. |
| `title`, `date`, `url` | Official title, first-publication month (`YYYY.MM`, when known), and primary source. |
| `sources` | All retained original paper, project, code, dataset, and demo URLs, including `url`. |
| `type` | `paper`, `resource`, `demo`, or `reading`; count papers by this field, not by section. |
| `scope` | `core`, `adjacent`, `resource`, `survey`, `demo`, or `reading`. A Survey is a paper with Survey scope; a resource or application does not become a paper because it has Adjacent scope. |
| `section`, `sub` | One canonical location. Use the section's allowed subgroups from `site.yaml`; this position is independent of scope. |
| `tldr.en`, `tldr.zh`, `tldr.ja` | Concise, equivalent summaries with the same limitations and attribution. No empty translations or placeholders. |
| `verification` | Retained English and Chinese evidence for Core entries: construction, execution, multimodal observation, subsequent revision, and what is checked. |
| `see_also` | Other relevant section IDs linking back to this record. Add only for a supported contribution. |

A section in `site.yaml` may carry an optional `guide` (one Markdown block per language) rendered under its heading; section 3.3 uses it for a fidelity-level overview table that links to `stage3/simulator-evaluation.md`. Keep its work links in sync when entries move.

The generator names supporting links by destination type using the localized `source_labels` in `data/site.yaml`. Record URL exceptions in `source_kind_overrides` when the destination cannot be inferred from its address. Stage 3 reading entries use the same labels. Keep all source URLs in the catalog. The generated entry displays one entrance per paper, using the linked title first. Record verified copies across publishers in `paper_url_aliases` and name direct section links in `source_kind_overrides`.

Stage 1 covers visual feedback in artifact construction; Stage 2 covers models used as tools; Stage 3 covers bridging digital and physical worlds. Method, evaluation, data, training, and resource roles remain distinct within these perspectives. A dataset release, a data-construction method, and experimental data are different contributions.

Scope identities stay in canonical data and metadata comments for maintenance. Public entries display the title, source links, and summary without scope badges. Every generated entry has a `mmac-record` comment with `id`, `scope`, `primary`, `stage`, and `type`, and a stable `paper-…` anchor. `site.yaml` also retains older anchors through `anchor_aliases`. Update local references to current anchors while keeping published aliases working. Preserve source URLs when reorganizing entries; a primary link alone is insufficient if earlier entries included supporting code or data.

## Validation and publication

Run the commands in the [contribution guide](../CONTRIBUTING.md#submit-a-pull-request). `--check` requires all translations, exact generated output, valid identities and scopes, and existing local files and fragments across the documentation. The GitHub Actions workflow runs the public checks on pull requests and pushes to main. The regression suite covers missing translations, lost evidence, source/ID mismatches, duplicate identities, and old cross-file links. It does not replace reading the primary sources or checking the claims in a summary.

Before publishing, compare the canonical ID/scope/source inventory with the previous main, inspect the rendered READMEs at mobile and desktop widths, and review the diff. Preserve release announcements, version information, and CITATION unless a maintainer explicitly requests a release change. Update the maintenance date only for real content changes.

The research workspace has additional private discovery, preservation, and digest checks. Its 12 discovery directions and method/evaluation/data searches are search axes, not public section numbers. New daily records use `routing.primary`, `routing.stage`, optional `routing.discovery_directions`, and evidence-bearing `routing.related` references with a saved `three-stages-v1` repository map. Historical `directions-v4` digests keep their original maps and rendering; a layout migration does not authorize resending a delivered email.
