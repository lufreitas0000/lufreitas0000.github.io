"""HTML & Quarto (.qmd) Renderer Adapter implementing RendererPort via external templates."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any, Iterable

from ..domain.models import (
    ContentSection,
    FeedNode,
    NotePost,
    PageSpec,
    PublicationRecord,
    SiteGraph,
)
from ..services.dag import compute_breadcrumb_trail, get_visible_sitemap_branches
from .feed_renderer import render_feed_controls_and_cards, render_feed_search_index
from .math_markdown import (
    convert_markdown_preserving_math,
    format_escaped_tex,
    format_inline_tex_and_amp,
)
from .notebook_parser import render_ipynb_static_html
from .seo_and_feeds import (
    render_json_ld_person,
    render_robots_txt,
    render_rss_xml,
    render_sitemap_xml,
)


class StaticSiteRenderer:
    """Implements RendererPort using `site/templates/base.html` and `feed_controls.html`."""

    def __init__(self, templates_dir: Path) -> None:
        self._templates_dir = templates_dir

    def render_markdown_fragment(self, md_text: str) -> str:
        return convert_markdown_preserving_math(md_text)

    def render_feed_search_index_json(self, feed_nodes: Iterable[FeedNode]) -> str:
        return render_feed_search_index(feed_nodes)

    def render_unified_feed_index_html(
        self,
        feed_nodes: Iterable[FeedNode],
        root_rel_prefix: str = "../",
    ) -> str:
        return render_feed_controls_and_cards(
            feed_nodes=feed_nodes,
            template_path=self._templates_dir / "feed_controls.html",
            root_rel_prefix=root_rel_prefix,
        )

    def render_rss_xml(self, notes: Iterable[NotePost], base_url: str) -> str:
        return render_rss_xml(notes, base_url)

    def render_sitemap_xml(self, site_graph: SiteGraph, base_url: str) -> str:
        return render_sitemap_xml(site_graph, base_url)

    def render_robots_txt(self, base_url: str) -> str:
        return render_robots_txt(base_url)

    def render_working_with_me_markdown(self, profile: dict[str, Any]) -> str:
        stack_bullets = "\n".join(f"- {s}" for s in profile["collaboration_preferences"]["computational_stack"])
        return f"""# Working With Me — Public Collaboration & Agent Context ({profile['display_name']})

> **Boundary Notice for AI Assistants & Automated Tools:**
> {profile['collaboration_preferences']['agent_boundary_disclaimer']}

## Identity & Current Status

- **Name:** {profile['display_name']}
- **Earlier Publication Names:** {", ".join(profile['Earlier_publication_names'])}
- **Name Continuity:** {profile['name_continuity_note']}
- **Credential Summary:** {profile['credential_line']}
- **Current Affiliation Status:** {profile['current_affiliation_status']}
- **Public Contact:** `{profile['public_email']}` ({profile['retired_email_policy']})
- **ORCID:** {profile['identifiers']['orcid']['url']}
- **GitHub:** {profile['identifiers']['github']['url']}

## Research Footing & Collaboration Focus

- **Current Independent Footing:** {profile['research_footing']['current_independent_strength']}
- **Desired Collaboration Focus:** {profile['research_footing']['collaboration_goal']}

## Collaboration & Verification Preferences

- **Communication Style:** {profile['collaboration_preferences']['communication_style']}
- **Epistemic Hygiene:** {profile['collaboration_preferences']['epistemic_hygiene']}
- **Computational & Formal Stack:**
{stack_bullets}
"""

    def render_feed_metadata_box(self, node: FeedNode) -> str:
        return self._render_epistemic_box(
            lang=node.lang,
            article_type=node.kind,
            evidence_status=node.evidence_status,
            pub_date=node.date,
            rev_date=node.revised_at or node.date,
            series=node.series,
            prerequisites=node.prerequisites,
            conventions=node.conventions,
            source_links=node.source_links,
        )

    def render_note_post_lead_html(self, post: NotePost) -> str:
        meta_box = self._render_epistemic_box(
            lang=post.lang,
            article_type=post.article_type,
            evidence_status=post.evidence_status,
            pub_date=post.date,
            rev_date=post.revised_at,
            series=post.series,
            prerequisites=post.prerequisites,
            conventions=post.conventions,
            source_links=post.source_links,
        )
        body_html = convert_markdown_preserving_math(post.body_markdown)
        if post.notebook_path and post.notebook_path.exists():
            body_html += "\n" + render_ipynb_static_html(post.notebook_path, f"../notebooks/{post.notebook_path.name}")
        return meta_box + "\n" + body_html

    def build_partials(
        self,
        profile: dict[str, Any],
        pubs_raw: dict[str, Any],
        published_notes: tuple[NotePost, ...],
    ) -> dict[str, str]:
        theses_items = []
        for ed in profile["education"]:
            if not ed.get("is_ufrn_thesis", True):
                continue
            t_title = format_escaped_tex(str(ed.get("thesis_title", "")))
            sup = html.escape(str(ed.get("supervisor", "")))
            repo_url = html.escape(str(ed.get("repository_item_url", "")))
            theses_items.append(
                f'<li><strong>{html.escape(ed["degree"])}</strong> ({html.escape(ed["institution"])}, {html.escape(ed["period_orcid"])}): '
                f'<em>{t_title}</em> · {sup} · <a href="{repo_url}">UFRN Repository Record</a>.</li>'
            )

        ext_items = [
            f'<li><a href="{html.escape(ex["url"])}">{html.escape(ex["citation"])}</a> — {html.escape(ex["role_in_narrative"])}</li>'
            for ex in pubs_raw["influential_external_works"]
        ]

        edu_rows = []
        for ed in profile["education"]:
            t_title = format_escaped_tex(str(ed.get("thesis_title", "")))
            sup = html.escape(str(ed.get("supervisor", "")))
            repo_url = str(ed.get("repository_item_url", ""))
            repo_link = f' · <a href="{html.escape(repo_url)}">UFRN Repository</a>' if repo_url else ""
            edu_rows.append(
                f'<tr><td><strong>{html.escape(ed["degree"])}</strong></td><td>{html.escape(ed["institution"])}</td>'
                f'<td>{html.escape(ed["period_orcid"])}</td><td><em>{t_title}</em><br>'
                f'<span style="color:var(--ink-secondary);font-size:0.86rem;">{sup}{repo_link}</span></td></tr>'
            )

        edu_table = f"""<div class="table-wrapper">
  <table>
    <thead>
      <tr>
        <th>Degree / Appointment</th>
        <th>Institution</th>
        <th>Period</th>
        <th>Thesis / Research Focus &amp; Supervisor</th>
      </tr>
    </thead>
    <tbody>
      {"".join(edu_rows)}
    </tbody>
  </table>
</div>"""

        if published_notes:
            cards = []
            for post in published_notes:
                lang_label = "PT-BR" if post.lang.lower().startswith("pt") else "EN"
                s_badge = f'<span class="margin-pill blue">Series: {html.escape(post.series)}</span>' if post.series else ""
                cards.append(
                    f"""<article class="entry-item">
  <div class="entry-header">
    <h3 class="entry-title"><a href="posts/{html.escape(post.slug)}.html">{html.escape(post.title)}</a></h3>
    <div class="badge-row">
      <span class="margin-pill blue">{html.escape(lang_label)}</span>
      <span class="margin-pill blue">{html.escape(post.article_type)}</span>
      <span class="margin-pill pink">{html.escape(post.evidence_status)}</span>
      {s_badge}
    </div>
  </div>
  <p style="margin-bottom:0;">{html.escape(post.subtitle)}</p>
</article>"""
                )
            notes_archive_html = '<div class="entry-list">\n' + "\n".join(cards) + "\n</div>"
        else:
            notes_archive_html = """<div class="scope-panel">
  <div class="scope-panel-title">Archive Status — Launch Baseline (0 Published Notes Yet)</div>
  <p style="margin-bottom:0;">No finished standalone articles have been published yet. Entries will appear here and in the <a href="index.xml">RSS Feed</a> as worked derivations, precomputed notebook studies, and readings in the <a href="series/papers-worth-understanding.html"><em>Papers worth understanding</em></a> series are finalized.</p>
</div>"""

        return {
            "{{THESES_HTML}}": "<ul>\n" + "\n".join(theses_items) + "\n</ul>",
            "{{EXTERNAL_REFERENCES_HTML}}": "<ul>\n" + "\n".join(ext_items) + "\n</ul>",
            "{{EDUCATION_TABLE_HTML}}": edu_table,
            "{{NOTES_ARCHIVE_LIST_HTML}}": notes_archive_html,
        }

    def render_page_qmd(self, page: PageSpec, partials: dict[str, str]) -> str:
        blocks: list[str] = []
        if page.colophon_html:
            blocks.append(page.colophon_html)
        if page.lead_html:
            blocks.append(page.lead_html)
        for sec in page.sections:
            blocks.append(self.render_section_html(sec, partials))
        body = "\n\n".join(blocks)
        return f"""---
title: "{page.title}"
subtitle: "{page.subtitle}"
page_id: "{page.page_id}"
lang: "{page.lang}"
hide_page_title: {str(page.hide_page_title).lower()}
toc: false
---

{body}
"""

    def render_page_html(
        self,
        page: PageSpec,
        profile: dict[str, Any],
        partials: dict[str, str],
        css_rel_path: str,
        root_rel_prefix: str,
        site_graph: SiteGraph | None = None,
    ) -> str:
        nav_notes_label = str(profile.get("nav_notes_label", "Feed"))
        nav_items = [
            ("home", "Home", f"{root_rel_prefix}index.html"),
            ("research", "Research", f"{root_rel_prefix}research.html"),
            ("about", "About Me", f"{root_rel_prefix}about.html"),
            ("notes", nav_notes_label, f"{root_rel_prefix}notes/index.html"),
        ]
        nav_lis = []
        for pid, label, href in nav_items:
            aria = ' aria-current="page"' if pid == page.page_id else ""
            nav_lis.append(f'<li><a href="{href}"{aria}>{label}</a></li>')

        breadcrumb_html = self._render_breadcrumbs_html(site_graph, page.node_id, root_rel_prefix) if site_graph else ""
        sitemap_html = self._render_sitemap_html(site_graph, root_rel_prefix) if site_graph else ""

        header_block = ""
        if not page.hide_page_title:
            sub_html = f'<p class="credential-line">{html.escape(page.subtitle)}</p>' if page.subtitle else ""
            header_block = f"""      <header class="article-header">
        <h1>{html.escape(page.title)}</h1>
        {sub_html}
      </header>"""

        blocks: list[str] = []
        if breadcrumb_html:
            blocks.append(breadcrumb_html)
        if page.colophon_html:
            blocks.append(page.colophon_html)
        if page.lead_html:
            blocks.append(page.lead_html)
        for sec in page.sections:
            blocks.append(self.render_section_html(sec, partials))

        brand_subtitle = profile.get("credential_line", "Theoretical quantum-matter physicist · PhD in Physics, UFRN, 2024")
        if page.hide_page_title:
            brand_el = f'<h1 style="margin:0;font-size:inherit;line-height:inherit;transform:none;"><a class="site-brand" href="{root_rel_prefix}index.html">Lu Freitas</a></h1>'
        else:
            brand_el = f'<a class="site-brand" href="{root_rel_prefix}index.html">Lu Freitas</a>'

        base_url = str(profile.get("canonical_base_url", "https://lufreitas0000.github.io")).rstrip("/")
        canonical_href = f"{base_url}/" if page.output_rel_path == "index.html" else f"{base_url}/{page.output_rel_path}"
        meta_desc = html.escape(page.subtitle or brand_subtitle)
        json_ld = render_json_ld_person(profile, base_url) if page.page_id in ("home", "about") else ""

        tmpl = (self._templates_dir / "base.html").read_text(encoding="utf-8")
        return (
            tmpl.replace("{{LANG}}", html.escape(page.lang))
            .replace("{{PAGE_TITLE}}", html.escape(page.title))
            .replace("{{META_DESCRIPTION}}", meta_desc)
            .replace("{{CANONICAL_HREF}}", html.escape(canonical_href))
            .replace("{{CSS_REL_PATH}}", css_rel_path)
            .replace("{{RSS_HREF}}", f"{root_rel_prefix}notes/index.xml")
            .replace("{{JSON_LD}}", json_ld)
            .replace("{{BRAND_EL}}", brand_el)
            .replace("{{BRAND_SUBTITLE}}", html.escape(brand_subtitle))
            .replace("{{NAV_ITEMS}}", " ".join(nav_lis))
            .replace("{{HEADER_BLOCK}}", header_block)
            .replace("{{BODY_HTML}}", "\n\n".join(blocks))
            .replace("{{PUBLIC_EMAIL}}", profile["public_email"])
            .replace("{{ORCID_URL}}", profile["identifiers"]["orcid"]["url"])
            .replace("{{GITHUB_URL}}", profile["identifiers"]["github"]["url"])
            .replace("{{SCHOLAR_URL}}", profile["identifiers"]["google_scholar"]["url"])
            .replace("{{SITEMAP_HTML}}", sitemap_html)
        )

    def render_section_html(self, section: ContentSection, partials: dict[str, str]) -> str:
        main_parts: list[str] = []
        if section.title:
            main_parts.append(f"    <h2>{format_inline_tex_and_amp(section.title)}</h2>")

        citation_html = self._format_citation_html(section.publication) if section.publication else (
            html.escape(section.citation_line_text) if section.citation_line_text else ""
        )
        if citation_html:
            main_parts.append(f'    <div class="paper-citation-line">{citation_html}</div>')

        if section.body_markdown:
            main_parts.append(f"    {convert_markdown_preserving_math(section.body_markdown)}")

        if section.directory_rows:
            rows_html = [
                f"""      <div class="readme-dir-row">
        <div><a href="{html.escape(r.href)}">{r.label}</a></div>
        {f'<div>{format_inline_tex_and_amp(r.description_text)}</div>' if r.description_text else ''}
      </div>"""
                for r in section.directory_rows
            ]
            main_parts.append(
                '    <div class="readme-directory" role="navigation" aria-label="Site directory">\n'
                + "\n".join(rows_html)
                + "\n    </div>"
            )

        if section.include_theses_list:
            main_parts.append("    " + partials.get("{{THESES_HTML}}", ""))
        if section.include_education_table:
            main_parts.append("    " + partials.get("{{EDUCATION_TABLE_HTML}}", ""))
        if section.include_external_references:
            main_parts.append(
                "    <h3>External Works Referenced in Narrative</h3>\n"
                "    <p>Foundational and external papers mentioned in my intellectual background above are listed separately from my authored publications:</p>\n"
                "    " + partials.get("{{EXTERNAL_REFERENCES_HTML}}", "")
            )
        if section.include_notes_archive:
            main_parts.append("    " + partials.get("{{NOTES_ARCHIVE_LIST_HTML}}", ""))

        margin_parts: list[str] = []
        for fig in section.figures:
            fig_cls = "labeled-svg" if fig.kind == "labeled-svg" else "vibe-art"
            cap_html = f'\n      <div class="margin-figcaption">{format_inline_tex_and_amp(fig.caption)}</div>' if fig.caption else ""
            style_attr = f' style="max-width:{html.escape(fig.max_width)};"' if fig.max_width != "100%" else ""
            margin_parts.append(
                f"""    <div class="margin-figure {fig_cls}">
      <img src="{html.escape(fig.src)}" alt="{html.escape(fig.alt)}" loading="lazy" decoding="async"{style_attr}>{cap_html}
    </div>"""
            )
        for note in section.margin_notes:
            id_attr = f' id="{html.escape(note.element_id)}"' if note.element_id else ""
            item_cls = "margin-note-item quiet-note" if note.pill_tone == "quiet" else "margin-note-item"
            margin_parts.append(
                f"""    <div class="{item_cls}"{id_attr}>
      <span class="margin-pill {html.escape(note.pill_tone)}">{note.pill_text}</span>
      <div>{format_inline_tex_and_amp(note.body_text)}</div>
    </div>"""
            )

        return f"""<div class="tufte-section page-section" id="{html.escape(section.section_id)}">
  <div class="tufte-main page-main">
{chr(10).join(main_parts)}
  </div>
  <aside class="tufte-margin page-margin">
{chr(10).join(margin_parts)}
  </aside>
</div>"""

    def _format_citation_html(self, pub: PublicationRecord) -> str:
        authors_str = html.escape(pub.authors)
        venue_label = f"{html.escape(pub.journal)} {html.escape(pub.volume_pages)} ({pub.year}) · DOI: {html.escape(pub.doi)}"
        parts = [authors_str, f'<a href="{html.escape(pub.doi_url)}">{venue_label}</a>']
        if pub.arxiv_id and pub.arxiv_url:
            parts.append(f'<a href="{html.escape(pub.arxiv_url)}">arXiv:{html.escape(pub.arxiv_id)}</a>')
        return " · ".join(parts)

    def _render_epistemic_box(
        self,
        lang: str,
        article_type: str,
        evidence_status: str,
        pub_date: str,
        rev_date: str,
        series: str,
        prerequisites: str,
        conventions: str,
        source_links: tuple[tuple[str, str], ...],
    ) -> str:
        lang_label = "PT-BR" if lang.lower().startswith("pt") else "EN"
        series_badge = f'<span class="margin-pill blue">Series: {html.escape(series)}</span>' if series else ""
        details = []
        if prerequisites:
            details.append(f"<div><strong>Prerequisites:</strong> {html.escape(prerequisites)}</div>")
        if conventions:
            details.append(f"<div><strong>Conventions:</strong> {html.escape(conventions)}</div>")
        if source_links:
            links_html = ", ".join(f'<a href="{html.escape(url)}">{html.escape(lbl)}</a>' for lbl, url in source_links)
            details.append(f"<div><strong>Primary Sources:</strong> {links_html}</div>")
        return f"""<div class="note-metadata-box" role="region" aria-label="Article epistemic metadata">
  <div style="margin-bottom:0.4rem;">
    <span class="margin-pill blue">Language: {lang_label}</span>
    <span class="margin-pill blue">Type: {html.escape(article_type)}</span>
    <span class="margin-pill pink">Status: {html.escape(evidence_status)}</span>
    {series_badge}
    <span class="margin-pill quiet" style="display:inline-block;margin-right:0.5rem;">Published: {html.escape(pub_date)} · Revised: {html.escape(rev_date)}</span>
  </div>
  {"".join(details)}
</div>"""

    def _render_breadcrumbs_html(self, graph: SiteGraph, node_id: str, root_rel_prefix: str) -> str:
        trail = compute_breadcrumb_trail(graph, node_id)
        if len(trail) <= 2 and node_id in ("home", "research", "about", "notes"):
            return ""
        items: list[str] = []
        for idx, node in enumerate(trail):
            if idx == len(trail) - 1:
                items.append(f'<li aria-current="page"><strong>{format_escaped_tex(node.title)}</strong></li>')
            else:
                href = f"{root_rel_prefix}{node.rel_href}"
                items.append(f'<li><a href="{html.escape(href)}">{format_escaped_tex(node.title)}</a></li>')
                items.append('<li class="breadcrumb-sep" aria-hidden="true">/</li>')
        return (
            '<nav class="breadcrumb-nav" aria-label="Breadcrumb">\n'
            '  <ol class="breadcrumb-list">\n    '
            + "\n    ".join(items)
            + "\n  </ol>\n</nav>"
        )

    def _render_sitemap_html(self, graph: SiteGraph, root_rel_prefix: str) -> str:
        branches_html: list[str] = []
        for br in get_visible_sitemap_branches(graph):
            p_href = f"{root_rel_prefix}{br.root.rel_href}"
            child_lis = []
            for ch in br.children:
                ch_href = f"{root_rel_prefix}{ch.rel_href}"
                tag_str = f' <span style="color:var(--ink-quiet);font-size:0.78rem;">[{html.escape(ch.kind)}]</span>' if ch.kind not in ("page", "subpage") else ""
                child_lis.append(f'<li><a href="{html.escape(ch_href)}">{format_escaped_tex(ch.title)}</a>{tag_str}</li>')
            children_ul = (
                f'<ul class="sitemap-children">{"".join(child_lis)}</ul>'
                if child_lis
                else '<div style="color:var(--ink-quiet);font-size:0.8rem;padding-left:0.5rem;">Primary page</div>'
            )
            branches_html.append(
                f"""<div class="sitemap-branch">
  <div class="sitemap-branch-title"><a href="{html.escape(p_href)}">{html.escape(br.root.title)}</a></div>
  {children_ul}
</div>"""
            )
        return f"""<details class="sitemap-details">
  <summary>Site Map &amp; Navigation Tree</summary>
  <nav class="sitemap-tree" aria-label="Site Map Tree">
    {"".join(branches_html)}
  </nav>
</details>"""
