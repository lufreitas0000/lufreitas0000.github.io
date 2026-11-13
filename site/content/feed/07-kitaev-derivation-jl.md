---
id: "kitaev-derivation-jl"
title: "KitaevDerivation.jl: Symbolic effective spin models"
subtitle: ""
date: "2026-11"
order: 60
visible: false
kind: "project"
evidence_status: "exploratory-draft"
external_url: "https://github.com/lufreitas0000/KitaevDerivation.jl"
tags:
  - "hubbard-kanamori"
  - "kitaev-heisenberg"
  - "symbolic-computation"
keywords:
  - "Julia"
  - "Schrieffer-Wolff"
  - "fermionic CAR"
summary: "A Julia-based symbolic framework for deriving Kitaev-type spin interactions from multiorbital Hamiltonians."
---

[`KitaevDerivation.jl`](https://github.com/lufreitas0000/KitaevDerivation.jl) is a symbolic-computation project for organizing derivations from multiorbital Hubbard–Kanamori Hamiltonians to effective Kitaev–Heisenberg-type spin models. The intended pipeline treats fermionic anticommutation relations, local multiplet projectors, perturbative Schrieffer–Wolff transformations, and exchange-tensor extraction as explicit computational operations.

The emphasis is on preserving physical assumptions and checking intermediate algebra without relying on unrestricted dense symbolic diagonalization. The repository documents the proposed modules and verification requirements; those requirements should not be mistaken for completed analytical results.

[Source code and project scope](https://github.com/lufreitas0000/KitaevDerivation.jl)
