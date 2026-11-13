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
    "note": ("Research note", "pink", "Research Notes"),
    "expository-note": ("Expository note", "blue", "Expository Notes"),
    "thesis-chapter": ("Expository note", "blue", "Expository Notes"),
    "reading": ("Reading", "blue", "Readings"),
    "series": ("Reading", "blue", "Readings"),
    "project": ("Project", "blue", "Projects"),
    "video": ("Video", "pink", "Videos"),
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

    if not nodes:
        return '<p class="feed-empty-notice">No notes published yet.</p>'

    cards: list[str] = []
    for n in nodes:
        kind_label, _, _ = KIND_LABELS.get(n.kind, (n.kind.title(), "blue", n.kind.title() + "s"))
        href = n.target_href or f"feed/{n.node_id}.html"
        raw_corpus = f"{n.title} {n.subtitle} {n.summary} {' '.join(n.tags)} {' '.join(n.keywords)} {n.kind}"
        search_corpus = re.sub(r"\s+", " ", raw_corpus).strip().lower()
        cards.append(
            f"""<article class="feed-card" data-kind="{html.escape(n.kind)}" data-search="{html.escape(search_corpus)}">
  <h3 class="feed-card-title"><a href="{html.escape(href)}">{format_inline_tex_and_amp(html.escape(n.title))}</a></h3>
  <div class="feed-card-meta">{html.escape(kind_label)} · {html.escape(n.date)}</div>
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
