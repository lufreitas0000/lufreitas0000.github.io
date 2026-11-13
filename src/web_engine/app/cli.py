"""Thin CLI entrypoint wiring concrete infra adapters into `build_site`."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from ..domain.models import BuildConfig
from ..infra.acid_store import AcidFilesystemStore
from ..infra.html_renderer import StaticSiteRenderer
from ..infra.markdown_repo import FileSystemContentRepository
from ..services.build_site import build_site


def scaffold_new_post(site_root: Path, slug: str, kind: str) -> Path:
    now_ym = datetime.now(timezone.utc).strftime("%Y-%m")
    feed_dir = site_root / "content" / "feed"
    target = feed_dir / f"{now_ym}-{slug}.md"
    if target.exists():
        raise FileExistsError(f"Post already exists: {target}")
    template = f"""---
id: "{slug}"
title: "TODO: Title for {slug}"
subtitle: "TODO: Short subtitle"
date: "{now_ym}"
order: 50
visible: false
kind: "{kind}"
lang: "en"
evidence_status: "exploratory-draft"
tags:
  - "{kind}"
keywords:
  - "{slug}"
summary: "TODO: One-sentence self-contained summary."
---

Write your note here in standard Markdown with `$inline$` or `$$display$$` LaTeX math.
"""
    target.write_text(template, encoding="utf-8")
    return target


def main() -> int:
    pkg_root = Path(__file__).resolve().parent.parent.parent.parent
    site_root = pkg_root / "site"
    fixtures_root = pkg_root / "test" / "fixtures"

    parser = argparse.ArgumentParser(description="Build Lu Freitas personal research website (Hexagonal Engine).")
    parser.add_argument("--out-dir", type=Path, default=pkg_root / "build" / "_site")
    parser.add_argument("--verify-fixtures", action="store_true", help="Also build test/fixtures into build/fixtures_site")
    parser.add_argument("--base-url", type=str, default=None)
    parser.add_argument("--new-post", type=str, default=None, help="Scaffold a new Feed Markdown file with this slug")
    parser.add_argument("--kind", type=str, default="note")
    args = parser.parse_args()

    if args.new_post:
        created = scaffold_new_post(site_root, args.new_post, args.kind)
        print(f"Created draft post: {created}")
        return 0

    repo = FileSystemContentRepository(site_root=site_root, fixtures_root=fixtures_root)
    renderer = StaticSiteRenderer(templates_dir=site_root / "templates")
    store = AcidFilesystemStore(site_root=site_root)

    pub_receipt = build_site(
        repo=repo,
        renderer=renderer,
        store=store,
        config=BuildConfig(out_dir=args.out_dir, include_dev_fixtures=False, base_url_override=args.base_url),
    )
    print(f"Built public site: {pub_receipt.out_dir} ({pub_receipt.pages_rendered} pages, {pub_receipt.feed_posts_count} feed posts)")

    if args.verify_fixtures:
        fix_dir = pkg_root / "build" / "fixtures_site"
        fix_receipt = build_site(
            repo=repo,
            renderer=renderer,
            store=store,
            config=BuildConfig(
                out_dir=fix_dir,
                include_dev_fixtures=True,
                base_url_override=args.base_url,
                write_qmd_sources=False,
            ),
        )
        print(f"Built fixture site: {fix_receipt.out_dir} ({fix_receipt.pages_rendered} pages, {fix_receipt.published_notes_count} fixture notes)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
