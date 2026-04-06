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
- [x] **`@mysql::service/ready`** — poll `mysqladmin ping` (container name encore placeholder)
- [ ] **`@mysql::service/ready`** — résoudre le container name depuis `service.app_workdir.get_runtime_config()`

### Phase 4 — Commandes DB (dépendent de app/exec)
- [ ] **`db/exec`** — exécute une commande dans le container DB
  - Délègue la construction de la commande SQL au service (`@service::db/exec`)
  - Puis appelle `app/exec` sur le container DB
  - **Test** : `db exec -c "SELECT 1"` sur network

- [ ] **`db/go`** — entre dans le CLI DB (mysql, psql…)
  - Récupère la commande via `@service::db/go`, puis `app/exec --interactive`
  - **Test** : `db go` sur network (doit ouvrir mysql CLI)

- [ ] **`db/dump`** — dump de la DB
  - Délègue au service (`@service::db/dump`), zip, symlink `db.latest`
  - **Test** : `db dump` sur network → vérifie le zip créé dans `.wex/mysql/dumps/`

- [ ] **`db/restore`** — restaure un dump
  - Liste les dumps disponibles (prompt si non précisé), unzip si besoin
  - Délègue à `@service::db/destroy` puis `@service::db/restore`
  - **Test** : `db restore` sur network → sélectionner un dump existant

### Phase 5 — Start (commande la plus complexe)
- [~] **`app/start`** — squelette avec todos, bloqué par `config/write`
  - Pré-requis : middleware Docker, app/started, app/exec, app/perms, app/stop
  - Pipeline :
    1. Checkup (déjà démarrée ? env défini ?)
    2. Proxy (démarrer le proxy si requis et absent)
    3. Config (`config/write` — génère docker-compose.runtime.yml)
    4. Hooks `app/start-pre`
    5. `docker compose up -d`
    6. Hosts update
    7. Wait services ready (poll `service/ready`)
    8. Hooks `app/start-post` + `app/serve`
    9. First-init (hook `app/first-init` + lock file)
  - **Test** : `app start` sur network (app arrêtée)

- [ ] **`app/perms`** — fix permissions (dépendance de start)
  - `chown` + `chmod` récursif selon config `permissions.*`
  - Local env : utilise l'utilisateur courant
  - Autre env : utilise `www-data` ou config
  - Requiert sudo (`@as_sudo`)
  - **Test** : `app perms` sur network

### Phase 6 — Config app (dépendances de start)
- [x] **`config/write`** — génère `config.runtime.yml` + `docker-compose.runtime.yml`
  - Testé sur network, fonctionne
  - Todos restants : services compose files via hook, domains/domain_tld, user/group/uid/gid

- [ ] **`config/get`** / **`config/set`** — lecture/écriture dans `.wex/config.yml`
  - Simple : wrap autour du loader de config v6

### Phase 7 — Commandes distantes (après tout le reste)
- [ ] **`remote/exec`** — SSH vers un serveur distant
  - Options : `--environment`, `--command`, `--terminal`
  - Construit la commande SSH depuis la config `env.<env>.server.ip`

- [ ] **`remote/push`** — SCP + webhook
  - Copie les fichiers marqués `remote: push` dans le schema
  - Appelle le webhook HTTP du serveur distant
  - **Complexe** — à faire en dernier

---

## Système de migration des apps v5→v6

> En v5 le système existait mais était peu utilisé.
> En v6 on le réactive et on l'enrichit pour couvrir la transition v5→v6.

### Commande à créer
- [ ] **`migration/migrate`** — migre une app v5 vers v6
  - Lit la version wex dans `config.yml` (clé `wex.version`)
  - Exécute les fichiers de migration dans l'ordre (par numéro de version)
  - Met à jour la version dans config.yml après chaque migration
  - **Test** : `migration migrate` sur network (actuellement en `5.0.51`)

### Fichiers de migration à créer dans `wex-addon-app/migrations/`
- [ ] **`migration_6_0_0.py`** — migration v5→v6
  - Choses à vérifier/adapter sur une app v5 :
    - Clé `wex.version` → devient `global.wex_version` (à confirmer)
    - Structure `.wex/tmp/` — vérifier que les fichiers runtime sont attendus au même endroit
    - Clé `docker.main_db_container` → inchangée (déjà v5-compatible)
    - Clé `global.type: app` — doit être présente (ajoutée par migration_5_0_1)
  - **Test** : faire tourner sur network, vérifier config.yml après

### App network — état actuel (ref pour les migrations)
```yaml
# .wex/config.yml (network)
wex:
  version: 5.0.51+build.20231203154926
global:
  type: app
  name: network
  main_service: symfony
docker:
  main_db_container: mysql
require_proxy: true
```

---

## Commandes hors scope (pour l'instant)

Ces commandes existent en v5 mais ne sont pas prioritaires :

- `app/init` — création d'une nouvelle app (complexe, peu urgent)
- `app/serve` — hook uniquement, trivial
- `app/go` — alias de `app/exec --interactive` avec le shell par défaut
- `hosts/update` — modifier `/etc/hosts` (sudo, dépend du proxy)
- `container/list` — liste les containers depuis docker-compose.runtime.yml
- `webhook/*` — système webhook complet (après app/start)
- `service/install`, `service/used` — gestion des services
- `remote/go`, `remote/available`, `remote/push_receive`
- `branch/env`, `branch/ip`
- `env/get`, `env/set`, `env/choose`
- `domain/list`, `logs/follow`, `notification/notify`
- `info/update` (AI)

---

## Définition of done pour chaque commande

1. Fichier `.py` (ou `.yml`) créé dans `wex-addon-app/commands/`
2. Testé manuellement sur l'app `network` via wex v6 (symlink)
3. Si l'app v5 ne démarre pas → migration créée et testée
4. Coché dans ce fichier
