# CLI / Bash

## v5 reference

`wex-5/cli/`

## Entry points

- [x] `wex` — main bash entry point
  - [x] Load `.env`
  - [x] Generate request ID (`YYYYMMDD-HHMMSS-nanoseconds-PID`)
  - [x] Invoke Python kernel with `--force-request-id`
  - [ ] Execute post-exec commands loop — SKIP in v6, no post-exec queue
  - [x] Handle interruption cleanup
- [ ] `wex-wrapper` — setuptools / system wrapper not present in `bin/`

## Install scripts

- [ ] `install` — script exists, but still depends on non-migrated `core::core/install`
- [x] `install-dev` — development installation
- [ ] `uninstall`
- [x] `_init.sh` — shell init (set error flags)
- [x] `_init_sudo.sh` — sudo init

## Shell integration

- [ ] `autocomplete` — script exists, but backend `default::autocomplete/suggest` is not runnable yet
- [ ] `autocomplete-handler` — script exists, but depends on incomplete autocomplete backend
- [ ] `terminal-handler` — not present in `bin/`
- [ ] `wex-coverage` — not present in `bin/`

## v6 target

- `wex-6/bin/` — entry point already exists, to be completed
