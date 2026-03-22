# Core Mechanisms

You are reading this file because you need to know what foundational mechanisms must be in place before migrating individual commands.

These are prerequisites — without them, migrated commands are incomplete or untestable.

## Command resolution (all resolver types)

- [x] Addon resolver — `addon::group/command`
- [x] Service resolver — `@service::group/command`
- [ ] App resolver — `.group/command` (app-local commands) — `AppCommandResolver` in v5
- [ ] User resolver — `~group/command` (user-local commands) — `UserCommandResolver` in v5

## Command execution

- [x] Python command runner
- [ ] YAML command runner — `CoreYamlCommandRunner` exists, needs validation
- [ ] Attach system — pre/post command hooks (`@attach("before", ...)`, `@attach("after", ...)`)

## Registry

- [ ] Central command registry — lists all available commands across all addons
- [ ] Used by: autocomplete, test runner (`test::run/all`), introspection (`default::info/show`)
- [ ] v5 reference: `registry/build` command + `KernelRegistryFileStructure`

## Structured output / response

- [ ] Define v6 pattern for structured output (table, list, dict, key-value…)
- [ ] Current state: only plain text via `ExecutionContext.io` — not enough for most commands
- [ ] v5 reference: `src/core/response/`

## Decorators (blocking for many commands)

- [ ] `@alias` — command aliasing
- [ ] `@attach` — pre/post hooks
- [ ] `@as_sudo` — privilege escalation
- [ ] `@no_log` — suppress logging
- [ ] `@verbosity` — verbosity requirement
- [ ] `@test_command` — mark as test-only

## CLI / shell

- [ ] Task ID generation in `bin/wex`
- [ ] Post-exec command loop (bash-side)
- [ ] Autocomplete — depends on registry
