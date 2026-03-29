# To do

You are reading this file because you want to check, update or add tasks in the migration process.
Active tasks only — completed items live in the inventory files.

## Inventory (to complete)

- [ ] Audit `helpers` package vs v5 helpers — check what's already ported
- [ ] Audit `file-system.md` — check what structure classes exist in `app` and `filestate` packages
- [x] Audit `cli-bash.md` — `bin/wex` corrigé : `WEX_REQUEST_ID` passé via `--force-request-id` (plus en positional)

## Code TODOs

- [ ] `wex-6/src/common/wex.py:44` — Remove commented TestAddonManager lines
- [ ] `wex-addon-app/…/basic_app_workdir.py:363` — Run tests
- [ ] `filestate-python/…/class_name_matches_file_name_option.py:42` — TODO vide, à préciser

## Command system

- [x] Test complete command execution flow end-to-end (ping/pong test)

## Response system

See full inventory: `inventory/response-system.md`

### Consolidation (done)
- [x] Tous les types de réponse déplacés de `wex-core/response/` → `wexample_app/response/`
- [x] `wex-core/response/` — répertoire entièrement supprimé
- [x] `DictResponse`, `ListResponse`, `TableResponse`, `FunctionResponse` (callable générique)
- [x] `ShellCommandResponse`, `InteractiveShellCommandResponse`
- [x] `ResponseCollectionResponse`, `QueuedCollectionResponse`, `QueuedCollectionStop*`
- [x] `StrResponse`, `IntResponse` — nouveaux types typés avec validation
- [x] `BooleanResponse`, `NullResponse` — corrigés (`@base_class`, validation)

### Render modes
- [x] Render modes → déjà mappés : `output_format` (str/json/yaml) sur `CommandRequest`, `_config_arg_output_format` sur le kernel, dispatché dans `AbstractResponse.get_formatted()`

### Test infrastructure
- [ ] `AbstractTestCase` equivalent — pytest base fixture + assertion helpers
- [ ] `for_each_render_mode()` — parametrized render mode testing
- [ ] Move `test_ping_executes` → co-located `commands/ping/test_pong.py`

## Decorators

- [x] Implement `@alias`
- [x] Implement `@attach` (before/after hooks) — supporte string ET référence directe à la CommandMethodWrapper
- [x] Implement `@as_sudo` — `decorator/as_sudo.py`, re-exec via `os.execvp("sudo", ...)` dans `Kernel._enforce_sudo_if_needed`
- [~] `@no_log` — **SKIP** : redondant avec `--quiet` / `output_target=none`
- [~] `@verbosity` — **SKIP** : faisable directement via `context.kernel.io`
- [~] `@test_command` — **SKIP** : auto-détecté par convention de chemin dans `build_registry_data`
- [x] `check/hi` — migré avec `@alias("hi")`

## Registry

- [x] Infrastructure de base — `registry/build`, `hydrate()`, `get_addon_commands()`

### Champs RegistryCommandData

- [x] `description` — extrait du `@command`
- [x] `alias` — liste des `@alias`
- [x] `attachments` — before/after de `@attach`
- [x] `sudo` — extrait du `@as_sudo`, utilisé par `_enforce_sudo_if_needed`
- [ ] `properties` — metadata custom des decorators
- [ ] `name` dans l'entrée addon
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
