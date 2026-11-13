"""Design-by-Contract pure validators for domain models and privacy hygiene."""

from __future__ import annotations

import re
from typing import Iterable

from .models import ContentSection, FeedNode, PageSpec, PublicationRecord


class ContractViolationError(ValueError):
    """Raised when a domain invariant, epistemic rule, or privacy contract is violated."""


FORBIDDEN_PRIVATE_TOKENS: tuple[str, ...] = (
    "physics.freitas@gmail.com",
    "lucas.rodrigues@fisica.ufrn.br",
    "lucas.freitas@fisica.ufrn.br",
    "lu.rdf@fisica.ufrn.br",
    "CPF",
    "RG:",
    "IMPA_ENROLMENT_HISTORY_PRIVATE",
    "MASTER_PROFILE_PRIVATE",
)

ALLOWED_FEED_KINDS: frozenset[str] = frozenset(
    {"note", "expository-note", "thesis-chapter", "reading", "series", "project", "video"}
)

ALLOWED_EVIDENCE_STATUSES: frozenset[str] = frozenset(
    {"verified-note", "exploratory-draft", "expository-synthesis", "obstructed-or-refuted"}
)


def require_privacy_hygiene(text: str, context: str = "") -> None:
    """Verifies that retired emails and private identifiers never appear in public content."""
    lower = text.lower()
    for token in FORBIDDEN_PRIVATE_TOKENS:
        if token.lower() in lower:
            raise ContractViolationError(f"Privacy contract violation ({token!r}) detected in {context}.")


def require_valid_section(
    section: ContentSection,
    known_publications: dict[str, PublicationRecord] | None = None,
) -> ContentSection:
    """Validates structural and epistemic contracts on a single ContentSection."""
    if not section.section_id or not re.match(r"^[a-z0-9][a-z0-9_-]*$", section.section_id):
        raise ContractViolationError(
            f"Invalid section_id {section.section_id!r} in {section.source_path}: must be lowercase alphanumeric/hyphen."
        )
    if not isinstance(section.order, int):
        raise ContractViolationError(f"Section {section.section_id!r} order must be an integer.")
    if not isinstance(section.visible, bool):
        raise ContractViolationError(f"Section {section.section_id!r} visible flag must be a boolean.")
    if section.visible and not (
        section.body_markdown.strip()
        or section.directory_rows
        or section.include_theses_list
        or section.include_education_table
    ):
        raise ContractViolationError(f"Visible section {section.section_id!r} cannot have empty content.")
    if section.publication_id and known_publications is not None:
        if section.publication_id not in known_publications:
            raise ContractViolationError(
                f"Section {section.section_id!r} references unknown publication_id {section.publication_id!r}."
            )
    for fig in section.figures:
        if not fig.src or not fig.alt:
            raise ContractViolationError(
                f"Section {section.section_id!r} has a figure missing required src or alt text."
            )
    require_privacy_hygiene(section.body_markdown, context=section.source_path)
    return section


def require_valid_feed_node(node: FeedNode) -> FeedNode:
    """Validates structural, metadata, and privacy contracts on a Unified Feed node."""
    if not node.node_id or not re.match(r"^[a-z0-9][a-z0-9_-]*$", node.node_id):
        raise ContractViolationError(
            f"Invalid feed node_id {node.node_id!r} in {node.source_path}: must be lowercase alphanumeric/hyphen."
        )
    if not re.match(r"^\d{4}-\d{2}(-\d{2})?$", node.date):
        raise ContractViolationError(
            f"Invalid feed date {node.date!r} in {node.source_path}: expected YYYY-MM or YYYY-MM-DD."
        )
    if node.kind not in ALLOWED_FEED_KINDS:
        raise ContractViolationError(
            f"Invalid feed kind {node.kind!r} in {node.source_path}: expected one of {sorted(ALLOWED_FEED_KINDS)}."
        )
    if node.evidence_status not in ALLOWED_EVIDENCE_STATUSES:
        raise ContractViolationError(
            f"Invalid evidence_status {node.evidence_status!r} in {node.source_path}."
        )
    if node.visible and (not node.title.strip() or not node.summary.strip()):
        raise ContractViolationError(f"Visible feed node {node.node_id!r} requires non-empty title and summary.")
    for fig in node.figures:
        if not fig.src or not fig.alt:
            raise ContractViolationError(
                f"Feed node {node.node_id!r} has a figure missing required src or alt text."
            )
    combined = " ".join(
        [node.title, node.subtitle, node.summary, node.body_markdown, " ".join(node.tags), " ".join(node.keywords)]
    )
    require_privacy_hygiene(combined, context=node.source_path)
    return node


def require_unique_feed_ids(nodes: Iterable[FeedNode]) -> tuple[FeedNode, ...]:
    """Ensures all FeedNode entries have unique node_id values."""
    items = tuple(nodes)
    seen: set[str] = set()
    for n in items:
        if n.node_id in seen:
            raise ContractViolationError(f"Duplicate feed node_id {n.node_id!r}.")
        seen.add(n.node_id)
    return items


def require_unique_ids_and_orders(sections: Iterable[ContentSection], page_id: str) -> tuple[ContentSection, ...]:
    """Ensures no two sections in the same page share a section_id or order key."""
    sec_tuple = tuple(sections)
    seen_ids: set[str] = set()
    seen_orders: set[int] = set()
    for s in sec_tuple:
        if s.section_id in seen_ids:
            raise ContractViolationError(f"Duplicate section_id {s.section_id!r} in page {page_id!r}.")
        if s.order in seen_orders:
            raise ContractViolationError(f"Duplicate section order {s.order} in page {page_id!r} ({s.section_id!r}).")
        seen_ids.add(s.section_id)
        seen_orders.add(s.order)
    return sec_tuple


def require_valid_page(page: PageSpec) -> PageSpec:
    """Validates page-level contracts."""
    if not page.page_id or not page.output_rel_path:
        raise ContractViolationError("PageSpec must define non-empty page_id and output_rel_path.")
    require_unique_ids_and_orders(page.sections, page.page_id)
    return page
