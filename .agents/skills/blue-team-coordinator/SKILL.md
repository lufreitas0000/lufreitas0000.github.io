---
name: blue-team-coordinator
description: >-
  Self-contained Portable Blue-Team Shift Coordinator & Constructive Executor (Spiral-3F v3.3,
  portable across Antigravity, Codex, Claude Code, and Qwen). Claims at most one locally
  approved Blue UoW under exclusive host flock, coordinates constructive implementation
  (<800 .lean / <900 .py LOC ratchet) + distinct-lineage W4 insider review, emits silent
  descriptive field notes to uow_stream.py, logs passive Pre-/Post-UoW Delta-I, commits
  candidate_sha on the District branch, and syncs idempotently to GitHub.
---

# Blue-Team Coordinator (`Spiral-3F` v3.3): Local-First Constructive Shift & Built-In `W4` Verification

Activate this self-contained skill whenever running an autonomous or manual **Blue-Team constructive UoW shift** (`W2` implementation + `W3` mechanical checks + `W4` distinct-lineage insider referee; `<= 20%` 5h cap, `0.0%` minimum burn floor; **`Argon` permanently banned**).

---

## District binding and review scope

Resolve the District from its State pointer and local contract. Use the gate, ledger and repositories identified there. Read the District's scheduler instructions for concrete paths and model routing. A shift claims one approved packet and records its authorship and evidence. The ledger owns mutable turn and pause state. GitHub is an asynchronous mirror.

A single model may approve and commit a scoped R0/R1 change under an approved packet when the mathematical contract, oracle, thresholds and governance stay fixed. R2/R3 science follows its required W4/W5 evidence. Shared changes to skills, gates or scheduler authority require an independent plan review and a PI adoption decision. Record the exact reviewed commit in the receipt.

Use native application accounts for shifts. For approved API work, use agentctl admission and receipts. Free or complimentary API packets contain public material only. Preserve provider-specific caps and expose neither API credentials nor subscription credentials in packets. Defer when a route is unavailable or exhausted.

## 1. Step 0 — Fail-Closed Local Claim & Pre-Flight (Before Touching Code)

1. **Exclusive Local-First Claim (Shared by Scheduled & Manual Runs):** Reuse a claim supplied by the native gatekeeper. For a directly started shift, obtain a claim once.
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B "<district_gate>" \
     claim --role blue --owner "<client>:<session_id>" --lineage "<worker_model>"
   ```
   - If `"proceed": false` (`paused`, `wrong_turn`, `claim_active`, `prerequisite_incomplete`, or `cycle_complete`), output 1 line with `"reason"` and **stop immediately**.
   - **CRITICAL LOCK RULE:** Once `"proceed": true`, you hold the exclusive host claim (`claim_token`) and **MUST** terminate via `the district gate complete` or `the district gate pause` so the claim is always released cleanly.
2. **Import Pending Local Red Reviews & Run Toolchain Pre-Flight:**
   - Import any validated `W5_red_team` JSON deposited locally in `.runtime/<district>/reviews/` into `doc/reviews/` (`the district gate import-local-reviews`).
   - Run `PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/preflight_check.py` (plus `lean_probe.py mcp-smoke` for Lean). On any missing MCP/binary, log to `LOG_DISCOVERY_AND_PIVOTS.md` and call `the district gate pause --claim-token <tok> --reason "<failure>" --notify`.
3. **Passive Pre-UoW Snapshot & Descriptive Stream `[CLAIM]`:**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/meta/project-governance/scripts/compression_audit.py \
     snapshot --output /tmp/uow_pre.json <repo_path>
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/uow_stream.py \
     --phase claim --project <municipality> --uow <uow_id> --team blue \
     --summary "Claimed <uow_id>: <1-sentence concrete goal & planned modules>"
   ```

---

## 2. Step 1 — Team-Orchestrated Constructive Execution (`Spiral-3F` Fronts 1–3)

1. **Multi-Agent Delegation (When Running on an Orchestrator Host):**
   - Keep the Lead context strategic and delegate focused sub-tasks (never invoking external third-party CLIs; use only native in-app workers):
     - *Scout / Harness Helper* (`claude-sonnet-5-5-high`, `gpt-oss-120b-medium`, or `gemini-3.8-flash-high`): scout `/home/lu/Projects/library/{references-transcripts,arxiv-harvest}`, `gemini-notebook-mcp`, Mathlib4/Physlib, and scaffold unit/ED test harnesses.
     - *Core Physics / Proof Builder* (`gemini-4-neon-high` or host primary): implement clean `domain/ -> services/ -> infra/` Python (`uv` `.venv`, strictly `< 900` LOC; `< 500` LOC target) or universal `G2..G4` Lean (`< 800` LOC outside `Lab/`).
2. **Hard Scientific Guardrails & Mid-UoW `[IDEA]` Annotations:**
   - Never modify `CONVENTIONS.md` or `TODO(owner)` thresholds in `doc/hypotheses/HC-*.yaml`.
   - **Differentiated Circuit Breaker:** At most **2** bounded mechanical repairs against an unchanged contract; **0** blind sign, prefactor, or tolerance (`atol`/`rtol`) guesses on physical invariant failures—halt, log a 5-column row in `doc/rnd/<stream>/pivot_log.md` (`LOG_DISCOVERY_AND_PIVOTS.md`), and call `the district gate pause --notify`.
   - Whenever an interesting physical mechanism, limiting behavior, or symmetry simplification emerges mid-run, annotate it silently to the lab ticker:
     ```bash
     PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/uow_stream.py \
       --phase idea --project <municipality> --uow <uow_id> --team blue \
       --summary "<concise physical insight or numerical observation>"
     ```

---

## 3. Step 2 — Distinct-Lineage `W4` Audit, Local Commit & Offline-Safe Sync

1. **Repository & Modularity Verification:**
   Run `make verify` (or `lake build`), standalone `python3 -B .agents/scripts/repo_governance_gate.py --repo <repo_path>`, and `python3 -B /home/lu/Projects/scripts/uow.py check --repo <repo_path>`.
2. **Commit the verified candidate.** Record passive compression telemetry and update the required scientific records. Commit the scoped changes using the repository Git identity and record its full SHA.
3. **Obtain the review for the committed SHA.** For R2/R3, hand a separate provider family the exact committed candidate and independent verification commands. Record `W4_insider`, the UoW ID, `candidate_commit`, author and reviewer lineages, and an explicit verdict. Write the record to the district's local evidence directory. Hold subsequent candidate edits until the handoff is resolved.
4. **Local Completion + Offline-Tolerant GitHub Sync + `[COMPLETE]` Stream:**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B "<district_gate>" \
     complete --role blue --claim-token "<tok>" --uow-id "<uow_id>" \
     --candidate-sha "$CANDIDATE_SHA" --review-file "<absolute_review_file>" \
     --summary "<1-line takeaway + question for Red Team to challenge>"
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/uow_stream.py \
     --phase complete --project <municipality> --uow <uow_id> --team blue --sha "$CANDIDATE_SHA" \
     --summary "Completed <uow_id> (W4 PASS); handed exact SHA to Red Team."
   ```
   For R0/R1 packets that permit single-model verification, omit the independent review file and record the verification evidence in the local receipt. If completion is refused, pause with the owner token and record the reason.

   *(If GitHub is temporarily unreachable during `complete`, local state + `CANDIDATE_SHA` are already durably saved for Red Team to fetch locally from `<repo_path>`, and `pending_sync` will push/comment once on recovery.)*
