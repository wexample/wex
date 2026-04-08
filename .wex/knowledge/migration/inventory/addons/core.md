# Addon: core

## v5 reference

`wex-5/addons/core/`

## Commands

- [x] `version/increment` — `default::version/increment` in wex-core
- [x] `test/run` — `test::run/all` in wex-core
- [x] `logo/show` — display wex logo
- [x] `check/hi` — health check (wex hi)
- [ ] `command/create` — generate new command scaffold
- [ ] `test/create` — create new test
- [ ] `test/cleanup` — clean test artifacts
- [x] `version/get` — SKIP: app version is already exposed via `app::info/show`
- [ ] `autocomplete/suggest` — shell completion suggestions ← depends on registry
- [x] `registry/build` — scan all addons, persist registry to disk ← unblocks autocomplete, alias, info/show, test runner
- [ ] `configure/all` — configure system
- [x] `service/resolve` — SKIP: absorbed by recursive resolution in `app::service/install`
- [ ] `core/install` — install wex
- [ ] `core/uninstall` — uninstall wex
- [ ] `core/cleanup` — cleanup wex
- [ ] `install/update` — update installation
- [x] `logs/show` — display logs
- [x] `logs/rotate` — rotate log files (SKIP)

## New in v6 (no v5 equivalent)

- `test::yaml/` — YAML-based test runner

## v6 target

- `PACKAGES/PYTHON/wex/wex-core` addons
