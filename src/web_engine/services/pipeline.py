"""Pure functional composition pipeline for assembling pages and Unified Feed nodes."""

from __future__ import annotations

import re
from typing import Iterable

from ..domain.contracts import (
    require_unique_feed_ids,
    require_unique_ids_and_orders,
    require_valid_feed_node,
    require_valid_page,
    require_valid_section,
)
from ..domain.models import ContentSection, FeedNode, PageSpec, PublicationRecord


def filter_visible_sections(sections: Iterable[ContentSection]) -> tuple[ContentSection, ...]:
    """Pure filter returning only sections with `visible=True`."""
    return tuple(s for s in sections if s.visible)


def count_hidden_sections(sections: Iterable[ContentSection]) -> int:
    """Pure count of sections toggled off via `visible=False`."""
    return sum(1 for s in sections if not s.visible)


def sort_sections(sections: Iterable[ContentSection]) -> tuple[ContentSection, ...]:
    """Pure deterministic sort by `(order, section_id)`."""
    return tuple(sorted(sections, key=lambda s: (s.order, s.section_id)))


def filter_and_sort_feed_nodes(nodes: Iterable[FeedNode], include_hidden: bool = False) -> tuple[FeedNode, ...]:
    """Pure validation, filter, and deterministic sort for Unified Feed nodes."""
    validated = require_unique_feed_ids(require_valid_feed_node(n) for n in nodes)
    filtered = tuple(n for n in validated if (include_hidden or n.visible))
    return tuple(sorted(filtered, key=lambda n: (n.order, n.node_id)))


def bind_publication_metadata(
    section: ContentSection,
    publications: dict[str, PublicationRecord],
    display_index: int | None = None,
) -> ContentSection:
    """Pure transformation attaching structured PublicationRecord and numbered title."""
    require_valid_section(section, known_publications=publications)
    pub = publications[section.publication_id] if section.publication_id else section.publication

    new_title = section.title
    if display_index is not None and section.publication_id and not re.match(r"^\d+\.", section.title):
        new_title = f"{display_index}. {section.title}"

    return ContentSection(
        section_id=section.section_id,
        title=new_title,
        order=section.order,
        visible=section.visible,
        body_markdown=section.body_markdown,
        source_path=section.source_path,
        sha256=section.sha256,
        publication_id=section.publication_id,
        publication=pub,
        citation_line_text=section.citation_line_text,
        figures=section.figures,
        margin_notes=section.margin_notes,
        directory_rows=section.directory_rows,
        include_theses_list=section.include_theses_list,
        include_education_table=section.include_education_table,
        include_external_references=section.include_external_references,
        include_notes_archive=section.include_notes_archive,
    )


def compose_page(
    page_id: str,
    slug: str,
    output_rel_path: str,
    title: str,
    subtitle: str,
    raw_sections: Iterable[ContentSection],
    publications: dict[str, PublicationRecord],
    node_id: str | None = None,
    lang: str = "en",
    hide_page_title: bool = False,
    lead_html: str = "",
    colophon_html: str = "",
    number_publication_sections: bool = False,
) -> PageSpec:
    """Pure functional pipeline: validate -> deduplicate -> filter visible -> sort -> bind metadata."""
    validated_all = tuple(require_valid_section(s, known_publications=publications) for s in raw_sections)
    require_unique_ids_and_orders(validated_all, page_id=page_id)
    visible_sorted = sort_sections(filter_visible_sections(validated_all))

    enriched: list[ContentSection] = []
    pub_counter = 0
    for sec in visible_sorted:
        idx = None
        if number_publication_sections and sec.publication_id:
            pub_counter += 1
            idx = pub_counter
        enriched.append(bind_publication_metadata(sec, publications, display_index=idx))

    page = PageSpec(
        page_id=page_id,
        node_id=node_id or page_id,
        slug=slug,
        output_rel_path=output_rel_path,
        title=title,
        subtitle=subtitle,
        lang=lang,
        hide_page_title=hide_page_title,
        lead_html=lead_html,
        colophon_html=colophon_html,
        sections=tuple(enriched),
    )
    return require_valid_page(page)
