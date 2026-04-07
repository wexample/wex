# Migration plan : Docker lifecycle (wex-addon-app)

> Fichier de suivi spécifique pour la migration des commandes Docker/app v5→v6.
> Les commandes "dev workflow" (package, suite…) sont déjà migrées — ce fichier ne couvre que le cycle de vie Docker.

---

## Contexte et contraintes

### App de test
- **App de référence** : `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/NETWORK/local/network/`
- App v5 avec services : `symfony`, `mysql`, `phpmyadmin`
- Config : `wex.version: 5.0.51`, `require_proxy: true`, `main_db_container: mysql`
- Commande v5 actuelle : `wex app/start` (fonctionne avec wex v5)

### Stratégie de test (symlink wex v6)
- Le symlink `wex-core/.wex/bin/app-manager` → `wex-addon-app/.../resources/app-manager.sh`
- Chaque commande migrée se teste via le wex v6 pointé par ce symlink
- Si une app v5 ne fonctionne pas en v6 → on crée une migration `migration/migrate` et on la fait tourner sur `network`
- Cycle : migrer commande → tester sur network → si besoin écrire migration → re-tester

### Architecture v6 retenue
- Les commandes Docker vont dans `wex-addon-app/src/wexample_wex_addon_app/commands/` (sous-dossiers `app/`, `db/`, `remote/`)
- Un nouveau middleware `DockerAppMiddleware` (ou variante de `AppMiddleware`) résout l'appdir Docker sans valider la structure "package"
- Le `AppCommandResolver` existant gère déjà les commandes locales `.wex/commands/` — pas de changement là

---

## Ordre de migration

### Phase 1 — Infrastructure middleware Docker
- [x] **`DockerAppMiddleware`** — **ABANDONNÉ** : fusionné dans `AppMiddleware` existant
  - `AppMiddleware` injecte déjà `app_workdir` sans valider la structure "package"
  - Aucun commit jamais créé — décision prise avant l'implémentation
  - `AppMiddleware` + `AppWorkdir` couvrent le cas Docker sans middleware séparé

### Phase 2 — Commandes simples (building blocks)
- [x] **`app/started`** — écrit, utilise `AppMiddleware` + `AppWorkdir`
  - Lit `config.runtime.yml` (clé `started`) + interroge `docker ps`
  - Modes : `config` / `any-container` / `full`
  - Retourne `BoolResponse`
  - **Test** : lancer sur network stoppée → `False`, network démarrée → `True`

- [x] **`app/exec`** — exécute une commande dans un container via `docker exec`
  - Options : `--container-name`, `--command`, `--user`, `--interactive`, `--sync`
  - Retourne `InteractiveShellCommandResponse` ou `ShellCommandResponse`
  - **Test** : `app exec -c "echo hello"` dans network

### Phase 3 — Stop/restart (pas de dépendance externe)
- [x] **`app/stop`** — arrête l'app
  - `docker compose stop` + `docker compose rm -f`
  - Hooks : `app/stop-pre`, `app/stop-post`
  - Met à jour `config.runtime.yml` (`started: false`)
  - **Test** : `app stop` sur network démarrée

- [x] **`app/restart`** — stop + start (squelette, délègue à stop + start)
  - Délègue à `app/stop` puis `app/start`
  - **Test** : `app restart` sur network

### Phase 3b — Services DB (wex-addon-services-db)
- [x] **`AppService`** — classe `wex-addon-app/service/app_service.py` : porte `name` + `app_workdir`
- [x] **`ServiceCommandResolver`** — déplacé de `wex-core` vers `wex-addon-app` ; injecte `service: AppService`
- [x] **`@mysql::config/runtime`** — écrit `mysql.cnf` + `db.main` dans runtime config
- [x] **`@mysql::service/ready`** — poll `mysqladmin ping`, container name résolu depuis runtime config

### Phase 4 — Commandes DB (dépendent de app/exec)
- [x] **`db/exec`** — exécute une commande SQL dans le container DB (`-s -N` pour mode scripting)
- [x] **`db/go`** — ouvre le CLI MySQL interactif (`docker exec -ti`)
- [x] **`db/dump`** — dump mysqldump → zip + symlinks `db.latest` / `db.latest.zip`
- [x] **`db/restore`** — liste dumps, prompt, unzip, destroy+restore ; `--database` pour override db.main

### Phase 5 — Start (commande la plus complexe)
- [x] **`app/start`** — fonctionnel sur network ✅
  - `docker compose up -d` avec `InteractiveShellCommandResponse` (output live)
  - `--env-file docker.env` passé au `up` (nécessaire pour les `extends` non résolus dans le runtime)
  - Stubs restants : voir Phase 7

### Décisions d'architecture prises lors de app/start

- **`APP_NAME` vs `APP_PROJECT_NAME`** : deux variables séparées dans le runtime
  - `APP_NAME=network` — nom de l'app seul, pour les service names dans compose et les `links`
  - `APP_PROJECT_NAME=network_local` — `{name}_{env}`, pour les container names et `--project-name` docker
  - Motivation : permettre de faire tourner la même app en dev et prod sur le même serveur sans conflit
- **Service composes dans `-f`** : seuls les composes sans clé `services` sont inclus (ex: proxy → `wex_net`)
  - Les service composes avec services (symfony, mysql…) sont référencés via `extends` uniquement
  - Inclure les deux causait des doublons de container names
- **Trailing slash sur `path` et `setup_path`** : cohérence avec v5 pour les concaténations dans compose (`${APP_SETUP_PATH}apache/…`)

- [x] **`app/perms`** — fix permissions via `filestate` (`Scope.PERMISSIONS` + `Scope.OWNERSHIP`)
  - `chown` + `chmod` récursif selon config `permissions.*`
  - Local env : utilise l'utilisateur courant
  - Autre env : utilise `www-data` ou config
  - Requiert sudo (`@as_sudo`)
  - **Test** : `app perms` sur network

### Phase 6 — Config app (dépendances de start)
- [x] **`config/write`** — génère `config.runtime.yml` + `docker.env` + `docker-compose.runtime.yml`
  - Testé sur network, fonctionne
  - Todos restants : domains/domain_tld, user/group/uid/gid

- [x] **`config/get`** / **`config/set`** — lecture/écriture dans `.wex/config.yml` + `--runtime` pour le runtime config

### Phase 7 — Stubs restants dans app/start
- [ ] **`_checkup`** — détecter app déjà démarrée + env absent (bloqué par `env/choose`)
- [ ] **`_proxy`** — démarrer le proxy si requis (bloqué par proxy helper)
- [ ] **`_update_hosts`** — appeler `hosts/update` (bloqué par proxy + sudo)
- ~~`_serve`~~ — supprimé, aucun usage trouvé en v5
- ~~`_first_init`~~ — supprimé, aucun usage trouvé en v5
- [x] **`_complete`** — domaines + suggestions de commandes via `AddonCommandResolver`

### Phase 8 — Migration fichier v5→v6
- [x] **`migration/run`** — commande existante (`migration/run`, `migration/status`, `migration/rollback`)
- [ ] **`migration_6_0_0.py`** — fichier de migration v5→v6
  - Clé `docker.main_db_container` → `docker.db.main`
  - Clé `global.type: app` — doit être présente
  - **Test** : faire tourner sur une app encore en v5

### Phase 9 — Commandes mineures manquantes
- ~~`app/serve`~~ — supprimé, aucun usage trouvé
- [ ] **`app/go`** — alias `app/exec --interactive` avec shell par défaut
- [ ] **`container/list`** — liste containers depuis docker-compose.runtime.yml
- [ ] **`env/choose`** / **`env/set`** / **`env/get`** — gestion environnement
- [ ] **`domain/list`** — liste les domaines configurés
- [ ] **`logs/follow`** — tail des logs docker compose
- [ ] **`config/write`** todos — domains/domain_tld, user/group/uid/gid

### Phase 10 (last) — Commandes distantes
- [ ] **`remote/exec`** — SSH vers un serveur distant
- [ ] **`remote/push`** — SCP + webhook (complexe)
- [ ] **`remote/go`**, **`remote/available`**, **`remote/push_receive`**

---

## Hors scope / non prioritaire

- `app/init` — création d'une nouvelle app (complexe, peu urgent)
- `hosts/update` — dépend du proxy
- `webhook/*` — après app/start complet
- `service/install`, `service/used`
- `branch/env`, `branch/ip`
- `notification/notify`, `info/update` (AI)

---

## App network — état actuel (ref)
```yaml
# .wex/config.yml (network)
wex:
  version: 6.0.9
global:
  type: app
  name: network
  main_service: symfony
docker:
  db.main: mysql
require_proxy: true
```
- `app/start` testé et fonctionnel sur network en wex v6 ✅
- `docker-compose.yml` migré : `${APP_NAME}` → `${APP_PROJECT_NAME}` pour les container names

---

## Définition of done pour chaque commande

1. Fichier `.py` (ou `.yml`) créé dans `wex-addon-app/commands/`
2. Testé manuellement sur l'app `network` via wex v6 (symlink)
3. Si l'app v5 ne démarre pas → migration créée et testée
4. Coché dans ce fichier
