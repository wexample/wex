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

## YAML executor

- [x] `CoreYamlCommandRunner` — full implementation
- [x] `YamlCommandDefinition` — immutable data object, parsed once, cached instance-level
- [x] `AbstractScriptRunner` + `get_step_options()` — contrat extensible par les addons
- [x] `BashScriptRunner` — inline script + file, `ignore_error`, `workdir`
- [x] `PythonScriptRunner` — inline script + file, `ignore_error`, lazy via `PythonScriptResponse`
- [x] `ScriptRunnerRegistry` sur le kernel — `kernel.script_runner_registry.register(MyRunner())`
- [x] Substitution globale en amont (`yaml_substitute_step`) — runners reçoivent des strings propres
- [x] Variables : env vars (basse priorité) < `PATH_CURRENT` < options (haute priorité)
- [x] `variable:` — capture output d'un step dans une variable pour les steps suivants
- [x] `command:` — appel interne via `kernel.execute_kernel_command()`
- [x] Validation des clés inconnues à l'exécution avec message clair
- [x] TypedDicts : `BashStepDict`, `PythonStepDict`, `InternalCommandStepDict`
- [x] Symétrie totale Python/YAML au niveau registry (description, alias, attachments, sudo)

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

- [x] `ServiceCommandResolver.build_registry_data()` — utilise `_scan_commands_dir` (yml + py, attachments, sudo)
- [ ] Résolution de l'héritage service (`config.extends` → merge récursif) — feature avancée, non bloquante

### Helpers & options

- [x] `get_all_commands()`, `get_all_command_names()`, `get_sudo_commands()`, `find_command()`, `suggest()` sur `KernelRegistry`
- [ ] `registry_find_commands_by_function_property()` — filter par custom property decorator
- [ ] `resolver.get_commands_registry()`
- [ ] Options `--test`, `--write`, `@alias("rebuild")` sur `registry/build`

### Autocomplete

Infrastructure bash en place (`bin/autocomplete-handler`, `bin/autocomplete`). Commande Python rollbackée — à refaire proprement.

#### Architecture retenue

**Principe :** chaque resolver implémente `autocomplete_suggest(cursor, search_split)`. Il reconnaît son propre pattern de commande, sait où chercher ses suggestions, et retourne une string espace-séparée ou `""`. La commande Python agrège tous les resolvers.

**Source de données par resolver :**
- `AddonCommandResolver` → **registry** (commandes globales, déjà buildées)
- `ServiceCommandResolver` → **registry** (services déclarés globalement)
- `AppCommandResolver` → **filesystem dynamique** — scan de `.wex/command/` dans le répertoire courant (contexte-dépendant, pas de cache possible)
- `UserCommandResolver` → **filesystem dynamique** — scan de `~/.wex/command/`

#### Contrat du mécanisme

**Flux complet :**
1. Bash appelle la completion function avec `COMP_WORDS` et `COMP_CWORD`
2. Bash construit `SEARCH` (tout après `wex`, re-joint par espace) et `CURSOR = COMP_CWORD - 1`
3. Bash appelle `wex --quiet default::autocomplete/suggest -s "${SEARCH}" -c "${CURSOR}"`
4. Python itère tous les resolvers → agrège leurs suggestions → retourne une string espace-séparée
5. Bash passe à `compgen -W "${SUGGESTIONS}" -- "${CURRENT}"` pour filtrer
6. Bash ajoute un espace final si une seule suggestion complète

> **Pourquoi SEARCH est re-joint par espace :** bash splitte sur `$COMP_WORDBREAKS` qui inclut `:` et `/`. `demo::ping/pong` devient `["demo", ":", ":", "ping", "/", "pong"]`. En re-joignant tout, Python reçoit un string stable et reconstruit lui-même le split sur les espaces.

**Format de sortie Python (contrat strict) :**
- Une seule ligne, suggestions séparées par des espaces
- Aucun log, aucun formatage — `--quiet` systématique dans le bash
- `""` si aucune suggestion

**Sémantique cursor/search_split :**
- `search` = tous les tokens après `wex` re-joints par espace
- `search_split = search.split(" ")`
- `cursor` = index 0-based dans `search_split` du mot en cours
- `cursor >= len(search_split)` → `""` immédiatement

#### Cas de figure par resolver

**AddonCommandResolver** — reconnaît : `search_split[0]` ne commence pas par `.`, `~`, `@`

| cursor | search_split exemple | résultat |
|--------|----------------------|----------|
| 0 | `[""]` | tous les addons : `demo:: default:: ...` |
| 0 | `["de"]` | addons commençant par `de` : `demo::` |
| 0 | `["pi"]` | alias correspondant : `ping` |
| 1 | `["demo", ":"]` | `:` (compléter `::`) |
| 1 | `["demo", "::"]` | toutes les commandes de `demo` : `ping/pong sudo/check` |
| 2 | `["demo", "::", "p"]` | commandes commençant par `p` : `ping/pong` |
| 2 | `["demo", "::", "ping/pong"]` | `ping/pong ` (complet, espace final) |
| ≥3 | `["demo", "::", "ping/pong", "--t"]` | options : `--type` |

**ServiceCommandResolver** — reconnaît : `search_split[0]` commence par `@`

| cursor | search_split exemple | résultat |
|--------|----------------------|----------|
| 0 | `[""]` | `@` |
| 0 | `["@"]` | tous les services |
| 1 | `["@myapp", ":"]` | `:` |
| 1 | `["@myapp", "::"]` | toutes les commandes du service |
| 2 | `["@myapp", "::", "cmd"]` | commandes filtrées |

**AppCommandResolver** — reconnaît : `search_split[0]` commence par `.`
Scan dynamique de `.wex/command/` dans le répertoire courant (remonte jusqu'à trouver un `.wex/`).

**UserCommandResolver** — reconnaît : `search_split[0]` commence par `~`
Scan dynamique de `~/.wex/command/`.

#### Plan d'implémentation — repoussé à la fin

L'autocomplete sera implémenté en une seule fois, une fois tous les resolvers migrés (addon ✓, service, app, user). Implémenter par morceaux livrerait quelque chose d'incomplet à chaque étape.

Prérequis bloquants avant autocomplete :
- [x] YAML executor
- [x] `ServiceCommandResolver` migré
- [x] `AppCommandResolver` migré
- [x] `UserCommandResolver` migré

## Prochaines étapes immédiates

- [ ] Commandes système dans `wex-core` en YAML : `os/name`, `system/ip`, `disk/spaces`, `dir/spaces`, `process/by_port`, `kill/by_port`, `own/this`

## Addons: core

- [x] `check/hi` — migré avec `@alias("hi")`
- [ ] `logo/show`
- [x] `command/create` — resolver delegation, templates yml/py, auto-rebuild registry
- [ ] `logs/show`, `logs/rotate`
- [ ] `core/install`, `core/uninstall` — à faire en dernier ; inclura config globale `~/.wex/config.yml` si besoin

## Addons: app (Docker lifecycle + config app)

> À faire une fois qu'une vraie app Docker est en place pour tester.

- [ ] `app/start`, `app/stop`, `app/restart`, `app/serve`, `app/exec`, `app/perms`
- [ ] `db/dump`, `db/exec`, `db/go`, `db/restore`
- [ ] `remote/*`
- [ ] `container/runs`, `docker/ip`, `docker/stop_all` — utils Docker légers, dans addon-app
- [ ] Config app `.wex/config.yml` — `config/get`, `config/set` dans addon-app

## Webhooks (addon-app)

> À faire après `app/start`. Dépend d'une vraie app en place.

- [ ] `@app_webhook` decorator
- [ ] `webhook/listen`, `webhook/exec`, `webhook/stop`

## Addons: ai / db / services

- [ ] ai: `talk/ask`, `talk/about_file`, `@ai_tool` decorator
- [ ] services-db, services-php, services-various

## SKIP définitifs

- [~] `file/append_once`, `file/remove_line` — helpers Python, pas des commandes
- [~] QueuedCollectionResponse, Task ID, post-exec queue, Logging JSON — v6 utilise des subprocesses
