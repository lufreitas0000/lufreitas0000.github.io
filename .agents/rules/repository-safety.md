# Repository Safety Rules

## Forbidden commands

Agents must not execute:

    dvc gc
    dvc destroy
    git reset --hard
    git clean -fd
    git push --force
    git branch -D

## Credential files

Never read, print, modify, or stage:

    .dvc/config.local
    .env
    .env.*
    credentials.*
    *.pem
    *.key

## Large files

Raw artifacts under `data/` should be DVC tracked when they exceed the
project threshold.

The deterministic repository scripts are authoritative.

## Git privacy identity

Commits across all repositories must use the privacy noreply email:
`220090559+lufreitas0000@users.noreply.github.com` (user: `lufreitas0000`).
Do not use personal email addresses to prevent GitHub push rejections under rule GH007.

## Agent scope

Do not modify unrelated phases.

Do not perform broad refactors during physics implementation tasks.
