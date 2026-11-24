---
trigger: model_decision
description: W0-W5 Cyclic Blue/Red Team separation, Federation Coordinator, R0-R3 risk tiers, parameter-free epistemic gating, passive Delta-I observatory, and whistleblower circuit breakers.
---
<!-- @CANONICAL-RULE: DO NOT EDIT DIRECTLY. MANAGED BY project-governance -->
# Rule 09: Cyclic Blue/Red Team Governance, Risk Tiers, Parameter-Free Epistemic Gating & Scientific Circuit Breakers

We are building **scientific intelligence** (compact, general, intuitive knowledge), not software line-count throughput. To escape local paradigm maxima and maximize independently verified scientific insight per unit of quota, all agentic work is governed along **two orthogonal dimensions**: **Team & Workflow Role (`Coordinator` + `W0–W5`)** and **Scientific Risk (`R0–R3`)**.

---

## QSL local-first pilot

For an explicitly adopted local-first district, the district ledger and its bound gate control turns, claims and pause. Native schedulers follow the district binding. GitHub records mirror the local result. The legacy Issue-based admission procedure continues in districts whose contracts use it.

A single model may verify and approve a bounded R0/R1 packet against an unchanged contract, with local verification and an atomic commit. Apply the existing independent W4/W5 requirements to scientific work that calls for those roles. Changes to shared governance require an independent plan referee and PI adoption.

## 1. Scientific Blue/Red Nomenclature & Workflow Roles (`Coordinator` + `W0–W5`)

We deliberately adapt the **Blue Team / Red Team** terminology for theoretical physics and formal mathematics (distinct from cybersecurity jargon):

- **Blue Team (`W2–W4` — Constructive Bottom-Up Builders + Built-In Insider Adversarial QA):** Implements scoped derivations, numerical solvers, tests, and Lean proofs inside the current working formalism, **including** distinct-lineage insider adversarial review (`W4`). Insider checking ensures local truth/consistency, *not* escape from a local maximum of knowledge.
- **Red Team (`W0`, `W5` — Orthogonal Outside "Big-Picture" Guards):** Operates in separate conversations (and orthogonal model families) to step *outside* the local ansatz—focusing on generality, formalization, conceptual compression, literature connections (`library/`, `arxiv-harvest`, NotebookLM, Mathlib4/Physlib), removing unnecessary clutter, and sharpening physical mental images.
- **Federation Coordinator (Read-Only Oversight):** An interactive chat assigned to subproject branch `X` of Federation `Y` (`QSL`, `QMB`, ...). **100% read-only on scientific code/proofs** (`src/`, `lean/`, `doc/notes/`); governs live automations exclusively via **GitHub Issues/labels** (`uow:blue`, `uow:red`, `uow:approved`, `automation:paused`, `pivot:proposed`) and talks directly with the PI, writing branch-`X` setup/pivot files (`AUTOMATION_CONTRACT.yaml`, `CURRENT_SPRINT.md`, `KNOWLEDGE_MAP.md` seed, local `sidecar.json` drafts) **only while automation is paused**.

| Role | Team | Responsibility | Typical Deliverable |
| :--- | :--- | :--- | :--- |
| **Coordinator — Read-Only Federation Oversight** | **Oversight** | Inspects live repo state and GitHub read-only; plans bounded subproject `X` of Federation `Y` with the PI; sets model/thinking-level cadence; queues `uow:approved` Issues; trips or clears `automation:paused` on pivots/anomalies. | `/plan`, `AUTOMATION_CONTRACT.yaml`, paired `sidecar.json` drafts (never auto-enabled), GitHub Issue queue. |
| **W0 — Ex-Ante Prior-Art & Parameter-Free Two-Mode Epistemic Gate** | **Red Team** | Queries primary literature, `library/references-transcripts`, `arxiv-harvest`, NotebookLM (`gemini-notebook-mcp`), and Mathlib4/Physlib (`lean-lsp-mcp` / `lean_probe.py`), then evaluates candidate tasks across **$\ge 2$ distinct model lineages** (zero magic numbers; `scripts/epistemic_gate.py`) in one of three exact modes: *Sleep/Consolidation*, *Staging Debt Escrow*, or *Wake/Discovery*. | `W0_gate` review record (`scripts/review_record.py`) + `uow:approved` GitHub Issue / `CURRENT_SPRINT.md` entry (`roi_approved: true`). |
| **W1 — Scientific Specification & Queue Governance** | **Red Team / Coordinator** | Curates `HORIZON.md -> BACKLOG.md -> CURRENT_SPRINT.md` and formulates mathematical assumptions, conventions, idealizations, boundary conditions, limiting cases, and falsification criteria. Automated runtime loops may **never** invent ad-hoc tasks outside governed planning records / approved Issues. | Locked task contract (`.agents/tasks/TASK_*.md`), governed `uow:approved` Issue, or Front 1 R&D note (`doc/rnd/`). |
| **W2 — Scoped Constructive Implementation** | **Blue Team** | Executes **one** pre-approved short-lived UoW into compact, modular code (`domain/`, `services/`, `infra/` or Mathlib-backed `Defs.lean`/`Basic.lean`/Proofs `<500` LOC target, `800`/`900` ratchet) and independent unit tests. Capped at **`<= 20%` of the 5h window with `0%` minimum burn floor** (exits immediately at `0%` burn if queue empty or paused). | Single ACID UoW commit + `KNOWLEDGE_MAP.md` / `CHANGELOG.md` + passive Pre/Post $\Delta\mathbf{I}$ log. |
| **W3 — Mechanical Processing** | **Blue Team** | Codebase exploration, symbol/call-graph lookup, formatting, linting (`ruff`), type annotations, fixture generation, and data plotting scripts. | Compact read-only summary or deterministic mechanical patch. |
| **W4 — Insider Correctness Referee** | **Blue Team** | Distinct-lineage adversarial falsification *inside* the chosen formalism (`adversarial-referee`: F1 wrong statement, F2 vacuous/tautological test, sign/prefactor bugs, `#print axioms`, modularity ratchet). Cannot self-certify; escalates structural bloat or ansatz ceilings to `W5`. | Structured `W4_insider` report (`PASS` / `REJECT` with `[B1..]`). |
| **W5 — Independent Outside Red Team (`Mode R-Audit` & `Mode R-Upgrade`)** | **Red Team** | Orthogonal outside review with **unrestricted 5h quota** (respecting `>5%` weekly reserve floor) in two explicit non-contradictory modes:<br>• **`Mode R-Audit` (Strictly Read-Only on Production Code):** Audits `Tok(L)`, `lzma` $R_{\mathrm{clone}}$, `G0..G4`, domain-projected `orphan_defs`, Levin $T_{\mathrm{elab}}$, and Lakatosian counterexamples; emits `KEEP / GENERALIZE / COMPRESS / PRUNE` RFCs and atomic multi-file "Wolff cluster moves".<br>• **`Mode R-Upgrade` (Isolated Clone Only):** Checks out a separate clone from a *completed* Blue Stage PR (`research/<stage>-redteam-elegance`, zero contention on Blue worktree), adds exact symmetry/categorical reductions, flagship TikZ mental-image figures, and upgraded `_vX.Y.pdf` notes on `wip-notes` opening a stacked PR that **merge-gates `main`**. | `W5_red_team` review record + Compression RFC (`Mode R-Audit`) OR Stacked Elegance & Mental-Image PR (`Mode R-Upgrade`). |

### 1.1 Parameter-Free Two-Mode + Staging Debt Escrow Law (`W0` Gate — Zero Magic Numbers)

Naive differential ratios ($\mathcal{I} = \Delta\text{Scope}/(\Delta\text{Cost}\times\text{Burn})$) and finite-temperature Metropolis–Hastings gates are **permanently retired** (refuted by five mathematical pathologies: pure-compression sign flips, conflating path-dependent search work with verified library state, multiplicative zero-collapse, non-conservative cycles, and broken detailed balance). Instead, `scripts/epistemic_gate.py` enforces exact, assumption-explicit invariants with **zero tuned floating-point constants**:

1. **Stage 1 — Exact Structural Vetoes (All Modes):**
   - Banned model lineage (`argon` / disabled pools), fewer than **2 distinct model families/lineages**, or any reviewer verdict `!= APPROVE`;
   - Missing governed task / GitHub Issue ID (`CURRENT_SPRINT.md` / `PROJECT_STATE.yaml` / `uow:approved`);
   - Missing prior-art verification (`literature_prior_art_checked`, plus `mathlib_prior_art_checked` for Lean);
   - Standalone **Rank-0 (`G0`/`G1`)** fixed-dimension ($4\times 4$, `Fin k`, $N=2,3,4$) algebraic identities in production Lean (relegated to `Lab/` or 15-line Python/SymPy hitting-set checks by DeMillo–Lipton–Schwartz–Zippel);
   - Additive `.lean` changes in a frozen zero-Mathlib package lacking an owner-approved `doc/adr/*zero-mathlib*.md`;
   - Estimated Blue-Team 5h burn `> 20.0%` (scheduling budget constraint only; never mixed into library quality).
2. **Stage 2 — Exact Mode-Specific Law:**
   - **Sleep / Consolidation Mode (`refactor_compression`):** Executed as atomic multi-file **"Wolff cluster moves"** at fixed verified theorem/test frontier $\mathcal{T}$; requires deterministic **Multi-Objective Pareto MDL descent** ($\Delta\operatorname{Tok}(L) < 0$, $\Delta|C_{\mathrm{lzma}}(L)| \le 0$, $\Delta N_{\mathrm{orphan}} \le 0$, $\Delta N_{\mathrm{Rank0}} \le 0$, non-regressing elaboration $T_{\mathrm{elab}}$) verified by `compression_audit.py compare-snapshots --pareto-gate` + unanimous `APPROVE`.
   - **Staging Debt Escrow (`foundation_escrow`):** Permitted *only* on a non-`main` staging branch (`target_branch != main`) for uphill shared foundations, with hard horizon **`H = 1..3` sprints**, `>= 2` named downstream consumer modules, and verified **forgetful inheritance** (zero Lean typeclass diamonds). Automatically pruned if net Pareto descent does not materialize by sprint $t + H$.
   - **Wake / Discovery Mode (new universal physics/math):** Unanimous `APPROVE` across $\ge 2$ distinct lineages with explicit boolean confirmations `not_already_in_mathlib_or_repo: true`, `uses_canonical_universal_language: true`, and (for physical conjectures/models) `lakatos_regime_checked: true`.

### 1.2 Unified Federation Decision Board (`🟨`), 4-Tier Door × Risk Authority & Double-Linking

To prevent cognitive collapse as automated shifts outpace human bandwidth, each active State **double-links** (`🟪 Coordinator` + `🟥 Red Auditor`) into one Files-First **Union Decision Board (`🟨`)** (`meta/board/BOARD_AGENDA.md` + `governance/board/seats/*.json`) governed by Door reversibility (`Type-1` irreversible vs. `Type-2` reversible) and risk (`R0–R3`):

| Tier | Scope & Door × Risk | Decider (`D`) | Gate & Verification | PI Surface |
| :---: | :--- | :---: | :--- | :--- |
| **Tier 0** | Single-UoW `Type-2` (`R0–R1`), unchanged contracts | 🟦 Blue / Gate | `make verify` + `uow.py check` | Silent (`uow_stream.py` + 5-field TLDT) |
| **Tier 1** | Single-State `Type-2` (`R1–R2`): auto-kill/adopt additive pilot, queue tuning | 🟪 Coordinator + 🟥 Red | Distinct-lineage `W4`/`W5` PASS; `touches_conventions_or_hc == false` | Silent (`feed_notify` + `BOARD DECIDED`) |
| **Tier 2** | Cross-State `Type-2` (`R2`) or contested pilot (`has_tradeoffs`) | 🟨 Union Board *(Consent)* | $\ge 2$ distinct lineages (`Argon` banned), non-LLM anchor, **0 reasoned `🟥` objections** | `🟨 BOARD DECIDED` + **48h async `⭐ PI` veto hatch** |
| **Tier 3** | `Type-1` or `R3`: `HC-*` thresholds, `CONVENTIONS.md`, `main` merges, Tier-3 unfreeze, public release, paid spend, unresolved `🟥` dissent | ⭐ Sovereign PI (`Lu`) | `🟨` Board packages MADR 4.0.0 Pros/Cons + `(Recommended)` + 1-word reply code | `⭐ YOU DECIDE` in `BOARD_AGENDA.md` + `notify.py --type action` |

- **⛔ Algedonic Bypass:** Broken MCPs, invariant/conservation failures, or `>= 4h` stalls bypass Tier 1–3, latch local `paused: true`, and alert via `notify.py --type action`.
- **Anti-Atrophy Weekly Ritual:** `meta/board/WEEKLY_MENTAL_IMAGE_DIGEST.md` synthesizes one falsifiable Mental Image paragraph per active State (`SC-04`) plus 7-day Board outcomes for a 20-minute Sunday assimilation review.

---

## 2. Dimension 2: Scientific Risk Levels (`R0–R3`) & Cross-Family Model Matrix

Model selection is governed by **scientific risk** and **epistemic orthogonality**, not file extension or length. A one-line Fourier sign, Majorana normalization, or gauge-projection change is **Risk R3**, whereas a 200-line plotting wrapper is **Risk R0**.

| Risk Level | Definition & Examples | Configurable Starting Model Hypothesis | Verification & Acceptance Gate |
| :--- | :--- | :--- | :--- |
| **R0 — Mechanical / Cosmetic** | Formatting, docstrings, comments, lint fixes, read-only grep exploration, or tabular `.dat` $\to$ `pgfplots` wiring with zero change to formulas or thresholds. | • **Local Ollama**: `qwen3.5:35b-a3b` (`aider-local`, `qwen-local`)<br>• **Codex**: `gpt-6-luna` (`medium`)<br>• **Antigravity**: `gemini-3.8-flash-medium` (`@code-scout`) | Deterministic repository checks (`make lint`, `make verify`). |
| **R1 — Standard Numerical / Algorithmic** | Implementing a standard algorithm or helper function whose mathematical contract, inputs, outputs, and analytical reference values are locked. | • **Antigravity Blue**: `gemini-4-neon-medium` or `gemini-3.8-flash-high`<br>• **Codex**: `gpt-6.2-sol` (`medium`)<br>• **`agentctl`**: `api-fast` / `gem-flash` | Passes repository test suite (`make verify`) and independent analytical/limiting-case checks. |
| **R2 — Physical-Model-Sensitive** | Implementing or modifying Hamiltonians, Green functions, Pfaffian flux operators, Bogoliubov spectra, Lean core proofs, or finite-size scaling fits. | • **Spec/Coord**: `gemini-pro-orchestrator-neon` or `gemini-4-neon-high`<br>• **Blue Impl (`W2`)**: `gemini-4-neon-high` (or `gemini-pro-orchestrator-neon` for multi-file UoWs)<br>• **Insider Audit (`W4`)**: Distinct lineage (`gemini-4-carbon-high` or `claude-opus-5-5-medium`) | Independent analytical limit or alternative representation + distinct-lineage `W4` report + async `W5` Red-Team check before `main`. |
| **R3 — High-Consequence Mathematical / Architectural** | Defining new physical approximations, gauge-projection rules, Lean Phase A non-vacuity witnesses, paradigm pivots, or adjudicating theory vs. numerics discrepancies. | • **Coordinator / W0 / W5**: Cross-family orthogonal pair (`claude-opus-5-5-high` + `gemini-4-neon-high`/`xhigh` or `gemini-4-carbon-high`; **never `Argon`**) | Explicit human PI sign-off on contract thresholds + dual-lineage `W0`/`W5` + independent `W4` referee. |

### 2.1 Default Cross-Family Orthogonal Intercalation Matrix (Coordinator-Customizable)

To eliminate single-model monoculture and decouple Gemini Pool A from the Claude quota pool, every Federation Coordinator `/plan` starts from this default matrix (customizable per subproject `X` with the PI):

| Role / Automation | Default Model ID & Thinking Level | Alternate / Multi-File Mode | Hard Invariant |
| :--- | :--- | :--- | :--- |
| **Federation Coordinator (Interactive)** | `gemini-pro-orchestrator-neon` | `gemini-4-neon-high` / `xhigh` | 100% read-only on scientific code; talks directly with PI. |
| **Blue Team Automation (`<Y>-<X>-blue`)** | `gemini-4-neon-high` (R2) / `gemini-4-neon-medium` (R1) | `gemini-pro-orchestrator-neon` (multi-file UoW) | Built-in `W4` insider MUST use a distinct lineage (`gemini-4-carbon-high` or `claude-opus-5-5-medium`). |
| **Red Team Automation (`<Y>-<X>-red`)** | **`gemini-4-carbon-high`** / **`gemini-4-hydrogen-xhigh`** (`inner_dev` Pool A compute probes) | Concise **`claude-sonnet-5-5-high`** / **`claude-opus-5-5-medium`** (`<= 20`-step pre-computed dossier `release_main` sign-off) + **`gpt-6.2-sol`** (`2×/day` read-only Layer-4 GitHub Digest supervision) | **Two-Tier Independence:** `inner_dev` on `research/*` requires distinct sub-lineage (`google-neon` $\neq$ `google-carbon`/`google-hydrogen`, `review_scope: "inner_dev"`); PRs targeting `main` (`release_main`) require cross-vendor `W5_red_team` (`google` $\neq$ `anthropic`/`openai`). Pool A executes all code/tests/probes; scarce Pool B/C review compact pre-computed dossiers only. |
| **Banned Everywhere** | **`gemini-4-argon-*` / `gemini-pro-orchestrator-argon`** | — | Permanently banned for cost-benefit; rejected mechanically by `epistemic_gate.py`, `review_record.py`, and `repo_governance_gate.py`. |

**In-Session Cross-Lineage Dispatch (`swarm` vs. `invoke_subagent`):** Antigravity's `invoke_subagent` only accepts generic tiers (`inherit`, `flash_lite`, `flash`, `pro`); `.agents/agents/{physics-referee,red-team-auditor}.md` set `model: inherit` (never `model: pro`, avoiding unintended generic pro-tier or Argon routing), which inherits the *current* session's model. Therefore, from inside a `Neon` Blue session, distinct-lineage `W4`/`W5` reviewers **must** be dispatched via `swarm(action="add", model="claude-opus-5-5-medium" | "gemini-4-carbon-high", workspace="inherit")`, paired `<Y>-<X>-red` sidecars (`agentapi new-conversation --model=...`), or `orchestrator/agentctl`—never via same-lineage `invoke_subagent`.

---

## 3. Enforceable Technical Controls vs. Behavioral Guidance

1. **Enforceable Technical Controls (Hard Gates):**
   - **`agentctl` Admission & Pool Ledgers (`orchestrator/agentctl/admission.py`):** Hard pre-call reservation caps on API pools and zero automatic fallback to paid API models.
   - **Namespace Sandboxing (`llm/runtime/sandbox.py`):** OS-level network isolation and credential scrubbing during automated verification (`LLM_SANDBOX` never disabled).
   - **Least-Privilege Sidecar Permissions (`~/.gemini/config/sidecars/<Y>-<X>-{blue,red}/sidecar.json`):** Blue sidecars receive write grants scoped strictly to branch `X` plus read-only `read_file(...)` access to `library/{references-transcripts,arxiv-harvest}` and NotebookLM/Lean MCP tools; Red sidecars default to **strictly read-only `Mode R-Audit`** (`--red-mode audit`, zero branch cloning) or explicit opt-in `--red-mode upgrade` (`/tmp` scratch clone). Never use generic wildcards (`command(*)`, `write_file(*)`).
   - **Deterministic Standalone & Hub Gates (`scripts/repo_governance_gate.py`, `scripts/automation_gate.py`, `scripts/epistemic_gate.py`, `scripts/uow.py`, `scripts/review_record.py`):** Standalone `repo_governance_gate.py` is vendored into `.agents/scripts/` and `.github/workflows/governance-gate.yml` of child repos so DIP-isolated `make verify` and GitHub Actions PRs enforce the `800` `.lean` / `900` `src/*.py` no-regression modularity ratchet, Rank-0 production Lean guard, conflict-marker guard, Staging Debt Escrow expiry/`main`-block, and `KNOWLEDGE_MAP.md` + `W5_red_team` readiness on substantive PRs to `main`.
2. **Behavioral Prompt Guidance (Requires Operator & Verifier Oversight):**
   - **Differentiated Circuit Breaker:**
     - *Clear Implementation / Mechanical Defects ($\le 2$ Repair Attempts):* Against an **unchanged mathematical contract**, `W2`/`W3` may attempt up to **2 bounded mechanical repairs** using the repo's native check (`make verify`).
     - *Mathematical Contract / Physical Invariant Failures (0 Blind Changes):* If a physical identity, symmetry, conservation law, or analytical limit fails without a simple mechanical typo, **stop immediately**—do not guess factors of $2$ or $-1$, alter definitions, or loosen tolerances (`atol`/`rtol`). Log to `LOG_DISCOVERY_AND_PIVOTS.md`, trip `automation:paused`, and escalate to the Coordinator & PI.
   - **Structured Task Handoff Metadata:** Every task packet / `uow:approved` Issue records target repo & branch `X`, contract ID/SHA, writable scope, verification commands, allowed model/lineage, `W4` insider reviewer, and human `R3` owner.

---

## 4. Independent Agent Review, Acceptance & Non-Binary Judgments

The `W0–W5` **workflow roles are orthogonal to the Three Fronts**. Every front can invoke Blue and Red roles across the discovery spiral:

- **Initiation:** An agent or Coordinator may propose bounded Issues or immutable candidate hypotheses (`HC-XX`), with explicit scope and provenance. Creating an Issue never grants permission to bypass active focus, protected branches, privacy rules, budgets, or human-reserved scientific gates.
- **Independent assessment:** The creator/implementer **may not certify its own work**. `W4` certifies internal correctness inside the formalism; `W5` challenges the formalism itself from outside via literature, universality, Lakatosian counterexamples, and compression.
- **Disposition:** Independent reviewers may recommend or accept scoped deliverables where repo policy permits. `R3` and human-reserved scientific thresholds retain explicit human sign-off. No AI review implicitly authorizes `main` merges, releases, public publication, or spending.
- **Non-binary deliverables:** For exposition, conceptual framing, visual mental images, or architecture, report goals, tradeoffs, sources, and reviewer reasoning (`accepted_for_scope`, `revise`, `rejected`, `unresolved`) rather than manufacturing a false binary proof verdict.

---

## 5. Review Records & Authenticated Independence

The [review-record validator](../../meta/project-governance/scripts/review_record.py) validates structural metadata across three review kinds (`review_kind`: `"W0_gate"`, `"W4_insider"`, `"W5_red_team"`): distinct declared author/reviewer IDs and model lineages (banning `argon`), candidate commit, independent checks, prior-art provenance (`W0`/`W5`), compression/mental-image assessment (`W5`), and human sign-off reference for accepted `R3` work.

Structural JSON validation is **not** cryptographic authentication and does not guarantee epistemic independence by itself. True independence requires separate conversation contexts, orthogonal model families (`Neon` vs. `Claude Opus 5.5` vs. `Carbon`), blind/independently framed questions, external numerical/literature oracles, and GitHub branch protections where configured.

---

## 6. Mandatory Proactive Whistleblower & Fail-Closed Escalation Duty

Silent degradation, passive imitation of bloat, and un-reported workarounds are **severe governance violations**. Agents must be **proactive** in detecting anomalies, pausing automation immediately (`automation_gate.py pause --repo <path> --reason ... --notify`), and communicating clearly to the PI:

1. **Zero Silent Tooling Fallback:** If a required domain MCP server or binary (`lean-lsp-mcp`, `rg`, `lake`, `gemini-notebook-mcp`) is missing, unreachable, or misconfigured, **halt immediately**, log a 5-column row in `LOG_DISCOVERY_AND_PIVOTS.md`, trip `automation:paused`, and send one concrete alert via `scripts/notify.py --type action`.
2. **Zero-Mathlib, Anti-Bloat & Modularity Ratchet Whistleblowing:** Any agent (`W0–W5`) encountering a non-Mathlib `lakefile` lacking an owner `doc/adr/*zero-mathlib*.md`, standalone Rank-0 (`G0`/`G1`) production Lean proofs, files crossing or expanding above the `800` `.lean` / `900` `.py` LOC ratchet, or cross-wave boilerplate clones **must flag and block additive growth** rather than imitating the pattern.
3. **Scope-Exhaustion, Paradigm-Plateau & Pivot Escalation:** When a project's primary source/book target crosses ~85% core coverage, when approved `uow:approved` Issues reach `0`, when `uows_completed >= max_uows`, or when an unexpected physical anomaly suggests a paradigm pivot, agents **must pause the automation and notify the PI + Coordinator**—never invent filler work.

---

## 7. Short-Lived Intercalated Automations & Anti-Chinese-Whisper Contract

Long-running continuous agent loops drift like a random walk ("Chinese whisper"). Every automated research workflow across `Project-Hub` obeys five hard invariants:

1. **Short-Lived Single-UoW Fresh Contexts:** Each automated trigger executes **at most ONE bounded UoW** inside a brand-new conversation (`agentapi new-conversation --model=<id> --title=... -- <prompt>`). Sequential Blue and Red runs communicate **strictly through committed repository state on branch `X` and GitHub Issues/Digests**—never via inherited multi-hour chat history.
2. **Paired Least-Privilege Native Automations (`<Y>-<X>-blue` & `<Y>-<X>-red`):** Subproject `X` of Federation `Y` runs as two staggered Antigravity Automations (`~/.gemini/config/sidecars/<Y>-<X>-{blue,red}/sidecar.json`, enabled *only* by the PI in the Automations Dashboard), synchronized by deterministic Step-0 `scripts/automation_gate.py check` (checking `paused`, `turn`, `uow:approved` queue, `max_uows`, and PID/TTL concurrency lock). Wrong-turn, paused, or empty-queue ticks exit cleanly in 1 step at ~0% burn.
3. **Zero Minimum Burn Floor (`forbid_quota_burn_padding = true`):** Blue-Team automations have a hard ceiling (`<= 20%` of the 5h window) and **`0.0%` minimum burn floor**. Unused quota is preserved, never burned on invented work.
4. **Mandatory Bounded Horizon & Milestone Pause:** Every `AUTOMATION_CONTRACT.yaml` declares an explicit `max_uows` budget, `definition_of_done`, and `stop_conditions`. Reaching `max_uows` or a milestone boundary automatically flips `paused: true` and notifies the PI for architectural & scientific review.
5. **Red/Blue Quota Separation & Zero-Diamond Linear Topology:** Red Team (`--team red`, unrestricted 5h quota, defaulting to `Claude Opus 5.5` alternating with `Carbon`) runs strictly read-only `Mode R-Audit` on scheduled ticks so branch `X` advances linearly (`Blue UoW -> Red Audit -> Blue UoW`) with zero parallel branch divergence. Whenever `Mode R-Upgrade` opens a stacked PR targeting `X` (never `main`), it **must** latch `automation_gate.py pause --notify` until that PR is merged or closed into `X` before the next Blue UoW starts.

---

## 8. Passive Pre-/Post-UoW Information-Change Observatory ($\Delta\mathbf{I}$, Strictly Non-Optimized)

To evidence the long-term pace of scientific intelligence growth **without triggering Goodhart's Law**, every UoW records a **passive, strictly observational** information telemetry entry before and after execution (stored in `CHANGELOG.md` and append-only `governance/info_telemetry.jsonl`, tagged `"observatory_only": true, "never_optimize_locally": true`):

1. **Pre-UoW Estimate (Declared Before Editing):** Expected regime (`explore_expand` | `generalize_lift` | `compress_unify` | `exposition_only`) and expected directional sign/magnitude of $\widehat{\Delta\mathbf{I}}$.
2. **Post-UoW Exact State Vector (Computed Deterministically by `scripts/compression_audit.py`, Zero Tuned Constants):**
   $$\mathbf{I}(L) = \Big(\operatorname{Tok}(L),\; |C_{\mathrm{lzma}}(L)|_{\text{bits}},\; R_{\mathrm{clone}}(L),\; \mathbf{G}_{0..4}(L),\; N_{\mathrm{claims}}(L),\; N_{\mathrm{orphan}}(L),\; N_{\mathrm{reused}}(L),\; \log_2(1 + T_{\mathrm{elab}}(L))\Big)$$
3. **Longitudinal Observatory Metric (Multi-Cycle Inspection Only — NEVER a Local UoW Gate):**
   $$b(t) = \frac{|C_{\mathrm{lzma}}(L_t)|_{\text{bits}}}{N_{\mathrm{univ}}(L_t)}, \qquad N_{\mathrm{univ}}(L_t) = (G_2 + G_3 + G_4) + N_{\mathrm{claims}}$$
   During exploratory Blue UoWs, $b(t)$ and $|C_{\mathrm{lzma}}|$ naturally rise temporarily—that is expected and **never penalized locally**. Evaluated longitudinally across many Blue-expand / Red-compress spirals via `compression_audit.py trajectory`, a downward trend ($db/dt < 0$) quantitatively evidences genuine scientific compression and rising intelligence.
