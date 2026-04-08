# Addon: core

## v5 reference

`wex-5/addons/core/`

## Commands

- [x] `version/increment` — `default::version/increment` in wex-core
- [x] `test/run` — `test::run/all` in wex-core
- [ ] `logo/show` — display wex logo
- [x] `check/hi` — health check (wex hi)
- [ ] `command/create` — generate new command scaffold
- [ ] `test/create` — create new test
- [ ] `test/cleanup` — clean test artifacts
- [ ] `version/get` — get wex version
- [ ] `version/new` — create new version
- [ ] `version/new_commit` — version commit
- [ ] `version/new_write` — write version file
- [ ] `autocomplete/suggest` — shell completion suggestions ← depends on registry
- [x] `registry/build` — scan all addons, persist registry to disk ← unblocks autocomplete, alias, info/show, test runner
- [ ] `configure/all` — configure system
- [ ] `service/resolve` — resolve service
- [ ] `core/install` — install wex
- [ ] `core/uninstall` — uninstall wex
- [ ] `core/cleanup` — cleanup wex
- [ ] `install/update` — update installation
- [ ] `logs/show` — display logs
- [ ] `logs/rotate` — rotate log files

## New in v6 (no v5 equivalent)

- `test::yaml/` — YAML-based test runner

## v6 target

- `PACKAGES/PYTHON/wex/wex-core` addons
