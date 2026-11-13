---
id: "open-followups-kitaev-defects-and-vortices"
title: "Open follow-up questions on line defects, operator realizability, and vortex dynamics"
subtitle: "Unpublished questions and exploratory calculations extending published work in Kitaev spin liquids"
date: "2026-11"
order: 10
visible: false
kind: "note"
tags:
  - "kitaev-model"
  - "line-defects"
  - "bcft"
  - "vortices"
  - "operator-realizability"
summary: "Why low-energy projection ($O \\mapsto P_{\\text{low}} O P_{\\text{low}}$) is non-multiplicative, how finite-length line defects and endpoint boundary conditions behave under scattering and conformal boundary conditions (BCFT), and what separates static $\\mathbb{Z}_2$ vortex gap reduction from selective dynamical control."
---

**1. Operator realizability versus formal power counting:** Because projecting a microscopic spin algebra onto a low-energy subspace ($O \mapsto P_{\text{low}} O P_{\text{low}}$) does not generally preserve operator products, an operator allowed by symmetry and power counting in a formal continuum expansion is not automatically realizable by local perturbations of the underlying lattice model:

$$\begin{aligned}
(P_{\text{low}} O P_{\text{low}})(P_{\text{low}} Q P_{\text{low}}) &= P_{\text{low}} O P_{\text{low}} Q P_{\text{low}} \neq P_{\text{low}} O Q P_{\text{low}}, \\[4pt]
\mathcal{O}_g(x) &= \big[i\gamma_R(x)\partial_x\gamma_R(x)\big]\,\big[i\gamma_L(x)\partial_x\gamma_L(x)\big], \qquad \Delta_g = 4,\; y_g = 2 - \Delta_g = -2.
\end{aligned}$$

Conversely, the absence of a gap within a restricted mean-field ansatz does not by itself guarantee nonperturbative protection. Which perturbations of a candidate effective theory actually arise from strictly local spin operators in a prescribed topological sector?

**2. Finite-length line defects, endpoint boundary conditions, and scattering:** In real Kitaev candidate crystals such as $\alpha\text{-RuCl}_3$, stacking faults and bond-altered seams have finite length $L$ or meet at $120^\circ$ junctions. When the infinite-seam Majorana theory is truncated to a finite segment of $N_d$ altered bonds, which microscopic endpoint perturbations realize consistent conformal boundary conditions (BCFT), how does the $T$-matrix govern bulk Majorana and vison scattering off the segment, and what happens when a finite spatial density $\rho_{\text{def}}$ of seams hybridizes across the bulk?

**3. Dynamical vortex preparation versus matter and flux leakage:** Extrapolation of our static Majorana mean-field energetics suggests electrically assisted vortex nucleation when potential-induced Dzyaloshinskii–Moriya terms are present. Following a time-dependent local tip bias $V_0(t)$ across competing flux sectors to quantify non-adiabatic leakage into matter fermions and unwanted vison pairs remains an open dynamical problem.
