# Migration plan: Docker lifecycle (`wex-addon-app`)

> Suivi de la migration v5→v6 des commandes Docker/app.
> Les commandes de workflow hors cycle de vie Docker ne sont pas couvertes ici.

## Référence et cadre de test

- App de référence: `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/NETWORK/local/network/`
- App v5 avec services: `symfony`, `mysql`, `phpmyadmin`
- Config notable: `wex.version: 5.0.51`, `require_proxy: true`, `main_db_container: mysql`
- Validation faite en pointant le symlink `app-manager` v6 vers `wex-addon-app/.../resources/app-manager.sh`
- Si une app v5 ne passe pas en v6, la migration est portée via `migration/run` sur `network`

## Architecture retenue

- Les commandes Docker vivent dans `wex-addon-app/src/wexample_wex_addon_app/commands/`
- Le cas Docker est couvert par `AppMiddleware` + `AppWorkdir`
- `DockerAppMiddleware` a été abandonné avant implémentation
- `ServiceCommandResolver` a été déplacé dans `wex-addon-app` et injecte `service: AppService`
- Un service `default` centralise les options Compose communes injectées via `extends`

## Fait

### Lifecycle app

- [x] `app/started`
- [x] `app/exec`
- [x] `app/go`
- [x] `app/stop`
- [x] `app/restart`
- [x] `app/start`
- [x] `app/perms`

### Config app

- [x] `config/write`
  - Génère `config.runtime.yml`, `docker.env`, `docker-compose.runtime.yml`
  - Reste à compléter: `domains`, `domain_tld`, `user/group/uid/gid`
- [x] `config/get`
- [x] `config/set`

### Base de données

- [x] `@mysql::config/runtime`
- [x] `@mysql::service/ready`
- [x] `db/exec`
- [x] `db/go`
- [x] `db/dump`
- [x] `db/restore`

### Environnement / migration

- [x] `env/choose`
- [x] `env/set`
- [x] `env/get`
- [x] `migration/run` et commandes liées
- [x] `migration_6_0_0.py`
  - Migration de `docker.main_db_container` vers `docker.db.main`
  - Vérifie la présence de `global.type: app`

### Support app/start

- [x] `_checkup`
- [x] `_proxy`
- [x] `_update_hosts`
- [x] `_complete`
- [x] `helper/start`
- [x] `hosts/update`

## Reste à faire

### Commandes locales manquantes

- [ ] `container/list`
- [ ] `domain/list`
- [ ] `logs/follow`
- [ ] Finaliser `config/write` pour `domains`, `domain_tld`, `user/group/uid/gid`

### Commandes distantes

- [ ] `remote/exec`
- [ ] `remote/push`
- [ ] `remote/go`
- [ ] `remote/available`
- [ ] `remote/push_receive`

## Hors scope / faible priorité

- `app/init`
- `webhook/*`
- `service/install`, `service/used`
- `branch/env`, `branch/ip`
- `notification/notify`, `info/update`
