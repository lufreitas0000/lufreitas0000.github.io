# Rule 02: TDD and Contract Verification

1. Pure `domain/` validators (`contracts.py`) and `services/` (`pipeline.py`, `dag.py`, `build_site.py`) must be tested in `test/unit/` without disk I/O using in-memory fake ports.
2. Infrastructure adapters (`infra/`) must be tested in `test/integration/`.
3. Full built site invariants (navigation count, zero broken internal links, RSS/sitemap/JSON-LD validity, privacy hygiene) must be tested in `test/e2e/`.
4. Report exact commands and outcomes (`make verify`).
