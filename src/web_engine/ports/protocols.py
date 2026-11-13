"""Abstract ports (Protocols) decoupling domain/services from I/O, rendering, and storage."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Protocol, runtime_checkable

from ..domain.models import (
    ContentSection,
    FeedNode,
    NotePost,
    PageSpec,
    PublicationRecord,
    SiteGraph,
    StagedArtifact,
)


@runtime_checkable
class ContentRepositoryPort(Protocol):
    """Driven port for loading profile metadata, publications, sections, feed nodes, and aux pages."""

    @property
    def site_root(self) -> Path: ...

    def load_profile(self) -> dict[str, Any]: ...

    def load_publications(self) -> dict[str, PublicationRecord]: ...

    def load_raw_publications_yaml(self) -> dict[str, Any]: ...

    def load_sections(self, group_dir: str) -> tuple[ContentSection, ...]: ...

    def load_feed_nodes(self) -> tuple[FeedNode, ...]: ...

    def load_note_posts(self, include_dev_fixtures: bool = False) -> tuple[NotePost, ...]: ...

    def load_aux_page_source(self, rel_qmd_path: str) -> tuple[dict[str, Any], str]: ...


@runtime_checkable
class RendererPort(Protocol):
    """Driving/Driven port for compiling PageSpecs, Feed controls, SEO/RSS, and Quarto .qmd."""

    def build_partials(
        self,
        profile: dict[str, Any],
        pubs_raw: dict[str, Any],
        published_notes: tuple[NotePost, ...],
    ) -> dict[str, str]: ...

    def render_page_html(
        self,
        page: PageSpec,
        profile: dict[str, Any],
        partials: dict[str, str],
        css_rel_path: str,
        root_rel_prefix: str,
        site_graph: SiteGraph | None = None,
    ) -> str: ...

    def render_page_qmd(
        self,
        page: PageSpec,
        partials: dict[str, str],
    ) -> str: ...

    def render_unified_feed_index_html(
        self,
        feed_nodes: Iterable[FeedNode],
        root_rel_prefix: str = "../",
    ) -> str: ...

    def render_feed_search_index_json(self, feed_nodes: Iterable[FeedNode]) -> str: ...

    def render_feed_metadata_box(self, node: FeedNode) -> str: ...

    def render_note_post_lead_html(self, post: NotePost) -> str: ...

    def render_markdown_fragment(self, md_text: str) -> str: ...

    def render_working_with_me_markdown(self, profile: dict[str, Any]) -> str: ...

    def render_rss_xml(self, notes: Iterable[NotePost], base_url: str) -> str: ...

    def render_sitemap_xml(self, site_graph: SiteGraph, base_url: str) -> str: ...

    def render_robots_txt(self, base_url: str) -> str: ...


@runtime_checkable
class AtomicStorePort(Protocol):
    """Driven port for ACID transactional artifact persistence and optional QMD sync."""

    def write_source_text(self, rel_path: str, content: str) -> None: ...

    def commit_artifacts_atomically(
        self,
        target_dir: Path,
        artifacts: tuple[StagedArtifact, ...],
        static_dirs_to_copy: tuple[tuple[Path, str], ...],
        static_files_to_copy: tuple[tuple[Path, str], ...],
    ) -> dict[str, str]: ...
