# Current sprint — personal-website / M2.0

Owning milestone: M2.0 (see [HORIZON.md](HORIZON.md))
Machine state: [PROJECT_STATE.yaml](PROJECT_STATE.yaml) (authoritative for task statuses)

## Scientific / engineering objective
Consolidate merged remote branch onto clean `main` and standardize `HORIZON.md`, `CURRENT_SPRINT.md`, `BACKLOG.md`, and UoW `CHANGELOG.md`.

## Implementation strategy
Preserve authoritative `PROJECT_STATE.yaml` and `doc/MILESTONE_ROADMAP.md` while keeping unpublished content strictly quarantined until verified.

## Scope and non-goals
Owns static web engine (`src/web_engine/`), page templates (`site/`), solver data contracts/fixtures, and verification suite (`make verify`).

## Current bounded tasks
- `T1` in `PROJECT_STATE.yaml`: Prune merged PR #1 branch and add HORIZON.md + UoW CHANGELOG + README headers

## Independent acceptance and reproduction
- `make verify && python3 /home/lucas/Projects/scripts/uow.py check --repo personal-website`

## Blockers and owner choices
- None blocking governance alignment; see repo-owned verification commands above.

## Exact Next Step
- Finalize M2.0 degree date conventions and public profile copy, run `make verify`, and deploy `main` to GitHub Pages.
