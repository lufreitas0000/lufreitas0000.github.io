---
id: "bosonize-lean"
title: "bosonize-lean: A finite-lattice playground for bosonization"
subtitle: ""
date: "2026-11"
order: 70
visible: true
kind: "project"
evidence_status: "expository-synthesis"
external_url: "https://github.com/lufreitas0000/bosonize-lean"
tags:
  - "bosonization"
  - "lean4"
  - "operator-algebras"
  - "finite-lattice"
keywords:
  - "fermionic CAR"
  - "polynomial CCR"
  - "finite energy cutoff"
  - "formal verification"
  - "renormalization group"
  - "continuum limit"
summary: "An ongoing personal theoretical playground: finite lattice bosonization, explicit energy cutoffs, and Lean 4 proofs."
---

[`bosonize-lean`](https://github.com/lufreitas0000/bosonize-lean) is my ongoing theoretical playground for understanding one-dimensional bosonization **first on a finite, discrete lattice with a finite energy cutoff**. I am interested in making the operator algebra, charge sectors, and projection remainders explicit before asking what survives a limit. Lean 4 helps me formulate and check statements across families of finite regulators. The project distinguishes finite fermionic CAR algebras from polynomial CCR constructions and formal power series; results at finite cutoff do not automatically establish continuum bosonization.

The longer-term question is how to construct and control the **continuum and infinite-volume limits**. Libraries such as [Mathlib](https://github.com/leanprover-community/mathlib4), [Physlib](https://github.com/leanprover-community/physlib), and [physicslib4](https://github.com/physicslib/physicslib4) already formalize relevant mathematical and quantum structures, but do not supply a ready-made limit construction for this particular system. I am following their development, Tadeusz Bałaban's multiscale renormalization-group methods, and the recent [OpenAI Yang–Mills Lean submission and its independent assessment](https://github.com/yang-mills-group/YM) as possible methodological references. Importing such ideas into this finite model is **future work**, not a result claimed here.

[GitHub repository and monograph](https://github.com/lufreitas0000/bosonize-lean)
