# To do

You are reading this file because you want to check, update or add tasks in the migration process.
Active tasks only — completed items live in the inventory files.

## Inventory (to complete)

- [ ] Audit `helpers` package vs v5 helpers — check what's already ported
- [ ] Audit `file-system.md` — check what structure classes exist in `app` and `filestate` packages
- [ ] Audit `cli-bash.md` — check `bin/wex` in wex-6 for task ID and post-exec handling

## Code TODOs

- [ ] `wex-6/src/common/wex.py:44` — Remove commented TestAddonManager lines
- [ ] `wex-addon-app/…/basic_app_workdir.py:363` — Run tests
- [ ] `filestate-python/…/class_name_matches_file_name_option.py:42` — TODO vide, à préciser

## Command system

- [x] Test complete command execution flow end-to-end (ping/pong test)

## Response system

See full inventory: `inventory/response-system.md`

### Phase 1 — render modes + simple structured output
- [ ] Render modes → map `TERMINAL/JSON/NONE` to `output_format` on kernel
- [x] `DictResponse` — dict → formatted lines or JSON
- [x] `ListResponse` — list → newline-separated or JSON array
- [x] `TableResponse` — rows + headers + title
- [x] `KeyValueResponse` — merged into DictResponse (same rendering via PropertiesPromptResponse)
- [~] `AbortResponse` — **SKIP** : redondant avec `QueuedCollectionStopResponse` + exceptions Python

### Phase 2 — special behaviours
- [x] `HiddenResponse` — replaced by `output_target=none`
- [ ] `FunctionResponse` — lazy callable wrapping (used by QueuedCollectionResponse steps, migrate with Phase 3)
- [x] `ShellCommandResponse` (ex-NonInteractive) — capture shell output via `shell_run(capture=True)`
- [x] `InteractiveShellCommandResponse` — live tty passthrough via `shell_run(inherit_stdio=True)`

### Phase 3 — collections
- [x] `ResponseCollectionResponse` — flat ordered list of responses
- [x] `QueuedCollectionResponse` — sequential steps, stop signals, previous_value pipeline (fast mode dropped)

### Test infrastructure
- [ ] `AbstractTestCase` equivalent — pytest base fixture + assertion helpers
- [ ] `for_each_render_mode()` — parametrized render mode testing
- [ ] Move `test_ping_executes` → co-located `commands/ping/test_pong.py`

## Decorators

- [x] Implement `@alias`
- [x] Implement `@attach` (before/after hooks) — supporte string ET référence directe à la CommandMethodWrapper
- [ ] Implement `@as_sudo` — bloqué par shell commands middleware, à faire avec les services
- [~] `@no_log` — **SKIP** : redondant avec `--quiet` / `output_target=none`
- [~] `@verbosity` — **SKIP** : faisable directement via `context.kernel.io`
- [~] `@test_command` — **SKIP** : auto-détecté par convention de chemin dans `build_registry_data`
- [x] `check/hi` — migré avec `@alias("hi")`

## Registry

- [x] Infrastructure de base — `registry/build`, `hydrate()`, `get_addon_commands()`

### Bloquant (description, alias, attachments, properties)

- [x] Ajouter `description` dans `RegistryCommandData` — extraire `help=` du `@command`
- [x] Ajouter `alias` dans `RegistryCommandData` — liste des alias `@alias`
- [x] Ajouter `attachments` dans `RegistryCommandData` — before/after de `@attach`
- [ ] Ajouter `properties` dans `RegistryCommandData` — metadata custom des decorators
- [ ] Ajouter `name` dans l'entrée addon
- [x] `resolver.resolve_alias(command)` — lookup avant pattern matching

### Service resolver registry

- [ ] `ServiceCommandResolver.build_registry_data()` — scanner `services/`, charger `service.yml`
- [ ] Résolution de l'héritage (`config.extends` → merge récursif)

### Helpers & options

- [ ] `registry_get_all_commands(kernel)`, `registry_find_commands_by_function_property()`
- [ ] `resolver.get_commands_registry()`
- [ ] Options `--test`, `--write`, `@alias("rebuild")` sur `registry/build`

### Autocomplete

- [ ] `resolver.autocomplete_suggest(cursor, search_split)` sur chaque resolver
- [ ] `default::autocomplete/suggest`

## Addons: core

- [ ] `logo/show`, `check/hi`, `command/create`
- [ ] `logs/show`, `logs/rotate`
- [ ] `core/install`, `core/uninstall`, `core/cleanup`, `install/update`

## Addons: app (Docker lifecycle)

- [ ] `app/start`, `app/stop`, `app/restart`, `app/serve`, `app/exec`, `app/perms`
- [ ] `db/dump`, `db/exec`, `db/go`, `db/restore`
- [ ] `remote/*`

## Webhooks (addon-app — wex-addon-app/resolver/app_command_resolver.py)

Webhooks = HTTP endpoints exposant des commandes app via `@app_webhook` decorator.
Dépend de : response system, `app/start`.

- [ ] `AppCommandResolver.run_command_request_from_url_path()` — migrer dans wex-addon-app
- [ ] `@app_webhook` decorator — marque une commande comme exposable via HTTP
- [ ] `webhook/listen`, `webhook/exec`, `webhook/stop` — commandes addon-app

## Addons: system / docker / ai / db / services

- [ ] system: `os/name`, `system/ip`, `disk/spaces`, `process/by_port`, `kill/by_port`, `own/this`
- [ ] docker: `container/runs`, `docker/ip`, `docker/stop_all`
- [ ] ai: `talk/ask`, `talk/about_file`, `@ai_tool` decorator
- [ ] services-db, services-php, services-various
