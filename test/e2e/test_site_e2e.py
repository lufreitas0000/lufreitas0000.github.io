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
        self.assertGreater(len(html_files), 5)
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

    def test_feed_toolbar_has_left_filter_right_search_and_json_index(self) -> None:
        feed_html = (PUBLIC_OUT / "notes" / "index.html").read_text(encoding="utf-8")
        soup = BeautifulSoup(feed_html, "html.parser")
        toolbar = soup.find("div", class_="feed-toolbar")
        self.assertIsNotNone(toolbar)
        self.assertIsNotNone(toolbar.find("div", class_="feed-filter-group"))
        self.assertIsNotNone(toolbar.find("div", class_="feed-search-box"))
        self.assertIsNotNone(soup.find("input", id="feed-search-input"))
        self.assertTrue((PUBLIC_OUT / "notes" / "search-index.json").exists())
        idx = json.loads((PUBLIC_OUT / "notes" / "search-index.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(idx), 4)

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
