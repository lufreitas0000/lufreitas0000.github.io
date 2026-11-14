from __future__ import annotations

import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup

from web_engine.domain.contracts import FORBIDDEN_PRIVATE_TOKENS

PKG_ROOT = Path(__file__).resolve().parent.parent.parent
PUBLIC_OUT = PKG_ROOT / "build" / "_site"
FIXTURE_OUT = PKG_ROOT / "build" / "fixtures_site"


class TestSiteE2E(unittest.TestCase):
    def test_primary_nav_has_exact_four_tabs_everywhere(self) -> None:
        html_files = list(PUBLIC_OUT.rglob("*.html"))
        self.assertGreaterEqual(len(html_files), 5)
        for html_file in html_files:
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
            nav = soup.find("nav", attrs={"aria-label": "Primary"})
            self.assertIsNotNone(nav, f"Missing primary nav in {html_file}")
            links = [a.get_text(strip=True) for a in nav.find_all("a")]
            self.assertEqual(links, ["Home", "Research", "About Me", "Feed"])

    def test_accessibility_landmarks_and_single_h1(self) -> None:
        for html_file in PUBLIC_OUT.rglob("*.html"):
            soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
            self.assertIsNotNone(soup.find("a", class_="skip-link"))
            self.assertIsNotNone(soup.find("main", id="main-content"))
            self.assertEqual(len(soup.find_all("h1")), 1, f"Expected 1 h1 in {html_file}")

    def test_three_project_notes_are_published(self) -> None:
        feed_html = (PUBLIC_OUT / "notes" / "index.html").read_text(encoding="utf-8")
        soup = BeautifulSoup(feed_html, "html.parser")
        cards = soup.select(".feed-card")
        self.assertEqual(len(cards), 3)
        self.assertTrue(all(card.get("data-kind") == "project" for card in cards))
        self.assertFalse(soup.select(".feed-tag-btn"))

        published = {
            "kitaev-mf": "https://github.com/lufreitas0000/kitaev-mf",
            "kitaev-derivation-jl": "https://github.com/lufreitas0000/KitaevDerivation.jl",
            "bosonize-lean": "https://github.com/lufreitas0000/bosonize-lean",
        }
        for slug, source in published.items():
            path = PUBLIC_OUT / "notes" / "feed" / f"{slug}.html"
            self.assertTrue(path.exists(), path)
            note = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
            self.assertEqual(len(note.find_all("h1")), 1)
            self.assertIsNotNone(note.find("a", href=source))
            self.assertTrue(note.select_one(".note-provenance").has_attr("hidden"))
            crumbs = note.find("nav", attrs={"aria-label": "Breadcrumb"})
            self.assertEqual(
                [link["href"] for link in crumbs.find_all("a")],
                ["../../index.html", "../index.html"],
            )

        julia = (PUBLIC_OUT / "notes" / "feed" / "kitaev-derivation-jl.html").read_text(encoding="utf-8")
        self.assertIn("currently paused", julia)
        self.assertIn("Lean 4", julia)
        bosonize = (PUBLIC_OUT / "notes" / "feed" / "bosonize-lean.html").read_text(encoding="utf-8")
        self.assertIn("finite energy cutoff", bosonize)
        self.assertIn("infinite-volume limits", bosonize)
        self.assertIn("https://github.com/yang-mills-group/YM", bosonize)

        self.assertFalse((PUBLIC_OUT / "notes" / "feed" / "open-followups-kitaev-defects-and-vortices.html").exists())
        self.assertFalse((PUBLIC_OUT / "notes" / "thesis-chapters.html").exists())
        self.assertFalse((PUBLIC_OUT / "notes" / "series").exists())

        search_index = json.loads(
            (PUBLIC_OUT / "notes" / "search-index.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(published), {entry["id"] for entry in search_index})
        self.assertTrue(all(entry["keywords"] for entry in search_index))
        self.assertTrue(all(entry["kind"] == "project" for entry in search_index))

    def test_kitaev_mf_hub_is_standalone_and_future_notes_are_not_linked(self) -> None:
        path = PUBLIC_OUT / "notes" / "feed" / "kitaev-mf.html"
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(len(soup.find_all("h1")), 1)

        headings = soup.select("main h2")
        section_ids = {heading.get("id") for heading in headings}
        self.assertGreaterEqual(len(headings), 5)
        self.assertTrue(
            {"majorana", "fixed-point", "benchmarks", "directions", "series"}.issubset(section_ids),
            section_ids,
        )
        text = soup.get_text(" ", strip=True)
        for phrase in (
            "quasifree",
            "fixed-point",
            "self-consistent",
            "anisotropic",
            "perturbation theory",
            "Gaussian",
            "physical",
            "planned",
        ):
            self.assertIn(phrase.lower(), text.lower())

        note_html = str(soup)
        self.assertIn(r"\Phi", note_html)
        self.assertIn(r"\bar U", note_html)
        self.assertIn(r"\mathbf 1", note_html)
        self.assertIsNotNone(
            soup.find("a", href="https://lufreitas0000.github.io/kitaev-mf/kitaev-mf-labbook.pdf")
        )
        self.assertIsNotNone(
            soup.find("a", href="https://github.com/lufreitas0000/kitaev-mf/blob/main/doc/MILESTONE_ROADMAP.md")
        )

        for link in soup.select("main a[href]"):
            href = link.get("href", "")
            if href.startswith(("http:", "https:", "mailto:", "#")):
                continue
            self.assertTrue(
                (path.parent / href).resolve().exists(),
                f"Broken internal article link: {href}",
            )
        self.assertEqual(len(soup.select(".note-provenance:not([hidden])")), 0)
        self.assertFalse(
            any(
                path.name in link.get("href", "")
                for path in (
                    Path("kitaev-mf-fixed-point-map.html"),
                    Path("kitaev-mf-exact-reference.html"),
                    Path("kitaev-mf-solver-acceleration.html"),
                )
                for link in soup.select("main a[href]")
            )
        )

    def test_kitaev_dispersion_local_fallback_and_controls(self) -> None:
        article_path = PUBLIC_OUT / "notes" / "feed" / "kitaev-mf.html"
        soup = BeautifulSoup(article_path.read_text(encoding="utf-8"), "html.parser")
        island = soup.find("figure", id="kmf-dispersion")
        self.assertIsNotNone(island)
        image = island.find("img")
        self.assertFalse(image.has_attr("hidden"))
        self.assertTrue((article_path.parent / image["src"]).resolve().is_file())
        self.assertTrue(island.find("canvas").has_attr("hidden"))
        self.assertTrue(island.find(class_="kmf-controls").has_attr("hidden"))
        slider = island.find("input", id="kmf-jz-ratio")
        self.assertEqual(
            (slider["min"], slider["max"], slider["step"], slider["value"]),
            ("0", "2", "0.02", "1"),
        )
        script = soup.find("script", src="../../assets/js/kitaev_dispersion.mjs")
        self.assertEqual(script.get("type"), "module")
        self.assertTrue((article_path.parent / script["src"]).resolve().is_file())
        for page in ("index.html", "research.html", "about.html"):
            html = (PUBLIC_OUT / page).read_text(encoding="utf-8")
            self.assertNotIn('id="kmf-dispersion"', html)
            self.assertNotIn("kitaev_dispersion.mjs", html)

    def test_ubar_quadrature_has_static_table_and_optional_controls(self) -> None:
        path = PUBLIC_OUT / "notes" / "feed" / "kitaev-mf.html"
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        island = soup.find("figure", id="kmf-ubar")
        self.assertIsNotNone(island)
        self.assertGreaterEqual(len(island.select("tbody tr")), 5)
        self.assertTrue(island.find(class_="kmf-ubar-controls").has_attr("hidden"))
        self.assertIn("0.5248657458506", island.get_text())
        self.assertIsNotNone(soup.find("script", src="../../assets/js/kitaev_ubar.mjs"))
        self.assertTrue((path.parent / "../../assets/js/kitaev_ubar.mjs").resolve().is_file())

    def test_jacobian_and_claim_ledger_have_accessible_static_fallbacks(self) -> None:
        path = PUBLIC_OUT / "notes" / "feed" / "kitaev-mf.html"
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        jac = soup.find("figure", id="kmf-jacobian")
        self.assertIsNotNone(jac)
        img = jac.find("img")
        self.assertFalse(img.has_attr("hidden"))
        self.assertTrue((path.parent / img["src"]).resolve().is_file())
        self.assertTrue(jac.find("canvas").has_attr("hidden"))
        self.assertTrue(jac.find(class_="kmf-controls").has_attr("hidden"))
        self.assertIsNotNone(soup.find("script", src="../../assets/js/kitaev_jacobian_toy.mjs"))
        details = soup.select("details.kmf-claim-ledger")
        self.assertEqual(len(details), 1)
        self.assertIn("Uncontrolled approximation", details[0].get_text())
        self.assertEqual(len(soup.select("details.kmf-figure-provenance")), 1)

    def test_home_personal_intro_and_gallery(self) -> None:
        import yaml

        home = BeautifulSoup((PUBLIC_OUT / "index.html").read_text(encoding="utf-8"), "html.parser")
        self.assertIn("passionate about understanding nature through theory and mathematics", home.get_text())
        img = home.find("img", src="assets/img/gallery/home/kitaev-vortex-gauge-string.svg")
        self.assertIsNotNone(img)
        self.assertIn("gauge string", img["alt"])

        gallery = PKG_ROOT / "site" / "assets" / "img" / "gallery"
        manifest = yaml.safe_load((gallery / "index.yml").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        ids = [entry["id"] for entry in manifest["entries"]]
        self.assertEqual(len(ids), len(set(ids)))
        for entry in manifest["entries"]:
            selected = gallery / entry["file"]
            original = gallery / entry["original"]
            self.assertTrue(selected.is_file(), selected)
            self.assertTrue(original.is_file(), original)
            self.assertEqual(selected.read_bytes(), original.read_bytes())
            self.assertTrue((PUBLIC_OUT / "assets" / "img" / "gallery" / entry["file"]).is_file())


    def test_fixture_notes_support_search_math_and_breadcrumbs(self) -> None:
        fixture_index = FIXTURE_OUT / "notes" / "index.html"
        soup = BeautifulSoup(fixture_index.read_text(encoding="utf-8"), "html.parser")
        self.assertIsNotNone(soup.find("button", id="feed-search-toggle"))
        search_input = soup.find("input", id="feed-search-input")
        self.assertIsNotNone(search_input)
        self.assertTrue(search_input.has_attr("hidden"))
        self.assertFalse(soup.select(".feed-tag-btn"))
        fixture_entries = json.loads((FIXTURE_OUT / "notes" / "search-index.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(fixture_entries), 4)
        self.assertTrue(any(entry["tags"] for entry in fixture_entries))

        note_path = FIXTURE_OUT / "notes" / "feed" / "microscopic-superexchange-and-electric-polarization.html"
        note = BeautifulSoup(note_path.read_text(encoding="utf-8"), "html.parser")
        title = note.find("h1")
        self.assertIsNotNone(title)
        self.assertIn(r"\(t_{2g}^5\)", title.get_text())
        breadcrumb = note.find("nav", attrs={"aria-label": "Breadcrumb"})
        self.assertIsNotNone(breadcrumb)
        links = [link["href"] for link in breadcrumb.find_all("a")]
        self.assertEqual(links, ["../../index.html", "../index.html"])
        for href in links:
            self.assertTrue((note_path.parent / href).resolve().exists())
        self.assertEqual(len(note.find_all("h1")), 1)
        self.assertFalse(note.select(".paper-citation-line"))
        provenance = note.select_one(".note-provenance")
        self.assertIsNotNone(provenance)
        self.assertTrue(provenance.has_attr("hidden"))
        self.assertNotIn("Category: Expository-Note", note.get_text())

    def test_floating_navigation_and_top_control(self) -> None:
        soup = BeautifulSoup((PUBLIC_OUT / "research.html").read_text(encoding="utf-8"), "html.parser")
        self.assertIsNotNone(soup.find("nav", id="floating-navigation"))
        self.assertIsNotNone(soup.find("button", id="quick-menu-toggle"))
        self.assertIsNotNone(soup.find("button", id="back-to-top"))
        self.assertIsNotNone(soup.find("script", src="assets/js/site_navigation.js"))
        self.assertTrue((PUBLIC_OUT / "assets" / "js" / "site_navigation.js").exists())

    def test_privacy_hygiene_across_all_public_outputs(self) -> None:
        for f in PUBLIC_OUT.rglob("*"):
            if f.is_file() and f.suffix in (".html", ".xml", ".json", ".md", ".txt"):
                txt = f.read_text(encoding="utf-8").lower()
                for tok in FORBIDDEN_PRIVATE_TOKENS:
                    self.assertNotIn(tok.lower(), txt, f"Token {tok!r} leaked in {f}")

    def test_rss_and_sitemap_and_json_ld_valid(self) -> None:
        ET.fromstring((PUBLIC_OUT / "notes" / "index.xml").read_text(encoding="utf-8"))
        ET.fromstring((PUBLIC_OUT / "sitemap.xml").read_text(encoding="utf-8"))
        home_html = (PUBLIC_OUT / "index.html").read_text(encoding="utf-8")
        self.assertIn("application/ld+json", home_html)
        self.assertIn("https://lufreitas0000.github.io/", home_html)

    def test_fixtures_isolated_from_public_build(self) -> None:
        self.assertFalse((PUBLIC_OUT / "notes" / "posts").exists())
        self.assertTrue((FIXTURE_OUT / "notes" / "posts").exists())


if __name__ == "__main__":
    unittest.main()
