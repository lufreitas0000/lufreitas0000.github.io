# Rule 01: Repository Safety and Atomic Publishing

1. Never execute destructive Git operations (`git reset --hard`, `git push --force`, `git clean -fdx`) without explicit user authorization.
2. Never commit credentials, private emails, or raw local paths.
3. Public site builds must write to an isolated staging directory, validate all internal links, SHA-256 checksums, and privacy hygiene, and commit atomically via `os.replace()`.
4. Keep `test/fixtures/` isolated from the production `build/_site/` output.
