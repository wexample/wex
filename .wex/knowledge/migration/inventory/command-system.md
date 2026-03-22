# Command System

## v5 reference

- Kernel: `wex-5/src/utils/kernel.py`
- Addon resolver: `wex-5/src/core/command/resolver/AddonCommandResolver.py`
- Decorators: `@command`, `@test_command`, `@alias`, `@attach`, `@as_sudo`, `@no_log`, `@verbosity`
- Registry-based command management with dynamic addon loading

## v6 architecture

- Entry point: `__main__.py` → `exec_argv()`
- Resolvers initialized in `AbstractKernel._init_resolvers()`
- Addon command format: `addon::group/command` (e.g. `default::info/show`)
- Addon locations: `{package}/wexample_wex_core/addons/`

## Status

### Resolvers

- [x] Addon resolver — `AddonCommandResolver` exists in wex-core
- [x] Service resolver — `ServiceCommandResolver` exists in wex-core
- [ ] User resolver — to evaluate

### Runners

- [x] Python runner — `CorePythonCommandRunner` implemented
- [x] YAML runner — `CoreYamlCommandRunner` implemented
- [ ] Execution pathway — not fully tested end-to-end

### Command request lifecycle

- [x] `CommandRequest` — exists in wex-core
- [x] `CommandMethodWrapper` — wraps decorated functions
- [x] `ExtendedCommand` — runs commands with `ExecutionContext`
- [x] `ExecutionContext` — passed to every command (kernel, request, io, middleware, progress) ← **new in v6**

### Response system

> ⚠️ Paradigm change: v5 used response objects (`DefaultResponse`, `TableResponse`…).
> v6 replaces this with `ExecutionContext` + pluggable output handlers.
> See `response-system.md` for migration status of individual response types.
