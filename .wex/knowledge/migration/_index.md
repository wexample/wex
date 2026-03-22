# Migration Index

Global dashboard for tracking the v5 → v6 migration progress.

## ⚠️ Core mechanisms (priority — do before individual commands)

- [ ] [core-mechanisms](inventory/core-mechanisms.md) — Registry, YAML runner, app/user resolvers, attach system, structured output

## Core

- [ ] [kernel](inventory/kernel.md) — Main orchestrator, task ID, verbosity, entry point
- [ ] [command-system](inventory/command-system.md) — Resolvers, runners, command request lifecycle
- [ ] [response-system](inventory/response-system.md) — All response types and rendering
- [ ] [decorators](inventory/decorators.md) — @command, @option, @alias, @attach, @as_sudo…
- [ ] [helpers](inventory/helpers.md) — command, string, file, service, prompt, user, routing…
- [ ] [file-system](inventory/file-system.md) — File/directory structure classes
- [ ] [resources-templates](inventory/resources-templates.md) — Code templates, systemd service
- [ ] [cli-bash](inventory/cli-bash.md) — Bash entry points, install, autocomplete, terminal handler

## Addons

- [ ] [core](inventory/addons/core.md) — logo, version, test, registry, install, logs
- [ ] [app](inventory/addons/app.md) — Full app lifecycle (start, stop, db, webhook, remote…)
- [ ] [default](inventory/addons/default.md) — config, file, version, python/init_dirs
- [ ] [system](inventory/addons/system.md) — OS, IP, disk, process, git permissions
- [ ] [docker](inventory/addons/docker.md) — Container list, docker IP, stop all
- [ ] [ai](inventory/addons/ai.md) — LLM integration, talk/ask, talk/about_file
- [ ] [db](inventory/addons/db.md) — remote/push_restore
- [ ] [services-php](inventory/addons/services-php.md) — php, symfony, laravel, wordpress, phpmyadmin
- [ ] [services-db](inventory/addons/services-db.md) — mysql, postgres, mongo, maria, redis, sqlserver
- [ ] [services-various](inventory/addons/services-various.md) — rocketchat, jenkins, gitlab, grafana…

## Files

- [context.md](context.md) — paths, breaking changes, objectives, methodology
- [todo.md](todo.md) — active task list
- [inventory/](inventory/) — feature-by-feature migration status
