"""Pure validation for unpublished paired Kitaev solver trajectory data."""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from statistics import NormalDist

FAILURES = {
    "stagnation", "oscillation", "divergence", "wrong_branch",
    "iteration_cap", "numerical_error",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_grid(data: dict) -> None:
    require(data.get("schema_version") == 1, "schema_version must be 1")
    require(data.get("publication_status") in ("draft", "reviewed"), "unknown publication status")
    meta = data.get("provenance")
    require(isinstance(meta, dict), "missing provenance")
    for key in (
        "source_commit", "protocol_commit", "reproduction_command",
        "h_units", "initial_state_distribution", "residual_definition",
    ):
        require(isinstance(meta.get(key), str) and bool(meta[key].strip()), "missing provenance." + key)
    for key in ("source_commit", "protocol_commit"):
        require(bool(re.fullmatch(r"[0-9a-fA-F]{40}", meta[key])), "invalid " + key)
    require(isinstance(meta.get("solver_configs"), dict), "missing solver configs")
    methods = list(meta["solver_configs"])
    require(bool(methods), "no solvers")
    seeds = data.get("seeds")
    require(isinstance(seeds, list) and bool(seeds), "missing seed list")
    require(all(type(s) is int and s >= 0 for s in seeds), "seeds must be nonnegative integers")
    require(len(seeds) == len(set(seeds)), "repeated seeds")
    h_grid = data.get("h_grid")
    require(isinstance(h_grid, list) and bool(h_grid), "missing field grid")
    require(all(finite_number(h) and 0 <= h <= 1 for h in h_grid), "field outside user-defined [0,1] range")
    require(h_grid == sorted(set(h_grid)), "h_grid must be strictly ascending")
    runs = data.get("runs")
    require(isinstance(runs, list), "missing runs")
    expected = {(h, seed, method) for h in h_grid for seed in seeds for method in methods}
    observed = set()
    initial_states: dict[tuple[float, int], str] = {}
    for idx, run in enumerate(runs):
        require(isinstance(run, dict), "invalid run")
        key = (run.get("h"), run.get("seed"), run.get("solver"))
        require(key in expected, f"run {idx}: unexpected h/seed/solver")
        require(key not in observed, f"run {idx}: duplicate paired observation")
        observed.add(key)
        for field in ("initial_state_id", "branch_id", "segment_id"):
            require(isinstance(run.get(field), str) and bool(run[field].strip()), f"run {idx}: missing {field}")
        pairing = (run["h"], run["seed"])
        previous = initial_states.setdefault(pairing, run["initial_state_id"])
        require(previous == run["initial_state_id"], f"run {idx}: unmatched initial state")
        require(type(run.get("converged")) is bool, f"run {idx}: missing convergence outcome")
        require(type(run.get("map_evaluations")) is int and run["map_evaluations"] > 0, f"run {idx}: invalid map count")
        residuals = run.get("residual_history")
        require(isinstance(residuals, list) and bool(residuals), f"run {idx}: empty residual history")
        require(all(finite_number(r) and r >= 0 for r in residuals), f"run {idx}: invalid residual")
        require(len(residuals) <= run["map_evaluations"], f"run {idx}: history exceeds map evaluations")
        require(run.get("history_origin") == "raw", f"run {idx}: histories must be unpadded raw records")
        failure = run.get("failure_reason")
        if run["converged"]:
            require(failure is None, f"run {idx}: success cannot have failure_reason")
        else:
            require(failure in FAILURES, f"run {idx}: categorize failure")
    require(observed == expected, "incomplete paired comparison")
    if data["publication_status"] == "reviewed":
        review = data.get("scientific_review")
        require(isinstance(review, dict), "missing scientific review")
        for key in ("reference", "heldout_error_report", "Lu_approved_thresholds"):
            require(review.get(key), "reviewed data requires " + key)
        require("TODO" not in meta["h_units"], "reviewed data must define h units")


def wilson_interval(successes: int, trials: int, confidence_level: float) -> tuple[float, float]:
    """Wilson binomial confidence interval; confidence level is supplied by user."""
    if type(successes) is not int or type(trials) is not int or not 0 <= successes <= trials or trials == 0:
        raise ValueError("invalid counts")
    if not finite_number(confidence_level) or not 0 < confidence_level < 1:
        raise ValueError("invalid confidence level")
    z = NormalDist().inv_cdf((1 + confidence_level) / 2)
    p = successes / trials
    denominator = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denominator
    half = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator
    return max(0., center - half), min(1., center + half)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_kmf_solver_grid.py FILE.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        validate_grid(data)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print("Invalid solver dataset: " + str(error), file=sys.stderr)
        return 1
    print("Solver dataset passes structural checks; scientific validation remains separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
