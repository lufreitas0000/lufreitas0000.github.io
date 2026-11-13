"""SEO, JSON-LD Person schema, RSS 2.0 XML, robots.txt, and sitemap.xml generators."""

from __future__ import annotations

import html
import json
import xml.etree.ElementTree as ET
from typing import Any, Iterable

from ..domain.models import NotePost, SiteGraph


def render_json_ld_person(profile: dict[str, Any], base_url: str) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": profile.get("display_name", "Lu Freitas"),
        "alternateName": profile.get(
            "Earlier_publication_names",
            ["Lucas R. D. Freitas", "L. R. D. Freitas", "Lucas Rodrigues Delgado de Freitas", "Lucas Freitas"],
        ),
        "jobTitle": "Theoretical Quantum-Matter Physicist",
        "url": f"{base_url.rstrip('/')}/",
        "alumniOf": [
            {
                "@type": "CollegeOrUniversity",
                "name": "Universidade Federal do Rio Grande do Norte (UFRN)",
                "sameAs": "https://www.ufrn.br",
            },
            {
                "@type": "CollegeOrUniversity",
                "name": "Heinrich-Heine-Universität Düsseldorf",
                "sameAs": "https://www.hhu.de",
            },
        ],
        "sameAs": [
            profile["identifiers"]["orcid"]["url"],
            profile["identifiers"]["github"]["url"],
            profile["identifiers"]["google_scholar"]["url"],
            "https://www.instagram.com/lu.scientist/",
            "https://www.instagram.com/luescaladora/",
        ],
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'


def render_rss_xml(notes: Iterable[NotePost], base_url: str) -> str:
    base = base_url.rstrip("/")
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Lu Freitas — Research Notes"
    ET.SubElement(channel, "link").text = f"{base}/notes/index.html"
    ET.SubElement(channel, "description").text = (
        "Unified feed of research notes, thesis chapters, reading series, projects, and science videos by Lu Freitas."
    )
    ET.SubElement(channel, "language").text = "en"
    ET.SubElement(channel, "lastBuildDate").text = "Wed, 11 Nov 2026 21:00:00 +0000"

    for post in notes:
        lang_label = "PT-BR" if post.lang.lower().startswith("pt") else "EN"
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = f"[{lang_label}] {post.title}"
        ET.SubElement(item, "link").text = f"{base}/notes/posts/{post.slug}.html"
        ET.SubElement(item, "guid", isPermaLink="true").text = f"{base}/notes/posts/{post.slug}.html"
        ET.SubElement(item, "description").text = f"({post.article_type} · {post.evidence_status}) {post.subtitle}"
        ET.SubElement(item, "pubDate").text = "Wed, 11 Nov 2026 21:00:00 +0000"

    return ET.tostring(rss, encoding="utf-8", xml_declaration=True).decode("utf-8")


def render_sitemap_xml(site_graph: SiteGraph, base_url: str) -> str:
    base_clean = base_url.rstrip("/")
    urls = []
    for s_node in site_graph.nodes.values():
        if not s_node.visible:
            continue
        loc = f"{base_clean}/" if s_node.rel_href == "index.html" else f"{base_clean}/{s_node.rel_href}"
        urls.append(f"  <url><loc>{html.escape(loc)}</loc></url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def render_robots_txt(base_url: str) -> str:
    return f"User-agent: *\nAllow: /\nSitemap: {base_url.rstrip('/')}/sitemap.xml\n"
