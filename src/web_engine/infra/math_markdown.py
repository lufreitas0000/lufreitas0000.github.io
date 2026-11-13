"""Pure Markdown and LaTeX math delimiter preprocessing."""

from __future__ import annotations

import html
import re
import markdown


def convert_markdown_preserving_math(md_text: str) -> str:
    """Converts Markdown to HTML while preserving LaTeX display (`$$...$$`) and inline (`$...$`) math."""
    math_store: list[str] = []

    def _stash_display(match: re.Match[str]) -> str:
        idx = len(math_store)
        expr = match.group(1).strip()
        math_store.append(f'<div class="math-scroll">\n$${expr}$$\n</div>')
        return f"@@MATH_TOKEN_{idx}@@"

    def _stash_inline(match: re.Match[str]) -> str:
        idx = len(math_store)
        expr = match.group(1).strip()
        math_store.append(f"\\({expr}\\)")
        return f"@@MATH_TOKEN_{idx}@@"

    staged = re.sub(r"\$\$(.*?)\$\$", _stash_display, md_text, flags=re.DOTALL)
    staged = re.sub(r"(?<!\$)\$(?!\$)([^\$\n]+?)\$(?!\$)", _stash_inline, staged)

    rendered = markdown.markdown(staged, extensions=["extra", "sane_lists"])
    for idx, replacement in enumerate(math_store):
        rendered = rendered.replace(f"@@MATH_TOKEN_{idx}@@", replacement)
    return rendered


def format_inline_tex_and_amp(text: str) -> str:
    """Escapes bare ampersands and converts `$...$` to MathJax `\\(...\\)` delimiters."""
    text = re.sub(r"&(?!(?:[a-zA-Z0-9]+|#\d+|#x[0-9a-fA-F]+);)", "&amp;", text)
    text = re.sub(r"(?<!\$)\$(?!\$)([^\$\n]+?)\$(?!\$)", lambda m: f"\\({m.group(1)}\\)", text)
    return text


def format_escaped_tex(text: str) -> str:
    """HTML-escapes plain text and converts inline `$...$` into MathJax delimiters."""
    return re.sub(r"(?<!\$)\$(?!\$)([^\$\n]+?)\$(?!\$)", lambda m: f"\\({m.group(1)}\\)", html.escape(text))
