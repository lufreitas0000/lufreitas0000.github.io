"""ACID Transaction Filesystem Store Adapter."""

from __future__ import annotations

import hashlib
import os
import shutil
import uuid
from pathlib import Path
from bs4 import BeautifulSoup

from ..domain.contracts import ContractViolationError, require_privacy_hygiene
from ..domain.models import StagedArtifact


class AcidFilesystemStore:
    """Implements AtomicStorePort with staging, verification, atomic swap, and rollback."""

    def __init__(self, site_root: Path) -> None:
        self._site_root = site_root

    def write_source_text(self, rel_path: str, content: str) -> None:
        dst = self._site_root / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.parent / f".{dst.name}.tmp_{uuid.uuid4().hex[:8]}"
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, dst)

    def commit_artifacts_atomically(
        self,
        target_dir: Path,
        artifacts: tuple[StagedArtifact, ...],
        static_dirs_to_copy: tuple[tuple[Path, str], ...],
        static_files_to_copy: tuple[tuple[Path, str], ...],
    ) -> dict[str, str]:
        parent = target_dir.parent
        parent.mkdir(parents=True, exist_ok=True)
        stage_dir = parent / f".{target_dir.name}.tx_stage_{uuid.uuid4().hex[:8]}"
        backup_dir = parent / f".{target_dir.name}.tx_backup_{uuid.uuid4().hex[:8]}"

        try:
            stage_dir.mkdir(parents=True, exist_ok=False)

            for src_dir, rel_dst in static_dirs_to_copy:
                if src_dir.exists():
                    shutil.copytree(src_dir, stage_dir / rel_dst, dirs_exist_ok=True)
            for src_file, rel_dst in static_files_to_copy:
                if src_file.exists():
                    dst_f = stage_dir / rel_dst
                    dst_f.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_f)

            recorded_hashes: dict[str, str] = {}
            for art in artifacts:
                actual_sha = hashlib.sha256(art.content_bytes).hexdigest()
                if actual_sha != art.sha256:
                    raise ContractViolationError(
                        f"ACID checksum mismatch for {art.rel_path}: expected {art.sha256}, got {actual_sha}"
                    )
                out_path = stage_dir / art.rel_path
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(art.content_bytes)
                recorded_hashes[art.rel_path] = actual_sha

            self._verify_staged_tree_consistency(stage_dir)

            if target_dir.exists():
                os.replace(target_dir, backup_dir)
            try:
                os.replace(stage_dir, target_dir)
            except Exception:
                if backup_dir.exists() and not target_dir.exists():
                    os.replace(backup_dir, target_dir)
                raise
            finally:
                if backup_dir.exists():
                    shutil.rmtree(backup_dir, ignore_errors=True)

            return recorded_hashes

        except Exception:
            if stage_dir.exists():
                shutil.rmtree(stage_dir, ignore_errors=True)
            raise

    def _verify_staged_tree_consistency(self, stage_dir: Path) -> None:
        for html_file in sorted(stage_dir.rglob("*.html")):
            text = html_file.read_text(encoding="utf-8")
            require_privacy_hygiene(text, context=str(html_file.relative_to(stage_dir)))
            soup = BeautifulSoup(text, "html.parser")
            for tag in soup.find_all(["a", "link", "img", "script"]):
                attr = "src" if tag.name in ("img", "script") else "href"
                ref = tag.get(attr, "")
                if not ref or ref.startswith(("http://", "https://", "mailto:", "#", "data:")):
                    continue
                rel_part = ref.split("#")[0]
                if not rel_part:
                    continue
                target = (html_file.parent / rel_part).resolve()
                if not target.exists():
                    raise ContractViolationError(
                        f"ACID Consistency Failure: Broken internal reference {ref!r} in {html_file.relative_to(stage_dir)}"
                    )
