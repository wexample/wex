# Core Mechanisms

You are reading this file because you need to know what foundational mechanisms must be in place before migrating individual commands.

These are prerequisites — without them, migrated commands are incomplete or untestable.

---

## Command resolution

- [x] Addon resolver — `addon::group/command`
- [x] Service resolver — `@service::group/command`
- [ ] App resolver — `.group/command` (app-local commands)
- [ ] User resolver — `~group/command` (user-local commands)

---

## Command execution

- [x] Python command runner
- [ ] YAML command runner — `CoreYamlCommandRunner` exists, needs end-to-end validation
- [ ] Sub-command execution — `kernel.run_command(command, args)` calls another command internally and returns its response; v5: `kernel.run_command()` + `kernel.previous_response`
- [ ] Click argument conversion — `click_args_convert_dict_to_args()` / `click_args_convert_to_dict()` / `click_args_convert_dict_to_long_names_dict()` — bridge between Python dicts and CLI args for sub-commands
- [ ] Attach system — pre/post command hooks (`@attach("before"/"after", cmd, pass_args, pass_previous)`) — attached commands run in fast mode

---

## YAML command definition system

- [ ] Validate `CoreYamlCommandRunner` supports full v5 YAML spec:
  - `scripts[]` — steps: `command:` (internal), `script:` (bash inline), `file:` (bash file)
  - `options[]` — Click options: name, short, type, default, help, is_flag, required
  - `properties[]` — decorator list
  - Variables in scripts: `PATH_CORE`, `PATH_CURRENT`, all options (uppercase)

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

- [x] `description` — extract `help=` from `@command` decorator at build time ← **blocks `info/show`**
- [x] `alias` — list of aliases registered via `@alias` ← **blocks alias resolution**
- [ ] `attachments` — `{before: [...], after: [...]}` from `@attach` ← blocks `@attach`
- [ ] `properties` — custom decorator metadata (`app_dir_required`, `ai_tool`, `app_webhook`…)

### Addon entry — field missing in v6

- [ ] `name` field per addon entry (v5: `{name: str, commands: {...}}`)

### Alias resolution — entirely missing in v6

- [x] `resolver.resolve_alias(command)` — linear lookup: if input matches any `alias[]`, return full command name
- [x] Called before pattern matching in `resolver.supports()` ← **blocks `@alias` end-to-end**

### Service resolver registry — entirely missing in v6

v5 stores per service: `addon`, `name`, `dir`, `config` (with `extends`), `commands`.

- [ ] `ServiceCommandResolver.build_registry_data()` — scan `addons/{addon}/services/`
- [ ] Service config loading from `service.yml`
- [ ] Service inheritance resolution (`config.extends` → recursive merge with parent)

### Helper functions — missing in v6

- [ ] `registry_get_all_commands(kernel)` — all commands across all resolvers (flat)
- [ ] `registry_get_all_commands_from_registry_part(part)` — commands from one resolver
- [ ] `registry_find_commands_by_function_property(kernel, prop)` — filter by custom property
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

> v5's most sophisticated mechanism — enables interactive multi-step workflows.

- [ ] `QueuedCollectionResponse` — sequential steps (values, callables, or responses)
- [ ] Step path manager — tracks hierarchy `[0, 2, 1]` for nested steps
- [ ] Default mode — stores step results in task files, one step per kernel invocation
- [ ] Fast mode (`--fast-mode`) — all steps in memory, re-executes immediately; used for `@attach` and perf-critical scripts
- [ ] `storable_data()` — controls what data passes between steps
- [ ] Stop signals — `QueuedCollectionStopResponse`, `QueuedCollectionStopCurrentStepResponse`

---

## Task ID & propagation

- [ ] Task ID as first `sys.argv` — identifies execution instance
- [ ] `--kernel-task-id` — redirect to another task context
- [ ] `--parent-task-id` — tracks parent kernel
- [ ] Task files — `{task_id}.json`, `{task_id}.response`, `{task_id}.post-exec` in `{kernel.path['task']}/`
- [ ] Post-exec queue — shell commands deferred to after kernel success; written to `{task_id}.post-exec`; supports async via `nohup` + `&`

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

- [ ] Task ID generation in `bin/wex` (format: `YYYYMMDD-HHMMSS-nanoseconds-PID`)
- [ ] Post-exec loop in bash — reads `{task_id}.post-exec` after kernel exits
- [ ] Autocomplete — depends on registry
- [ ] Internal command → shell conversion — `internal_command_to_shell()`: `["bash", cli_path, command, ...args, "--kernel-task-id", ...]`
- [ ] Process control — `process_kill_by_port()`, `process_kill_by_command()`, `process_get_all_by_port()`
