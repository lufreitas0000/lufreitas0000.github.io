# Kitaev dispersion — one-parameter scientific contract

**Scope:** `kitaev-mf` Feed note only · **Revised:** 2026-11-14
**Research status:** exact zero-field vortex-free dispersion, not a field-driven mean-field calculation.

## LU-DECIDED: notation and domain

Use the same symbols as the `kitaev-walk-geometry` monograph: structure factor
`f`, complex three-step endpoint `Z=f`, and radial modulus `r=|Z|=|f|`.
Do not introduce `g`, `S`, or lowercase coupling symbols `j_gamma`.

The physical Kitaev couplings are `J_x,J_y,J_z`. Set
`J_x=J_y=J>0`, vary `0<=J_z<=2J`, and default to `J_z=J`.
With `k=(k1,k2) in [0,1)^2` and `theta_a=2*pi*k_a`,

```text
f(k; J_z/J) = J_z/J + exp(2*pi*i*k1) + exp(2*pi*i*k2)
Z(k; J_z/J) = f(k; J_z/J)
r(k; J_z/J) = |Z(k; J_z/J)| = |f(k; J_z/J)|.
```

The dimensionless display is `r`. It is **not** labelled a physical
excitation energy. Fix the palette scale at `0<=r<=4` for the
whole slider range, so changing the coupling does not silently
change the color normalization. The wavevector is the reduced torus,
not a hexagonal Brillouin-zone projection.

At the isotropic point `J_z=J`, this is the three **unit**-phasor
sum of the walk-geometry project; then `Z` is the orthocenter
of the inscribed unit-circle triangle, and `r=|Z|`.
For `J_z!=J`, this is a weighted walk. The isotropic orthocenter
identity and radial law `p_3(r)` are **not** carried over to it.

## Derived exact zero-field identities

Let `t=J_z/J` only as a temporary abbreviation in calculations
(not as a visible widget variable). For `0<t<2`, let

```text
q(t) = acos(-t/2) / (2*pi).
zeros: (q(t),1-q(t)) and (1-q(t),q(t)).
```

Each is verified directly by `f=0`. At `t=1` these become
`(1/3,2/3)` and `(2/3,1/3)`.
At `t=2` they coalesce into `(1/2,1/2)`.
At `t=0` the zeros are **not two isolated points**:
`k2=k1+1/2 (mod 1)` is a continuous line of zeros.

This is a one-parameter interval on the gapless side, including
its two singular endpoints. No gapped regime beyond `2J` is
displayed; no field-induced mass, `C_3` symmetry claim or finite-field
mean-field spectrum is made.

## VERIFIED provenance (source checked 2026-11-14)

- `kitaev-walk-geometry`, `main` at `f5a006dad55a445fd3e4afdf4addd36fdf69806b`,
  `doc/labbook/chapters/ch01_kitaev_kinematics.tex`, "Notation and Geometric Dictionary".
  Its `src/walk.py` gives the angular-momentum version.
- `kitaev-mf`, `main` at `4c2d629ec7ee924c731c566fc00d9dc0411217c6`,
  `doc/rnd/exact-perturbation-theory/notes/02_normalization_and_bloch_conventions.md`,
  which distinguishes the canonical excitation frequencies from the
  matrix eigenvalues reported by the production Bloch builder.
- The existing website article `site/content/feed/06-kitaev-mf.md`
  uses `f(k)=1+exp(2*pi*i*k1)+exp(2*pi*i*k2)` in its zero-field benchmark.

No build-time dependency on the private `kitaev-walk-geometry` repository
is introduced and no private source content is copied to the public
build. Only the common mathematical notation and independently
checked formulas are used.

## Implementation (Phase 1)

One optional island next to the article's existing exact-limit
dispersion discussion. Source article prose and equations stay intact.

- Static self-contained SVG is visible by default without JavaScript.
- Self-hosted vanilla ES module progressively enhances it with a
  responsive canvas, a `J_z/J` slider (0 to 2, default 1), node
  markers or the boundary nodal line, and a textual node readout.
- No simplex, other coupling sliders, Python, Pyodide, CDNs, or
  extra mathematics libraries.
- Scoped CSS only; no change to global layout or navigation.
- Unit tests for all endpoints and the isotropic point, cross-runtime
  verification of node positions, rendered HTML test of no-JS fallback,
  and independent test of static SVG semantics.

## TODO(Lu) — future scientific decisions

1. Whether a later interactive note should display **physical** excitation
   energies, in which operator normalization and gauge convention.
2. Whether to add a second, separately reviewed random-walk
   visualization for `p_3(r)` or `\bar U`, only in the isotropic case.
3. Exact finite-field symmetry contract, perturbative reference
   coefficients, statistical solver initial-state ensemble and tolerances.
4. The published-method citation for a later research-level benchmark
   figure; the current dispersion display illustrates an exact known formula.

The broader wish list (fixed-point lab, solver data, claim ledger)
remains in `doc/FEED_KITAEV_MF_SERIES.md` and is not implemented here.

## Local preview, rollback and publication

Use a dedicated worktree and `make verify`, `make serve` to preview
`http://localhost:8000/notes/feed/kitaev-mf.html`. The published
article remains a complete static reading experience with JS disabled.

To roll back, revert the widget-specific article HTML, scoped
CSS and self-hosted SVG/module in one commit. Never modify the
`kitaev-mf` numerical solver as part of this publication change.
