---
id: "ch3-micro"
title: "Chapter 3 Note: Microscopic $t_{2g}^5$ superexchange & effective electric polarization operator"
order: 30
visible: true
citation_line: "Expository Physics Note · Spin–Orbit Superexchange"
figures:
  - src: "../assets/img/note-ch2-basis-vectors.svg"
    alt: "Honeycomb lattice basis vectors a1, a2, bond vectors delta_x,y,z, and normal vectors Nx,y,z"
    kind: "labeled-svg"
    caption: "Bravais lattice vectors $\mathbf{a}_{1,2}$, nearest-neighbor vectors $\boldsymbol{\delta}_{x,y,z}$, and boundary normals $\mathbf{N}_{x,y,z}$."
---

In edge-sharing $d^5$ transition-metal compounds such as $\alpha\text{-RuCl}_3$, crystal-field splitting and strong spin–orbit coupling isolate a Kramers doublet $j_{\text{eff}} = 1/2$. Perturbative projection of the three-orbital Hubbard–Kanamori model to fourth order in hopping yields both the extended $JK\Gamma$ spin Hamiltonian and the effective spin-dependent local charge operator $\delta n_l$:

$$\begin{aligned}
\boldsymbol{\delta}_z &= \frac{\mathbf{a}_1 + \mathbf{a}_2}{3}, \qquad
\boldsymbol{\delta}_x = \frac{-2\mathbf{a}_1 + \mathbf{a}_2}{3}, \qquad
\boldsymbol{\delta}_y = \frac{\mathbf{a}_1 - 2\mathbf{a}_2}{3}, \\[4pt]
\delta n_l &= \sum_{\gamma \neq \gamma'} C_{\gamma\gamma'} \left( \mathbf{S}_l \cdot \mathbf{S}_{l+\boldsymbol{\delta}_\gamma} \right) + \text{anisotropic three-site virtual-hopping terms}.
\end{aligned}$$

Consistency requires applying the same low-energy projection to both the Hamiltonian and the electromagnetic current/density operators before evaluating inhomogeneous expectation values around defects or vortices.
