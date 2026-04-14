# Decorators

## v5 reference

`wex-5/src/decorator/`

## Decorators

- [x] `@command(help="...")` — exists in `wex-core/decorator/command.py`
- [x] `@option(...)` — exists in `wex-core/decorator/option.py`
- [x] `@alias("name")` — `wex-core/decorator/alias.py`
- [x] `@attach(position, command, ...)` — `wex-core/decorator/attach.py` (before/after hooks, string + wrapper ref)
- [x] `@as_sudo()` — `wex-core/decorator/as_sudo.py` — sets `wrapper.sudo = True`; kernel re-exec via `os.execvp("sudo", ...)` si non-root
- [~] `@no_log()` — **SKIP** : redondant avec `--quiet` / `output_target=none`
- [~] `@verbosity(level)` — **SKIP** : faisable directement via `context.kernel.io`
- [~] `@test_command()` — **SKIP** : auto-détecté par convention de chemin dans `build_registry_data`

## New in v6

- [x] `@middleware` — exists in `wex-core/decorator/middleware.py`

## v6 target

- `wex-core/decorator/`
