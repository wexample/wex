# Addon: app

> ⚠️ Paradigm change: `wex-addon-app` in v6 is a **dev workflow tool** (package management, versioning, suites).
> The v5 app addon was a **Docker app lifecycle manager** (start, stop, webhook, db…).
> These are largely separate concerns — v6 app commands are new, v5 commands need new homes.

## v5 reference

`wex-5/addons/app/`
Key classes: `AppAddonManager.py`, `WebhookHttpRequestHandler.py`

## Already in v6 (new commands, no v5 equivalent)

- [x] `app::dependencies/check` — validate dependencies
- [x] `app::dependencies/publish` — publish dependencies
- [x] `app::file_state/rectify` — file state rectification
- [x] `app::libraries/sync` — sync shared libraries
- [x] `app::package/bump` — bump package versions
- [x] `app::package/publish` — publish packages
- [x] `app::package/publish_bumped` — publish bumped packages
- [x] `app::suite/publish` — publish entire suite
- [x] `app::suite/exec_command` — execute command across suite
- [x] `app::suite/exec_shell` — execute shell across suite
- [x] `app::suite/packages` — list suite packages
- [x] `app::test/run` — run suite tests
- [x] `app::version/propagate` — propagate versions
- [x] `app::registry/write` — write registry
- [x] `app::setup/install` — setup install
- [x] `app::info/show` — show app info

## v5 commands to migrate (Docker app lifecycle)

### app/
- [ ] `app/init` — initialize app
- [ ] `app/start` — start app (Docker)
- [ ] `app/stop` — stop app (Docker)
- [ ] `app/restart`
- [ ] `app/serve`
- [ ] `app/exec` — execute in app context
- [ ] `app/perms` — fix permissions
- [ ] `app/started` — check if app is started
- [ ] `app/go` — navigate to app directory

### branch/ env/ config/ container/ db/ domain/ hosts/ location/ migration/ notification/
- [ ] `branch/env`, `branch/ip`
- [ ] `config/get`, `config/set`, `config/bind_files`, `config/write`
- [ ] `container/list`
- [ ] `db/dump`, `db/exec`, `db/go`, `db/restore`
- [ ] `domain/list`
- [ ] `env/get`, `env/set`, `env/choose`
- [ ] `hosts/update`
- [ ] `info/update`
- [ ] `location/find`
- [ ] `logs/follow`
- [ ] `migration/migrate`
- [ ] `notification/notify`

### remote/
- [ ] `remote/available`, `remote/exec`, `remote/go`, `remote/push`, `remote/push_receive`

### service/ services/ hook/ helper/
- [ ] `service/install`, `service/used`
- [ ] `services/exec`
- [ ] `hook/exec`
- [ ] `helper/start`, `helper/stop`

### code/
- [ ] `code/check`, `code/format`

### webhook/
- [ ] `webhook/exec`, `webhook/listen`, `webhook/status`, `webhook/status_process`, `webhook/stop`

### version/
- [ ] `version/get`, `version/new`, `version/new_commit`, `version/new_write`

## v6 target

- Docker lifecycle → `PACKAGES/PYTHON/wex/wex-addon-app` (new commands to add)
- Webhook → `WebhookHttpRequestHandler` to migrate/rewrite
