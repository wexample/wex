# To do

You are reading this file because you want to check, update or add tasks in the migration process.
Active tasks only — completed items live in the inventory files.

## Inventory (to complete)

- [ ] Audit `helpers` package vs v5 helpers — check what's already ported
- [ ] Audit `file-system.md` — check what structure classes exist in `app` and `filestate` packages
- [ ] Audit `cli-bash.md` — check `bin/wex` in wex-6 for task ID and post-exec handling

## Code TODOs

- [ ] `wex-6/src/common/wex.py:44` — Add TestAddonManager only when testing core
- [x] `wex-core/…/test/commands/run/all.py:25` — Finaliser le registre pour pouvoir lister les tests
- [ ] `wex-addon-app/…/basic_app_workdir.py:363` — Run tests
- [ ] `filestate-python/…/class_name_matches_file_name_option.py:42` — TODO vide, à préciser

## Command system

- [ ] Test complete command execution flow end-to-end
- [ ] Implement proper response handling (decide v6 pattern for structured output)

## Decorators

- [ ] Implement `@alias`
- [ ] Implement `@attach` (before/after hooks)
- [ ] Implement `@as_sudo`
- [ ] Implement `@no_log`
- [ ] Implement `@verbosity`
- [ ] Implement `@test_command`

## Registry

- [x] Infrastructure de base — `registry/build`, `hydrate()`, `get_addon_commands()`, `test::run/all`

### Bloquant (description, alias, attachments, properties)

- [x] Ajouter `description` dans `RegistryCommandData` — extraire `help=` du `@command`
- [x] Ajouter `alias` dans `RegistryCommandData` — liste des alias `@alias`
- [ ] Ajouter `attachments` dans `RegistryCommandData` — before/after de `@attach`
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
- [ ] `webhook/listen`, `webhook/exec`, `webhook/stop`
- [ ] `remote/*`

## Addons: system / docker / ai / db / services

- [ ] system: `os/name`, `system/ip`, `disk/spaces`, `process/by_port`, `kill/by_port`, `own/this`
- [ ] docker: `container/runs`, `docker/ip`, `docker/stop_all`
- [ ] ai: `talk/ask`, `talk/about_file`, `@ai_tool` decorator
- [ ] services-db, services-php, services-various
