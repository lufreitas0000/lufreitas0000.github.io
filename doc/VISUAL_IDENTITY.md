# Lu Freitas Personal Research Website — Visual Identity & Content Architecture (`VISUAL_IDENTITY.md`)

Date: 11 November 2026. Approved visual identity and content grounding specification (v3).

---

## 1. Core Message & Structural Principles

The website serves as a personal research home, living open CV, and scientific notebook for **Lu Freitas** (PhD in Physics, UFRN, 2024). Its architecture follows four guiding decisions:

1. **`Home` as a Single-Screen (`100vh`) Entrance / README Page (Zero Equations, Zero Scroll):**
   - Fits on a single standard desktop screen without scrolling.
   - Introduces Lu's scientific approach—connecting concrete lattice models to emergent low-energy descriptions and mathematical principles that constrain which phases, excitations, and responses nature can support, while viewing science as social knowledge—followed by a three-line directory (`Research`, `Notes`, `About`) and a clean, text-free, caption-free native vector honeycomb illustration in the right margin.
2. **Hyperlink & Visual Restraint (Distraction-Free Prose):**
   - Prose paragraphs across `Home`, `Research`, `Notes`, and `About` contain **zero mid-sentence hyperlinks**, eliminating visual clutter and supporting reading retention.
   - Hyperlinks appear only where structurally expected: the top navigation bar, the single contact/profile colophon strip, the single metadata line (`Journal · DOI · arXiv`) beneath each paper title, and the reference list or subpage links.
3. **Native Vector `.svg` Graphics & Epistemic Separation of Figures:**
   - All TikZ and arXiv figures are converted from vector PDFs to **native `.svg` vector graphics** via `pdftocairo -svg`.
   - On `Home` and `Research`, textual labels (`BT ... ET` blocks) and coordinate axes are stripped from the figures and **no captions are shown**, so the figures act purely as clean geometric visual identity alongside the prose.
   - On `Notes`, dedicated **PhD Thesis & MSc Dissertation Expository Chapter Notes** preserve and update the **labeled native `.svg` vector TikZ figures** alongside multi-line equations (`\begin{aligned} ... \end{aligned}`) that never require horizontal scrolling.
4. **Epistemic Grounding Across Pages (Aligned with Research Statement V10):**
   - `Research` gives primary prominence to the doctoral core (**Electric polarization near vortices in the extended Kitaev model**, *npj Quantum Mater.* 2024), followed by the diagnostic spectroscopic contrast (**STS of Majorana zero modes**, *PRB* 2023 vs. **Magnetic quantum impurities in 2D magnets**, *PRB* 2024), the operator-content obstruction along **Line defects in Kitaev spin liquids** (*PRB* 2022), and **Thermodynamic reversibility** (*RBEF* 2019).
   - `Notes` holds unpublished follow-up questions, incomplete calculations, modular thesis chapters, and the *Papers worth understanding* reading series.
   - `About` discusses broader intellectual horizons (joining formal AQFT / von Neumann algebras to QIQM, Lean 4 formalization, and social and feminist epistemology including Helen E. Longino's *Science as Social Knowledge* and William P. Thurston's *On proof and progress in mathematics*) in natural biographical prose.

---

## 2. Color Palette Specification

| Token | Value | Role & Origin |
| :--- | :--- | :--- |
| `--bg-paper` | `#FAF6EE` | **Warm Parchment Vellum** (matches `project-governance` Living Lab Book background; avoids stark `#FFFFFF` white glare) |
| `--bg-subtle` | `#F3EDE0` | **Soft Sand Tint** (used for multi-line equation blocks and subtle notes) |
| `--ink-primary` | `#2B2B2B` | **Deep Charcoal Ink** (`12.8:1` AAA contrast on `#FAF6EE`; avoids harsh `#000000` black) |
| `--rule-stone` | `#D1C7B7` | **Warm Stone Hairline** (`1px` horizontal section dividers and colophon rules) |
| `--bond-x-red` | `#E41A1C` | **Kitaev $x$-bond Scarlet Red** (`\bm{\delta}_x` down-left honeycomb bonds in thesis TikZ figures) |
| `--bond-y-green` | `#4DAF4A` / `#3B8E38` | **Kitaev $y$-bond Leaf Green** (`\bm{\delta}_y` down-right honeycomb bonds in thesis TikZ figures) |
| `--bond-z-blue` | `#00639A` | **Kitaev $z$-bond Cobalt Blue & Link Color** (`\bm{\delta}_z` vertical bonds and citation links) |
| `--normal-slate` | `#374151` | **Neutral Dark Slate** (replaces magenta for normal vectors $\mathbf{N}_x, \mathbf{N}_y, \mathbf{N}_z$) |
| `--accent-pink` | `#FFCCD7` | **Soft Light Pink** ($\mathbb{Z}_2$ vortex plaquette fill $W_p = -1$ and `Open question` margin pills) |
| `--accent-blue` | `rgba(91, 206, 250, 0.34)` / `#8FDDF9` | **Softened Translucent Light Blue** (less opaque than raw `#5BCEFA`, harmonizing with `#FFCCD7` for flipped-bond strings, equation left borders, and margin pills) |

---

## 3. Typography & Equation Layout (`Bitstream Charter`)

- **Primary Typeface:** **Bitstream Charter** (designed by Matthew Carter, 1987), loaded via **Charis SIL** (`font-family: "Bitstream Charter", "Charis SIL", "Charter", Georgia, serif`).
- **Heading Proportions:** Upright bold (`font-style: normal; font-weight: 700`), zero ALL CAPS, gentle `1.14x–1.20x` heading-to-body ratio, and `transform: scaleY(0.94–0.95)` vertical compactness.
- **No Horizontal-Scrolling Equations:** Zero equations appear on `Home`. On `Research` and `Notes`, equations use multi-line `\begin{aligned} ... \end{aligned}` blocks so the full mathematical expression is visible at once without horizontal scrollbars.
