# Review a website change locally in a separate Git worktree

Use WSL Ubuntu. The worktree is an **independent checkout** of the same
Git repository. Its private \`build/\` output never enters \`main\`
and nothing is published by running this command.

From an existing website clone:

\`\`\`sh
git fetch origin
git worktree add -b feat/local-preview ../website-preview origin/main
cd ../website-preview
python3 -m venv .venv
. .venv/bin/activate
python -m pip install PyYAML Markdown beautifulsoup4
make verify
make preview PORT=8001
\`\`\`

Open \`http://localhost:8001/notes/feed/kitaev-mf.html\` in a browser,
including Windows browsers connected to WSL.

To review another development branch already checked out remotely,
fetch it and use a **different** worktree directory. Choose a new
branch name or pass the remote branch as a detached checkout when it
is already occupied in another worktree. Never reset or clean someone
else's worktree.

The \`make preview\` target binds the preview server to 127.0.0.1,
unlike a public hosting deployment. It builds the current worktree
and serves its generated \`build/_site/\` files.

Before publishing:

1. Run \`make verify\` and any scoped JS tests.
2. Inspect layout, mathematical notation, links, no-JS behavior,
   mobile width, and static print behavior manually.
3. Independently validate claims, exact limits and source data.
4. Open or merge a reviewed PR, then check the Pages workflow.
5. Never deploy \`test/fixtures/\` or experimental solver datasets.

The preview procedure gives a manual review opportunity; it is not
a substitute for scientific or browser accessibility testing.
