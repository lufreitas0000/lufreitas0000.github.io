"""Static parser for legacy .qmd note posts and precomputed .ipynb notebooks."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any
import yaml

from .math_markdown import convert_markdown_preserving_math


def parse_qmd_file(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, flags=re.DOTALL)
    if not m:
        return {}, raw
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def render_ipynb_static_html(ipynb_path: Path, download_href: str) -> str:
    nb = json.loads(ipynb_path.read_text(encoding="utf-8"))
    cells_html: list[str] = [
        f"""<div class="scope-panel">
  <div class="scope-panel-title">Precomputed Static Notebook (Zero Build-Time Execution)</div>
  <p style="margin-bottom:0;">This notebook is rendered statically from saved cells without running heavy computation during site builds. <a href="{html.escape(download_href)}">Download notebook</a>.</p>
</div>"""
    ]
    for cell in nb.get("cells", []):
        ctype = cell.get("cell_type", "")
        src = "".join(cell.get("source", []))
        if ctype == "markdown":
            cells_html.append(convert_markdown_preserving_math(src))
        elif ctype == "code":
            cells_html.append(f"<pre><code>{html.escape(src)}</code></pre>")
            for out in cell.get("outputs", []):
                text_out = "".join(out.get("text", []))
                if text_out:
                    cells_html.append(f'<pre aria-label="Notebook output"><code>{html.escape(text_out)}</code></pre>')
    return "\n".join(cells_html)
