# Addon: app

> En v6, `wex-addon-app` couvre surtout le workflow de dev (packages, suites, versions).
> Le cycle de vie Docker hérité de v5 est suivi séparément dans `app-docker-lifecycle.md`.

## Référence v5

- Source: `wex-5/addons/app/`
- Classes notables: `AppAddonManager.py`, `WebhookHttpRequestHandler.py`

## Déjà présent en v6

- [x] `app::dependencies/check`
- [x] `app::dependencies/publish`
- [x] `app::file_state/rectify`
- [x] `app::libraries/sync`
- [x] `app::package/bump`
- [x] `app::package/publish`
- [x] `app::package/publish_bumped`
- [x] `app::suite/publish`
- [x] `app::suite/exec_command`
- [x] `app::suite/exec_shell`
- [x] `app::suite/packages`
- [x] `app::test/run`
- [x] `app::version/propagate`
- [x] `app::registry/write`
- [x] `app::setup/install`
- [x] `app::info/show`

## Migration v5→v6 restant à suivre ici

### Non détaillé ici car suivi dans la roadmap Docker dédiée

- Cycle de vie Docker `app/*`
- `config/get`, `config/set`, `config/write`
- `container/list`
- `db/*`
- `domain/list`
- `env/*`
- `hosts/update`
- `logs/follow`
- `migration/*`
- `remote/*`
- `helper/start`

### À traiter hors roadmap Docker

- [ ] `config/bind_files`
- [ ] `location/find`
- [ ] `services/exec`
- [ ] `hook/exec`
- [ ] `helper/stop`
- [ ] `code/check`
- [ ] `code/format`
- [ ] `version/get`
- [ ] `version/new`
- [ ] `version/new_commit`
- [ ] `version/new_write`

### Faible priorité / à clarifier

- [ ] `webhook/exec`
- [ ] `webhook/listen`
- [ ] `webhook/status`
- [ ] `webhook/status_process`
- [ ] `webhook/stop`
- [ ] `service/install`
- [ ] `service/used`
- [ ] `branch/env`
- [ ] `branch/ip`
- [ ] `notification/notify`
- [ ] `info/update`
- [ ] `app/init`

## Autres

- `app/init`
- `webhook/*`
- `service/install`, `service/used`
- `branch/env`, `branch/ip`
- `notification/notify`, `info/update`

### Commandes distantes

- [ ] `remote/exec`
- [ ] `remote/push`
- [ ] `remote/go`
- [ ] `remote/available`
- [ ] `remote/push_receive`

## Cible v6

- Workflow app: `wex-addon-app`
- Lifecycle Docker: suivi dédié dans `app-docker-lifecycle.md`
- Webhook: à migrer ou réécrire à partir de `WebhookHttpRequestHandler`

