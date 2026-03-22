# CLI / Bash

## v5 reference

`wex-5/cli/`

## Entry points

- [ ] `wex` — main bash entry point
  - [ ] Load `.env`
  - [ ] Generate task ID (`YYYYMMDD-HHMMSS-nanoseconds-PID`)
  - [ ] Invoke Python kernel with task ID
  - [ ] Execute post-exec commands loop
  - [ ] Handle interruption cleanup
- [ ] `wex-wrapper` — setuptools entry point wrapper

## Install scripts

- [ ] `install` — check Python/pip/venv, create venv, install deps, update bashrc
- [ ] `install-dev` — development installation
- [ ] `uninstall`
- [ ] `_init.sh` — shell init (set error flags)
- [ ] `_init_sudo.sh` — sudo init

## Shell integration

- [ ] `autocomplete` — bash completion script
- [ ] `autocomplete-handler` — completion handler
- [ ] `terminal-handler` — terminal integration
- [ ] `wex-coverage` — coverage testing wrapper

## v6 target

- `wex-6/bin/` — entry point already exists, to be completed
