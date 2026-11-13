"""Application orchestration service accepting Ports via Dependency Injection."""

from __future__ import annotations

import hashlib
from pathlib import Path

from ..domain.models import (
    BuildConfig,
    BuildReceipt,
    ContentSection,
    FeedNode,
    NotePost,
    SiteGraph,
    SiteNode,
    StagedArtifact,
)
from ..ports.protocols import AtomicStorePort, ContentRepositoryPort, RendererPort
from .dag import build_and_verify_site_dag
from .pipeline import compose_page, count_hidden_sections, filter_and_sort_feed_nodes


def make_staged_artifact(rel_path: str, text_content: str) -> StagedArtifact:
    b = text_content.encode("utf-8")
    return StagedArtifact(rel_path=rel_path, content_bytes=b, sha256=hashlib.sha256(b).hexdigest())


def assemble_site_graph(
    all_feed_nodes: tuple[FeedNode, ...],
    note_posts: tuple[NotePost, ...],
    include_dev_fixtures: bool,
) -> SiteGraph:
    dag_nodes: list[SiteNode] = [
        SiteNode(node_id="home", title="Home", rel_href="index.html", parent_id=None, visible=True, kind="root"),
        SiteNode(node_id="research", title="Published Research", rel_href="research.html", parent_id="home", visible=True, kind="page"),
        SiteNode(node_id="about", title="About Me", rel_href="about.html", parent_id="home", visible=True, kind="page"),
        SiteNode(node_id="working-with-me", title="Working With Me", rel_href="about/working-with-me.html", parent_id="about", visible=True, kind="subpage"),
        SiteNode(node_id="notes", title="Feed", rel_href="notes/index.html", parent_id="home", visible=True, kind="page"),
        SiteNode(node_id="thesis-chapters", title="Expository Physics Notes", rel_href="notes/thesis-chapters.html", parent_id="notes", visible=True, kind="expository-note"),
        SiteNode(node_id="series", title="Series: Papers worth understanding", rel_href="notes/series/papers-worth-understanding.html", parent_id="notes", visible=True, kind="series"),
    ]
    for fn in all_feed_nodes:
        if fn.target_href:
            continue
        dag_nodes.append(
            SiteNode(
                node_id=f"feed-{fn.node_id}",
                title=fn.title,
                rel_href=f"notes/feed/{fn.node_id}.html",
                parent_id="notes",
                visible=(fn.visible or include_dev_fixtures),
                kind=fn.kind,
                tags=fn.tags,
            )
        )
    for post in note_posts:
        dag_nodes.append(
            SiteNode(
                node_id=f"post-{post.slug}",
                title=post.title,
                rel_href=f"notes/posts/{post.slug}.html",
                parent_id="notes",
                visible=True,
                kind=post.article_type,
            )
        )
    return build_and_verify_site_dag(dag_nodes)


def build_site(
    repo: ContentRepositoryPort,
    renderer: RendererPort,
    store: AtomicStorePort,
    config: BuildConfig,
) -> BuildReceipt:
    """Orchestrates full site composition and atomic commit strictly through abstract Ports."""
    profile = repo.load_profile()
    pubs_map = repo.load_publications()
    pubs_raw = repo.load_raw_publications_yaml()
    base_url = config.base_url_override or str(profile.get("canonical_base_url", "https://lufreitas0000.github.io"))

    all_feed_nodes = repo.load_feed_nodes()
    visible_feed_nodes = filter_and_sort_feed_nodes(all_feed_nodes, include_hidden=config.include_dev_fixtures)
    note_posts = repo.load_note_posts(include_dev_fixtures=config.include_dev_fixtures)

    partials = renderer.build_partials(profile, pubs_raw, note_posts)
    site_graph = assemble_site_graph(all_feed_nodes, note_posts, config.include_dev_fixtures)

    staged_artifacts: list[StagedArtifact] = []
    static_files_to_copy: list[tuple[Path, str]] = [
        (repo.site_root / "references.bib", "references.bib"),
    ]

    for fn in visible_feed_nodes:
        if fn.target_href:
            continue
        tags_str = " · ".join(f"#{t}" for t in fn.tags)
        meta_box = renderer.render_feed_metadata_box(fn)
        sec = ContentSection(
            section_id=fn.node_id,
            title=fn.subtitle or "Entry Notes & Commentary",
            order=10,
            visible=True,
            body_markdown=fn.body_markdown,
            source_path=fn.source_path,
            sha256=fn.sha256,
            citation_line_text=f"Category: {fn.kind.title()} · Tags: {tags_str}",
            figures=fn.figures,
        )
        feed_page = compose_page(
            page_id="notes",
            node_id=f"feed-{fn.node_id}",
            slug=fn.node_id,
            output_rel_path=f"notes/feed/{fn.node_id}.html",
            title=fn.title,
            subtitle=fn.subtitle,
            raw_sections=(sec,),
            publications=pubs_map,
            lang=fn.lang,
            lead_html=meta_box,
        )
        f_html = renderer.render_page_html(
            page=feed_page,
            profile=profile,
            partials=partials,
            css_rel_path="../../styles/custom.css",
            root_rel_prefix="../../",
            site_graph=site_graph,
        )
        staged_artifacts.append(make_staged_artifact(f"notes/feed/{fn.node_id}.html", f_html))

    for post in note_posts:
        if post.notebook_path and post.notebook_path.exists():
            static_files_to_copy.append((post.notebook_path, f"notes/notebooks/{post.notebook_path.name}"))
        lead_html = renderer.render_note_post_lead_html(post)
        note_page = compose_page(
            page_id="notes",
            node_id=f"post-{post.slug}",
            slug=post.slug,
            output_rel_path=f"notes/posts/{post.slug}.html",
            title=post.title,
            subtitle=post.subtitle,
            raw_sections=(),
            publications=pubs_map,
            lang=post.lang,
            lead_html=lead_html,
        )
        full_html = renderer.render_page_html(
            page=note_page,
            profile=profile,
            partials=partials,
            css_rel_path="../../styles/custom.css",
            root_rel_prefix="../../",
            site_graph=site_graph,
        )
        staged_artifacts.append(make_staged_artifact(f"notes/posts/{post.slug}.html", full_html))

    home_raw = repo.load_sections("home")
    res_raw = repo.load_sections("research")
    about_raw = repo.load_sections("about")
    notes_raw = repo.load_sections("notes_index")
    ch_raw = repo.load_sections("thesis_chapters")

    total_hidden = (
        count_hidden_sections(home_raw)
        + count_hidden_sections(res_raw)
        + count_hidden_sections(about_raw)
        + count_hidden_sections(notes_raw)
        + count_hidden_sections(ch_raw)
        + sum(1 for fn in all_feed_nodes if not fn.visible)
    )

    res_lead = (
        '<p>My published research examines how microscopic interactions, local perturbations, and gauge or '
        "symmetry constraints govern low-energy excitations and their physical responses in quantum spin systems. "
        'Open follow-up questions and self-contained expository derivations from my PhD and MSc research live on the <a href="notes/index.html">Feed</a> page.</p>'
    )
    feed_index_html = renderer.render_unified_feed_index_html(visible_feed_nodes, root_rel_prefix="../")
    notes_lead = (
        '<p>This unified blog feed collects my unpublished academic notes, reflections on academic and pop-culture texts, '
        'explanations of my open-source projects on <a href="https://github.com/lufreitas0000">GitHub</a>, and video scripts '
        'for <a href="https://www.instagram.com/lu.scientist/"><code>@lu.scientist</code></a>.</p>\n'
        + feed_index_html
    )
    ch_colophon = (
        '<div class="colophon-strip" role="region" aria-label="Topic navigation">\n'
        '  <a href="#ch2-kitaev">Exact Kitaev Solution &amp; Gauge Fluxes</a>\n  <span>·</span>\n'
        '  <a href="#ch3-micro">Microscopic Superexchange &amp; Polarization</a>\n  <span>·</span>\n'
        '  <a href="#ch6-kmf">Real-Space Majorana Mean-Field</a>\n  <span>·</span>\n'
        '  <a href="#ch7-vortices">Vortex Quadrupoles &amp; Local Bias</a>\n</div>'
    )
    ch_lead = (
        "<p>This page hosts modular expository notes adapted from chapters of my PhD thesis "
        "(<em>Majorana mean-field theory with \\(\\mathbb{Z}_2\\) vortices: Electrical tests in the extended Kitaev model</em>, UFRN, 2024) "
        "and MSc dissertation (<em>Gapless excitations in Kitaev materials with defects</em>, UFRN, 2019–2021), "
        "preserving the full labeled diagrams alongside multi-line aligned equations.</p>"
    )

    composed_pages = [
        (
            compose_page(
                page_id="home",
                node_id="home",
                slug="index",
                output_rel_path="index.html",
                title="Lu Freitas",
                subtitle="Theoretical quantum-matter physicist · PhD in Physics, UFRN, 2024",
                raw_sections=home_raw,
                publications=pubs_map,
                hide_page_title=True,
            ),
            "index.qmd",
            "styles/custom.css",
            "",
        ),
        (
            compose_page(
                page_id="research",
                node_id="research",
                slug="research",
                output_rel_path="research.html",
                title="Published Research",
                subtitle="",
                raw_sections=res_raw,
                publications=pubs_map,
                lead_html=res_lead,
                number_publication_sections=True,
            ),
            "research.qmd",
            "styles/custom.css",
            "",
        ),
        (
            compose_page(
                page_id="about",
                node_id="about",
                slug="about",
                output_rel_path="about.html",
                title="About Me",
                subtitle="",
                raw_sections=about_raw,
                publications=pubs_map,
            ),
            "about.qmd",
            "styles/custom.css",
            "",
        ),
        (
            compose_page(
                page_id="notes",
                node_id="notes",
                slug="notes-index",
                output_rel_path="notes/index.html",
                title="Feed",
                subtitle="",
                raw_sections=notes_raw,
                publications=pubs_map,
                lead_html=notes_lead,
            ),
            "notes/index.qmd",
            "../styles/custom.css",
            "../",
        ),
        (
            compose_page(
                page_id="notes",
                node_id="thesis-chapters",
                slug="thesis-chapters",
                output_rel_path="notes/thesis-chapters.html",
                title="Expository Physics Notes",
                subtitle="",
                raw_sections=ch_raw,
                publications=pubs_map,
                lead_html=ch_lead,
                colophon_html=ch_colophon,
            ),
            "notes/thesis-chapters.qmd",
            "../styles/custom.css",
            "../",
        ),
    ]

    total_visible_sections = 0
    for page_spec, qmd_rel, css_rel, root_pref in composed_pages:
        total_visible_sections += len(page_spec.sections)
        if config.write_qmd_sources:
            store.write_source_text(qmd_rel, renderer.render_page_qmd(page_spec, partials))
        html_text = renderer.render_page_html(
            page=page_spec,
            profile=profile,
            partials=partials,
            css_rel_path=css_rel,
            root_rel_prefix=root_pref,
            site_graph=site_graph,
        )
        staged_artifacts.append(make_staged_artifact(page_spec.output_rel_path, html_text))

    aux_specs = [
        ("about", "working-with-me", "about/working-with-me.qmd", "about/working-with-me.html", "../styles/custom.css", "../"),
        ("notes", "series", "notes/series/papers-worth-understanding.qmd", "notes/series/papers-worth-understanding.html", "../../styles/custom.css", "../../"),
    ]
    for p_id, n_id, qmd_rel, rel_out, css_rel, root_pref in aux_specs:
        fm, body_md = repo.load_aux_page_source(qmd_rel)
        for token, replacement in partials.items():
            body_md = body_md.replace(token, replacement)
        body_html = renderer.render_markdown_fragment(body_md)
        aux_page = compose_page(
            page_id=p_id,
            node_id=n_id,
            slug=Path(qmd_rel).stem,
            output_rel_path=rel_out,
            title=str(fm.get("title", Path(qmd_rel).stem)),
            subtitle="",
            raw_sections=(),
            publications=pubs_map,
            lang=str(fm.get("lang", "en")),
            lead_html=body_html,
        )
        full_html = renderer.render_page_html(
            page=aux_page,
            profile=profile,
            partials=partials,
            css_rel_path=css_rel,
            root_rel_prefix=root_pref,
            site_graph=site_graph,
        )
        staged_artifacts.append(make_staged_artifact(rel_out, full_html))

    wwm_md = renderer.render_working_with_me_markdown(profile)
    if config.write_qmd_sources:
        store.write_source_text("about/working-with-me.md", wwm_md)
    staged_artifacts.append(make_staged_artifact("about/working-with-me.md", wwm_md))
    staged_artifacts.append(make_staged_artifact("notes/search-index.json", renderer.render_feed_search_index_json(visible_feed_nodes)))
    staged_artifacts.append(make_staged_artifact("notes/index.xml", renderer.render_rss_xml(note_posts, base_url)))
    staged_artifacts.append(make_staged_artifact("robots.txt", renderer.render_robots_txt(base_url)))
    staged_artifacts.append(make_staged_artifact("sitemap.xml", renderer.render_sitemap_xml(site_graph, base_url)))

    hashes = store.commit_artifacts_atomically(
        target_dir=config.out_dir,
        artifacts=tuple(staged_artifacts),
        static_dirs_to_copy=(
            (repo.site_root / "styles", "styles"),
            (repo.site_root / "assets", "assets"),
        ),
        static_files_to_copy=tuple(static_files_to_copy),
    )

    return BuildReceipt(
        out_dir=str(config.out_dir),
        pages_rendered=len(staged_artifacts) - 5,
        visible_sections_count=total_visible_sections,
        hidden_sections_count=total_hidden,
        published_notes_count=len(note_posts),
        feed_posts_count=len(visible_feed_nodes),
        artifact_hashes=hashes,
    )
