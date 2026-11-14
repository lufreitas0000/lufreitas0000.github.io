"""Synthetic contract tests; contain no physical solver results."""
from __future__ import annotations

import copy
import unittest

from scripts.validate_kmf_solver_grid import validate_grid, wilson_interval


def synthetic() -> dict:
    result = {
        "schema_version": 1,
        "publication_status": "draft",
        "provenance": {
            "source_commit": "0" * 40,
            "protocol_commit": "1" * 40,
            "reproduction_command": "synthetic-test-only",
            "h_units": "synthetic-unit-not-physical",
            "initial_state_distribution": "synthetic-test-only",
            "residual_definition": "synthetic-test-only",
            "solver_configs": {"Picard": {}, "damped": {"alpha": 0.5}},
        },
        "seeds": [1, 2],
        "h_grid": [0.0, 0.5],
        "runs": [],
    }
    for h in result["h_grid"]:
        for seed in result["seeds"]:
            for solver in result["provenance"]["solver_configs"]:
                result["runs"].append({
                    "h": h, "seed": seed, "solver": solver,
                    "initial_state_id": f"synthetic-h{h}-seed{seed}",
                    "branch_id": "synthetic-A", "segment_id": "synthetic-1",
                    "converged": True, "failure_reason": None,
                    "map_evaluations": 3, "residual_history": [1, 0.3, 0.01],
                    "history_origin": "raw",
                })
    return result


class TestSolverGridContract(unittest.TestCase):
    def test_accepts_complete_synthetic_paired_design(self) -> None:
        validate_grid(synthetic())

    def test_rejects_missing_pair(self) -> None:
        data = synthetic()
        data["runs"].pop()
        with self.assertRaisesRegex(ValueError, "incomplete"):
            validate_grid(data)

    def test_rejects_unpaired_initial_state(self) -> None:
        data = synthetic()
        data["runs"][1]["initial_state_id"] = "different"
        with self.assertRaisesRegex(ValueError, "unmatched initial"):
            validate_grid(data)

    def test_rejects_padded_history_label_and_unclassified_failure(self) -> None:
        data = synthetic()
        data["runs"][0]["history_origin"] = "padded"
        with self.assertRaisesRegex(ValueError, "unpadded"):
            validate_grid(data)
        data = synthetic()
        data["runs"][0]["converged"] = False
        data["runs"][0]["failure_reason"] = None
        with self.assertRaisesRegex(ValueError, "categorize failure"):
            validate_grid(data)

    def test_reviewed_requires_lu_scientific_review(self) -> None:
        data = synthetic()
        data["publication_status"] = "reviewed"
        with self.assertRaisesRegex(ValueError, "scientific review"):
            validate_grid(data)

    def test_wilson_is_explicit_and_symmetric_for_half_success(self) -> None:
        low, high = wilson_interval(5, 10, .95)
        self.assertAlmostEqual(low, 1 - high, places=12)
        self.assertLess(low, .5)
        self.assertGreater(high, .5)
        with self.assertRaises(ValueError):
            wilson_interval(5, 0, .95)


if __name__ == "__main__":
    unittest.main()
