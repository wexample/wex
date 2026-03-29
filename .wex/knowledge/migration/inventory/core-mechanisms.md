# Core Mechanisms

You are reading this file because you need to know what foundational mechanisms must be in place before migrating individual commands.

These are prerequisites — without them, migrated commands are incomplete or untestable.

---

## Command resolution

- [x] Addon resolver — `addon::group/command`
- [x] Service resolver — `@service::group/command`
- [x] App resolver — `.group/command` (app-local commands)
- [x] User resolver — `~group/command` (user-local commands)

---

## Command execution

- [x] Python command runner
- [x] YAML command runner — `CoreYamlCommandRunner` — full implementation: bash/python runners, options, decorators, variable substitution, internal command calls
- [ ] Sub-command execution — `kernel.run_command(command, args)` calls another command internally and returns its response; v5: `kernel.run_command()` + `kernel.previous_response`
- [ ] Click argument conversion — `click_args_convert_dict_to_args()` / `click_args_convert_to_dict()` / `click_args_convert_dict_to_long_names_dict()` — bridge between Python dicts and CLI args for sub-commands
- [x] Attach system — `@attach(position, command/wrapper, pass_args)` — string ET référence directe à CommandMethodWrapper

---

## YAML command definition system

> V6 — implémenté. Architecture finale ci-dessous pour référence.

### Format v6 (décisions de design)

```yaml
description: "Command description"       # remplace 'help' de v5
decorators:                              # remplace 'properties' de v5 — symétrique avec @decorators Python
  - name: sudo                           # équivaut à @as_sudo()
  - name: alias                          # équivaut à @alias("hi")
    args: hi
  - name: attach                         # équivaut à @attach(position="after", command="...")
    args:
      position: after
      command: demo::ping/pong
      pass_args: true
options:                                 # options CLI — inchangé vs v5
  - name: type
    short: t
    type: str
    required: true
    help: "Response type"
scripts:
  - runner: bash                         # remplace 'type' de v5 — extensible via addons
    script: echo "hello"
  - runner: python
    script: print("world")
  - runner: bash
    file: path/to/script.sh
  - command: demo::ping/pong            # appel interne — inchangé vs v5
    args:
      type: dict
```

### Principes de design

- **`type` top-level supprimé** — le type de resolver est inféré depuis le resolver qui a trouvé le fichier (comme pour `.py`)
- **`decorators` unifié** — tout décorateur Python a son équivalent YAML ; les addons peuvent en enregistrer de nouveaux
- **`runner` au lieu de `type` script** — extensible : `bash`/`python` built-in, d'autres fournis par addons (`rust`, `node`, `docker`…)
- **`ScriptRunnerRegistry`** sur le kernel — les addons y enregistrent leurs runners
- **Symétrie stricte** — un YAML et un Python doivent produire le même `CommandMethodWrapper` (mêmes champs registry : `description`, `alias`, `attachments`, `sudo`…)

### Ce qui est reporté (dépendances non migrées)

- `context: container` → Docker addon non migré
- `app_should_run` → AppResolver non migré
- `webhook` → addon-app concern

### Plan d'implémentation

- [x] Detection `.yml` dans `AddonCommandResolver.build_registry_data()`
- [x] Parser YAML → extraire `description`, `options`, `decorators`, `scripts`
- [x] `decorators` → appliquer sur `CommandMethodWrapper` (même logique que les décorateurs Python)
- [x] `options` → `Option` objects avec type, required, default, short
- [x] `scripts` → exécuter séquentiellement, retourner `ResponseCollectionResponse`
- [x] Built-in runners : `bash` (inline + file), `python` (inline + file)
- [x] Variables : substitution `${VAR}`, `variable: VAR_NAME` pour capturer l'output, `PATH_CURRENT` built-in
- [x] `command:` dans un script → appel interne via `kernel.execute_kernel_command()`
- [x] `ScriptRunnerRegistry` — `kernel.script_runner_registry.register(MyRunner())` sur le kernel

---

## Registry

The registry is a central artifact — built once, persisted to disk (YAML via `KernelRegistryFile`), consumed by many features. Commands should read it, not rebuild it.

v5 reference: `registry/build` + `KernelRegistryFileStructure` + `AddonCommandResolver` + `src/helper/registry.py`

### Infrastructure

- [x] `default::registry/build` — scans all addons, persists to `{workdir}/.wex/tmp/registry.yml`
- [x] Registry built at kernel startup if file is empty (`_init_registry()`)
- [x] `KernelRegistry.hydrate()` loads full resolver data from file
- [x] `KernelRegistry.get_addon_commands()` accessor
- [x] `test::run/all` reads registry from `kernel.get_configuration_registry()`

### Command schema — fields missing in v6

Each command entry in v5 has: `command`, `file`, `test`, `alias`, `attachments`, `description`, `properties`.
v6 currently only has: `command`, `path`, `test`.

- [x] `description` — extract `help=` from `@command` decorator at build time
- [x] `alias` — list of aliases registered via `@alias`
- [x] `attachments` — `{before: [...], after: [...]}` from `@attach`
- [x] `sudo` — extrait du `@as_sudo`
- [ ] `properties` — custom decorator metadata (`app_dir_required`, `ai_tool`, `app_webhook`…)

### Addon entry — field missing in v6

- [ ] `name` field per addon entry (v5: `{name: str, commands: {...}}`)

### Alias resolution — entirely missing in v6

- [x] `resolver.resolve_alias(command)` — linear lookup: if input matches any `alias[]`, return full command name
- [x] Called before pattern matching in `resolver.supports()` ← **blocks `@alias` end-to-end**

### Service resolver registry

- [x] `ServiceCommandResolver.build_registry_data()` — utilise `_scan_commands_dir` (yml + py, attachments, sudo)
- [ ] Service config loading from `service.yml` — feature avancée, non bloquante
- [ ] Service inheritance resolution (`config.extends` → recursive merge) — feature avancée, non bloquante

### Helper functions

- [x] `get_all_commands()`, `get_all_command_names()`, `get_sudo_commands()`, `find_command()`, `suggest()` sur `KernelRegistry`
- [ ] `registry_find_commands_by_function_property(kernel, prop)` — filter by custom property decorator
- [ ] `resolver.get_commands_registry()` — commands dict for active resolver

### registry/build options — missing in v6

- [ ] `--test` flag — include `@test_command` entries in registry
- [ ] `--write` flag — dry-run mode (build without saving)
- [ ] `@alias("rebuild")` — short alias for the command

### Autocomplete — missing in v6

- [ ] `resolver.autocomplete_suggest(cursor, search_split)` — cursor-aware suggestions per resolver
- [ ] `autocomplete/suggest` command — aggregate suggestions across all resolvers
- [ ] AddonCommandResolver: cursor=0 → addon names/aliases, cursor=1 → groups, cursor=2 → commands, cursor≥3 → args
- [ ] ServiceCommandResolver: cursor=0 → `@`, cursor=1 → service names, cursor=2-3 → commands

---

## Structured output / response system

> v6 has a good log/print vs return value separation via `ExecutionContext` — but structured types are missing.

- [x] Log/print separation — `ExecutionContext.io` handles display; return values separate
- [x] Render modes — `terminal` / `json` / `none` (output handlers in wex-core)
- [ ] Response type wrapping — auto-convert return values: `dict` → `DictResponse`, `list` → `ListResponse`, `None` → `NullResponse`, callable → `FunctionResponse`, etc.
- [ ] Structured response types — `TableResponse`, `KeyValueResponse`, `DictResponse`, `ListResponse`
- [ ] `AbortResponse` — signals `--help` or command abort
- [ ] `ResponseCollectionResponse` — multiple responses in one
- [ ] JSON render mode per response — `render_mode_json_wrap_data()`

---

## Queued collection (multi-step interactive execution)

> **SKIP** — v6 uses subprocesses instead. No use case for in-process multi-step state machine.

## Task ID & propagation

> **SKIP** — v6 uses subprocesses instead. Post-exec queue has no use case.

---

## Click integration

- [x] `@command` / `@option` decorators
- [x] `--quiet`, `-v`, `-vv`, `-vvv`, `--output_format`, `--output_target`
- [ ] Auto-injected options on every command: `--fast-mode`, `--command-request-step`, `--kernel-task-id`, `--parent-task-id`, `--log-indent`, `--log-length`, `--render-mode`
- [ ] `--help` → `AbortResponse(reason="INFO_COMMAND")` (caught Click exit)
- [ ] `ctx.obj = kernel` — kernel passed via `@click.pass_obj`

---

## Decorators

- [x] `@command`, `@option`
- [x] `@middleware` (new in v6)
- [ ] `@alias` — registered in registry at build time; resolved before command execution
- [ ] `@attach`
- [ ] `@as_sudo` — triggers `os.execvp("sudo", ...)` before execution
- [ ] `@no_log` — exclude command from log files
- [ ] `@verbosity` — force verbosity level for this command only
- [ ] `@test_command`

---

## Logging & event tracking

- [ ] `Logger` — JSON log per task: command, trace, dateStart, duration, errors, events, parent/child task IDs
- [ ] `append_error(level)` — FATAL or ERROR
- [ ] `append_event(name, data)` — custom events (e.g. `EVENT_SWITCH_SUDO`)
- [ ] IOManager log frame — scrolling display with `log_length` / `log_indent` + ANSI cursor control

---

## Addon hooks

- [ ] `kernel.hook_addons(name, args)` — calls `hook_{name}()` on all addon managers
- [ ] Available hooks: `render_request_pre`, `render_request_post`

---

## Environment & config

- [ ] `.env` loading — `dotenv_values()` → `kernel.env_values`; access via `kernel.env(key, default, required)`
- [ ] CommandRequest storage — `request.storage: dict` — per-request data store for sharing state across rendering steps

---

## CLI / shell

- [~] Task ID generation in `bin/wex` — **SKIP** : no post-exec queue in v6
- [~] Post-exec loop in bash — **SKIP** : no post-exec queue in v6
- [ ] Autocomplete — depends on registry
- [ ] Internal command → shell conversion — `internal_command_to_shell()`: `["bash", cli_path, command, ...args, "--kernel-task-id", ...]`
- [ ] Process control — `process_kill_by_port()`, `process_kill_by_command()`, `process_get_all_by_port()`
