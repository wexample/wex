## Addons

wex implements no command itself. Every feature comes from an addon, and
the list below is the one declared in pyproject.toml — installing
wex installs all of them.

| Addon | Role |
| --- | --- |
| [ai](https://pypi.org/project/wexample-wex-addon-ai/) | Adds a Claude-backed AI agent to the wex CLI with persistent sessions, engram memory, and MCP access to kernel commands. |
| [app](https://pypi.org/project/wexample-wex-addon-app/) | Adds Docker application management to wex: service lifecycle commands, environment config, and managed workdir setup |
| [dev-css](https://pypi.org/project/wexample-wex-addon-dev-css/) | Plugs a named CSS addon manager into the wex CLI kernel, serving as the registration entry point for CSS development tooling within the wex addon ecosystem |
| [dev-javascript](https://pypi.org/project/wexample-wex-addon-dev-javascript/) | Extends wex with JavaScript support: enforces JS/TS project layout and symlinks local npm packages into node_modules |
| [dev-php](https://pypi.org/project/wexample-wex-addon-dev-php/) | Extends wex with PHP-specific development commands for Composer, Laravel, Symfony, and WordPress services running in Docker containers |
| [dev-python](https://pypi.org/project/wexample-wex-addon-dev-python/) | Extends wex with commands to format, lint, and rename Python symbols, plus workdir types for Python packages and suites |
| [filestate](https://pypi.org/project/wexample-wex-addon-filestate/) | Integrates wexample-filestate's declarative file-tree reconciliation engine into the wex CLI as a pluggable addon |
| [master](https://pypi.org/project/wexample-wex-addon-master/) | Extends wex to fan out commands across all managed apps and manage DNS zones against Cloudflare, Route53, OVH, and Gandi |
| [package](https://pypi.org/project/wexample-wex-addon-package/) | Extends wex with commands to bump, publish to PyPI, and coordinate releases across a Python package suite |
| [process](https://pypi.org/project/wexample-wex-addon-process/) | Executes process runs defined on disk—either directly or by consuming them from a queue as a worker—against filestate selections |
| [services-collab](https://pypi.org/project/wexample-wex-addon-services-collab/) | Extends wex with install and configuration commands for self-hosted collaboration services — Nextcloud, OnlyOffice, Synapse, and Rocket.Chat |
| [services-db](https://pypi.org/project/wexample-wex-addon-services-db/) | Provides wex with dump, restore and connect commands for PostgreSQL, MySQL, MongoDB, Redis and other database containers |
| [services-monitoring](https://pypi.org/project/wexample-wex-addon-services-monitoring/) | Registers monitoring services — Grafana, Kibana, Plausible, and Elastic Fleet — as wex app services with lifecycle commands |
| [services-platform](https://pypi.org/project/wexample-wex-addon-services-platform/) | Adds wex service commands (install, setup, ready) for platforms like GitLab, Supabase, n8n, Odoo, and Ollama |

Each addon documents its own commands. This repository documents the kernel: how it
boots, how a command string is resolved, and what an addon may contribute.
