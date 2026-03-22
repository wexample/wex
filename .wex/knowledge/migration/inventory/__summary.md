# Feature Inventory

You are reading this file because you need to understand the migration status of a specific wex-5 feature.

Each file covers one functional domain. For each item: v5 location, migration status via `[ ]` checkboxes, and v6 target.

## Directory registry

- 📄 core-mechanisms.md — **priority** — registry, resolvers, YAML runner, attach, structured output
- 📄 kernel.md — main orchestrator, task ID, verbosity, render modes
- 📄 command-system.md — resolvers, runners, command request lifecycle
- 📄 response-system.md — all response types and rendering pipeline
- 📄 decorators.md — @command, @option, @alias, @attach, @as_sudo…
- 📄 helpers.md — command, string, file, service, prompt, user, routing…
- 📄 file-system.md — file/directory structure classes
- 📄 resources-templates.md — code templates, systemd service
- 📄 cli-bash.md — bash entry points, install scripts, autocomplete
- 📁 addons/ — one file per addon
