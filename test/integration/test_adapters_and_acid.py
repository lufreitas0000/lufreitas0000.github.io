from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from web_engine.domain.contracts import ContractViolationError
from web_engine.domain.models import FeedNode, StagedArtifact
from web_engine.infra.acid_store import AcidFilesystemStore
from web_engine.infra.feed_renderer import render_feed_search_index
from web_engine.infra.markdown_repo import FileSystemContentRepository
from web_engine.services.build_site import make_staged_artifact

PKG_ROOT = Path(__file__).resolve().parent.parent.parent
SITE_ROOT = PKG_ROOT / "site"


class TestAdaptersAndAcid(unittest.TestCase):
    def test_repository_loads_profile_publications_and_feed_nodes(self) -> None:
        repo = FileSystemContentRepository(SITE_ROOT, PKG_ROOT / "test" / "fixtures")
        profile = repo.load_profile()
        self.assertEqual(profile["public_email"], "lu.rdf@icloud.com")
        pubs = repo.load_publications()
        self.assertEqual(len(pubs), 5)
        feed_nodes = repo.load_feed_nodes()
        self.assertGreaterEqual(len(feed_nodes), 4)

    def test_search_index_json_omits_body_markdown(self) -> None:
        node = FeedNode(
            node_id="k1",
            title="Kitaev Note",
            subtitle="Sub",
            date="2026-11",
            order=10,
            visible=True,
            kind="note",
            tags=("kitaev",),
            keywords=("vortex", "majorana"),
            summary="Short summary",
            body_markdown="VERY_LONG_BODY_SHOULD_NOT_BE_IN_INDEX",
            source_path="content/feed/k1.md",
            sha256="0",
        )
        raw = render_feed_search_index((node,))
        data = json.loads(raw)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["keywords"], ["vortex", "majorana"])
        self.assertNotIn("VERY_LONG_BODY_SHOULD_NOT_BE_IN_INDEX", raw)

    def test_acid_store_rolls_back_on_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "_site"
            target.mkdir()
            sentinel = target / "index.html"
            sentinel.write_text("<html><body>good</body></html>", encoding="utf-8")

            store = AcidFilesystemStore(SITE_ROOT)
            bad = make_staged_artifact("index.html", '<html><body><a href="missing.html">bad</a></body></html>')
            with self.assertRaises(ContractViolationError):
                store.commit_artifacts_atomically(target, (bad,), (), ())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "<html><body>good</body></html>")


if __name__ == "__main__":
    unittest.main()
