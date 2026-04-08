# Migration plan: Docker lifecycle (`wex-addon-app`)

> Suivi ciblé du cycle de vie Docker/app en v6.
> L'inventaire général de l'addon vit maintenant dans `addons/app.md`.

## Référence et cadre de test

- App de référence: `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/NETWORK/local/network/`
- App v5 avec services: `symfony`, `mysql`, `phpmyadmin`
- Validation helper/proxy faite aussi avec `/var/www/local/wex-proxy`
- Si une app v5 ne passe pas en v6, la migration est portée via `migration/run`

## Architecture retenue

- Les commandes Docker vivent dans `wex-addon-app/src/wexample_wex_addon_app/commands/`
- Le cas Docker repose sur `AppMiddleware` + `AppWorkdir`
- `ServiceCommandResolver` injecte `service: AppService`
- Le service `default` centralise les options Compose communes via `extends`
- Le flux helper/proxy repose désormais sur `app/init` + `service/install`

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
- [x] `config/get`
- [x] `config/set`

### Containers / services / helper

- [x] `container/list`
- [x] `service/install`
- [x] `helper/start`
- [x] `helper/stop`
- [x] `hosts/update`

### Base de données

- [x] `db/exec`
- [x] `db/go`
- [x] `db/dump`
- [x] `db/restore`
- [x] `docker.db.main` remplace `docker.main_db_container`

### Environnement / migration

- [x] `env/choose`
- [x] `env/set`
- [x] `env/get`
- [x] `migration/run` et commandes liées

## Validé récemment

- Le helper proxy est bien créé dans `/var/www/{env}/wex-proxy`
- Les samples proxy sont bien copiés dans l'app helper
- `config/write` génère un `docker-compose.runtime.yml` valide pour le helper
- Le container proxy démarre correctement via le flux v6 restauré

## À surveiller

- Le cycle helper/proxy est réparé; les prochains incidents probables sur `app/start`
  viendront plutôt du compose de l'app métier elle-même que du helper.
- Les webhook restent hors de ce périmètre.
