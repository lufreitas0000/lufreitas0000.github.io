---
id: "kitaev-derivation-jl"
title: "KitaevDerivation.jl: Symbolic derivations and formal proofs"
subtitle: ""
date: "2026-11"
order: 60
visible: true
kind: "project"
evidence_status: "expository-synthesis"
external_url: "https://github.com/lufreitas0000/KitaevDerivation.jl"
tags:
  - "hubbard-kanamori"
  - "kitaev-heisenberg"
  - "symbolic-computation"
  - "lean4"
keywords:
  - "Julia"
  - "Schrieffer-Wolff"
  - "fermionic CAR"
  - "computer algebra"
  - "formal verification"
summary: "A paused Julia symbolic derivation project, with a planned complementary Lean 4 proof track."
---

I started [`KitaevDerivation.jl`](https://github.com/lufreitas0000/KitaevDerivation.jl) to explore symbolic derivations of effective Kitaev and extended Kitaev–Heisenberg spin interactions from multiorbital Hubbard–Kanamori Hamiltonians. The intended approach keeps fermionic anticommutation relations, local multiplet projectors, and perturbative transformations explicit, rather than relying on unrestricted symbolic matrix diagonalization.

**The Julia development is currently paused.** I want to rewrite selected parts of the algebra in Lean 4 before resuming it, so the project can eventually pursue two complementary methods: Julia for symbolic computation and Lean for precise statements and machine-checked proofs. This remains a research and software-development direction, not a completed end-to-end derivation.

[GitHub repository](https://github.com/lufreitas0000/KitaevDerivation.jl)
