# Addon: app

> En v6, `wex-addon-app` couvre à la fois le workflow de dev et le cycle de vie Docker principal.
> Le chantier helper/proxy v5 -> v6 est considéré comme migré.

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

## Fermé ou absorbé

- [x] `config/bind_files` SKIP
- [x] `location/find`
- [x] `hook/exec` SKIP
- [x] `version/get` SKIP replace par info/show

## Reste à migrer

### Publication / versioning app

- [x] `version/new` — absorbé par `app::package/bump` + `app::app/publish`
- [x] `version/new_commit` — absorbé par `app::package/commit_and_push` + `app::app/publish`
- [x] `version/new_write` — absorbé par `app::file_state/rectify` + `app::app/publish`
- [x] `app::app/publish` — orchestrateur de publication d'application validé en réel

### À clarifier / faible priorité

- [ ] `branch/env`
- [ ] `branch/ip`
- [x] `notification/notify` SKIP for now — lightweight v6 proof of concept already exists via `@n8n::notification/notify`, but the final product shape is not stable enough to justify a generic app-level migration yet
- [x] `info/update` SKIP

### Webhooks et commandes distantes

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
- `notification/notify` n'est pas traité comme une dette bloquante : le besoin existe peut-être, mais le bon design sera probablement redéfini plus tard autour des workflows distants / déploiement / automation.
- Le sujet `version/new*` n'est plus traité comme une migration 1:1 ; il est désormais requalifié en pipeline `app::app/publish`.
- Le premier `app::app/publish` successful a été validé en local en fin de journée.
- La roadmap détaillée associée est archivée dans `../../done/addons/app-publication-lifecycle.md`.
- Le détail du périmètre Docker déjà migré est archivé dans `../../done/addons/app-docker-lifecycle.md`.
