# How to Use and Maintain Your Website Without an LLM (`HOW_TO_USE_AND_MAINTAIN.md`)

This manual is designed so you have **100% ownership and long-term independence** over your website—solving the "vibe-coding dependency" problem.

The system is split into two strictly separated worlds:
1. **Part I — Day-to-Day Content Authoring (99% of your time, Zero Code Changes):** You only touch plain Markdown files in `site/content/` and YAML data in `site/data/`.
2. **Part II — Backend Engineering Reference (`site/engine/`):** A clean, 550-line Python standard-library + PyYAML/Markdown/BeautifulSoup **Hexagonal Architecture** with 26 automated unit tests so you can modify or extend the backend yourself in minutes without breaking anything.

---

## Part I — Day-to-Day Content Operations (Zero Backend Code Changes)

### 1. Where Every Piece of Content Lives

You never edit monolithic HTML files. Every section of every page and every entry in the Unified Feed is its own small Markdown file under `site/content/`:

```text
site/
├── data/
│   ├── profile.yml                # Your single-source contact, ORCID, GitHub, and UFRN degree table
│   └── publications.yml           # Your 5 authored papers (as L. R. D. Freitas) & external references
├── content/
│   ├── home/
│   │   └── 01-intro.md            # Home page paragraph, flagship SVG, and 3 directory links
│   ├── research/                  # One Markdown file per section on "Published Research"
│   │   ├── 01-electric-polarization-vortices-2024.md   (visible: true)
│   │   ├── 02-sts-majorana-zero-modes-2023.md          (visible: true)
│   │   ├── 03-magnetic-quantum-impurities-2024.md      (visible: true)
│   │   ├── 04-line-defects-kitaev-2022.md              (visible: true)
│   │   ├── 05-entropy-heat-reservoirs-2019.md          (visible: false  <-- currently hidden!)
│   │   └── 06-ufrn-theses.md                           (visible: true)
│   ├── about/                     # One Markdown file per section on "About Me"
│   │   ├── 01-mathematics-and-orientation.md
│   │   ├── 02-broader-horizons-postdoc.md
│   │   ├── 02b-github-projects.md                      # Open-Source Software & GitHub Projects
│   │   ├── 03-philosophy-social-science.md
│   │   ├── 03b-outreach-and-climbing.md                # @lu.scientist & @luescaladora
│   │   └── 04-academic-chronology-cv.md
│   ├── feed/                      # Unified Feed child nodes (Notes, Thesis Chapters, Videos, Projects)
│   │   ├── 01-open-followups-kitaev.md                 (kind: "note",           visible: true)
│   │   ├── 02-thesis-chapters-entry.md                 (kind: "thesis-chapter", visible: true)
│   │   ├── 03-papers-worth-understanding-entry.md      (kind: "series",         visible: true)
│   │   ├── 04-video-lu-scientist-template.md           (kind: "video",          visible: false <-- unpublished!)
│   │   └── 05-project-kitaev-mf-template.md            (kind: "project",        visible: false <-- unpublished!)
│   ├── notes_index/               # Sections displayed below the Unified Feed on Notes
│   └── thesis_chapters/           # Modular chapters on /notes/thesis-chapters.html
└── assets/
    └── img/                       # Native vector .svg figures
```

---

### 2. Five Common Daily Tasks

#### Task A — Turn a Section or Feed Item On or Off (`visible: true / false`)
Open the `.md` file (for example, `site/content/research/05-entropy-heat-reservoirs-2019.md`) and change one word in the YAML header at the top:

```yaml
---
id: "paper-entropy-2019"
title: "Total entropy variation for an object in contact with heat reservoirs: the path to reversibility"
order: 50
visible: false   # <-- Change to `true` to show on Research, or `false` to hide!
publication_id: "freitas2019entropy"
---
```
When `visible: false`, the engine automatically hides the section and re-numbers the remaining visible papers (`1..4`).

#### Task B — Publish a New `@lu.scientist` Video Post in the Unified Feed
1. Copy `site/content/feed/04-video-lu-scientist-template.md` to a new file in `site/content/feed/`, e.g. `site/content/feed/2026-12-what-is-a-vison.md`.
2. Fill in the frontmatter and set `visible: true`:
```yaml
---
id: "what-is-a-vison"
title: "Video (@lu.scientist): What is a Z2 vortex (vison) in a Kitaev spin liquid?"
subtitle: "Short reel & written physical commentary"
date: "2026-12"
order: 15
visible: true
kind: "video"
external_url: "https://www.instagram.com/lu.scientist/"
tags:
  - "video"
  - "lu.scientist"
  - "kitaev-model"
figures:
  - src: "../../assets/img/flagship-vortex-charge.svg"
    alt: "Thumbnail for vison video"
    kind: "flagship"
    max_width: "220px"
summary: "A 90-second visual explanation of Z2 plaquette fluxes on the honeycomb lattice, with companion notes below."
---

**Watch the video:** [Instagram Reel on `@lu.scientist` →](https://www.instagram.com/lu.scientist/)

Write your extended thoughts, equations, and references here in normal Markdown...
```
3. As soon as at least one `kind: "video"` file has `visible: true`, the **Science Videos** filter button automatically appears on the `Feed` page, a standalone child page `notes/feed/what-is-a-vison.html` (with Breadcrumb `Home / Feed / Video...`) is generated, and the node is added to the footer **Site Map Tree**.

#### Task C — Publish a GitHub Project Write-Up in the Unified Feed
1. Copy `site/content/feed/05-project-kitaev-mf-template.md` (or set `visible: true` on it).
2. Use `kind: "project"` and `tags: ["project", "github", ...]`. The **GitHub Projects** filter button will automatically appear in the Feed bar.

#### Task D — Add a New Section to `About Me` or `Research`
Create a new `.md` file in `site/content/about/` or `site/content/research/`. Set `order:` to control where it appears (e.g. `order: 27` places it between `order: 25` and `order: 30`). You can write LaTeX like `$\mathbb{Z}_2$` directly inside YAML quotes—the parser escapes backslashes automatically.

#### Task E — Build & Verify Locally (1 Command)
From the repository root, run:
```bash
python3 site/tools/build_and_check.py --verify-fixtures && python3 tests/test_site_verification.py
```
- This compiles all modular `.md` files into `preview/_site/` (and updates the `.qmd` files in `site/`), verifies all 26 unit tests (links, DAG acyclicity, privacy guardrails, ACID store), and prints `OK`.

---

## Part II — Backend Engineering Reference (`site/engine/`)

If you ever want to modify how the website engine works, you do **not** need an LLM. The engine (`site/engine/`) is ~550 lines of standard Python organized using **Hexagonal Architecture (Ports & Adapters)**, **Pure Functional Services**, **Design-by-Contract**, and **ACID Transactions**.

### 1. Architecture Map

```text
site/engine/
├── domain/
│   ├── models.py          # Immutable @dataclass(frozen=True) value objects:
│   │                      #   ContentSection, FeedNode, SiteNode, SiteGraph (DAG), PageSpec
│   └── contracts.py       # Pure Design-by-Contract validators:
│                          #   require_valid_section(), require_unique_ids_and_orders(), require_privacy_hygiene()
├── ports/
│   └── protocols.py       # Abstract typing.Protocol interfaces (SOLID Dependency Inversion):
│                          #   ContentRepositoryPort, RendererPort, AtomicStorePort
├── services/
│   ├── pipeline.py        # Pure functions (zero I/O, deterministic):
│   │                      #   filter_visible_sections(), sort_sections(), compose_page()
│   └── dag.py             # Pure DAG navigation functions:
│                          #   build_and_verify_site_dag(), compute_breadcrumb_trail(),
│                          #   render_breadcrumb_html(), render_sitemap_tree_html()
└── adapters/
    ├── markdown_repository.py  # Driven Adapter: reads YAML + Markdown from site/content/ and site/data/
    ├── tufte_renderer.py       # Frontend Adapter: renders HTML & Quarto .qmd from PageSpec + SiteGraph
    └── acid_store.py           # Driven Adapter: stages build in .tx_stage_<id>, verifies links/hashes,
                                #   and commits atomically via os.replace() (or rolls back on error)
```

### 2. How to Make Backend Changes Safely

| What you want to change | Exact file & function to edit | Why nothing else breaks |
| :--- | :--- | :--- |
| **Change colors, fonts, spacing, or responsive breakpoints** | `site/styles/custom.css` (`:root` CSS variables at lines 10–30) | Pure CSS presentation; zero Python changes needed. |
| **Change the HTML layout of a section, header, or footer** | `site/engine/adapters/tufte_renderer.py` (`TuftePageRenderer.render_section_html` or `render_page_html`) | Decoupled from `domain/` and `services/`; `acid_store.py` automatically verifies that your new HTML has zero broken links before committing. |
| **Add a new YAML frontmatter field to sections (e.g. `epigraph:`)** | 1. Add `epigraph: str = ""` to `ContentSection` in `domain/models.py`<br>2. Read `fm.get("epigraph", "")` in `adapters/markdown_repository.py`<br>3. Render it in `adapters/tufte_renderer.py` | Immutable dataclass defaults mean all existing `.md` files continue working without edits. |
| **Add a new top-level or child page to the DAG navigation tree** | Add a `SiteNode(node_id=..., parent_id=...)` entry in `dag_nodes` inside `site/tools/build_and_check.py` | `build_and_verify_site_dag()` automatically verifies there are no cycles and generates the Breadcrumb bar and Footer Sitemap Tree entry. |
| **Add a new safety/quality rule** | Add a check in `site/engine/domain/contracts.py` and a unit test in `tests/test_site_verification.py` | Enforced automatically on every build before `AcidFilesystemStore` swaps the output directory. |
