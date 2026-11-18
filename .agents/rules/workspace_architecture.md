# Workspace architecture and development scope

`workspace.toml` is the repository inventory and stack/tier authority.
`/home/lucas/Projects/ACTIVE_FOCUS.md` is the current sprint authority; read it
before starting work. Tiers determine audit coverage, not permission to expand
implementation scope. Root files belong to the hub; child projects are independent
Git repositories, never automatically submodules of the hub.

## Current allocation

Read ACTIVE_FOCUS.md for the latest project-specific authorization; dated
infrastructure snapshots do not determine current chapter status. 

## Domain and verification contracts
.

Local agents implement, test and review repository changes. Browser LLMs receive
bounded packets and return candidate files; whitelist, interface checks and local
verification decide acceptance. Colab performs background compute/transcription;
Jules works only on explicitly assigned jobs. Configured API/Jules transports and browser handoffs share acceptance gates. No subscription or model
availability is assumed. See the hub README routing table, `resource_routing.md`, and llm/PROTOCOL.md.

## Resource allocation and offloading

Consult `.agents/rules/resource_routing.md` for resource routing logic across Jules,
OpenAI Complimentary Pools, Gemini API (prepaid credits), Google Colab CLI (`colab-cli`),
Local Ollama, and AWS. Automated tasks route through `orchestrator/agentctl` with
strict admission control; interactive work leverages specialized skills; compute jobs
on Colab enforce auto-terminating `--gpu L4`/`G4` execution.

Keep valid GitHub remotes on lufreitas0000 for active repositories. Preview all
external candidate diffs and keep independent specifications/oracles. Compiler
success and non-vacuity/physical correctness are separate requirements. Use the
five-column discovery journal before changing definitions or pivoting algorithms.

