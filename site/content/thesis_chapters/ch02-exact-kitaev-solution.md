---
id: "ch2-kitaev"
title: "Chapter 2 Note: Exact solution & $\mathbb{Z}_2$ gauge structure of the Kitaev honeycomb model"
order: 20
visible: true
citation_line: "Expository Physics Note · Kitaev Honeycomb Model"
figures:
  - src: "../assets/img/note-ch2-plaquette.svg"
    alt: "Labeled hexagonal plaquette p with sites p1 to p6"
    kind: "labeled-svg"
    caption: "Hexagonal plaquette $p$ with sites $p_1 \\dots p_6$ and bond-directional <span style=\"color:#E41A1C;font-weight:700;\">$x$</span>, <span style=\"color:#3B8E38;font-weight:700;\">$y$</span>, <span style=\"color:#00639A;font-weight:700;\">$z$</span> links."
  - src: "../assets/img/note-ch2-wilson-loops.svg"
    alt: "Non-contractible Wilson loops W(1) and W(2) on the honeycomb torus"
    kind: "labeled-svg"
    caption: "Non-contractible topological Wilson loop paths $W^{(1)}$ and $W^{(2)}$ across the honeycomb cluster."
---

On the honeycomb lattice with nearest-neighbor bond vectors $\boldsymbol{\delta}_x, \boldsymbol{\delta}_y, \boldsymbol{\delta}_z$, the Kitaev Hamiltonian couples spin-$1/2$ operators via bond-directional Ising interactions. Around each hexagonal plaquette $p$ with vertices $(p_1, p_2, p_3, p_4, p_5, p_6)$, the plaquette operator $W_p$ commutes with the Hamiltonian and partitions the Hilbert space into static $\mathbb{Z}_2$ flux sectors ($w_p = \pm 1$):

$$\begin{aligned}
H_K &= -K_x \sum_{\langle ij \rangle_x} \sigma_i^x \sigma_j^x - K_y \sum_{\langle ij \rangle_y} \sigma_i^y \sigma_j^y - K_z \sum_{\langle ij \rangle_z} \sigma_i^z \sigma_j^z, \\[4pt]
W_p &= \sigma_{p_1}^x \sigma_{p_2}^y \sigma_{p_3}^z \sigma_{p_4}^x \sigma_{p_5}^y \sigma_{p_6}^z = \prod_{\langle ij \rangle_\gamma \in \partial p} (-i\,\hat{u}_{\langle ij \rangle_\gamma}).
\end{aligned}$$

Representing each spin by four Majorana fermions ($\sigma_i^\alpha = i b_i^\alpha c_i$) enlarges the Hilbert space from $2^N$ to $4^N$. Physical states must satisfy the local gauge projection $D_i |\psi_{\text{phys}}\rangle = |\psi_{\text{phys}}\rangle$ with $D_i = b_i^x b_i^y b_i^z c_i$, and on a torus of $N = 2 L_1 L_2$ sites the global topological sector is additionally specified by two non-contractible Wilson loop operators $W^{(1)}$ and $W^{(2)}$.
