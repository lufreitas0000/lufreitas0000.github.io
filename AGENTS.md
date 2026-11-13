# Workspace Agent Operating Guidelines (personal-website)

This repository implements Lu Freitas's personal research website (`https://lufreitas0000.github.io/`, repo `lufreitas0000/lufreitas0000.github.io`) using a Hexagonal Architecture Python static site engine (`src/web_engine/`) and modular Markdown/YAML content (`site/`).

---

## 1. Authority & Boundaries
1. **Content Workspace (`site/`):** Day-to-day content updates only touch `site/content/**/*.md`, `site/data/*.yml`, `site/assets/`, `site/templates/`, and `site/styles/`.
2. **Engine (`src/web_engine/`):** Strictly follows Hexagonal Architecture (`domain/`, `ports/`, `services/`, `infra/`, `app/`). Keep `domain/` and `services/` free of I/O and HTML generation.
3. **Never Deploy Private Files or Fixtures:** `test/fixtures/` and `build/fixtures_site/` are strictly for local verification and must never be deployed to GitHub Pages.
4. **Verification Gate:** Every change must pass `make verify` before commit or push.

---

## 2. Core Rules (`.agents/rules/`)
- `00_workspace_hygiene.md`: Single-responsibility modules, clean root, git-ignored `build/`.
- `01_repository_safety.md`: No destructive git commands (`push --force`, `reset --hard`, `clean -fdx`); atomic writes via `AcidFilesystemStore`.
- `02_tdd_protocol.md`: Contract-driven tests (`test/unit/`, `test/integration/`, `test/e2e/`).
- `03_website_editorial_and_privacy.md`: Privacy tokens, author-name continuity (`Lu Freitas` vs `L. R. D. Freitas`), and anti-fabrication rules.
