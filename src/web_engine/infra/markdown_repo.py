"""Driven Adapter: Loads YAML data, modular Markdown sections, Feed nodes, and NotePosts."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any
import yaml

from ..domain.contracts import ContractViolationError, require_privacy_hygiene
from ..domain.models import (
    ContentSection,
    DirectoryRow,
    FeedNode,
    MarginFigure,
    MarginNote,
    NotePost,
    PublicationRecord,
)
from .notebook_parser import parse_qmd_file


class FileSystemContentRepository:
    """Implements ContentRepositoryPort against `site/` and optional `test/fixtures/`."""

    def __init__(self, site_root: Path, fixtures_root: Path | None = None) -> None:
        self._site_root = site_root
        self._data_dir = site_root / "data"
        self._content_dir = site_root / "content"
        self._fixtures_root = fixtures_root

    @property
    def site_root(self) -> Path:
        return self._site_root

    def load_profile(self) -> dict[str, Any]:
        return yaml.safe_load((self._data_dir / "profile.yml").read_text(encoding="utf-8"))

    def load_raw_publications_yaml(self) -> dict[str, Any]:
        return yaml.safe_load((self._data_dir / "publications.yml").read_text(encoding="utf-8"))

    def load_publications(self) -> dict[str, PublicationRecord]:
        raw = self.load_raw_publications_yaml()
        records: dict[str, PublicationRecord] = {}
        for item in raw.get("authored_publications", []):
            rec = PublicationRecord(
                pub_id=str(item["id"]),
                title=str(item["title"]),
                authors=str(item["authors"]),
                journal=str(item["journal"]),
                volume_pages=str(item.get("volume_pages", "")),
                year=int(item["year"]),
                doi=str(item["doi"]),
                doi_url=str(item["doi_url"]),
                arxiv_id=str(item["arxiv_id"]) if item.get("arxiv_id") else None,
                arxiv_url=str(item["arxiv_url"]) if item.get("arxiv_url") else None,
            )
            records[rec.pub_id] = rec
        return records

    def load_sections(self, group_dir: str) -> tuple[ContentSection, ...]:
        folder = self._content_dir / group_dir
        if not folder.exists():
            raise ContractViolationError(f"Missing modular content folder: {folder}")
        return tuple(self._parse_section_file(p) for p in sorted(folder.glob("*.md")))

    def load_feed_nodes(self) -> tuple[FeedNode, ...]:
        folder = self._content_dir / "feed"
        if not folder.exists():
            return ()
        return tuple(self._parse_feed_file(p) for p in sorted(folder.glob("*.md")))

    def load_note_posts(self, include_dev_fixtures: bool = False) -> tuple[NotePost, ...]:
        sources: list[Path] = []
        posts_dir = self._site_root / "notes" / "posts"
        if posts_dir.exists():
            sources.extend(sorted(posts_dir.glob("*.qmd")))
        if include_dev_fixtures and self._fixtures_root:
            dev_notes = self._fixtures_root / "notes"
            if dev_notes.exists():
                sources.extend(sorted(dev_notes.glob("*.qmd")))

        posts: list[NotePost] = []
        for qmd_path in sources:
            fm, body_md = parse_qmd_file(qmd_path)
            if fm.get("draft", False) or not fm.get("visible", True):
                continue
            require_privacy_hygiene(body_md, context=str(qmd_path))
            slug = qmd_path.stem
            pub_date = str(fm.get("date", "2026-11-09"))
            nb_rel = fm.get("notebook_path")
            nb_path = (qmd_path.parent / str(nb_rel)).resolve() if nb_rel else None
            src_links = tuple(
                (str(s.get("label", s["url"])), str(s["url"]))
                for s in (fm.get("source_links") or [])
                if isinstance(s, dict) and s.get("url")
            )
            posts.append(
                NotePost(
                    slug=slug,
                    title=str(fm.get("title", slug)),
                    subtitle=str(fm.get("subtitle", "")),
                    date=pub_date,
                    revised_at=str(fm.get("revised_at", pub_date)),
                    lang=str(fm.get("lang", "en")),
                    article_type=str(fm.get("article_type", "research-note")),
                    evidence_status=str(fm.get("evidence_status", "exploratory-draft")),
                    body_markdown=body_md,
                    series=str(fm.get("series") or ""),
                    prerequisites=str(fm.get("prerequisites") or ""),
                    conventions=str(fm.get("conventions") or ""),
                    source_links=src_links,
                    notebook_path=nb_path,
                )
            )
        return tuple(posts)

    def load_aux_page_source(self, rel_qmd_path: str) -> tuple[dict[str, Any], str]:
        return parse_qmd_file(self._site_root / rel_qmd_path)

    def _parse_frontmatter(self, path: Path) -> tuple[dict[str, Any], str, str]:
        raw_bytes = path.read_bytes()
        sha = hashlib.sha256(raw_bytes).hexdigest()
        raw_text = raw_bytes.decode("utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw_text, flags=re.DOTALL)
        if not m:
            raise ContractViolationError(f"Modular file {path} is missing YAML frontmatter (--- ... ---).")
        fm_clean = re.sub(r'(?<!\\)\\(?![\\"])', r"\\\\", m.group(1))
        fm = yaml.safe_load(fm_clean) or {}
        body_md = m.group(2).strip()
        require_privacy_hygiene(body_md, context=str(path))
        return fm, body_md, sha

    def _parse_figures(self, fm: dict[str, Any]) -> tuple[MarginFigure, ...]:
        return tuple(
            MarginFigure(
                src=str(f["src"]),
                alt=str(f["alt"]),
                caption=str(f.get("caption", "")),
                kind=str(f.get("kind", "flagship")),
                max_width=str(f.get("max_width", "100%")),
            )
            for f in (fm.get("figures") or [])
        )

    def _parse_section_file(self, path: Path) -> ContentSection:
        fm, body_md, sha = self._parse_frontmatter(path)
        notes = tuple(
            MarginNote(
                pill_text=str(n["pill"]),
                body_text=str(n["body"]),
                pill_tone=str(n.get("tone", "neutral")),
                element_id=str(n.get("id", "")),
            )
            for n in (fm.get("margin_notes") or [])
        )
        dir_rows = tuple(
            DirectoryRow(
                label=str(r["label"]),
                href=str(r["href"]),
                description_text=str(r["description"]),
            )
            for r in (fm.get("directory_rows") or [])
        )
        return ContentSection(
            section_id=str(fm.get("id", path.stem)),
            title=str(fm.get("title", "")),
            order=int(fm.get("order", 100)),
            visible=bool(fm.get("visible", True)),
            body_markdown=body_md,
            source_path=str(path.relative_to(self._site_root)),
            sha256=sha,
            publication_id=str(fm["publication_id"]) if fm.get("publication_id") else None,
            citation_line_text=str(fm["citation_line"]) if fm.get("citation_line") else None,
            figures=self._parse_figures(fm),
            margin_notes=notes,
            directory_rows=dir_rows,
            include_theses_list=bool(fm.get("include_theses_list", False)),
            include_education_table=bool(fm.get("include_education_table", False)),
            include_external_references=bool(fm.get("include_external_references", False)),
            include_notes_archive=bool(fm.get("include_notes_archive", False)),
        )

    def _parse_feed_file(self, path: Path) -> FeedNode:
        fm, body_md, sha = self._parse_frontmatter(path)
        tags = tuple(str(t) for t in (fm.get("tags") or []))
        keywords = tuple(str(k) for k in (fm.get("keywords") or []))
        src_links = tuple(
            (str(s.get("label", s["url"])), str(s["url"]))
            for s in (fm.get("source_links") or [])
            if isinstance(s, dict) and s.get("url")
        )
        pub_date = str(fm.get("date", "2026-11"))
        return FeedNode(
            node_id=str(fm.get("id", path.stem)),
            title=str(fm["title"]),
            subtitle=str(fm.get("subtitle", "")),
            date=pub_date,
            order=int(fm.get("order", 100)),
            visible=bool(fm.get("visible", True)),
            kind=str(fm.get("kind", "note")),
            tags=tags,
            summary=str(fm.get("summary", "")),
            body_markdown=body_md,
            source_path=str(path.relative_to(self._site_root)),
            sha256=sha,
            target_href=str(fm.get("target_href", "")),
            external_url=str(fm.get("external_url", "")),
            figures=self._parse_figures(fm),
            lang=str(fm.get("lang", "en")),
            keywords=keywords,
            evidence_status=str(fm.get("evidence_status", "verified-note")),
            revised_at=str(fm.get("revised_at", pub_date)),
            series=str(fm.get("series", "")),
            prerequisites=str(fm.get("prerequisites", "")),
            conventions=str(fm.get("conventions", "")),
            source_links=src_links,
        )
