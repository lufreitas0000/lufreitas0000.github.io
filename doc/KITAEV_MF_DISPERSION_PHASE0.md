# Kitaev dispersion — Phase 0 reference specification

**Status:** unpublished fixture · **Date:** 2026-11-14 · **Branch:** `feat/kitaev-mf-dispersion-island`

No change to the published article, layout, navigation, scripts or production assets.
This phase delivers a mathematical reference, tests and a static SVG under
`test/fixtures/`, not an interactive island.

## Research and publication contract

The program connects (1) literature, assumptions and hypotheses,
(2) exploratory numerical experiments, and (3) self-contained published notes.
Discovery and justification are interconnected; a failed numerical check can
change a hypothesis or its exposition. The website pilots the third activity
for `kitaev-mf`; laboratory outputs are **not** automatically published.

## LU-DECIDED — reuse the established notation

The user's `kitaev-walk-geometry` project (private at audit time) defines
the isotropic structure factor `f`, the three-phasor endpoint `Z=f`,
and the dimensionless radial observable `r=|Z|=|f|`.
Reuse those objects without inventing symbols `g` or `S`.

Introduce one positive reference energy `J_ref` and reduced positive
couplings `j_gamma=J_gamma/J_ref`. With reduced torus coordinates
`k=(k1,k2) in [0,1)^2`, define

```text
f(k; j) = jz + jx exp(2*pi*i*k1) + jy exp(2*pi*i*k2),
Z(k; j) = f(k; j),
r(k; j) = |Z(k; j)| = |f(k; j)|.
```

The Phase 0 SVG plots **r=|f| (dimensionless)** for
`jx=jy=jz=1`; it does **not** label this quantity a physical
quasiparticle energy. It contains no field-induced mass and no
mean-field self-consistency calculation.

**Geometric limitation:** for equal step lengths, `Z` is a sum of
three unit phasors, interpretable as the orthocenter of their inscribed
triangle in the source project. For unequal `j_gamma`, `Z` is a
*weighted* three-step endpoint. The unit-circle orthocenter construction
and the isotropic radial density `p_3(r)` cannot be reused unchanged.
No anisotropic `p_3` formula is claimed.

**Momentum conversion:** the source project uses angular
`theta_a in [-pi,pi)`, while the website uses reduced `k_a in [0,1)`.
Identify `theta_a=2*pi*k_a` modulo `2*pi`. This changes coordinates,
not the mathematical structure factor.

## Source and spectral-normalization audit

**VERIFIED (inspected 2026-11-14):**

- Alexei Kitaev, *Anyons in an exactly solved model and beyond*,
  Annals of Physics **321** (2006), 2–111,
  https://doi.org/10.1016/j.aop.2005.10.005.
  The original Pauli-spin Hamiltonian sums physical bonds once.
- `kitaev-mf/doc/rnd/exact-perturbation-theory/notes/02_normalization_and_bloch_conventions.md:7–89,255–326`
  reconciles `K_P=-K_R` and distinguishes canonical excitation
  frequencies from eigenvalues of the production `iA/4` Bloch matrix.
- `kitaev-mf/doc/labbook/chapters/ch_m1_2_bloch_and_folding.tex:141–202`
  discusses this factor of four and uses a complex-conjugate Fourier
  convention. Simultaneous momentum inversion preserves `r=|f|`.
- `kitaev-walk-geometry/doc/labbook/chapters/ch01_kitaev_kinematics.tex`,
  Section "Notation and Geometric Dictionary", names
  `Z=z_1+z_2+z_3=f` and `r=|Z|`.
- `kitaev-walk-geometry/src/walk.py` already provides an anisotropic
  structure-factor function (in angular momentum coordinates),
  the triangle-closure test, and the spectral-gap formula.
  The website tests here are *independent*, not code copied from that
  repository or an implicit build dependency.

**INFERRED:** reuse `f,Z,r` for the dispersion visualization and
separate the later choice of physical energy normalization from its
dimensionless shape.

## Exact reference identities

For `jx,jy,jz>0`, `f=0` has two distinct torus roots iff every
triangle inequality is strict. At a saturated inequality, the roots
merge; beyond it no zero exists. The zero-coupling boundary is outside
this Phase 0 contract, as nonisolated zeros can arise there.

With `theta_a=2*pi*k_a`, direct use of `|jz+jx exp(i theta1)|=jy`
and its counterpart yields

```text
cos(theta1) = (jy^2-jx^2-jz^2)/(2*jx*jz)
cos(theta2) = (jx^2-jy^2-jz^2)/(2*jy*jz)
jx*sin(theta1) + jy*sin(theta2) = 0.
```

For strict inequalities, choose `theta1=acos(cos(theta1))` and
`theta2=-acos(cos(theta2))`; the second root is the simultaneous
negative modulo `2*pi`. Check both directly in the complex equation
independently of the trigonometric derivation.

```text
min_(k in T^2) r(k;j)
  = max(0, 2*max(jx,jy,jz)-(jx+jy+jz)).
```

At `(1,1,1)`, the nodes are `(1/3,2/3)` and `(2/3,1/3)`.
With `jx=jy=1`, they merge at `(1/2,1/2)` for `jz=2`,
and `min r = 0.5` at `jz=2.5`. Further anisotropic and
other-axis gapped cases are included in the machine fixture.

## TODO(Lu) — decisions still open

1. Reference energy `J_ref`, simplex total `jx+jy+jz=C`,
   value of `C`, and preset configurations (the reference isotropic
   case is not a simplex UI choice).
2. `jx=jy` animation range for `jz`, speed and sampling.
3. If any physical energy is shown in Phase 1, its precise prefactor,
   units, and relation to both the project Bloch and canonical spectra.
4. Finite-field [111] versus zero-field symmetry statements.
5. Scientific tolerance and the exact published-method citation
   for the eventual interactive caption.
6. Future solver-comparison `h` units/grid, paired random initial
   states and distribution, seed list, observables, failure criteria,
   residual weighting and precommitted hyperparameters.
7. Weak-/strong-field perturbative orders, coefficients and observables.
8. Feasibility of obtaining browser Bloch bands from precomputed
   converged mean-field variables; requires source-builder audit.
9. Whether to adopt visited-state/navigation features after the pilot.

## Maximalist wish list and staged publication

**Physics:** dispersion/Dirac migration; `Ubar` quadrature;
Berry/Chern; flux editor; CAR/projection checker; Gaussian-vs-exact;
field perturbation; vortex modes; phase diagram; dynamical response.

**Separate fixed-point lab:** Picard/damped/Anderson/Broyden/JFNK
trajectories; Jacobian-spectrum viewer; basins; gap-conditioning;
matrix-sign purification; map-evaluation costs; DIIS-history debugger.
Kitaev MF is a case study rather than the only admissible map.

**Reading:** default five-station spine, optional Recall/Depth/Evidence/
Tool/Playground detours, claim ledger with falsifiability criteria,
per-figure provenance, notation glossary and note map. No changes to
global site layouts.

**Later numerical widgets:** locally run the actual solver, export
versioned data with original commit, parameters, selected branch, seed
list, residual definition and map-evaluation telemetry; forbid padded
histories and interpolation across transitions/branches; report
held-out errors. JS interpolates precomputed values; no live Python.

**Reuse policy:** `kitaev-walk-geometry` is private at this audit.
Its mathematical notation and tests can inform the **independently
readable** public note, but no private files, internal URLs or
unreviewed passages should automatically be mirrored in site output.
Any future shared geometry exposition is explicitly reviewed for
publication and source provenance.

## Phase 0 acceptance and rollback

- `test/fixtures/kitaev-mf-dispersion/cases.v1.json`: exact
  dimensionless reference values and source conventions.
- `test/fixtures/kitaev-mf-dispersion/isotropic-r-reference.svg`:
  unpublished SVG of `r=|f|`.
- `test/unit/test_kitaev_dispersion_reference.py`: independent
  stdlib numerical tests of the complex zeros, momentum periodicity,
  isotropic geometric landmarks, anisotropic roots and gap minima,
  plus checks that fixtures cannot be mistaken for published assets.
- `make verify` must pass; no changed `site/content/`,
  `site/assets/`, `src/web_engine/`, or production workflows.

Undo by dropping the draft branch; there is no site-facing state.

