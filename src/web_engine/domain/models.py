"""Immutable domain value objects for the website engine and DAG navigation graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class MarginFigure:
    src: str
    alt: str
    caption: str = ""
    kind: str = "flagship"
    max_width: str = "100%"


@dataclass(frozen=True)
class MarginNote:
    pill_text: str
    body_text: str
    pill_tone: str = "neutral"  # "neutral" | "quiet" | "pink" | "blue"
    element_id: str = ""


@dataclass(frozen=True)
class DirectoryRow:
    label: str
    href: str
    description_text: str


@dataclass(frozen=True)
class PublicationRecord:
    pub_id: str
    title: str
    authors: str
    journal: str
    volume_pages: str
    year: int
    doi: str
    doi_url: str
    arxiv_id: str | None = None
    arxiv_url: str | None = None


@dataclass(frozen=True)
class ContentSection:
    section_id: str
    title: str
    order: int
    visible: bool
    body_markdown: str
    source_path: str
    sha256: str
    publication_id: str | None = None
    publication: PublicationRecord | None = None
    citation_line_text: str | None = None
    figures: tuple[MarginFigure, ...] = ()
    margin_notes: tuple[MarginNote, ...] = ()
    directory_rows: tuple[DirectoryRow, ...] = ()
    include_theses_list: bool = False
    include_education_table: bool = False
    include_external_references: bool = False
    include_notes_archive: bool = False


@dataclass(frozen=True)
class FeedNode:
    """Unified blog/feed post node (Note, Expository Note, Series, Video, or Project)."""

    node_id: str
    title: str
    subtitle: str
    date: str
    order: int
    visible: bool
    kind: str
    tags: tuple[str, ...]
    summary: str
    body_markdown: str
    source_path: str
    sha256: str
    target_href: str = ""
    external_url: str = ""
    figures: tuple[MarginFigure, ...] = ()
    lang: str = "en"
    keywords: tuple[str, ...] = ()
    evidence_status: str = "verified-note"
    revised_at: str = ""
    series: str = ""
    prerequisites: str = ""
    conventions: str = ""
    source_links: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class NotePost:
    """Legacy/fixture .qmd note post loaded for static rendering."""

    slug: str
    title: str
    subtitle: str
    date: str
    revised_at: str
    lang: str
    article_type: str
    evidence_status: str
    body_markdown: str
    series: str = ""
    prerequisites: str = ""
    conventions: str = ""
    source_links: tuple[tuple[str, str], ...] = ()
    notebook_path: Path | None = None


@dataclass(frozen=True)
class SiteNode:
    """A node in the website's Directed Acyclic Graph (DAG) navigation hierarchy."""

    node_id: str
    title: str
    rel_href: str
    parent_id: str | None = None
    visible: bool = True
    kind: str = "page"
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class SitemapBranch:
    """Pure structural grouping of a primary node and its visible child nodes."""

    root: SiteNode
    children: tuple[SiteNode, ...]


@dataclass(frozen=True)
class SiteGraph:
    """Verified Directed Acyclic Graph (DAG) of website nodes."""

    nodes: dict[str, SiteNode]
    children_map: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class PageSpec:
    page_id: str
    node_id: str
    slug: str
    output_rel_path: str
    title: str
    subtitle: str
    lang: str = "en"
    hide_page_title: bool = False
    lead_html: str = ""
    colophon_html: str = ""
    sections: tuple[ContentSection, ...] = ()


@dataclass(frozen=True)
class StagedArtifact:
    rel_path: str
    content_bytes: bytes
    sha256: str


@dataclass(frozen=True)
class BuildConfig:
    out_dir: Path
    include_dev_fixtures: bool = False
    base_url_override: str | None = None
    write_qmd_sources: bool = True


@dataclass(frozen=True)
class BuildReceipt:
    out_dir: str
    pages_rendered: int
    visible_sections_count: int
    hidden_sections_count: int
    published_notes_count: int
    feed_posts_count: int
    artifact_hashes: dict[str, str] = field(default_factory=dict)
