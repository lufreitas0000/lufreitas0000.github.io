---
id: "microscopic-superexchange-and-electric-polarization"
title: "Microscopic $t_{2g}^5$ superexchange and electric polarization around $\mathbb{Z}_2$ vortices"
subtitle: "Self-contained derivation of how virtual hopping in spin-orbit coupled honeycomb magnets generates spin-dependent charge dipoles and orbital quadrupoles"
date: "2026-10"
order: 15
visible: false
kind: "expository-note"
tags:
  - "kitaev-model"
  - "superexchange"
  - "electric-polarization"
  - "z2-vortices"
  - "quadrupole"
figures:
  - src: "../../assets/img/note-ch2-basis-vectors.svg"
    alt: "Honeycomb lattice basis vectors and nearest-neighbor bond vectors"
    kind: "labeled-svg"
    caption: "Bravais lattice vectors $\\mathbf{a}_{1,2}$, nearest-neighbor vectors $\\boldsymbol{\\delta}_{x,y,z}$, and boundary normals $\\mathbf{N}_{x,y,z}$."
  - src: "../../assets/img/note-ch7-vortex-cluster.svg"
    alt: "Symmetric honeycomb cluster with central Z2 vortex and flipped gauge links"
    kind: "labeled-svg"
    caption: "Honeycomb cluster hosting a central $\\mathbb{Z}_2$ vortex ($W_p = -1$) and flipped gauge string."
summary: "In edge-sharing $d^5$ transition-metal compounds with a $t_{2g}^5$ ($J_{\\text{eff}} = 1/2$) configuration such as $\\alpha\\text{-RuCl}_3$, virtual electron hopping across ligand bridges dresses magnetic exchange with local charge redistribution $\\delta n_l$ and orbital quadrupole moments $Q_{\\alpha\\beta}$ around $\\mathbb{Z}_2$ vortices."
---

In edge-sharing $d^5$ transition-metal compounds such as $\alpha\text{-RuCl}_3$, octahedral crystal-field splitting and strong spin–orbit coupling isolate a low-energy Kramers doublet $J_{\text{eff}} = 1/2$ in the $t_{2g}^5$ manifold. Even deep inside the Mott-insulating regime, virtual electron excursions between neighboring sites perturbatively dress the low-energy spin states with small charge fluctuations.

Applying fourth-order Schrieffer–Wolff projection to the three-orbital Hubbard–Kanamori Hamiltonian yields both the extended $JK\Gamma$ spin Hamiltonian and the effective spin-dependent local charge redistribution operator $\delta n_l$:

$$\begin{aligned}
\boldsymbol{\delta}_z &= \frac{\mathbf{a}_1 + \mathbf{a}_2}{3}, \qquad
\boldsymbol{\delta}_x = \frac{-2\mathbf{a}_1 + \mathbf{a}_2}{3}, \qquad
\boldsymbol{\delta}_y = \frac{\mathbf{a}_1 - 2\mathbf{a}_2}{3}, \\[4pt]
\delta n_l &= \sum_{\gamma \neq \gamma'} C_{\gamma\gamma'} \left( \mathbf{S}_l \cdot \mathbf{S}_{l+\boldsymbol{\delta}_\gamma} \right) + \text{anisotropic three-site virtual-hopping terms}.
\end{aligned}$$

When a $\mathbb{Z}_2$ vortex ($W_p = -1$) is present in the extended Kitaev model ($J, \Gamma \neq 0$), translation invariance is broken around the plaquette core. Evaluating $\langle \delta n_l \rangle$ self-consistently in real space reveals a radial charge imbalance and an in-plane electric dipole $\mathbf{P}_v$ together with a field-tunable orbital quadrupole moment $Q_{\alpha\beta}(\mathbf{h})$. See also the companion [Expository Physics Notes](../../notes/thesis-chapters.html) page for the full four-part derivation.
