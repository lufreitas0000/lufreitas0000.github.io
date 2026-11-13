"""Unified Feed Renderer: builds multi-option left filter, right search box, and search-index.json."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Iterable

from ..domain.models import FeedNode
from .math_markdown import format_inline_tex_and_amp

KIND_LABELS: dict[str, tuple[str, str, str]] = {
    "note": ("Research Note", "pink", "Research Notes"),
    "expository-note": ("Expository Note", "blue", "Expository Notes"),
    "thesis-chapter": ("Expository Note", "blue", "Expository Notes"),
    "reading": ("Reading & Reflection", "blue", "Readings & Reflections"),
    "series": ("Reading & Reflection", "blue", "Readings & Reflections"),
    "project": ("Open-Source (@github)", "blue", "Open-Source (@github)"),
    "video": ("Video Script (@lu.scientist)", "pink", "Video Scripts (@lu.scientist)"),
}


def render_feed_search_index(feed_nodes: Iterable[FeedNode]) -> str:
    """Emits a compact JSON index (metadata + keywords + tags + summary) without full body bloat."""
    items = []
    for n in feed_nodes:
        href = n.target_href or f"feed/{n.node_id}.html"
        items.append(
            {
                "id": n.node_id,
                "title": n.title,
                "subtitle": n.subtitle,
                "date": n.date,
                "kind": n.kind,
                "tags": list(n.tags),
                "keywords": list(n.keywords),
                "summary": n.summary,
                "href": href,
            }
        )
    return json.dumps(items, ensure_ascii=False, indent=2)


def render_feed_controls_and_cards(
    feed_nodes: Iterable[FeedNode],
    template_path: Path,
    root_rel_prefix: str = "../",
) -> str:
    nodes = tuple(feed_nodes)
    present_kinds: list[str] = []
    for n in nodes:
        if n.kind not in present_kinds:
            present_kinds.append(n.kind)

    filter_btns = [
        '<button type="button" class="feed-filter-btn active" data-filter="all" onclick="setFeedCategory(\'all\')">All posts</button>'
    ]
    for k in present_kinds:
        _, _, plural_label = KIND_LABELS.get(k, (k.title(), "blue", k.title() + "s"))
        filter_btns.append(
            f'<button type="button" class="feed-filter-btn" data-filter="{html.escape(k)}" onclick="setFeedCategory(\'{html.escape(k)}\')">{html.escape(plural_label)}</button>'
        )

    cards: list[str] = []
    for n in nodes:
        k_label, k_tone, _ = KIND_LABELS.get(n.kind, (n.kind.title(), "blue", n.kind.title() + "s"))
        href = n.target_href or f"feed/{n.node_id}.html"
        tag_btns = " ".join(
            f'<button type="button" class="feed-tag-btn" data-tag="{html.escape(t)}" onclick="toggleFeedTag(\'{html.escape(t)}\')" title="Filter posts by #{html.escape(t)}">#{html.escape(t)}</button>'
            for t in n.tags
        )
        raw_corpus = f"{n.title} {n.subtitle} {n.summary} {' '.join(n.tags)} {' '.join(n.keywords)} {n.kind}"
        search_corpus = re.sub(r"\s+", " ", raw_corpus).strip().lower()
        tags_csv = ",".join(t.lower() for t in n.tags)

        cards.append(
            f"""<article class="feed-card" data-kind="{html.escape(n.kind)}" data-tags="{html.escape(tags_csv)}" data-search="{html.escape(search_corpus)}">
  <div class="feed-card-header">
    <h3 class="feed-card-title"><a href="{html.escape(href)}">{format_inline_tex_and_amp(n.title)}</a></h3>
  </div>
  <div class="feed-card-meta">
    <span class="margin-pill {k_tone}" style="margin-bottom:0;">{html.escape(k_label)}</span>
    <span>{html.escape(n.date)}</span>
    <span class="feed-tag-list">{tag_btns}</span>
  </div>
  <p style="margin-bottom:0.4rem;">{format_inline_tex_and_amp(n.summary)}</p>
  <div><a href="{html.escape(href)}" style="font-size:0.9rem;font-weight:700;text-decoration:none;">Read post →</a></div>
</article>"""
        )

    tmpl = template_path.read_text(encoding="utf-8")
    return (
        tmpl.replace("{{FILTER_BUTTONS}}", "\n      ".join(filter_btns))
        .replace("{{TOTAL_COUNT}}", str(len(nodes)))
        .replace("{{SEARCH_INDEX_URL}}", "search-index.json")
        .replace("{{FEED_CARDS}}", "\n".join(cards))
        .replace("{{FEED_JS_URL}}", f"{root_rel_prefix}assets/js/feed_filter.js")
    )
