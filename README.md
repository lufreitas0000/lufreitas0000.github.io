# Lu Freitas — Personal Research Website

Static research website (`https://lufreitas0000.github.io/`, repo `lufreitas0000/lufreitas0000.github.io`) built with a Hexagonal Architecture Python engine (`src/web_engine/`) and modular Markdown/YAML content (`site/`).

## Quick Commands (WSL / Linux)

```bash
make verify          # Build public + fixture previews and run all 20 tests
make build           # Build public site into build/_site/
make serve           # Serve http://localhost:8000 locally
make new-post SLUG=my-topic KIND=note
make clean-build     # Remove ephemeral build/ and cache directories
```

## Where to Edit Content

- `site/data/profile.yml` — Contact email (`lu.rdf@icloud.com`), ORCID, GitHub, Google Scholar, education table.
- `site/data/publications.yml` — Authored publications (`L. R. D. Freitas`) and external references.
- `site/content/feed/*.md` — Unified Feed posts (`note`, `expository-note`, `reading`, `series`, `project`, `video`).
- `site/templates/*.html` & `site/assets/js/feed_filter.js` — HTML shells and client-side multi-filter + search.
- `site/styles/custom.css` — Bitstream Charter typography, `#FAF6EE` warm parchment, and RGB bond palette.

See `doc/HOW_TO_USE_AND_MAINTAIN.md` for the full operator manual.
