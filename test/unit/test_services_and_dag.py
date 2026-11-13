from __future__ import annotations

import unittest
from pathlib import Path
from typing import Any, Iterable

from web_engine.domain.contracts import ContractViolationError
from web_engine.domain.models import (
    BuildConfig,
    ContentSection,
    FeedNode,
    NotePost,
    PageSpec,
    PublicationRecord,
    SiteGraph,
    SiteNode,
    StagedArtifact,
)
from web_engine.ports.protocols import AtomicStorePort, ContentRepositoryPort, RendererPort
from web_engine.services.build_site import build_site
from web_engine.services.dag import (
    build_and_verify_site_dag,
    compute_breadcrumb_trail,
    get_visible_sitemap_branches,
)
from web_engine.services.pipeline import compose_page


class _FakeRepo:
    @property
    def site_root(self) -> Path:
        return Path("/fake/site")

    def load_profile(self) -> dict[str, Any]:
        return {"canonical_base_url": "https://lufreitas0000.github.io"}

    def load_publications(self) -> dict[str, PublicationRecord]:
        return {}

    def load_raw_publications_yaml(self) -> dict[str, Any]:
        return {}

    def load_sections(self, group_dir: str) -> tuple[ContentSection, ...]:
        return (
            ContentSection(
                section_id=f"{group_dir}-1",
                title="Section",
                order=10,
                visible=True,
                body_markdown="Hello",
                source_path=f"{group_dir}/01.md",
                sha256="0",
            ),
        )

    def load_feed_nodes(self) -> tuple[FeedNode, ...]:
        return (
            FeedNode(
                node_id="test-post",
                title="Test Post",
                subtitle="Sub",
                date="2026-11",
                order=10,
                visible=True,
                kind="note",
                tags=("kitaev",),
                summary="Summary",
                body_markdown="Body",
                source_path="feed/01.md",
                sha256="0",
            ),
        )

    def load_note_posts(self, include_dev_fixtures: bool = False) -> tuple[NotePost, ...]:
        return ()

    def load_aux_page_source(self, rel_qmd_path: str) -> tuple[dict[str, Any], str]:
        return {"title": "Aux", "lang": "en"}, "Aux body"


class _FakeRenderer:
    def build_partials(self, profile: dict[str, Any], pubs_raw: dict[str, Any], published_notes: tuple[NotePost, ...]) -> dict[str, str]:
        return {}

    def render_page_html(self, page: PageSpec, profile: dict[str, Any], partials: dict[str, str], css_rel_path: str, root_rel_prefix: str, site_graph: SiteGraph | None = None) -> str:
        return f"<html><body>{page.title}</body></html>"

    def render_page_qmd(self, page: PageSpec, partials: dict[str, str]) -> str:
        return f"---\ntitle: {page.title}\n---\n"

    def render_unified_feed_index_html(self, feed_nodes: Iterable[FeedNode], root_rel_prefix: str = "../") -> str:
        return "<div>feed</div>"

    def render_feed_search_index_json(self, feed_nodes: Iterable[FeedNode]) -> str:
        return "[]"

    def render_feed_metadata_box(self, node: FeedNode) -> str:
        return "<div>meta</div>"

    def render_note_post_lead_html(self, post: NotePost) -> str:
        return "<div>lead</div>"

    def render_markdown_fragment(self, md_text: str) -> str:
        return f"<p>{md_text}</p>"

    def render_working_with_me_markdown(self, profile: dict[str, Any]) -> str:
        return "# WWM"

    def render_rss_xml(self, notes: Iterable[NotePost], base_url: str) -> str:
        return "<rss/>"

    def render_sitemap_xml(self, site_graph: SiteGraph, base_url: str) -> str:
        return "<urlset/>"

    def render_robots_txt(self, base_url: str) -> str:
        return "User-agent: *"


class _FakeStore:
    def __init__(self) -> None:
        self.committed: dict[str, bytes] = {}

    def write_source_text(self, rel_path: str, content: str) -> None:
        pass

    def commit_artifacts_atomically(
        self,
        target_dir: Path,
        artifacts: tuple[StagedArtifact, ...],
        static_dirs_to_copy: tuple[tuple[Path, str], ...],
        static_files_to_copy: tuple[tuple[Path, str], ...],
    ) -> dict[str, str]:
        self.committed = {a.rel_path: a.content_bytes for a in artifacts}
        return {a.rel_path: a.sha256 for a in artifacts}


class TestServicesAndDag(unittest.TestCase):
    def test_compose_page_filters_hidden_and_sorts(self) -> None:
        secs = (
            ContentSection("b", "B", 20, True, "b", "b.md", "0"),
            ContentSection("h", "H", 5, False, "h", "h.md", "0"),
            ContentSection("a", "A", 10, True, "a", "a.md", "0"),
        )
        page = compose_page("p", "p", "p.html", "P", "", secs, {})
        self.assertEqual([s.section_id for s in page.sections], ["a", "b"])

    def test_dag_detects_cycle(self) -> None:
        n1 = SiteNode("a", "A", "a.html", parent_id="b")
        n2 = SiteNode("b", "B", "b.html", parent_id="a")
        with self.assertRaises(ContractViolationError):
            build_and_verify_site_dag((n1, n2))

    def test_dag_breadcrumbs_and_branches(self) -> None:
        g = build_and_verify_site_dag(
            (
                SiteNode("home", "Home", "index.html", parent_id=None, kind="root"),
                SiteNode("notes", "Feed", "notes/index.html", parent_id="home", kind="page"),
                SiteNode("post", "Post", "notes/feed/post.html", parent_id="notes", kind="note"),
            )
        )
        trail = compute_breadcrumb_trail(g, "post")
        self.assertEqual([n.node_id for n in trail], ["home", "notes", "post"])
        branches = get_visible_sitemap_branches(g)
        self.assertEqual(len(branches), 2)
        self.assertEqual([c.node_id for c in branches[1].children], ["post"])

    def test_build_site_orchestrator_with_fake_ports(self) -> None:
        repo = _FakeRepo()
        renderer = _FakeRenderer()
        store = _FakeStore()
        self.assertIsInstance(repo, ContentRepositoryPort)
        self.assertIsInstance(renderer, RendererPort)
        self.assertIsInstance(store, AtomicStorePort)

        receipt = build_site(repo, renderer, store, BuildConfig(out_dir=Path("/fake/out"), write_qmd_sources=False))
        self.assertEqual(receipt.feed_posts_count, 1)
        self.assertIn("notes/search-index.json", store.committed)
        self.assertIn("notes/feed/test-post.html", store.committed)


if __name__ == "__main__":
    unittest.main()
