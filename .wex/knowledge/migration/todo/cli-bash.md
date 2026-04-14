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

- [x] `install` — symlink + autocomplete handler + registry build intégrés directement en bash (plus de dépendance Python pour l'install)
- [x] `install-dev` — development installation
- [ ] `uninstall`
- [x] `_init.sh` — shell init (set error flags)
- [x] `_init_sudo.sh` — sudo init

## Shell integration

- [x] `autocomplete` — fonctionnel, permissions fixées (+x)
- [x] `autocomplete-handler` — fonctionnel, sourcé depuis `/etc/bash_completion.d/wex`
- [x] `default::autocomplete/suggest` — stub vide (retourne []), suggestions à implémenter
- [~] `terminal-handler` — absent de `bin/`, non nécessaire en v6 (symlink suffit)
- [~] `wex-coverage` — hors scope publication

## v6 target

- `wex-6/bin/` — entry point already exists, to be completed
