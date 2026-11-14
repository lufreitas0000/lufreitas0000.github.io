# kitaev-mf: Feed series

The published page [kitaev-mf: Majorana mean-field theory](../site/content/feed/06-kitaev-mf.md) is the standalone hub. This is an editorial backlog, not a set of published URLs.

## Editorial contract

- Every note is readable independently: define the physical problem, conventions, mathematical objects, approximations, and what is established.
- Prefer a small number of informative headings; suppress repeated subtitles, tag badges, and introduction-by-enumeration.
- Use $...$ and $$...$$ for Markdown math. Explain nontrivial symbols at first use.
- Each new file must remain `visible: false` until its sources, equations, internal links and scientific claims have been reviewed and its public build has passed `make verify`.
- Add live hyperlinks in the hub only after a new note's actual route exists. Never ship a link to a future placeholder.
- Cite relevant original literature and point readers to the actual source files, but do not make the note dependent on opening the external PDF.

## Queue (one note at a time)

| ID | Working title | Primary source files | Scientific gate |
| --- | --- | --- | --- |
| KM-01 | Exact Kitaev spectra, physical parity, and perturbative resolvents | `doc/rnd/exact-perturbation-theory/notes/01_flux_sectors_and_spectrum.md`, `03_low_energy_projector_and_feshbach.md`, `doc/labbook/chapters/ch_m1_10_vortices_real_lattice.tex` | Fix finite-torus physical parity and resolvent domain; avoid denominator substitutions without control |
| KM-02 | Dirac matter, field-induced masses, and vortex excitations | `doc/labbook/chapters/ch_m1_6_solvers_and_basins.tex`, `ch_m1_10_vortices_real_lattice.tex` | Separate perturbative order, fitted coefficients and finite-size effects |
| KM-03 | Anisotropic chains, dimers, and polarized limits | `doc/labbook/chapters/ch_m1_4_5_invariants_dualities.tex` | Say exactly which limits are solvable; do not call the generic finite-field phases exact |
| KM-04 | When a converged Majorana mean field can be trusted | `doc/labbook/chapters/ch_m1_4_5_invariants_dualities.tex`, `ch_m1_11_hypothesis_contracts.tex`, `data/processed/benchmarks/` | Distinguish convergence, kinematic admissibility, physical accuracy and true error bounds |
| KM-05 | Fixed-point iteration and the map `Phi` | `doc/labbook/chapters/ch_m1_3_spectral_projector_diis.tex`, `ch_m1_6_solvers_and_basins.tex` | Correctly distinguish contraction mapping conditions from local linear stability |
| KM-06 | DIIS, Anderson, Broyden, and Newton–Krylov methods | `doc/labbook/chapters/ch_m1_6_solvers_and_basins.tex`, `data/processed/benchmarks/m1_6/` | Reconcile trial-count and residual-history provenance before quoting performance tables |
| KM-07 | Matrix-sign purification and large real-space lattices | `doc/labbook/chapters/ch_m1_9_real_space_and_purification.tex`, `src/kitaev_mf/services/purification.py` | Verify finite-size spectra and zero-mode safeguards |
| KM-08 | Spin correlations, gauge quenches, and tunneling spectroscopy | `doc/rnd/phase_3_dynamical_spin_correlations/blueprint.md`, `doc/MILESTONE_ROADMAP.md` | Separate reproducible exact results from the unimplemented dynamical program |

## Labbook extraction and auditing

The public hub adapts the following material from the source LaTeX:

- Ch. M1.1b: Wick factorization as a property of quasifree states, not an operator identity.
- Ch. M1.2: bond and site Majorana covariances and constrained quadratic Hamiltonians.
- Ch. M1.3: negative-energy projectors, the exact `K-006` Brillouin integral and the DIIS residual.
- Ch. M1.4.5: semidefinite and kinematic checks and solvable 1D/dimer reductions.
- Ch. M1.6: the nonlinear fixed-point problem, Picard damping, quasi-Newton methods, critical basins and spinodal caution.
- Ch. M1.9: real-space matrix-sign purification.
- Ch. M1.10: vortex pairs and finite-size Majorana modes.

Editorial risks found during the source review (not claims resolved by this website update):

1. Ch. M1.6 phrases local Picard convergence as an "if and only if" consequence of Banach contraction; contractivity is sufficient, but general equivalence is not established. The website uses only the defensible local-linear stability statement.
2. The labbook's solver convergence figure caption says DIIS reaches machine precision, while `data/processed/benchmarks/solver_convergence.dat` has nonmonotone histories with residuals around `1e-2` in the displayed window. Do not reuse the caption as a validated claim without reconciling the underlying run.
3. The archived statistical solver report refers to 30 trials, while `statistical_solver_scorecard.dat` labels 40. Check the raw sample counts and confidence intervals before publishing performance summaries.
4. Different source notes encode the spin–Majorana bilinear and local parity signs differently. Any future explicit operator formula needs a single stated CAR representation and independent physical-projection checks.

These discrepancies are internal R&D review items and should not silently become published "theorems".

## Interactive publishing pilot (14 November 2026)

**Published within the main `kitaev-mf` note:**
- Dimensionless $r=|f|$ at $J_x=J_y=J$, sweeping $0\le J_z/J\le2$; the $J_z=0$ nodal line and $J_z=2J$ merger are identified, with an isotropic static SVG fallback.
- Deterministic midpoint quadrature for the exact-limit $\bar U$ integral, a static table and downloadable CSV.
- Two-dimensional linear fixed-point Jacobian toy showing damping as $\lambda\mapsto1-\alpha+\alpha\lambda$; explicitly *not* a Kitaev solver result.
- Optional claim ledger and immutable source links. All mathematical UI elements are optional to understand the article.

**Implemented but not published:**
- [Paired solver data schema and validator](KITAEV_MF_SOLVER_DATA_CONTRACT.md).
- Independent, branch/segment-aware interpolation candidate in `test/support/`.
- [Local isolated WSL worktree preview](WEBSITE_PREVIEW_WORKTREE.md).

**Blocked by human-owned scientific decisions:** field units and sampling;
initial-state ensemble/seed list; solver fairness and residual contracts;
branches/transition exclusions; benchmark observables; exact-reference
orders; held-out interpolation tolerances. No trajectories or physical
phase-diagram curves should go public before those decisions and
reproduction evidence exist.

The broader fixed-point lab remains a distinct prospective series:
methods and maps should be independent; the Kitaev mean-field map
will be one scientifically audited case study.
