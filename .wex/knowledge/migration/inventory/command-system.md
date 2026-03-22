# Command System

You are reading this file because you need to understand the command system migration status.

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

- [x] Service resolver — functional
- [ ] Addon resolver — `AddonCommandResolver` to create
  - [ ] Parse `addon::group/command` format
  - [ ] Register addon directories
  - [ ] Resolve Python file path
  - [ ] Convert path to method name
  - [ ] Test with `default::info/show`
- [ ] User resolver — to evaluate

### Runners

- [x] Python runner — implemented
- [ ] Execution pathway — not fully tested
  - [ ] Verify Python script path resolution
  - [ ] Validate module execution mechanism

### Response system

- [ ] Connect command responses to prompt system
- [ ] Restore sophisticated response handling from v5
