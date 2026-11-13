# Content Review & Editorial Decisions Ledger (`CONTENT_REVIEW.md`)

Prepared 9 November 2026 for Lu Freitas's review prior to public deployment.

---

## 1. Source-Backed Facts Included in the Site

| Fact / Section | Source Used | Where Appearing |
| :--- | :--- | :--- |
| Display name **Lu Freitas** and discreet bibliographic continuity note (*Lucas R. D. Freitas*, *Lucas Rodrigues Delgado de Freitas*, *Lucas Freitas*) | Confirmed by Lu (`WEBSITE_CONTENT_DOSSIER.md`) + ORCID `0000-0002-4491-8492` | `Home`, `Research`, `About (#name-continuity)`, `/about/working-with-me.{html,md}` |
| PhD in Physics completed at UFRN in 2024; currently unaffiliated; public contact `lu.rdf@icloud.com` | Confirmed by Lu (`WEBSITE_CONTENT_DOSSIER.md`) | `site/data/profile.yml`, `Home`, `About`, Footer |
| Five peer-reviewed publications (`PRB` 2024 `L220403`, `npj Quantum Materials` 2024 `9, 33`, `PRB` 2023 `054432`, `PRB` 2022 `L041104`, `RBEF` 2019 `e20180331`) with exact author lists, DOIs, and arXiv IDs | Verified directly against arXiv (`2405.19962`, `2311.15750`, `2209.12930`, `2108.04320`), ORCID, and SciELO | `site/data/publications.yml`, `site/references.bib`, `Home`, `Research (#publications)` |
| Distinction between current independent footing (1D spin chains, 2D Kitaev models) and three broader research directions (Lean 4 formalization & finite/infinite boundaries; AQFT/type III von Neumann algebras & open dynamics; generalized symmetries, fractionalization & coupled-wire dualities) | `RESEARCH_NARRATIVE_DRAFT.md` (`V4`) & `WEBSITE_CONTENT_DOSSIER.md` | `Home`, `Research` |
| Aesthetic motivation in pure mathematics and physics, IMPA coursework context (without claiming an IMPA degree or publishing grade tables), and formative 2019 reading of Kitaev (2006) | `RESEARCH_NARRATIVE_DRAFT.md` (`V4`) & `WEBSITE_CONTENT_DOSSIER.md` | `About (#mathematics-and-beauty, #turning-points)` |
| Formative 2018 History and Philosophy of Science course, William P. Thurston's *On proof and progress in mathematics* (`math/9404236`, DTP model), and **Helen E. Longino's *Science as Social Knowledge: Values and Objectivity in Scientific Inquiry* (1990)** along with **social epistemology** and **feminist epistemology** | `WEBSITE_CONTENT_DOSSIER.md` + Lu's explicit 9 Nov 2026 prompt update | `About (#philosophy-of-science)` |
| *Papers worth understanding* series inspired by Pedro Vieira's *Beautiful Papers* course at Perimeter Institute (crediting inspiration without claiming course attendance) | `SITE_SPECIFICATION.md` & `WEBSITE_CONTENT_DOSSIER.md` | `Notes`, `/notes/series/papers-worth-understanding.html` |

---

## 2. Deliberately Omitted or Quarantined Items (Privacy & Anti-Fabrication)

1. **Private Master Profile & Private Email (`physics.freitas@gmail.com`)**: Completely excluded from all files in `site/`, `preview/`, and `dev-fixtures/`.
2. **Retired Institutional UFRN Email**: Completely excluded.
3. **Legal ID / CPF Context & Pronouns**: Completely excluded; pronouns are not inferred.
4. **IMPA Registration Screenshot & Raw Grade Table**: Excluded from public pages; mentioned on `About` only as summer/visiting mathematics coursework at IMPA.
5. **Unresolved Phrase `"higher order tensors"`**: Omitted from public technical claims per `WEBSITE_CONTENT_DOSSIER.md` until a specific mathematical object is selected.
6. **Missing Standalone PDF CV & Portrait**: No fake CV PDF or stock portrait was generated. `About (#cv)` provides a clean living academic chronology and notes that a standalone PDF CV will be linked once degree-date conventions are finalized.
7. **No Fabricated Published Blog Posts**: `preview/_site/notes/index.html` ships with an honest launch baseline (`0` published posts). Authoring validation fixtures live strictly in `dev-fixtures/` and `dev-fixtures-preview/`.

---

## 3. Open Decisions for Lu Before Public Launch

1. **Degree Date Conventions & Thesis Metadata (`site/data/profile.yml`)**: Confirm the preferred start/end/defense years for BSc (`2015–2018`), MSc (`2019–2020` in ORCID vs. `2021` repository deposit), and PhD (`2020–2024`), as well as exact thesis titles and supervisor names once UFRN repository access is available.
2. **Public Lattes Short URL**: Add your canonical `lattes.cnpq.br/<16-digit-id>` URL to `site/data/profile.yml` if you want it displayed alongside ORCID, GitHub, and Google Scholar.
3. **First Published Note**: Decide whether to promote the `successive_heat_reservoirs.ipynb` study (or a first *Papers worth understanding* note on Kitaev 2006) from `dev-fixtures/` to `site/notes/posts/` for launch, or launch with the honest empty Notes introduction.
4. **Content & Code License**: Choose your preferred license wording for `site/` code vs. authored prose/notes before enabling public GitHub Pages deployment.
