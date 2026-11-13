---
id: "kitaev-mf"
title: "kitaev-mf: Majorana mean-field theory"
subtitle: ""
date: "2026-11"
order: 50
visible: true
kind: "project"
evidence_status: "expository-synthesis"
external_url: "https://github.com/lufreitas0000/kitaev-mf"
tags:
  - "kitaev-model"
  - "majorana-mean-field"
  - "numerical-methods"
keywords:
  - "Kitaev spin liquid"
  - "real-space mean field"
  - "self-consistency"
  - "vortices"
figures:
  - src: "../../assets/img/gallery/feed/kitaev-mf-torus-geometry.svg"
    alt: "Honeycomb torus geometry for calculations involving Kitaev quantum magnets"
    kind: "labeled-svg"
    max_width: "100%"
summary: "Analytical and numerical tools for self-consistent Majorana mean-field calculations in Kitaev quantum magnets."
---

The [`kitaev-mf` project](https://github.com/lufreitas0000/kitaev-mf) develops analytical and numerical methods for Majorana-parton mean-field theory of Kitaev quantum magnets. It connects honeycomb-lattice models to self-consistent fermionic covariances and physical observables, including cases where spatial inhomogeneities require a real-space treatment.

The code separates lattice and algebraic definitions, numerical fixed-point solvers, and observables. Its completed first phase benchmarks solver behavior and analytical constraints in the ferromagnetic Kitaev model under a $[111]$ field; vortex, thermodynamic, and dynamical response calculations are subsequent research targets, not results already established by the software.

[Source code and technical documentation](https://github.com/lufreitas0000/kitaev-mf)
