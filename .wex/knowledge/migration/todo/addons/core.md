# Addon: core

## v5 reference

`wex-5/addons/core/`

## Already covered

- [x] `version/increment` — `default::version/increment` in wex-core
- [x] `logo/show` — display wex logo
- [x] `check/hi` — health check (wex hi)
- [x] `command/create` — generate new command scaffold
- [x] `version/get` — SKIP: app version is already exposed via `app::info/show`
- [x] `registry/build` — scan all addons, persist registry to disk ← unblocks autocomplete, alias, info/show, test runner
- [x] `service/resolve` — SKIP: absorbed by recursive resolution in `app::service/install`
- [x] `logs/show` — display logs
- [x] `logs/rotate` — rotate log files (SKIP)

## Still missing for functional parity

- [ ] `autocomplete/suggest` — shell completion suggestions
- [ ] `configure/all` — configure system
- [ ] `core/install` — install wex
- [ ] `core/uninstall` — uninstall wex
- [ ] `core/cleanup` — cleanup wex
- [ ] `install/update` — update installation

## Out of scope here

- [~] `test/run`
- [~] `test/create`
- [~] `test/cleanup`

## New in v6 (no v5 equivalent)

- `test::yaml/` — YAML-based test runner

## v6 target

- `PACKAGES/PYTHON/wex/wex-core` addons
