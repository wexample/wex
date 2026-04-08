# Addon: app

> En v6, `wex-addon-app` couvre à la fois le workflow de dev et une partie du cycle de
> vie Docker. Le chantier helper/proxy v5 → v6 est désormais migré.

## Référence v5

- Source: `wex-5/addons/app/`
- Classes notables: `AppAddonManager.py`, `WebhookHttpRequestHandler.py`

## Déjà présent en v6

### Workflow packages / suites

- [x] `app::dependencies/check`
- [x] `app::dependencies/publish`
- [x] `app::file_state/rectify`
- [x] `app::libraries/sync`
- [x] `app::package/bump`
- [x] `app::package/publish`
- [x] `app::package/publish_bumped`
- [x] `app::suite/status`
- [x] `app::suite/publish`
- [x] `app::suite/exec_command`
- [x] `app::suite/exec_shell`
- [x] `app::suite/packages`
- [x] `app::test/run`
- [x] `app::version/propagate`
- [x] `app::registry/write`
- [x] `app::setup/install`
- [x] `app::info/show`

### Cycle app / Docker déjà migré

- [x] `app::app/init`
- [x] `app::app/start`
- [x] `app::app/stop`
- [x] `app::app/restart`
- [x] `app::app/started`
- [x] `app::app/go`
- [x] `app::app/exec`
- [x] `app::config/get`
- [x] `app::config/set`
- [x] `app::config/write`
- [x] `app::container/list`
- [x] `app::db/dump`
- [x] `app::db/exec`
- [x] `app::db/go`
- [x] `app::db/restore`
- [x] `app::domain/list`
- [x] `app::env/choose`
- [x] `app::env/get`
- [x] `app::env/set`
- [x] `app::helper/start`
- [x] `app::helper/stop`
- [x] `app::hosts/update`
- [x] `app::logs/follow`
- [x] `app::service/install`
- [x] `app::service/used`
- [x] `app::services/exec`

## Reste à migrer

### Priorité utile

- [x] `config/bind_files` SKIP
- [x] `location/find`
- [x] `hook/exec` SKIP
- [x] `version/get` SKIP replace par info/show

### Update lifecycle

- [ ] `version/new`
- [ ] `version/new_commit`
- [ ] `version/new_write`

### À clarifier / faible priorité

- [ ] `branch/env`
- [ ] `branch/ip`
- [ ] `notification/notify`
- [ ] `info/update`

### Commandes distantes

- [ ] `webhook/exec`
- [ ] `webhook/listen`
- [ ] `webhook/status`
- [ ] `webhook/status_process`
- [ ] `webhook/stop`
- [ ] `remote/exec`
- [ ] `remote/push`
- [ ] `remote/go`
- [ ] `remote/available`
- [ ] `remote/push_receive`

## Notes

- Le flux helper/proxy v5 a été restauré autour de `app/init` + `service/install`.
- `samples/` redevient la source de vérité des fichiers copiés lors de l'installation d'un service.
- `container/list` existe maintenant en rendu compact orienté app Wex, plus lisible que `docker ps`.
- En v5, `code/check` et `code/format` étaient des placeholders sans logique addon effective.
- Ils ne sont donc pas à migrer tels quels en v6 ; le besoin de rectification passe déjà par `app::file_state/rectify`.
- La partie webhook reste un chantier distinct si elle doit revenir en v6.
