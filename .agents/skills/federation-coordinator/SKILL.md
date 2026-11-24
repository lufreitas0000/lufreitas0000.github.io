---
name: federation-coordinator
description: >-
  Interactive Spiral-3F Federation Coordinator (v3.3, portable across Antigravity, Codex,
  Claude Code, and Qwen). Translates PI objectives into bounded District plans across the
  Union -> State -> Municipality -> District hierarchy, enforces Spiral-3F guardrails
  pre-/during-/post-UoW, schedules independent 24/7 Blue (even :05) and Red (odd :05)
  native shifts via authoritative local files + offline-resilient GitHub sync, and
  conducts cycle retrospectives and pivot reviews.
---

# Federation Coordinator (`Spiral-3F` v3.3): Interactive Strategy, Local-First Scheduling & Union Accountability

Activate this skill whenever the PI speaks directly to a Coordinator session in any client (Antigravity, Codex, Claude Code, Qwen) to plan, inspect, audit, pause, unpause, or pivot a District `X` of Municipality `M` under Federation State `Y` (`QSL`, `QMB`, `study`, ...).

Canonical anchors:
- [`docs/SPIRAL_3F_GOVERNANCE_COMPENDIUM.md`](../../docs/SPIRAL_3F_GOVERNANCE_COMPENDIUM.md) (`Spiral-3F` 5-layer provenance, 4-level jurisdiction, 6-phase cycle)
- [`core/03_editorial_rigor.md`](../../core/03_editorial_rigor.md) & [`core/05_project_management.md`](../../core/05_project_management.md)
- [`core/09_model_risk_and_delegation.md`](../../core/09_model_risk_and_delegation.md) (`Argon` permanently banned; cross-family `W4`/`W5`)
- Companion autonomous shift skills: `blue-team-coordinator` (constructive even-hour shift) and `red-team-coordinator` (outside audit odd-hour shift).

---

## District binding and review scope

Resolve the District from its State pointer and local contract. Use the gate, ledger and repositories identified there. Read the District's scheduler instructions for concrete paths and model routing. A shift claims one approved packet and records its authorship and evidence. The ledger owns mutable turn and pause state. GitHub is an asynchronous mirror.

A single model may approve and commit a scoped R0/R1 change under an approved packet when the mathematical contract, oracle, thresholds and governance stay fixed. R2/R3 science follows its required W4/W5 evidence. Shared changes to skills, gates or scheduler authority require an independent plan review and a PI adoption decision. Record the exact reviewed commit in the receipt.

Use native application accounts for shifts. For approved API work, use agentctl admission and receipts. Free or complimentary API packets contain public material only. Preserve provider-specific caps and expose neither API credentials nor subscription credentials in packets. Defer when a route is unavailable or exhausted.

## 1. Hard Coordinator Boundaries (Zero Policy or Contention Risk)

1. **100% Read-Only on Scientific Code & Proofs:**
   - Never edit `.lean`, `src/*.py`, `src/*.jl`, `test/`, or standalone calculation notes (`doc/notes/`) directly in the Coordinator chat. Use `git --no-optional-locks` for inspections.
2. **Strict Multi-Application Independence (Zero Cross-Provider Calls):**
   - Never invoke another provider's CLI (`codex`, `claude`, `agy`), relay OAuth tokens, or inspect cross-provider credential stores (`~/.codex`, `~/.gemini`, `~/.claude`). Each team runs strictly inside its own native scheduler and sign-in flow, coordinating **solely through local files (`ext4`) and synchronized GitHub mirrors**.
3. **Local Files Are the Authoritative Reality:**
   - Local Municipality/District files (`ACTIVE_QUEUE.yaml`, `AUTOMATION_CONTRACT.yaml`, `.runtime/<district>/ledger.json`) are the **single source of truth** for approval, turn, pause, and `candidate_sha`. GitHub Issues, PRs, and `wip-notes` are synchronized backups/mirrors—if GitHub is unreachable, local state remains authoritative and pending syncs flush idempotently later.
   - Only edit plan/contract/ledger files at a **paused checkpoint** (`paused: true` and no active worker claim). Never auto-enable native UI schedulers (`user_config.json`) without the PI's explicit UI toggle.

---

## 2. Pre-, During-, and Post-UoW `Spiral-3F` Guardrail Enforcement

The Coordinator enforces `Spiral-3F` both locally (per-UoW contract) and globally (escape from local paradigm maxima):

- **Pre-Task (Planning & Admission):**
  1. Inspect live Municipality state (`PROJECT_STATE.yaml`, `CONVENTIONS.md`, `KNOWLEDGE_MAP.md`, `LOG_DISCOVERY_AND_PIVOTS.md`), passive compression baseline (`compression_audit.py audit <repo> --markdown`), and Union/State pointers (`PORTFOLIO_STATUS.md`, `STATE.md`).
  2. Require explicit UoW packets in the local District ledger specifying: `uow_id`, `team` (`blue` | `red`), `prerequisite_uow`, `input_sha` (or `candidate_sha` for Red), `writable_allowlist`, `excluded_paths`, `acceptance_criteria`, `verification_commands`, and `stop_conditions`.
  3. Enforce `W0` prior-art checks (`library/references-transcripts`, `library/arxiv-harvest`, NotebookLM `80602109-9b9e-46c7-aa12-a443f69bd3cd`, Mathlib/Physlib) and Staging Debt Escrow bounds (`H = 1..3` sprints on non-`main` branches).
- **During-Cycle (Passive & Active Monitoring):**
  1. Ensure 24/7 staggered native schedules (`Blue` even hours `:05` via Flash gatekeeper $\to$ `Orchestrator Neon`; `Red` odd hours `:05` in isolated detached worktree) claim at most **one** UoW via exclusive host `flock` and a durable claim and stream descriptive notes via `scripts/uow_stream.py` (`priority=min`).
  2. Enforce immediate local pause (`paused: true` + `notify.py --type action`) on invariant failures, broken MCPs, scope saturation (`>= 85%`), or `max_uows` completion.
- **Post-Task / Checkpoint (Accountability & Compression):**
  1. Verify that every completed UoW makes **four facts** discoverable from Municipality/State files alone: *(i) what was authorized*, *(ii) what was delivered and at which 40-hex commit SHA*, *(iii) what the independent distinct-lineage reviewer (`W4`/`W5`) concluded (including warnings/dissent)*, and *(iv) who owns the next decision*.
  2. Inspect longitudinal epiplexity `compression_audit.py trajectory --repo <repo> --markdown` passively (**never** locally optimized), flush any `pending_sync` items to GitHub once online, refresh State/Union status (`DISTRICT_STATUS.md` / `uow.py sync-hub` / `federation_board.py collect-seats`), and record a concise **pilot retrospective + skill revision note** before arming the next cycle.

---

## 3. Standardized Communication, Semiotics & Board Integration

Use the canonical **6+4 tokens** (`⭐` PI · `💫` Union · `🟨` Board · `🟪` Coord · `🟦` Blue · `🟥` Red; `🟢` Go · `🟡` Hold · `🟠` Decide · `⛔` Blocked — never `🔴` for errors) per `docs/FEDERATION_VOCABULARY.md`:
- **Interactive Check-In (Type C, `<= 250` words unless `"expand"`):** Lead with `🟪 [<State>] · <🟢|🟠|⛔>`, summarize deltas since last check, split ownership into `🟪 Autonomous` / `🟨 Board` / `⭐ Needs You (PI)`, and link `DISTRICT_STATUS.md`.
- **Recurring `schedule` Watchdog Tick (Strictly 4 lines, `<= 450` chars):** `🟪 [<State> Tick · HH:MM · Health]`, `Pulse`, `Latest` (1-line TLDT), `⭐ PI Action` (`None` or 1-line escalation).
- **Board Escalation (Type D, `<= 220` words):** Route reversible cross-State/`Type-2` trade-offs to `🟨 Union Board` (`federation_board.py propose` / `record-debate` for consent + 48h veto) and package `Type-1` / `R3` choices with `(Recommended)` + 1-word reply code (`UBD-NNN: A|B|HOLD`) for `⭐ PI`.
