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

- [ ] Central command registry — lists all available commands across all addons
- [ ] Used by: autocomplete, `test::run/all`, `default::info/show`
- [ ] v5 reference: `registry/build` + `KernelRegistryFileStructure`

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
- [ ] `@alias`
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
