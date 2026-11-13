# Discovery & Pivot Log (`LOG_DISCOVERY_AND_PIVOTS.md`)

| Date | Module/Context | Obstruction | Pivot/Resolution | Status |
| :--- | :--- | :--- | :--- | :---: |
| 2026-11-12 | `site/engine/` & `site/tools/build_and_check.py` | Monolithic 686-line build script and 461-line `tufte_renderer.py` with HTML/JS embedded in Python and drifted `ports/protocols.py`. | Separated into `src/web_engine/` (`domain/`, `ports/`, `services/`, `infra/`, `app/`) and external `site/templates/` + `site/assets/js/`. | `Active` |
| 2026-11-12 | `notes/index.html` Feed Search | Full `body_markdown` embedded in `data-search` HTML attribute does not scale cleanly; single-select filter buttons only. | Emit lightweight `notes/search-index.json`, move filters to multi-select `Set` on the left and search input on the right. | `Active` |
