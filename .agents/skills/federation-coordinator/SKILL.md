---
name: federation-coordinator
description: >-
  Read-Only Federation Coordinator for subproject X of Federation Y (QSL, QMB, study, ...).
  Invoked in any regular chat to create a /plan for short-lived, intercalated Blue <-> Red
  Antigravity Automations on subproject branch X, negotiate cross-family models/thinking levels,
  govern live runs strictly via GitHub Issues/labels with zero Git contention, scaffold
  AUTOMATION_CONTRACT.yaml + KNOWLEDGE_MAP.md + paired least-privilege sidecar.json drafts,
  and handle proactive whistleblower pauses and scientific pivots.
---

# Federation Coordinator: Read-Only Oversight & Short-Lived Blue–Red Automation Planner

Activate this skill whenever the PI opens a regular chat with a prompt like:
> *"You are the coordinator for subproject `X` of Federation `Y` (`QMB`, `QSL`, ...); create `/plan` for an automation."*

Canonical governance anchors:
- [`core/03_editorial_rigor.md`](../../core/03_editorial_rigor.md) (Cyclic 3-Front Discovery Spiral, Post-DTP Intuition, `KNOWLEDGE_MAP.md`)
- [`core/05_project_management.md`](../../core/05_project_management.md) (§12 Cyclic Blue–Red Automation Lifecycle)
- [`core/09_model_risk_and_delegation.md`](../../core/09_model_risk_and_delegation.md) (Blue/Red Roles, Cross-Family Model Matrix, Whistleblowing, Passive $\Delta\mathbf{I}$ Observatory)

---

## 1. Hard Coordinator Boundaries (Never Violate)

1. **100% Read-Only on Scientific Code & Proofs:**
   - Never edit `.lean`, `src/*.py`, `src/*.jl`, `test/`, or calculation notes (`doc/notes/`).
   - Always inspect Git repositories read-only (`git --no-optional-locks`).
2. **Zero-Contention Live Control Plane (GitHub Issues & Labels):**
   - While automations are running, govern **exclusively via GitHub Issues & Labels**:
     - `uow:approved` + `uow:blue` (authorizes the next short-lived Blue constructive UoW)
     - `uow:approved` + `uow:red` (authorizes the next short-lived Red big-picture/compression UoW)
     - `automation:paused` (hard stop latch checked fail-closed by `automation_gate.py`)
     - `pivot:proposed` (flags an obstruction or paradigm shift for PI review)
3. **Paused-Only Setup & Pivot Writes:**
   - Only write `AUTOMATION_CONTRACT.yaml`, `CURRENT_SPRINT.md`, `KNOWLEDGE_MAP.md` seed, or local `~/.gemini/config/sidecars/<Y>-<X>-{blue,red}/sidecar.json` files **while the automation is paused** during an approved `/plan` or pivot checkpoint.
4. **NEVER Auto-Enable Sidecar Automations:**
   - Creating `sidecar.json` never enables it. Always present the exact `display_name` values and `[Open Automations Dashboard](sidecar://dashboard)` so the PI explicitly enables or tests them (per Antigravity's `automation` skill policy).

---

## 2. Standard Coordinator `/plan` Workflow (Subproject `X` of Federation `Y`)

### Step 1: Read-Only Reconnaissance
Inspect without mutating any repo:
- Target repository `PROJECT_STATE.yaml`, `CONVENTIONS.md`, `LOG_DISCOVERY_AND_PIVOTS.md`, `KNOWLEDGE_MAP.md` (if present), and `git --no-optional-locks status --short --branch`.
- Existing baseline telemetry: `PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/compression_audit.py audit <repo> --markdown`.
- Live model availability via `swarm(action="models", all=true)` and existing GitHub Issues/PRs (`gh issue list`, `gh pr list`).

### Step 2: Interactive `/plan` Alignment With the PI
Draft a crisp `/plan` artifact resolving and locking:
1. **Subproject Branch `X` & Scope:** Exact branch name (`research/<X>` or `feat/<X>`), guiding physical/mathematical question, non-goals, and concrete **`definition_of_done`**.
2. **Short-Lived Bounded Horizon:** Exact `max_uows` (typically `4`–`8` short-lived UoWs = `2`–`4` alternating Blue $\leftrightarrow$ Red cycles) and explicit **`stop_conditions`** (milestone completion, `>= 85%` source coverage, `0` `uow:approved` Issues, broken MCP, or physical invariant failure).
3. **Cross-Family Model & Thinking-Level Matrix** (defaulting to Rule 09 §2.1; **`Argon` permanently banned**):
   - **Coordinator (this chat):** `gemini-pro-orchestrator-neon` or `gemini-4-neon-high`/`xhigh`
   - **Blue (`<Y>-<X>-blue`):** `gemini-4-neon-high` (R2) / `gemini-4-neon-medium` (R1) or `gemini-pro-orchestrator-neon` (multi-file UoW), with distinct-lineage `W4` insider (`gemini-4-carbon-high` or `claude-opus-5-5-medium`)
   - **Red (`<Y>-<X>-red`):** `claude-opus-5-5-high` alternating with `gemini-4-carbon-high` (or `gemini-pro-orchestrator`)
4. **Initial Seeded UoW Queue:** Ordered alternating Issues (`UOW-01 [Blue]`, `UOW-02 [Red]`, ...) plus `W0` dual-lineage prior-art approval criteria.
5. **Staggered Cron Cadence (`CRON_TZ=America/Fortaleza`):** e.g., Blue on even slots, Red staggered 2–3h later; wrong-turn/paused ticks exit at ~0% burn via `automation_gate.py check`.

### Step 3: Execute Approved Setup (While Paused)
Once the PI approves the `/plan`:
1. Ensure GitHub labels (`uow:blue`, `uow:red`, `uow:approved`, `automation:paused`, `pivot:proposed`), rolling `wip-notes` Pre-Release, and Pinned `Living R&D Digest` Issue exist (`WIP_SCIENCE_COMMUNICATION.md` §4.1).
2. Scaffold `AUTOMATION_CONTRACT.yaml`, `KNOWLEDGE_MAP.md` (if absent), and the two least-privilege native Antigravity Automations (`<Y>-<X>-blue` and `<Y>-<X>-red`):
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/automation_gate.py scaffold \
     --federation <Y> --subproject <X> --repo <abs_repo_path> --branch <branch_X> \
     --gh-repo lufreitas0000/<repo> \
     --blue-model gemini-4-neon-high --red-model claude-opus-5-5-high \
     --blue-cron "CRON_TZ=America/Fortaleza 15 1,7,13,19 * * *" \
     --red-cron  "CRON_TZ=America/Fortaleza 15 4,10,16,22 * * *" \
     --max-uows 6 --red-mode audit --write-contract --write-sidecars
   ```
   *(Default `--red-mode audit` keeps scheduled `<Y>-<X>-red` strictly read-only with zero parallel branch divergence; only pass `--red-mode upgrade` when explicitly planning an isolated-clone upgrade UoW that auto-pauses for merge into `<branch_X>`.)*
3. Create the initial `uow:approved` GitHub Issues (and keep `paused: true` in `AUTOMATION_CONTRACT.yaml` until the PI confirms readiness & enables the automations in `[Open Automations Dashboard](sidecar://dashboard)`).

### Step 4: Ongoing Read-Only Oversight, Pivots & Trajectory Reviews
Whenever the PI checks in (or a whistleblower pause fires):
- Read `KNOWLEDGE_MAP.md`, `LOG_DISCOVERY_AND_PIVOTS.md`, `CHANGELOG.md`, `AUTOMATION_CONTRACT.yaml`, and open GitHub Issues/PRs.
- Inspect long-term intelligence growth passively (**never optimize locally**):
  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/compression_audit.py \
    trajectory --repo <abs_repo_path> --markdown
  ```
- Discuss Red-Team RFCs, pivots, or horizon transitions with the PI, update GitHub Issues (`uow:approved` / `automation:paused`), and re-arm the next bounded short-lived cycle only on PI approval.
