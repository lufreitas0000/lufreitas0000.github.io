# Current sprint — personal-website / M3.4

Owning milestone: M3.4 (see [HORIZON.md](HORIZON.md))
Machine state: [PROJECT_STATE.yaml](PROJECT_STATE.yaml) (authoritative for task statuses)

## Scientific / engineering objective
Validate paired Kitaev solver campaigns (`doc/KITAEV_MF_SOLVER_DATA_CONTRACT.md`) and resolve finite-torus parity/resolvent assumptions for `KM-01` before publishing any interpolation curves, trajectory figures, or companion series notes.

## Implementation strategy
Preserve authoritative [PROJECT_STATE.yaml](PROJECT_STATE.yaml) (`waiting-on-scientific-specification`), [doc/MILESTONE_ROADMAP.md](doc/MILESTONE_ROADMAP.md), and Rule 03 quarantine (`visible: false` until primary-source review and `make verify` pass).

## Scope and non-goals
Owns static web engine (`src/web_engine/`), page templates (`site/`), solver data contracts/fixtures, and verification suite (`make verify`). Does not invent physical parameter units, solver acceptance thresholds, or unverified curves.

## Current bounded tasks (`M3.4`)
- Owner specification: define `h` units, precommitted `h` grid, initial-state ensemble, seeds, target observable, residual definition, stopping criteria, and numerical acceptance tolerances.
- Verification & audit: independently rerun and audit Kitaev solver campaigns with branch labels and held-out errors against the paired-data validator.
- Series preparation: resolve exact-perturbation parity/resolvent assumptions for `KM-01` (*Exact Kitaev spectra, physical parity, and perturbative resolvents*).

## Independent acceptance and reproduction
- `PATH="$PWD/.venv/bin:$PATH" make verify && python3 /home/lu/Projects/scripts/uow.py check --repo admin/personal-website`

## Blockers and owner choices
- Human-owned scientific specification required in [PROJECT_STATE.yaml](PROJECT_STATE.yaml) before any `M3.4` solver trajectory or phase-diagram curve goes public.

## Exact Next Step
- Specify M3.4 h-grid/seed/residual thresholds, rerun/audit paired Kitaev solver campaigns, and resolve KM-01 parity/resolvent assumptions.
