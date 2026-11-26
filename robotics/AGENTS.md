# Agent guide

This repository is the robotics branch of https://github.com/jiangjin1999/awesome-multimodal-agentic-coding. Its READMEs, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md` and `LICENSE` are generated upstream by `scripts/build_readme.py` into the `robotics/` folder and copied here by `.github/workflows/sync.yml`.

- **Do not edit those files here:** the next sync overwrites them. Change `data/works.yaml`, or the `robotics` block in `data/site.yaml`, upstream, run `python3 scripts/build_readme.py` there, and commit upstream.
- **Only `.github/workflows/sync.yml` is maintained in this repository.** It runs every hour and on demand, copies `robotics/` from upstream `main`, and pins the footer's `upstream@main` link to the upstream commit it copied.
