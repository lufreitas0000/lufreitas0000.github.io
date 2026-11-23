---
name: governed-blue-team
description: >-
  Workspace-wide Governed Blue Team Execution Skill (W2 constructive bottom-up implementation,
  W3 mechanical checks, W4 distinct-lineage insider referee). Runs short-lived single-UoW
  conversations synchronized by automation_gate.py, enforces <=20% 5h quota cap with 0% burn floor,
  fail-closed lean-lsp-mcp + preflight gates, 800/900 LOC no-regression modularity ratchet,
  passive Pre-/Post-UoW Delta-I observatory logging, continuous KNOWLEDGE_MAP.md / wip-notes
  deliverables, and proactive Rule 09 §6 whistleblower pausing.
---

# Governed Blue Team: Short-Lived Single-UoW Constructive Execution & Built-In `W4` Verification (v3.0)

Activate this skill whenever executing **Blue-Team constructive implementation or consolidation UoWs (`W2` / `W3` / `W4`)** across any repository in `/home/lu/Projects`.

*(Note on terminology: Blue Team encompasses bottom-up constructive builders AND their built-in distinct-lineage insider adversarial referee `W4`. Outside big-picture generalization, literature compression, and clutter removal belong to the orthogonal Red Team via `scientific-red-team`.)*

---

## 1. Hard Fail-Closed Pre-Flight (Before Writing 1 Line of Code)

1. **Step 0 — Turn-Lock, Pause-Latch & Queue Check (Short-Lived Automations):**
   - If running under an `AUTOMATION_CONTRACT.yaml` subproject (`<Y>-<X>-blue`):
     ```bash
     PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/automation_gate.py \
       check --repo <repo_path> --role blue
     ```
   - If `proceed: false` (paused, `turn != blue`, `uows_completed >= max_uows`, or `0` `uow:approved` tasks), **exit immediately at ~0% burn**. Never invent tasks or chain slices to pad quota (`<= 20%` 5h cap, **`0.0%` floor**).
2. **Tooling & Governance Parity Pre-Flight:**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/preflight_check.py
   ```
   For any Lean 4 UoW, also verify live LSP + `ripgrep` readiness:
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/lean_probe.py mcp-smoke
   ```
   If `lean-lsp-mcp`, `rg`, `lake`, `gemini-notebook-mcp`, or `mathlib` is missing/broken, **HALT immediately**, record a 5-column row in `LOG_DISCOVERY_AND_PIVOTS.md`, and trip the whistleblower brake:
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/automation_gate.py \
     pause --repo <repo_path> --reason "<concrete failure>" --notify
   ```
3. **Passive Pre-UoW Information Snapshot (Non-Optimized — Rule 09 §8):**
   - Capture the baseline state vector before editing (`observatory_only: true`, never gamed locally):
     ```bash
     PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/compression_audit.py \
       snapshot --output /tmp/uow_pre.json <repo_path>
     ```
   - Declare the expected regime (`explore_expand` | `generalize_lift` | `compress_unify` | `exposition_only`) and directional pre-estimate before starting edits.

---

## 2. Disciplined Constructive Execution (Lean 4 & Python)

1. **Lean 4 — 5-Step Efficient Loop (No Blind `lake build` Loops):**
   - Search Mathlib4 & Physlib first (`lean_probe.py mathlib-grep`, `lean_loogle`, `lean_leansearch`, `lean_local_search`). Never add `.lean` code to frozen zero-Mathlib islands without an owner ADR.
   - Keep Rank-0 ($N=2,3,4$ / $4\times 4$) checks in 15-line Python/SymPy oracles (STOKE pre-filtering) or `Lab/`; target `G2..G4` universal carriers in production Lean (`Defs.lean`, `Basic.lean`, focused proofs).
   - Probe automation in memory (`lean_probe.py tactic-probe`, `lean_goal`, `lean_multi_attempt`) and check forgetful inheritance + `lake env lean --profile` so syntax brevity never causes slow elaboration.
2. **Python — Layered Reuse & `900`-LOC No-Regression Ratchet:**
   - Extend shared `domain/ -> services/ -> infra/` modules instead of cloning JW/Fock bitmasks, Lanczos `eigsh`, BIC fitters, or `.dat` writers.
   - Obey the **no-regression modularity ratchet** enforced by `uow.py check` (`800` LOC `.lean` outside `Lab/`, `900` LOC Python `src/` on both new AND expanded files).
3. **Differentiated Circuit Breaker:**
   - Max **2** bounded mechanical repairs against an unchanged contract; **0** blind sign/tolerance changes on physical invariant failures (halt, log to `LOG_DISCOVERY_AND_PIVOTS.md`, trip `automation_gate.py pause --notify`).

---

## 3. Built-In `W4` Insider Audit, Passive Post-UoW $\Delta\mathbf{I}$ & Continuous Deliverables

1. Run full repo verification (`lake build`, `stub_lock.py`/`core_lock.py`, `uv run pytest`, `uv run ruff check`, `uv run mypy --strict`, and standalone `python3 -B .agents/scripts/repo_governance_gate.py`).
2. Dispatch a **distinct-lineage insider `W4` referee** (`Carbon` or `Claude Opus 5.5` auditing `Neon` work; **never `Argon`**) via **`swarm(action="add", model="claude-opus-5-5-medium" | "gemini-4-carbon-high", workspace="inherit")`** (never via same-lineage `invoke_subagent`, which inherits `Neon`) to verify `F1`/`F2`, signs/prefactors, `#print axioms`, and test independence—and record a `W4_insider` report (`doc/reviews/*.json`, validated by `review_record.py` and `repo_governance_gate.py`).
3. Measure Post-UoW actual $\mathbf{I}(L)$ and append passive telemetry (strictly non-optimized; for Sleep refactors only, also verify `compare-snapshots --pareto-gate`):
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/compression_audit.py \
     snapshot --output /tmp/uow_post.json <repo_path>
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/compression_audit.py \
     log-uow --repo <repo_path> --uow-id <UOW-ID> --team blue --regime <regime> \
     --pre-snapshot /tmp/uow_pre.json --post-snapshot /tmp/uow_post.json
   ```
4. **Update Continuous Deliverables Atomically:** Update `KNOWLEDGE_MAP.md` (if concepts/claims/pivots moved), `CHANGELOG.md`, `PROJECT_STATE.yaml` / `CURRENT_SPRINT.md`; if a note/labbook PDF was built, upload to `wip-notes` (`--clobber`) and post a 3-minute digest comment on the Pinned `Living R&D Digest` Issue.
5. Run `PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/uow.py check --repo <repo>`, commit with GH007 identity (`lufreitas0000` / `220090559+lufreitas0000@users.noreply.github.com`), push branch `X`, hand turn to Red Team (`automation_gate.py complete --repo <repo_path> --role blue --uow-id <UOW-ID> --flip-to red`), and **exit cleanly** after this single UoW.
