---
name: red-team-coordinator
description: >-
  Self-contained Portable Outside Red-Team Shift Coordinator & W5 Auditor (Spiral-3F v3.3,
  portable across Codex, Antigravity, Claude Code, and Qwen). Claims at most one locally
  approved Red UoW pinned to an exact Blue candidate_sha under exclusive host flock,
  fetches candidate_sha locally into an isolated detached worktree (works 100% offline),
  executes the 4-pillar Spiral-3F Lakatosian/vault/compression/mental-image audit, saves
  attributed W5_red_team JSON locally, enforces pause precedence on blockers, streams
  notes via uow_stream.py, and syncs idempotently to GitHub.
---

# Red-Team Coordinator (`Spiral-3F` v3.3): Local-First Outside `W5` Audit, Compression & Lakatosian Guard

Activate this self-contained skill whenever running an autonomous or manual **Outside Red-Team shift** (`W0` epistemic gate / `W5` outside audit; **`Argon` permanently banned**; **zero cross-provider CLI calls**).

---

## District binding and review scope

Resolve the District from its State pointer and local contract. Use the gate, ledger and repositories identified there. Read the District's scheduler instructions for concrete paths and model routing. A shift claims one approved packet and records its authorship and evidence. The ledger owns mutable turn and pause state. GitHub is an asynchronous mirror.

A single model may approve and commit a scoped R0/R1 change under an approved packet when the mathematical contract, oracle, thresholds and governance stay fixed. R2/R3 science follows its required W4/W5 evidence. Shared changes to skills, gates or scheduler authority require an independent plan review and a PI adoption decision. Record the exact reviewed commit in the receipt.

Use native application accounts for shifts. For approved API work, use agentctl admission and receipts. Free or complimentary API packets contain public material only. Preserve provider-specific caps and expose neither API credentials nor subscription credentials in packets. Defer when a route is unavailable or exhausted.

## 1. Step 0 — Fail-Closed Local Claim & Exact `candidate_sha` Pinning

1. **Exclusive Local-First Claim (Verifies Prerequisite & Exact `candidate_sha`):**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B "<district_gate>" \
     claim --role red --owner "<client>:<session_id>" --lineage "<worker_model>"
   ```
   - Exits immediately (`"proceed": false`) if the cycle is `paused`, `turn != red`, another worker holds the claim, the Blue prerequisite UoW is incomplete, or `candidate_sha` is missing/stale.
   - **CRITICAL LOCK RULE:** Once `"proceed": true`, you hold `claim_token` and **MUST** finish via `the district gate complete` or `the district gate pause`.
2. **Offline-Capable Isolated Snapshot Checkout (Zero Contention With Blue):**
   - Never edit `<repo_path>` or commit to Blue's branch. Sync `<codex_red_worktree>` directly from the **local** Git object store `<repo_path>` (so Red works even when GitHub is 100% offline!):
     ```bash
     git -C "<codex_red_worktree>" fetch "<repo_path>" "<candidate_sha>" && \
       git -C "<codex_red_worktree>" checkout --detach FETCH_HEAD
     test "$(git -C "<codex_red_worktree>" rev-parse HEAD)" = "<candidate_sha>"
     ```
3. **Descriptive Stream `[CLAIM]`:**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/uow_stream.py \
     --phase claim --project <municipality> --uow <uow_id> --team red --sha "<candidate_sha>" \
     --summary "Claimed Red audit <uow_id> pinned to exact SHA <candidate_sha_short>."
   ```

---

## 2. Step 1 — Four-Pillar `Spiral-3F` Outside Audit (Read-Only on Code)

Run deterministic telemetry (`compression_audit.py audit "<codex_red_worktree>" --markdown`, `trajectory --repo "<repo_path>" --markdown`, and `<codex_red_worktree>/.agents/scripts/repo_governance_gate.py --repo "<codex_red_worktree>"`), then challenge the local paradigm maximum across all four `Spiral-3F` pillars:

1. **Pillar 1 — Multi-Tier Vault & Primary Literature Reality Check:**
   - Cross-check `/home/lu/Projects/library/references-transcripts` (Coleman, Altland–Simons, Tasaki, Blaizot–Ripka, Di Francesco, Etingof, Bratteli–Robinson), `/home/lu/Projects/library/arxiv-harvest`, NotebookLM (`80602109-9b9e-46c7-aa12-a443f69bd3cd` if MCP mounted), and Mathlib4/Physlib. Never read copyrighted raw PDFs in `doc/reference/*.pdf`.
2. **Pillar 2 — Lakatosian Falsification & Anti-Assumption Probes:**
   - Using `<codex_red_worktree>/.venv/bin/python -B -c "..."` (writing zero files in the worktree), actively attempt to falsify Blue's claims at boundary/degenerate regimes ($\kappa \to 0$, $\Delta \to 0$, Dirac $\mu = 0$, van Hove $|\mu|=t$, extreme $t/K$, non-unitary spin vectors, open boundaries).
   - Forbid hardcoded Chern numbers, pre-assumed preferred symmetries, silent tolerance loosening, or monster-barring. Emit `[IDEA]` stream notes via `uow_stream.py --phase idea` when uncovering structural simplifications or edge-case physics.
3. **Pillar 3 — Parameter-Free Compression (`KEEP / GENERALIZE / COMPRESS / PRUNE`):**
   - Hunt Rank-0 (`G0`/`G1`) DTP bloat, duplicated solver loops (`R_clone`), and escrowed monoliths; propose atomic multi-file "Wolff cluster moves" for consolidation.
4. **Pillar 4 — Mental Image & Continuous Maze Navigation:**
   - Verify that `KNOWLEDGE_MAP.md`, standalone notes, and Regime Ledgers state a clear 1-paragraph physical Mental Image and separate exact proofs, controlled expansions, finite-size numerics, and conjectures.

---

## 3. Step 2 — Local Review Deposit, Pause Precedence & Idempotent Sync

1. **Write Attributed `W5_red_team` Review Locally (Outside Blue's Working Tree):**
   Write `<local_review_out>` (`.runtime/<district>/reviews/w5_<uow_slug>_<sha12>.json`, validated against `repo_governance_gate.py:validate_review_json`, recording `"review_scope": "inner_dev"` for per-UoW Gemini sub-lineage audits on `research/*` or `"review_scope": "release_main"` for cross-vendor Milestone Release-Candidate audits targeting `main`, exact `candidate_commit: "<candidate_sha>"`, `author_lineage`, `reviewer_lineage`, `verdict`, `prior_art_sources`, `compression_assessment`, `mental_image_assessment`, and `findings`) plus markdown RFC `/tmp/w5_<uow_slug>_rfc.md`.
   For `inner_dev`, enforce distinct sub-lineage (`google-neon` $\neq$ `google-carbon`/`google-hydrogen`); for `release_main` (PRs to `main`), enforce distinct provider family (`google` $\neq$ `openai`/`anthropic`). If ineligible, stop before acquiring a claim.
2. **Complete Locally (Enforcing Pause Precedence on Blockers or Checkpoints) & Sync:**
   - If `verdict` is `"REJECT"` / `"PIVOT"` (or `is_cycle_checkpoint` is `true`, e.g., `UOW-06`), pass `--pause-reason "<why>"` so `paused: true` is recorded locally **before** any subsequent scheduled turn can advance!
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -B "<district_gate>" \
     complete --role red --claim-token "<tok>" --uow-id "<uow_id>" \
     --candidate-sha "<candidate_sha>" --review-file "<local_review_out>" \
     --rfc-file "/tmp/w5_<uow_slug>_rfc.md"
   PYTHONDONTWRITEBYTECODE=1 python3 -B /home/lu/Projects/scripts/uow_stream.py \
     --phase complete --project <municipality> --uow <uow_id> --team red --sha "<candidate_sha>" \
     --summary "Completed W5 audit <uow_id>: verdict=<verdict>."
   ```
   *(If GitHub is offline, `complete` saves the review and turn transition locally and queues an idempotent `pending_sync` entry that publishes the Issue RFC once when online; re-running after local completion never duplicates the review.)*

---

## 4. Standardized Chat Reply Contract (`SKIP` & 5-Field `TLDT`)

- **No-Op / Wrong-Turn (`proceed: false`, Type A1 — Strictly 1 line, `<= 140` chars):**
  `🟥 [<State>/<District>] · 🟡 SKIP (<reason>) · Next: <next_role> (<uow_id>) · 0% burn`
- **Completed / Paused Audit (Type A2 — 5-Field TLDT, `<= 12` lines, zero raw log dumps; use `⛔ PAUSED` on blockers, never `🔴`):**
  - Header: `🟥 [<State>/<Municipality>/<District>] · <uow_id> · <🟢 PASS|🟠 DECIDE|⛔ PAUSED>`
  - **Done (SA1):** 1–2 plain-language sentences (verdict + key physics/compression finding + non-LLM anchor) · SHA `<sha12>`
  - **Who:** Audited `🟦 <author>` · Auditor `🟥 <reviewer_model>` (`<review_scope>`) · Burn `<pool delta>`
  - **Decision & Owner:** `<🟪 Coord|🟨 Board|⭐ PI>` — `⭐ PI: None` *(or explicit dissent / `Type-1` ruling needed)*
  - **Next (SA3):** `<next_uow_id>` (`<next_role>`, auto or paused)
  - **Horizon:** `<k/N>` UoWs · Review `[file](file://...)`
