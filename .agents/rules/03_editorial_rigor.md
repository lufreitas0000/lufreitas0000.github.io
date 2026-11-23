---
trigger: model_decision
description: Three-Front R&D architecture (doc/rnd, doc/labbook, doc/manuscript), citation verification, and claim rigor.
---
<!-- @CANONICAL-RULE: DO NOT EDIT DIRECTLY. MANAGED BY project-governance -->
# Rule 03: Three-Front R&D Architecture, Editorial Rigor, and Provenance

Apply these standards to research notes, living labbooks, architecture records, code documentation, and publication-facing manuscripts.

## Principle of comprehension and pragmatic compression

1. **Co-equal standard of correctness and intelligibility:** Mathematical rigor and clear physical explanation are equally binding. A correct proof, formalization, or numerical benchmark that the reader or principal investigator cannot transparently understand and reconstruct is scientifically incomplete.
2. **Context of discovery vs. context of justification:** Exploratory research (dead-ends, numerical checks, verbose algebra) belongs to the *context of discovery*. Iterative refinement distills raw findings into the minimal logical spine of the *context of justification*—separating what was tested from why the surviving physics works.
3. **Pragmatic compression across formats:** Conceptual understanding behaves like information compression. In human-facing standalone notes and manuscripts (LaTeX/PDF), compress the *conceptual and algebraic skeleton* in the Main Text (minimal assumptions, clean narrative, prose-only summaries for dead-ends, full derivations and numerical tables deferred to Appendices), while intentionally retaining **human-ergonomic redundancy**: plain-language motivation, schematic diagrams, visual hierarchy, explicit definitions and first-use expansions of every acronym, and a compact jargon/acronym glossary so no undefined shorthand blocks comprehension.
4. **Visual paradigm hooks early in design:** Schematic flagship diagrams ("visual hooks") are conceptual infrastructure, not decorative afterthoughts; design and iterate intuitive topological/geometric diagrams alongside the derivations so readers grasp the physical picture before dense algebra.
5. **Single-scope research branches & explicit spin-offs:** Keep temporary research branches and standalone notes focused on a crisp coherent domain (e.g. bulk/translationally invariant physics vs.\ open-boundary/edge topology); spin off orthogonal lines explicitly to `BACKLOG.md` + `doc/rnd/exploratory/` with concise pointers in the note's status banner.
6. **Escaping local paradigm maxima via literature, universality & mental images:** Passing unit tests and insider bug checks within a chosen ansatz does not guard against plateauing in a *local maximum of knowledge* ("useless true facts", brute-force algebra, or repetitive special-case curves). Anchor every research cycle in primary literature, curated library monographs (`library/references-transcripts`, `library/arxiv-harvest`), and NotebookLM (`gemini-notebook-mcp` / `nlm`) to uncover unifying universality classes, symmetric-space/representation invariants, and categorical or topological structures that compress verbose calculations into transparent proofs and a vivid physical **mental image** (`../../meta/project-governance/docs/PARADIGM_AND_RED_TEAM_PROTOCOL.md`).

## Governing principle — three interconnected fronts inside a cyclic Blue–Red discovery spiral

We are building **scientific intelligence**, not software throughput: **science development and science communication evolve together continuously**, and R&D has **no "end"** where deliverables are deferred until final cleanup.

The **three fronts** name continuous **artifact and accountability axes**, not mutually exclusive epistemic stages, job titles, or one-way waterfalls:

- **Front 1 — Theory, discovery and hypotheses:** formulate questions, review literature, identify assumptions and idealizations, derive relations, register immutable hypotheses (`HC-XX`), and log obstructions and pivots (`LOG_DISCOVERY_AND_PIVOTS.md`).
- **Front 2 — Laboratory, code and formal verification:** carry out analytical, numerical, and Lean 4 experiments, build modular reusable libraries (`domain/` $\to$ `services/` $\to$ `infra/`, Mathlib/Physlib-backed `Core/`), verify invariants, and preserve independently inspectable provenance.
- **Front 3 — Continuous scientific exposition and navigation:** maintain living, self-contained explanations, visual mental-image hooks, `KNOWLEDGE_MAP.md`, compiled `wip-notes` PDFs, Living R&D Digests, and publication manuscripts whose claims and limitations can be evaluated at any point in the program.

To prevent autonomous R&D from drifting into a local maximum of "useless true facts" (William Thurston), the three fronts operate inside an explicit **6-Phase Cyclic Blue–Red Discovery Spiral** (paired with [Rule 09](09_model_risk_and_delegation.md)):

1. **Goals, Ideas & Hypotheses (Front 1):** State the guiding physical question, candidate hypotheses (`HC-XX`), and non-goals.
2. **Literature, Curated Vault & `W0` Strategy (Red Team / Coordinator):** Cross-examine primary literature, `library/`, NotebookLM, and Mathlib4/Physlib before authoring code; approve bounded, short-lived UoWs (`uow:approved`).
3. **Constructive Blue-Team R&D + Immediate Live Sharing (Blue Team `W2–W4`, Fronts 1–3):** Execute trial-and-error derivations, brute-force numerics, or Lean proofs as short-lived single-UoW runs (audited internally by a distinct-lineage `W4` referee), immediately annotating findings honestly at the current level of understanding.
4. **Mandatory Pause & Orthogonal Red-Team Simplification (Red Team `W5`, Fronts 1–3):** Pause additive expansion; step outside the ansatz to formalize, generalize, connect ideas, remove unnecessary clutter/clones, and upgrade the physical **mental image** and flagship visual schematic.
5. **Return to Literature & Cross-Domain Connections (Red Team + PI):** Re-query monographs, modern papers, and NotebookLM using what the brute-force cycle revealed; update `KNOWLEDGE_MAP.md`, `wip-notes` PDFs, and the Pinned Living Digest so the informational network remains navigable.
6. **Pivot, Sharpen & Re-Seed (Front 1 + Coordinator):** Record obstructions and pivots in `LOG_DISCOVERY_AND_PIVOTS.md`, formulate sharper hypotheses from the higher vantage point, and begin the next spiral—or pause for human owner review when a milestone or source horizon completes.

**There is no strict boundary between the contexts of discovery and justification.** Exposition can expose an unrecognized assumption; a failed numerical experiment can revise a hypothesis; and a Red-Team compression pass can collapse ten brute-force scripts into one analytical theorem. Work moves bidirectionally across all three fronts on every cycle.

One person, agent, file, or repository may contribute to several fronts. Assign ownership to a **bounded UoW deliverable**, not permanently to a person, scientific topic, language, or directory. The division of a broad research program into projects is partly an organizational, editorial, and historical choice: related repositories may share theory and literature while retaining distinct objectives and their own authoritative records.

Cross-front and cross-repository requests should name the needed result, its owner, assumptions, evidence standard, source links, and outstanding decisions. An Issue can request a handoff; a reviewed PR integrates an artifact. Neither an Issue nor an automated check certifies a scientific result by itself. Preserve independent review, explicit uncertainty, provenance, and the owner's authority over hypotheses and scientific acceptance criteria.

Roadmaps are **adaptive plans**, not predictions of discovery. Update priorities, milestones, and dependencies as evidence changes while preserving decisions and the rationale for changes; Rule 05 governs the concrete milestone/task lifecycle.

## 1. The Three-Front R&D Document Architecture

Scientific software and theoretical physics repositories may organize documentation
around the three fronts using the artifact-specific conventions below. This table
describes **documentary emphasis**, not a rigid workflow or epistemic partition:

| Front | Canonical Path | Epistemic Role | Audience & Format |
| :--- | :--- | :--- | :--- |
| **Front 1: Agentic R&D Front** | `doc/rnd/phase_<N>/` & `doc/rnd/exploratory/` | **Context of Discovery:** Derivations, conventions, idealization boundaries, algorithmic edge cases, numerical experiments, and failed approaches. | Machine- and developer-first Markdown (`m<P>_<M>_t<T>_<slug>.md`) with mandatory YAML frontmatter, paired with `LOG_DISCOVERY_AND_PIVOTS.md`. |
| **Front 2: Living Lab Book** | `doc/labbook/` | **Context of Justification:** Cumulative pedagogical synthesis integrating the motivating questions and dead ends from Front 1 with complete derivations, verified invariants, and reproducible `.dat` plots. | Human-first `memoir` LaTeX book (`doc/labbook/main.tex`) using the shared warm parchment theme (`#FAF6EE` background, `#2B2B2B` text) and `pgfplotstable`. |
| **Front 3: Publication Manuscript** | `doc/manuscript/` (or `doc/report/`) | **Context of Exposition:** Self-contained journal paper or monograph narrative stripped of internal project scaffolding. | External referees and readers (`revtex4-2`, `article`, or `memoir` with white print toggle `\warmthemefalse`). Must never depend on unpublished `doc/rnd/` scratch notes. |

The traditional labels *context of discovery*, *context of justification*,
and *context of exposition* describe the usual emphasis of these documents.
They are not exclusive philosophical categories. In particular, Front 2 also
includes source code, calculation notebooks, test suites, and raw experimental
records outside `doc/labbook/`; Front 3 can be a website note or other
standalone published artifact outside `doc/manuscript/`.

### 1.1 Front 1 (`doc/rnd/`) YAML Frontmatter Contract

Every milestone-indexed R&D note (`doc/rnd/phase_<P>/m<P>_<M>_t<T>_<slug>.md`) must begin with structured YAML frontmatter so `make_snapshot.py` and `build_blueprint.py` can index the epistemic graph:

```yaml
---
id: RND-P1-M1.1-T1
title: "Finite-Lattice Conventions and Local Majorana Algebra"
phase: 1
milestone: M1.1
task: T1
status: completed # draft | active | blocked | completed | pivoted
questions:
  - "What local Majorana representation and parity projection uniquely fix the spin-1/2 algebra?"
depends_on: []
contracts:
  - A01
  - A02
claims:
  - K-001
  - K-002
artifacts:
  - src/pkg/domain/algebra.py
  - test/unit/test_algebra.py
---
```

### 1.2 Mandatory LaTeX Provenance & Editorial Comments (Fronts 2 & 3)

Every chapter and section in `doc/labbook/` and `doc/manuscript/` must obey three source-comment contracts:

1. **Guiding Question (`% EDITORIAL QUESTION:`):**
   - Place `% EDITORIAL QUESTION: <concise physical or mathematical question>` immediately before every numbered `\section` (and any `\subsection` addressing an independent question).
   - Lead with the physical observable or concrete motivating example before introducing abstract apparatus.
   - Explicitly answer the guiding question in the section's scientific conclusion.
2. **External Reference Locators (`% SOURCE [STATUS]:`):**
   - Every nonstandard or externally sourced formula/theorem requires a comment:
     `% SOURCE [VERIFIED|UNVERIFIED]: <Author (Year), Edition, Ch/Sec/Eq locator — supported claim>`
   - Never fabricate page numbers, equation numbers, or locators.
3. **Internal Claim Traceability (`% CLAIM:`):**
   - When promoting a verified project result into `doc/labbook/` or `doc/manuscript/`, annotate its provenance:
     `% CLAIM: <ID> (note: doc/rnd/..., test: test/..., data: data/processed/benchmarks/...)`

### 1.3 Post-DTP Knowledge Representation (Thurston & Lakatos Standard)

Raw Definition–Theorem–Proof (DTP) scripts and dense parameter-sweep tables are a lossy 1D linearization that obscures physical intuition, regime boundaries, and edge-case structure. Pair formal/computational modules with two co-equal intuition layers:

1. **Mental Image & Flagship Visual Hook:** Every standalone technical note (`doc/notes/`), labbook chapter, and manuscript section introducing a core mechanism must open with (a) a concise 1-paragraph **Mental Image** describing what the degrees of freedom do geometrically or topologically, and (b) a conceptual **Flagship Visual Schematic** (TikZ/vector diagram) establishing the paradigm *before* dense derivations or `pgfplots` sweeps.
2. **Physical Regime & Lakatosian Counterexample Ledger:** Every major Lean `Defs.lean` core or analytical model must explicitly record excluded physical effects, non-commuting limits (e.g. $\lim_{h\to 0^+}\lim_{V\to\infty}$ vs. $\lim_{V\to\infty}\lim_{h\to 0^+}$), and near-miss counterexamples linked to fast Python/SymPy oracles. Agents must practice **lemma-incorporation** (upgrading concepts to absorb genuine anomalies), never silent **monster-barring** (artificially narrowing binders to evade difficult cases).

### 1.4 Continuous 3-Layer Deliverable Bundle & Navigating the Informational Maze

Because R&D has no "end", deliverable knowledge is produced **continuously inside the ACID UoW pipeline** so the PI can inspect and navigate active work directly on GitHub without wading through raw commit logs:

1. **Always-Current Living Atlas (`KNOWLEDGE_MAP.md` at repo root):** A concise, 1-page GitHub-native map (`templates/KNOWLEDGE_MAP.md.tmpl`) containing the current *Mental Image*, a Mermaid concept/dependency DAG, active hypotheses (`HC-XX`), verified core theorems/results + Regime Ledger pointers, direct links to compiled `wip-notes` PDFs, and active pivots/open questions. Updated atomically whenever concepts, verified results, or pivots move.
2. **GitHub Live Reading Hub (`wip-notes` Pre-Release + Pinned `Living R&D Digest` Issue + Front-3 PR Cards):** Refreshed at every compiled note, stage PR, or Red-Team checkpoint following [`../docs/WIP_SCIENCE_COMMUNICATION.md`](../../meta/project-governance/docs/WIP_SCIENCE_COMMUNICATION.md) (keeping binary PDFs out of Git history per Rule 01 Tier 4).
3. **Per-UoW ACID Knowledge Stamp (`CHANGELOG.md` + `governance/info_telemetry.jsonl`):** Every UoW atomically records *Ideas & Contracts Evolved*, *Code & Artifacts Changed*, *Pre-/Post-UoW Passive $\Delta\mathbf{I}$ Vector* (Rule 09 §8), and updated deliverable links.

## 2. Mathematical claims, idealizations, and provenance

1. State definitions, domains, idealizations (mean-field, finite-size cluster, perturbative order, gauge sector, regulator), and boundary conditions before relying on them.
2. Give proofs for nontrivial claims when presenting them as established results. Identify omitted arguments and cite a verifiable source when relying on an external result.
3. Strictly distinguish:
   - exact algebraic identities and analytical theorems;
   - finite-volume or finite-dimensional exact results;
   - floating-point numerical benchmarks and convergence tests;
   - approximations, extrapolations, and conjectures.
4. Do not promote finite-size numerical agreement into a thermodynamic claim without a controlled limiting argument. A passing test certifies only its tested computational contract and parameter domain.
5. Record limiting-case checks and independent validations when they materially support the result. Explain what those checks do and do not establish.
6. **Basis bijections vs.\ Hilbert-space expansions & parameter compression:** Explicitly separate exact unitary changes of local basis (e.g.\ spinful fermions written as four Majoranas on the same $2^2=4$-dimensional Fock space) from genuine Hilbert-space extensions requiring projection (e.g.\ Kitaev $2\to 4$ spin partons with $D_j=+1$), and never present omitted projections or frozen fields as derived consequences. Compress model parameters via an explicit hierarchy ledger separating units, fixed non-singular shaping constants, and varied physical control axes.

## 3. Conventions and mathematical typography

State conventions explicitly whenever they affect signs, prefactors, symmetry representations, or physical interpretation:
- lattice graph, sublattice, and bond orientation;
- Fourier-transform and Brillouin-zone normalization;
- operator/parton representation, normal ordering, and physical-state projection;
- index ranges, summation conventions, and matrix ordering;
- boundary conditions and finite-size geometry.

Typographical standards across Markdown and LaTeX:
- Use upright Roman type for named operators and labels (`\Tr`, `\tr`, `\Pf`, `\sgn`, `\diag`, `\mathrm{d}k`, `\mathrm{MF}`, `\mathrm{BdG}`, `\mathrm{BZ}`).
- Use blackboard bold for number fields and identity operators (`\mathbb{R}`, `\mathbb{C}`, `\mathbb{Z}_2`, `\mathbb{1}`).
- Use `\DeclarePairedDelimiter{\abs}{\lvert}{\rvert}` and `\DeclarePairedDelimiter{\norm}{\lVert}{\rVert}` for properly scaled delimiters.
- Punctuate displayed equations as part of the surrounding prose sentence.

## 4. Code and mathematical notation

1. Use descriptive English identifiers by default. Conventional uppercase names for matrices, Hamiltonians, exchange tensors, and operator representations are acceptable when they improve correspondence with the mathematical notation.
2. Maintain strict architectural separation:
   - `domain/`: pure mathematical entities, parameters, lattices, and port interfaces;
   - `services/`: physics and numerical algorithms depending only on domain abstractions;
   - `infra/`: hardware backends (CPU/CUDA), file I/O, and `.dat` tabular exporters;
   - `app/`: CLI entrypoints and workflow orchestration.
3. Avoid semicolon-compressed statements and minified code. Preserve readability and explicit control flow.

## 5. References and bibliographic integrity

1. Cite primary literature, peer-reviewed work, authoritative books, and original software documentation as appropriate to the claim.
2. Verify bibliographic metadata against publisher records, DOI registries, arXiv records, or the cited source itself. Never invent or infer a DOI, arXiv identifier, title, author list, page range, or publication year.
3. Use a consistent citation style appropriate to the document. Author-year citations are suitable for Markdown research notes (`doc/rnd/`); use BibTeX (`refs.bib`) and the target venue style for `doc/labbook/` and `doc/manuscript/`.
