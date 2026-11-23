#!/usr/bin/env python3
"""Standalone zero-dependency repository governance gate (Governance v3.1).

Designed to run identically inside standalone child repositories (local `make verify` /
`make ci` and disposable GitHub Actions runners with zero hub checkout) AND via Hub
`scripts/uow.py check`. Uses 100% Python 3.10+ standard library.

Enforces:
1. No-regression modularity ratchet:
   - `.lean` outside `Lab/` <= 800 LOC on added or net-expanded (`cur_loc > base_loc`) files;
   - Python `src/*.py` <= 900 LOC on added or net-expanded (`cur_loc > base_loc`) files.
2. Rank-0 fixed-dimension production Lean guard (>= 3 concrete `Fin 2..16` theorems with
   0 `variable`/typeclass binders outside `Lab/`).
3. Unresolved Git merge-conflict marker guard (`<<<<<<< ` ... `>>>>>>> `).
4. Staging Debt Escrow (`AUTOMATION_CONTRACT.yaml`) expiry check + unconditional block on
   PRs targeting `main`.
5. Structural & cross-lineage validation of `doc/reviews/*.json` (`W0_gate`, `W4_insider`,
   `W5_red_team`; permanently banning `argon`).
6. PR-to-`main` readiness gate: when `--target-branch` equals the canonical branch (`main`),
   substantive scientific PRs (> 50 changed lines in `src/`, `.lean`, or `doc/{notes,manuscript,labbook}/`,
   or any repo with `AUTOMATION_CONTRACT.yaml`) require `KNOWLEDGE_MAP.md` and >= 1 valid
   approving `W5_red_team` record in `doc/reviews/` (unless labeled `skip-w5-chore`).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

LEAN_LOC_LIMIT = 800
PYTHON_SRC_LOC_LIMIT = 900
MAIN_SCIENTIFIC_DIFF_THRESHOLD = 50

SKIP_DIRS = {
    ".git", ".lake", ".venv", "venv", "build", "dist", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".worktrees", "node_modules",
    "archive_builds", "cache_tikz",
}
TEXT_CHECK_SUFFIXES = {
    ".py", ".lean", ".yaml", ".yml", ".toml", ".json", ".md", ".tex", ".bib", ".sh",
}

FIXED_DIM_PAT = re.compile(r"\bFin\s+(?:[2-9]|1[0-6])\b|\bMatrix\s*\(\s*Fin\s+(?:[2-9]|1[0-6])\b")
THEOREM_DECL_PAT = re.compile(r"(?m)^\s*(?:private\s+|protected\s+)?(?:theorem|lemma)\s+([A-Za-z0-9_'.]+)")
UNIV_BINDER_PAT = re.compile(r"(?m)^\s*variable\b|\[[A-Za-z0-9_.\s]*?(?:Fintype|Finset|Module|Ring|Field|Group|Algebra|InnerProductSpace|NormedAddCommGroup)\b")
CONFLICT_START_RE = re.compile(r"(?m)^<<<<<<< ")
CONFLICT_SEP_RE = re.compile(r"(?m)^=======\s*$")
CONFLICT_END_RE = re.compile(r"(?m)^>>>>>>> ")

APPROVING_W5_VERDICTS = {"APPROVE", "ACCEPTED_FOR_SCOPE", "KEEP", "COMPRESS", "GENERALIZE", "PASS"}


def _git(repo: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _strip_lean_comments(src: str) -> str:
    out: list[str] = []
    i, n, depth = 0, len(src), 0
    while i < n:
        if depth == 0 and src[i : i + 2] == "--":
            nl = src.find("\n", i + 2)
            if nl == -1:
                break
            out.append("\n")
            i = nl + 1
            continue
        if src[i : i + 2] == "/-":
            depth += 1
            i += 2
            continue
        if depth > 0 and src[i : i + 2] == "-/":
            depth -= 1
            i += 2
            continue
        if depth == 0:
            out.append(src[i])
        elif src[i] == "\n":
            out.append("\n")
        i += 1
    return "".join(out)


def _is_skipped_rel(rel: str) -> bool:
    parts = Path(rel).parts
    return any(p in SKIP_DIRS for p in parts)


def _is_lab_lean(rel: str) -> bool:
    norm = f"/{rel.strip('/')}/"
    return "/Lab/" in norm or "/BosonizeStubs/" in norm or "/FiniteQMBStubs/" in norm


def _is_python_src(rel: str) -> bool:
    norm = f"/{rel.strip('/')}"
    return norm.startswith("/src/") or "/src/" in norm


def _is_scientific_path(rel: str) -> bool:
    if rel.endswith(".lean") and not _is_lab_lean(rel):
        return True
    if rel.endswith(".py") and _is_python_src(rel):
        return True
    norm = rel.strip("/")
    return norm.startswith(("doc/notes/", "doc/manuscript/", "doc/labbook/", "notes/latex/"))


def _iter_candidate_files(repo: Path) -> list[Path]:
    proc = _git(repo, ["rev-parse", "--is-inside-work-tree"])
    if proc.returncode == 0:
        tracked = _git(repo, ["ls-files"]).stdout.splitlines()
        untracked = _git(repo, ["ls-files", "--others", "--exclude-standard"]).stdout.splitlines()
        rels = sorted(set(tracked) | set(untracked))
        out: list[Path] = []
        for rel in rels:
            if not rel or _is_skipped_rel(rel):
                continue
            p = repo / rel
            if p.is_file() and not p.is_symlink():
                out.append(p)
        return out

    out = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in sorted(files):
            p = Path(root) / fname
            if p.is_file() and not p.is_symlink():
                out.append(p)
    return out


def _resolve_effective_base_ref(repo: Path, explicit_base: str | None, canonical_branch: str) -> str | None:
    if explicit_base:
        eb = explicit_base.strip()
        if eb and not set(eb) <= {"0"}:
            if _git(repo, ["rev-parse", "--verify", f"{eb}^{{commit}}"]).returncode == 0:
                return eb
    if _git(repo, ["rev-parse", "--verify", "HEAD^{commit}"]).returncode != 0:
        return None
    branch = _git(repo, ["symbolic-ref", "--short", "-q", "HEAD"]).stdout.strip()
    if branch and branch != canonical_branch:
        for cand in (f"origin/{canonical_branch}", canonical_branch):
            if _git(repo, ["rev-parse", "--verify", f"{cand}^{{commit}}"]).returncode == 0:
                mb = _git(repo, ["merge-base", "HEAD", cand])
                if mb.returncode == 0 and mb.stdout.strip():
                    return mb.stdout.strip()
    return "HEAD"


def _base_file_loc(repo: Path, base_ref: str | None, rel_posix: str) -> int | None:
    if not base_ref:
        return None
    proc = _git(repo, ["show", f"{base_ref}:{rel_posix}"])
    if proc.returncode != 0:
        return None
    return len(proc.stdout.splitlines())


def _parse_automation_contract_escrow(repo: Path) -> dict[str, Any]:
    cpath = repo / "AUTOMATION_CONTRACT.yaml"
    if not cpath.is_file():
        return {"present": False, "current_sprint": 0, "escrows": [], "expired": []}
    text = cpath.read_text(encoding="utf-8", errors="replace")
    cur_m = re.search(r"(?m)^\s*current_sprint:\s*(\d+)\b", text)
    cur_sprint = int(cur_m.group(1)) if cur_m else 0

    escrows: list[dict[str, Any]] = []
    expired: list[str] = []
    in_escrow = False
    escrow_indent = 0
    current_item: dict[str, Any] | None = None

    for raw in text.splitlines():
        stripped = raw.split("#", 1)[0].rstrip()
        if not stripped.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        s = stripped.strip()
        if re.match(r"^staging_debt_escrow:\s*(\[\s*\])?$", s):
            if s.endswith("[]"):
                in_escrow = False
            else:
                in_escrow = True
                escrow_indent = indent
            continue
        if in_escrow:
            if indent <= escrow_indent and not s.startswith("-"):
                if current_item is not None:
                    escrows.append(current_item)
                    current_item = None
                in_escrow = False
                continue
            if s.startswith("- "):
                if current_item is not None:
                    escrows.append(current_item)
                current_item = {}
                s = s[2:].strip()
            if current_item is not None and ":" in s:
                k, v = s.split(":", 1)
                val = v.strip().strip("'\"")
                current_item[k.strip()] = int(val) if val.isdigit() else val

    if current_item is not None:
        escrows.append(current_item)

    for item in escrows:
        created = int(item.get("created_sprint", 0) or 0)
        horizon = int(item.get("horizon_sprints", item.get("max_sprints", 3)) or 3)
        eid = str(item.get("id") or item.get("path") or "escrow")
        if cur_sprint > created + horizon:
            expired.append(f"{eid} (created_sprint={created}, horizon_sprints={horizon}, current_sprint={cur_sprint})")
    return {"present": True, "current_sprint": cur_sprint, "escrows": escrows, "expired": expired}


def _lineage_family(lineage: str) -> str:
    low = lineage.strip().lower()
    if "argon" in low:
        raise ValueError(f"Banned Argon model lineage is forbidden by Rule 09 §2.1: {lineage!r}")
    return low


def validate_review_json(data: dict[str, Any], source: str = "<record>") -> None:
    kind = str(data.get("review_kind", "W4_insider"))
    if kind not in {"W4_insider", "W0_gate", "W5_red_team"}:
        raise ValueError(f"{source}: unsupported review_kind {kind!r}")

    if kind == "W0_gate":
        revs = data.get("reviewers")
        if not isinstance(revs, list) or len(revs) < 2:
            raise ValueError(f"{source}: W0_gate requires >= 2 reviewers")
        lins = set()
        for r in revs:
            if not isinstance(r, dict):
                raise ValueError(f"{source}: invalid reviewer object in W0_gate")
            lin = str(r.get("model_lineage") or "").strip()
            if not lin:
                raise ValueError(f"{source}: W0_gate reviewer missing model_lineage")
            lins.add(_lineage_family(lin))
        if len(lins) < 2:
            raise ValueError(f"{source}: W0_gate requires >= 2 distinct model lineages; got {sorted(lins)}")
        return

    author_agent = str(data.get("author_agent") or "").strip()
    rev_agent = str(data.get("reviewer_agent") or "").strip()
    if author_agent and rev_agent and author_agent == rev_agent:
        raise ValueError(f"{source}: author_agent and reviewer_agent must be distinct ({rev_agent!r})")

    raw_author_lin = str(data.get("author_lineage") or data.get("producer_lineage") or "").strip()
    raw_rev_lin = str(data.get("reviewer_lineage") or "").strip()
    for val in (raw_author_lin, raw_rev_lin, author_agent, rev_agent):
        if "argon" in val.lower():
            raise ValueError(f"{source}: Banned Argon model lineage is forbidden by Rule 09 §2.1: {val!r}")

    if kind == "W5_red_team":
        if not raw_author_lin or not raw_rev_lin:
            raise ValueError(f"{source}: W5_red_team requires non-empty author_lineage and reviewer_lineage")
        if _lineage_family(raw_author_lin) == _lineage_family(raw_rev_lin):
            raise ValueError(f"{source}: W5_red_team requires distinct author_lineage and reviewer_lineage ({raw_rev_lin!r})")
        sources = data.get("prior_art_sources")
        if not isinstance(sources, list) or len(sources) == 0:
            raise ValueError(f"{source}: W5_red_team requires non-empty prior_art_sources list")
    else:
        # W4_insider: enforce distinct lineages when declared; accept legacy schema_version=1 records that declare distinct author_agent != reviewer_agent
        if raw_author_lin and raw_rev_lin and _lineage_family(raw_author_lin) == _lineage_family(raw_rev_lin):
            raise ValueError(f"{source}: W4_insider requires distinct author_lineage and reviewer_lineage ({raw_rev_lin!r})")
        if not (raw_author_lin and raw_rev_lin) and not (author_agent and rev_agent):
            raise ValueError(f"{source}: W4_insider requires distinct author/reviewer lineages or agents")


def _scientific_diff_lines(repo: Path, base_ref: str | None) -> int:
    if not base_ref:
        total = 0
        for p in _iter_candidate_files(repo):
            rel = p.relative_to(repo).as_posix()
            if _is_scientific_path(rel):
                total += len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        return total

    proc = _git(repo, ["diff", "--numstat", base_ref])
    if proc.returncode != 0:
        return 0
    changed = 0
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        add_s, del_s, rel = parts
        if _is_scientific_path(rel):
            changed += (int(add_s) if add_s.isdigit() else 0) + (int(del_s) if del_s.isdigit() else 0)
    # Also include untracked scientific files
    for rel in _git(repo, ["ls-files", "--others", "--exclude-standard"]).stdout.splitlines():
        if rel and not _is_skipped_rel(rel) and _is_scientific_path(rel):
            p = repo / rel
            if p.is_file():
                changed += len(p.read_text(encoding="utf-8", errors="replace").splitlines())
    return changed


def evaluate_repository(
    repo_path: Path,
    *,
    base_ref: str | None = None,
    target_branch: str = "",
    canonical_branch: str = "main",
    pr_labels: set[str] | None = None,
) -> dict[str, Any]:
    repo = repo_path.resolve()
    labels = {x.strip() for x in (pr_labels or set()) if x.strip()}
    eff_base = _resolve_effective_base_ref(repo, base_ref, canonical_branch)
    targeting_main = bool(target_branch and target_branch.strip() == canonical_branch)

    errors: list[str] = []
    warnings: list[str] = []

    escrow_info = _parse_automation_contract_escrow(repo)
    escrowed_paths = {
        str(e.get("path") or "").strip("/")
        for e in escrow_info["escrows"]
        if e.get("path")
    }
    for exp in escrow_info["expired"]:
        errors.append(f"[ESCROW-EXPIRED] Staging Debt Escrow expired in AUTOMATION_CONTRACT.yaml: {exp}")
    if targeting_main and escrow_info["escrows"]:
        errors.append(
            f"[ESCROW-MAIN-BLOCK] {len(escrow_info['escrows'])} active staging_debt_escrow item(s) in "
            f"AUTOMATION_CONTRACT.yaml must be retired before merging into '{canonical_branch}'."
        )

    candidates = _iter_candidate_files(repo)

    # 1. Modularity ratchet + 2. Rank-0 Lean + 3. Conflict markers
    for p in candidates:
        rel = p.relative_to(repo).as_posix()
        suffix = p.suffix.lower()
        need_text = (
            suffix in TEXT_CHECK_SUFFIXES
            or p.name in {"Makefile", "AGENTS.md", "CONVENTIONS.md", "KNOWLEDGE_MAP.md"}
        )
        if not need_text:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")

        if CONFLICT_START_RE.search(text) and CONFLICT_SEP_RE.search(text) and CONFLICT_END_RE.search(text):
            errors.append(f"[CONFLICT-MARKERS] Unresolved Git merge-conflict markers in {rel}")

        cur_loc = len(text.splitlines())

        if suffix == ".lean" and not _is_lab_lean(rel):
            prev_loc = _base_file_loc(repo, eff_base, rel)
            if cur_loc > LEAN_LOC_LIMIT and (prev_loc is None or cur_loc > prev_loc):
                msg = (
                    f"[RATCHET-LEAN-800] {rel} has {cur_loc} LOC (> {LEAN_LOC_LIMIT} limit; "
                    f"baseline={prev_loc if prev_loc is not None else 'new'}). Split into focused modules."
                )
                if not targeting_main and rel in escrowed_paths and not escrow_info["expired"]:
                    warnings.append(f"[ESCROWED] {msg}")
                else:
                    errors.append(msg)
            elif cur_loc > LEAN_LOC_LIMIT and prev_loc is not None:
                warnings.append(f"[LEGACY-LEAN-GRANDFATHERED] {rel} ({cur_loc} LOC <= baseline {prev_loc} LOC)")

            # Check Rank-0 fixed-dim theorems on net-new or modified Lean files
            if prev_loc is None or _git(repo, ["diff", "--quiet", eff_base or "HEAD", "--", rel]).returncode != 0:
                stripped = _strip_lean_comments(text)
                thms = len(THEOREM_DECL_PAT.findall(stripped))
                has_univ = bool(UNIV_BINDER_PAT.search(stripped))
                fixed_hits = len(FIXED_DIM_PAT.findall(stripped))
                if thms >= 3 and not has_univ and fixed_hits >= 3:
                    errors.append(
                        f"[RANK0-LEAN] {rel} defines {thms} theorem(s) over concrete fixed dimensions "
                        f"({fixed_hits} Fin 2..16 hits) with 0 universal binders outside Lab/."
                    )

        elif suffix == ".py" and _is_python_src(rel):
            prev_loc = _base_file_loc(repo, eff_base, rel)
            if cur_loc > PYTHON_SRC_LOC_LIMIT and (prev_loc is None or cur_loc > prev_loc):
                msg = (
                    f"[RATCHET-PY-900] {rel} has {cur_loc} LOC (> {PYTHON_SRC_LOC_LIMIT} limit; "
                    f"baseline={prev_loc if prev_loc is not None else 'new'}). Extract domain/services submodules."
                )
                if not targeting_main and rel in escrowed_paths and not escrow_info["expired"]:
                    warnings.append(f"[ESCROWED] {msg}")
                else:
                    errors.append(msg)
            elif cur_loc > PYTHON_SRC_LOC_LIMIT and prev_loc is not None:
                warnings.append(f"[LEGACY-PY-GRANDFATHERED] {rel} ({cur_loc} LOC <= baseline {prev_loc} LOC)")

    # 4. Validate doc/reviews/*.json if present
    reviews_dir = repo / "doc" / "reviews"
    valid_w5_approvals: list[str] = []
    if reviews_dir.is_dir():
        for rfile in sorted(reviews_dir.glob("*.json")):
            rel_r = rfile.relative_to(repo).as_posix()
            try:
                rdata = json.loads(rfile.read_text(encoding="utf-8"))
                if not isinstance(rdata, dict):
                    raise ValueError(f"{rel_r}: top-level JSON must be an object")
                validate_review_json(rdata, source=rel_r)
                if rdata.get("review_kind") == "W5_red_team":
                    verdict = str(rdata.get("verdict") or rdata.get("disposition") or "").upper()
                    if verdict in APPROVING_W5_VERDICTS:
                        valid_w5_approvals.append(rel_r)
            except Exception as exc:
                errors.append(f"[REVIEW-RECORD-INVALID] {exc}")

    # 5. PR-to-main readiness gate
    sci_diff_lines = _scientific_diff_lines(repo, eff_base) if targeting_main else 0
    if targeting_main and "skip-w5-chore" not in labels:
        if escrow_info["present"] or sci_diff_lines > MAIN_SCIENTIFIC_DIFF_THRESHOLD:
            if not (repo / "KNOWLEDGE_MAP.md").is_file():
                errors.append(
                    f"[MAIN-GATE-KNOWLEDGE-MAP] PR targeting '{canonical_branch}' ({sci_diff_lines} scientific diff lines) "
                    f"requires root KNOWLEDGE_MAP.md (or 'skip-w5-chore' label for pure CI/chore fixes)."
                )
            if not valid_w5_approvals:
                errors.append(
                    f"[MAIN-GATE-W5-REQUIRED] PR targeting '{canonical_branch}' ({sci_diff_lines} scientific diff lines) "
                    f"requires >= 1 valid cross-family W5_red_team JSON record in doc/reviews/ with approving verdict."
                )

    return {
        "ok": len(errors) == 0,
        "repo": str(repo),
        "effective_base_ref": eff_base,
        "target_branch": target_branch,
        "canonical_branch": canonical_branch,
        "scientific_diff_lines": sci_diff_lines,
        "valid_w5_records": valid_w5_approvals,
        "errors": errors,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Standalone Governance v3.1 repository gate (stdlib-only).")
    ap.add_argument("--repo", type=Path, default=Path("."), help="Target repository root (default: .)")
    ap.add_argument("--base-ref", default=os.environ.get("GOVERNANCE_BASE_REF", ""), help="Git base commit/ref for ratchet comparison")
    ap.add_argument("--target-branch", default=os.environ.get("GITHUB_BASE_REF", ""), help="Target PR base branch (e.g. main)")
    ap.add_argument("--canonical-branch", default="main", help="Canonical protected branch name (default: main)")
    ap.add_argument("--pr-labels", default=os.environ.get("GITHUB_PR_LABELS", ""), help="Comma-separated GitHub PR labels")
    ap.add_argument("--json", action="store_true", help="Emit structured JSON report")
    args = ap.parse_args(argv)

    labels = {s.strip() for s in args.pr_labels.split(",") if s.strip()}
    report = evaluate_repository(
        args.repo,
        base_ref=args.base_ref or None,
        target_branch=args.target_branch,
        canonical_branch=args.canonical_branch,
        pr_labels=labels,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for w in report["warnings"]:
            print(f"WARN: {w}", file=sys.stderr)
        if report["errors"]:
            for e in report["errors"]:
                print(f"FAIL: {e}", file=sys.stderr)
            return 1
        print(
            f"[OK] Governance v3.1 gate passed ({Path(report['repo']).name}, "
            f"base={report['effective_base_ref'] or 'none'})."
        )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
