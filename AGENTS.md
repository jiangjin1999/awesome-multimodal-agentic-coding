# Agent guide

This repository is a curated research map. The three root READMEs are generated from data files.

- **Finding, adding or correcting works:** follow [docs/AUTO_UPDATE.md](docs/AUTO_UPDATE.md). Start at its §0. The queue of works still to read is the `pending` candidates in `data/triage.yaml`.
- **Entry fields and checks:** [docs/MAINTENANCE.md](docs/MAINTENANCE.md). Scope identities are defined in [CONTRIBUTING.md](CONTRIBUTING.md).
- **Do not edit the generated READMEs by hand:** `README.md`, `README.zh-CN.md` and `README.ja.md` come from `data/works.yaml` and `data/site.yaml`. Edit those files, then run `python3 scripts/build_readme.py`.
- **Before committing, run:**

  ```sh
  python3 scripts/build_readme.py --check
  python3 -m unittest discover -s scripts -p 'test_*.py'
  ```
