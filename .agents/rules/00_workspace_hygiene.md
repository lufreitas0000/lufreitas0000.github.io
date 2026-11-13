# Rule 00: Workspace Hygiene and Repository Layout

1. Inspect `git status --short --branch` before editing. Preserve unrelated user changes.
2. Keep generated artifacts (`build/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`) git-ignored.
3. Follow the Single Responsibility Principle: each module in `src/web_engine/` owns one cohesive concern.
4. Keep HTML/CSS/JS presentation templates in `site/templates/`, `site/styles/`, and `site/assets/js/` rather than embedding large markup strings inside Python modules.
