"""Exact zero-field reference checks for the Jx=Jy=J, 0<=Jz<=2J sweep."""
from __future__ import annotations

import cmath
import json
import math
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "kitaev-mf-dispersion"
DATA = json.loads((FIXTURE_DIR / "cases.v1.json").read_text(encoding="utf-8"))
TOLERANCE = 5e-12


def structure_factor(J_z_over_J: float, k1: float, k2: float) -> complex:
    return (
        J_z_over_J
        + cmath.exp(2j * math.pi * k1)
        + cmath.exp(2j * math.pi * k2)
    )


def periodic_distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return max(min(abs(x - y), 1 - abs(x - y)) for x, y in zip(a, b))


class TestKitaevDispersionReference(unittest.TestCase):
    def test_notation_and_single_parameter_domain(self) -> None:
        self.assertEqual(DATA["schema_version"], 1)
        self.assertEqual(DATA["publication_status"], "unpublished-fixture")
        self.assertEqual(DATA["symbols"]["structure_factor"], "f")
        self.assertEqual(DATA["symbols"]["walk_endpoint"], "Z=f")
        self.assertEqual(DATA["symbols"]["radial_modulus"], "r=|Z|=|f|")
        self.assertEqual(DATA["color_range"], [0, 4])
        self.assertEqual(
            [case["ratio_Jz_over_J"] for case in DATA["cases"]],
            [0, 0.5, 1, 1.5, 2],
        )
        self.assertNotIn("j_gamma", json.dumps(DATA))

    def test_two_nodes_for_interior_couplings(self) -> None:
        for case in DATA["cases"]:
            ratio = case["ratio_Jz_over_J"]
            if not 0 < ratio < 2:
                continue
            q = math.acos(-ratio / 2) / (2 * math.pi)
            roots = [(q, 1 - q), (1 - q, q)]
            self.assertEqual(case["zero_set"], "two-points")
            self.assertEqual(len(case["roots"]), 2)
            for k in roots:
                with self.subTest(ratio=ratio, k=k):
                    self.assertLess(abs(structure_factor(ratio, *k)), TOLERANCE)
                    self.assertTrue(
                        any(
                            periodic_distance(k, tuple(p)) < TOLERANCE
                            for p in case["roots"]
                        )
                    )

    def test_zero_coupling_has_line_not_two_points(self) -> None:
        case = DATA["cases"][0]
        self.assertEqual(case["zero_set"], "line")
        self.assertEqual(case["roots"], [])
        for k1 in (0, 0.17, 0.24, 0.5, 0.8):
            with self.subTest(k1=k1):
                self.assertLess(
                    abs(structure_factor(0, k1, (k1 + 0.5) % 1)),
                    TOLERANCE,
                )
        self.assertGreater(abs(structure_factor(0, 0.13, 0.13)), 1.9)

    def test_merger_at_two_J(self) -> None:
        case = DATA["cases"][-1]
        self.assertEqual(case["zero_set"], "merged")
        self.assertEqual(case["roots"], [[0.5, 0.5]])
        self.assertLess(abs(structure_factor(2, 0.5, 0.5)), TOLERANCE)
        self.assertGreater(abs(structure_factor(2, 0.49, 0.5)), 0)

    def test_isotropic_walk_landmarks(self) -> None:
        self.assertAlmostEqual(abs(structure_factor(1, 0, 0)), 3, delta=TOLERANCE)
        for k in ((0.5, 0), (0, 0.5), (0.5, 0.5)):
            self.assertAlmostEqual(abs(structure_factor(1, *k)), 1, delta=TOLERANCE)
        for k in ((1 / 3, 2 / 3), (2 / 3, 1 / 3)):
            self.assertLess(abs(structure_factor(1, *k)), TOLERANCE)

    def test_periodicity_and_nonnegative_modulus(self) -> None:
        for case in DATA["cases"]:
            ratio = case["ratio_Jz_over_J"]
            for k1, k2 in ((0.137, 0.293), (0.481, 0.659), (0.812, 0.044)):
                r = abs(structure_factor(ratio, k1, k2))
                self.assertGreaterEqual(r, 0)
                self.assertAlmostEqual(
                    r,
                    abs(structure_factor(ratio, k1 + 1, k2 - 1)),
                    delta=TOLERANCE,
                )
                self.assertLessEqual(r, 2 + ratio + TOLERANCE)

    def test_unpublished_reference_svg(self) -> None:
        path = FIXTURE_DIR / "isotropic-r-reference.svg"
        root = ET.parse(path).getroot()
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        text = "".join(root.itertext())
        self.assertIn("r = |f(k)|", text)
        self.assertIn("UNPUBLISHED", text)
        self.assertIn("Jz = J", text)
        self.assertTrue("jₓ" not in text)
        self.assertGreater(len(root.findall(".//{http://www.w3.org/2000/svg}rect")), 1000)


if __name__ == "__main__":
    unittest.main()
