# Precomputed Kitaev solver data — unpublished validation contract

**Status:** engineering infrastructure only. No physical dataset or trajectory has been published.

## Research and publication boundary

The website uses a three-part, interconnected research workflow:
literature/hypotheses; laboratory numerical experiments; and self-contained
published notes. An exported laboratory run is not automatically a publishable
result. The public kitaev-mf hub remains correct without solver widgets.

The user has selected: ferromagnetic, isotropic Kitaev honeycomb model,
field along [111], nominal 0 <= h <= 1. The field's units, sampling grid,
initial-state ensemble, seed count, observables and acceptance thresholds
are **TODO(Lu)**. Do not infer values from prior benchmark runs.

## Dataset contract (proposed schema_version=1)

One versioned JSON file per fully declared experimental campaign:

- \`publication_status\`: \`draft\` or \`reviewed\`; the validator does not
  certify physical correctness. Only \`reviewed\` data are candidates
  for a public article and require a scientific-review reference.
- \`provenance\`: exact 40-character upstream solver \`source_commit\`,
  experimental \`protocol_commit\`, executable \`reproduction_command\`,
  \`h_units\`, initial-state distribution, residual definition and
  method-specific frozen \`solver_configs\`.
- \`h_grid\`: ascending grid within user-declared [0,1] field domain;
  \`seeds\`: a precommitted list of distinct integers.
- \`runs\`: exactly one run for every (field, seed, solver). For each:
  \`initial_state_id\` shared across methods at fixed (field, seed),
  \`branch_id\`, \`segment_id\`, \`converged\`, categorized
  \`failure_reason\` (if not converged), \`map_evaluations\`, *raw*
  unpadded \`residual_history\`. Future observables may carry named
  units and independent validation metadata.
- \`scientific_review\` for reviewed data: review reference, held-out
  interpolation-error report, and explicit Lu-approved thresholds.
  Validation checks *presence*, never infers approval from CI.

The validator \`scripts/validate_kmf_solver_grid.py\` enforces syntactic,
paired-design and provenance consistency. It cannot check whether a
claimed source commit actually generated the data, whether a raw history
was fabricated, or whether a mean-field solution is physically correct.
Scientific audit and independent reproduction remain necessary.

## Interpolation — candidate only

\`test/support/kitaev_grid_interpolation.mjs\` exports a pure
segment-filtered candidate linear interpolator. It requires explicit
\`branch_id\` and \`segment_id\`, prohibits extrapolation and
cross-segment evaluation, and reports source grid nodes. This is **not
loaded by the website**.

Before publishing an interpolation widget:
1. Lu supplies h units, grid, branch semantics, observable and initial ensemble.
2. Run the actual solver locally with paired, recorded seeds and identical
   residual/stopping rules and precommitted solver hyperparameters.
3. Compare held-out actual solver observations against interpolation;
   report maximum/quantiles of errors by physical branch and phase segment.
4. Lu chooses acceptance thresholds and reviews the results; never
   interpolate over unresolved transitions or between stationary branches.
5. Publish data with a static figure/table, compressed size and reproducibility
   manifest. Record raw and compressed bytes and test on the local preview.
6. Do not extrapolate or interpret a solver branch as a physically proven phase.

## Open scientific decisions — TODO(Lu)

- Precise normalization and sampling of h in [0,1].
- Fixed initial-state distribution, seed list/count and confidence level.
- Solver methods and frozen damping/DIIS/Broyden/JFNK hyperparameters.
- Weighted residual norm, common stopping rule and iteration cap.
- Branch identification, transition-exclusion intervals and failure classification.
- Observables, held-out grid and numerical interpolation error thresholds.
- Weak/strong field exact orders and comparison targets.
- Whether the mean-field Bloch Hamiltonian can be reconstructed in the
  browser from stored converged covariances.

## Browser execution and dependency policy

No Pyodide, native solver, or new numerical framework runs in the browser.
Experimental data must be precomputed offline. The browser may eventually
interpolate a **validated** scalar table using the candidate algorithm;
full mean-field band recomputation awaits a distinct mathematical specification.

No synthetic numerical results in the contract's tests are physical claims.
Nothing in this infrastructure is linked from the published article.
