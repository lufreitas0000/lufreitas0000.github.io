from __future__ import annotations

import unittest

from web_engine.domain.contracts import (
    ContractViolationError,
    require_privacy_hygiene,
    require_unique_feed_ids,
    require_valid_feed_node,
    require_valid_section,
)
from web_engine.domain.models import ContentSection, FeedNode, PublicationRecord


def _sample_feed_node(**overrides: object) -> FeedNode:
    base = dict(
        node_id="sample-note",
        title="Sample Note",
        subtitle="Subtitle",
        date="2026-11",
        order=10,
        visible=True,
        kind="note",
        tags=("kitaev-model",),
        summary="A concise summary.",
        body_markdown="Body text.",
        source_path="content/feed/01.md",
        sha256="abc",
    )
    base.update(overrides)
    return FeedNode(**base)  # type: ignore[arg-type]


class TestDomainAndContracts(unittest.TestCase):
    def test_valid_feed_node_passes(self) -> None:
        node = _sample_feed_node(keywords=("majorana", "vortex"))
        self.assertEqual(require_valid_feed_node(node).node_id, "sample-note")

    def test_invalid_feed_node_id_rejected(self) -> None:
        with self.assertRaises(ContractViolationError):
            require_valid_feed_node(_sample_feed_node(node_id="Bad Id!"))

    def test_invalid_feed_date_rejected(self) -> None:
        with self.assertRaises(ContractViolationError):
            require_valid_feed_node(_sample_feed_node(date="Nov 2026"))

    def test_invalid_feed_kind_rejected(self) -> None:
        with self.assertRaises(ContractViolationError):
            require_valid_feed_node(_sample_feed_node(kind="blog-spam"))

    def test_duplicate_feed_ids_rejected(self) -> None:
        n1 = _sample_feed_node(node_id="dup")
        n2 = _sample_feed_node(node_id="dup", order=20)
        with self.assertRaises(ContractViolationError):
            require_unique_feed_ids((n1, n2))

    def test_privacy_hygiene_blocks_private_emails_and_tokens(self) -> None:
        for bad in ("physics.freitas@gmail.com", "lucas.rodrigues@fisica.ufrn.br", "IMPA_ENROLMENT_HISTORY_PRIVATE"):
            with self.assertRaises(ContractViolationError):
                require_privacy_hygiene(f"contact: {bad}", context="unit-test")

    def test_section_unknown_publication_rejected(self) -> None:
        sec = ContentSection(
            section_id="sec-1",
            title="Title",
            order=10,
            visible=True,
            body_markdown="Body",
            source_path="content/research/01.md",
            sha256="abc",
            publication_id="missing_pub",
        )
        known = {
            "p1": PublicationRecord("p1", "T", "A", "PRB", "1", 2024, "10.1", "https://doi.org/10.1")
        }
        with self.assertRaises(ContractViolationError):
            require_valid_section(sec, known_publications=known)


if __name__ == "__main__":
    unittest.main()
