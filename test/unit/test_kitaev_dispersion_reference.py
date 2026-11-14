"""Independent checks for the unpublished Kitaev-walk dispersion fixture."""
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


def structure_factor(j: list[float], k1: float, k2: float) -> complex:
    jx, jy, jz = j
    return jz + jx * cmath.exp(2j * math.pi * k1) + jy * cmath.exp(2j * math.pi * k2)


def analytic_roots(j: list[float]) -> list[tuple[float, float]]:
    jx, jy, jz = j
    if max(j) > sum(j) - max(j):
        return []
    c1 = (jy**2 - jx**2 - jz**2) / (2 * jx * jz)
    c2 = (jx**2 - jy**2 - jz**2) / (2 * jy * jz)
    t1 = math.acos(max(-1.0, min(1.0, c1)))
    t2 = -math.acos(max(-1.0, min(1.0, c2)))
    first = (t1 / (2 * math.pi) % 1, t2 / (2 * math.pi) % 1)
    second = (-first[0] % 1, -first[1] % 1)
    if all(
        min(abs(a - b), 1 - abs(a - b)) < TOLERANCE
        for a, b in zip(first, second)
    ):
        return [first]
    return [first, second]


def torus_distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return max(min(abs(x - y), 1 - abs(x - y)) for x, y in zip(a, b))


class TestKitaevDispersionReference(unittest.TestCase):
    def test_reference_contract_and_notation(self) -> None:
        self.assertEqual(DATA["schema_version"], 1)
        self.assertEqual(DATA["publication_status"], "unpublished-fixture")
        self.assertEqual(DATA["notation"]["structure_factor"], "f")
        self.assertEqual(DATA["notation"]["walk_endpoint"], "Z=f")
        self.assertEqual(DATA["notation"]["radial_modulus"], "r=|Z|=|f|")
        self.assertTrue(all(all(x > 0 for x in case["j"]) for case in DATA["cases"]))

    def test_roots_independently_satisfy_complex_equation(self) -> None:
        for case in DATA["cases"]:
            with self.subTest(case=case["id"]):
                j = case["j"]
                roots = analytic_roots(j)
                self.assertEqual(len(roots), case["zero_count"])
                for root in roots:
                    self.assertLess(abs(structure_factor(j, *root)), TOLERANCE)
                    self.assertTrue(
                        any(torus_distance(root, tuple(target)) < TOLERANCE
                            for target in case["roots"])
                    )
                for target in case["roots"]:
                    self.assertLess(abs(structure_factor(j, *target)), TOLERANCE)

    def test_triangle_closure_and_exact_gap_minimum(self) -> None:
        for case in DATA["cases"]:
            with self.subTest(case=case["id"]):
                j = case["j"]
                expected = max(0.0, 2 * max(j) - sum(j))
                self.assertAlmostEqual(expected, case["min_r"], delta=TOLERANCE)
                self.assertEqual(case["zero_count"] > 0, expected == 0.0)
                if "min_at" in case:
                    self.assertAlmostEqual(
                        abs(structure_factor(j, *case["min_at"])),
                        expected,
                        delta=TOLERANCE,
                    )

    def test_periodicity_and_reality_of_modulus(self) -> None:
        for case in DATA["cases"]:
            j = case["j"]
            for k in ((0.137, 0.293), (0.481, 0.659), (0.812, 0.044)):
                r = abs(structure_factor(j, *k))
                self.assertGreaterEqual(r, 0)
                self.assertAlmostEqual(
                    r, abs(structure_factor(j, k[0] + 1, k[1] - 1)),
                    delta=TOLERANCE,
                )

    def test_isotropic_walk_landmarks(self) -> None:
        j = [1, 1, 1]
        self.assertAlmostEqual(abs(structure_factor(j, 0, 0)), 3.0, delta=TOLERANCE)
        for k1, k2 in ((0.5, 0), (0, 0.5), (0.5, 0.5)):
            self.assertAlmostEqual(
                abs(structure_factor(j, k1, k2)), 1.0, delta=TOLERANCE
            )
        for root in ((1 / 3, 2 / 3), (2 / 3, 1 / 3)):
            self.assertLess(abs(structure_factor(j, *root)), TOLERANCE)

    def test_svg_is_valid_unpublished_reference(self) -> None:
        path = FIXTURE_DIR / "isotropic-r-reference.svg"
        root = ET.parse(path).getroot()
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn("r = |f(k)|", "".join(root.itertext()))
        self.assertIn("UNPUBLISHED", "".join(root.itertext()))
        self.assertGreater(len(root.findall(".//{http://www.w3.org/2000/svg}rect")), 1000)
        self.assertTrue(str(path).endswith("test/fixtures/kitaev-mf-dispersion/isotropic-r-reference.svg"))


if __name__ == "__main__":
    unittest.main()

