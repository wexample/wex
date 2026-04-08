# Migration v5 → v6 : app/init + service/install + helper générique

## Contexte

Ce chantier fait suite à la correction du bug helper/proxy (voir `helper-start.md`).
Le problème central est que `helper/start` v6 crée le proxy "à la main" (écriture manuelle
de fichiers YAML/conf) sans passer par un flux d'initialisation structuré.

En v5, ce flux était porté par deux commandes génériques :
- `app/init` : initialise une app (structure, config, .env, services)
- `service/install` : installe un service dans une app (copie les samples, merge les configs)

Ces deux commandes n'existent pas encore en v6. L'objectif est de les créer proprement
en respectant les patterns v6 existants, puis de refactoriser `helper/start` pour qu'il
passe par ce flux — sans mention explicite du proxy, exactement comme en v5.

---

## Fichiers de référence

### v5 (à lire pour comprendre la logique)
- `wex-5/addons/app/command/app/init.py` — flux complet d'init d'une app
- `wex-5/addons/app/command/service/install.py` — installation générique d'un service
- `wex-5/addons/app/services/proxy/command/service/install.py` — hook install proxy-spécifique
- `wex-5/addons/app/services/proxy/samples/` — fichiers copiés lors de l'install du proxy
- `wex-5/addons/app/command/helper/start.py` — flux helper générique (proxy passé en argument)
- `wex-5/addons/app/const/app.py` — `HELPER_APPS_LIST`, `HELPER_APP_PROXY_SHORT_NAME`

### v6 (état actuel, à modifier)
- `wex-addon-app/commands/app/start.py` — `_proxy()` appelle `helper/start` hardcodé proxy
- `wex-addon-app/commands/helper/start.py` — crée le proxy freestyle (à refactoriser)
- `wex-addon-app/commands/helper/stop.py` — déjà ok
- `wex-addon-app/services/proxy/service.yml` — tags: proxy, network
- `wex-addon-app/services/proxy/docker/docker-compose.yml` — ne contient que le réseau
- `wex-addon-app/app_addon_manager.py` — `find_service_dir()`, `run_service_hook()`
- `wex-addon-app/workdir/app_workdir.py` — `is_app_workdir_path()` vérifie `global.version`

---

## Analyse détaillée de l'écart v5 → v6

### 1. `app/init` — inexistant en v6

En v5, `app/init` fait :
1. Crée le répertoire de l'app
2. Copie la structure sample depuis `addons/app/samples/app/.wex/` (docker-compose vide, .gitignore, tmp/, etc.)
3. Crée `.wex/.env` avec `APP_ENV={env}`
4. Crée `.wex/config.yml` avec `global.name`, `global.version`, et la liste des services
5. Pour chaque service : appelle `app/service/install`
6. Init git (optionnel)
7. Appelle le hook `app/init-post`

En v6, l'équivalent partiel serait :
- Créer `.wex/config.yml` avec `global.name`, `global.version`, `global.main_service`, `service.{name}: {}`
- Créer `.wex/.env` avec `APP_ENV={env}`
- Créer `.wex/tmp/`
- Pour chaque service : appeler `service/install`

Notes v6 :
- Pas de structure "sample" à copier (l'arborescence est plus légère en v6)
- `is_app_workdir_path()` vérifie uniquement `global.version` dans config.yml
- Le git n'est pas nécessaire pour les helpers

### 2. `service/install` — inexistant en v6

En v5, `app/service/install` fait :
1. Résout les dépendances du service (récursif)
2. Vérifie que le service existe dans le registry
3. Si le service n'est pas encore dans la config → l'ajoute
4. Copie les samples du service dans l'app (merge docker-compose, merge .gitignore, copie le reste)
5. Set `global.main_service` si pas encore défini
6. Set `docker.main_db_container` si le service a le tag `db`
7. Merge les clés `docker` et `global` depuis `service.config.yml`
8. Appelle le hook `@{service}::service/install` pour les actions service-spécifiques

Le hook `proxy::service/install` (v5) :
- Copie `services/proxy/samples/proxy/` → `{app_dir}/proxy/`
  - `proxy/certs/`, `proxy/html/`, `proxy/logs/`, `proxy/vhost.d/`
  - `proxy/wex.conf`
- Set `port.public = 80` et `port.public_secure = 443`

En v6, l'équivalent serait :
- `app/service/install` : ajoute le service à config.yml + appelle hook `service/install`
- `services/proxy/commands/service/install.py` : crée les répertoires proxy + wex.conf + docker-compose.yml

**Point crucial sur le docker-compose du proxy** :

En v5 : `service/install` copie `.wex/docker/docker-compose.yml` depuis les samples du service.
Ce fichier référence `${RUNTIME_SERVICE_PROXY_YML_ENV}` (résolu à la runtime par `config/write`).

En v6 : le docker-compose proxy est une string literal dans `helper/start.py`.
Il doit migrer vers `services/proxy/samples/docker/docker-compose.yml`, car en continuité
avec v5 le dossier `samples/` définit les fichiers copiés ou mixés lors de l'install
d'un service.

Le hook `service/install` copierait `services/proxy/samples/docker/docker-compose.yml`
vers `.wex/docker/docker-compose.yml` dans l'app helper — c'est le "base app compose"
que `config/write` cherche ici :
```python
base_compose = app_path / WORKDIR_SETUP_DIR / "docker" / "docker-compose.yml"
```

### 3. `helper/start` — proxy-centric et non générique

En v5, `helper/start` :
- Prend `--name` parmi une liste `HELPER_APPS_LIST` (ex: `proxy`, `ai`)
- Crée l'app via `app/init` avec `services=[name]` → complètement générique
- Vérifie si l'app existe déjà et tourne → skip si oui
- Lance l'app via `app/start`

En v6, `helper/start` :
- Hardcode "proxy" partout
- Écrit manuellement les fichiers
- Pas de liste de helpers supportés
- Le flag `--name` n'existe même pas

À corriger :
- Réintroduire `--name` avec validation contre une liste `HELPER_APPS_LIST`
- Déléguer la création à `app/init` avec `services=[name]`
- Supprimer tout code proxy-spécifique de `helper/start`

### 4. `app/start._proxy()` — référence proxy en dur

Dans `app/start._proxy()` v6, le path du proxy est calculé depuis `"wex-proxy"` en dur.
En v5, il passait `name=HELPER_APP_PROXY_SHORT_NAME` à `helper/start`.
Le calcul du path helper (`/var/www/{env}/wex-{name}`) devrait être centralisé
dans une méthode utilitaire (ex: `AppAddonManager.get_helper_app_path(name, env)`).

Cette méthode existe déjà en v5 mais pas en v6.

---

## Plan d'implémentation

### Étape 1 — Constantes helper

- [x] Créer `wex-addon-app/const/app.py` (ou compléter s'il existe) avec :
  - `HELPER_APP_PROXY_SHORT_NAME = "proxy"`
  - `HELPER_APPS_LIST = ["proxy"]`
- [x] Créer `wex-addon-app/helpers/app.py` avec :
  - `get_helper_app_path(name, env)` → `Path(f"/var/www/{env}/wex-{name}")`
- [x] Exposer ce calcul via une méthode utilitaire de `AppAddonManager`

### Étape 2 — Samples proxy

- [x] Créer les fichiers sample du service proxy (à copier lors de `service/install`) :
  - `services/proxy/samples/proxy/certs/.gitkeep`
  - `services/proxy/samples/proxy/html/.gitkeep`
  - `services/proxy/samples/proxy/logs/.gitkeep`
  - `services/proxy/samples/proxy/vhost.d/.gitkeep`
  - `services/proxy/samples/proxy/wex.conf` (contenu = `_PROXY_WEX_CONF` actuellement dans `helper/start.py`)
  - `services/proxy/samples/docker/docker-compose.yml` (contenu = `_PROXY_DOCKER_COMPOSE` actuellement dans `helper/start.py`)

### Étape 3 — Hook `service/install` pour le proxy

- [x] Créer `services/proxy/commands/service/__init__.py`
- [x] Créer `services/proxy/commands/service/install.py` :
  - Type `COMMAND_TYPE_SERVICE`
  - Reçoit `app_path` et `service` (comme les autres hooks de service)
  - Copie `services/proxy/samples/proxy/` → `{app_path}/proxy/`
  - Copie `services/proxy/samples/docker/docker-compose.yml` → `{app_path}/.wex/docker/docker-compose.yml`
  - Set `port.public = 80` et `port.public_secure = 443` dans config.yml
  - S'inspirer de `v5/addons/app/services/proxy/command/service/install.py`

### Étape 4 — Commande `app/service/install`

- [ ] Créer `commands/service/__init__.py`
- [ ] Créer `commands/service/install.py` :
  - Options : `--service / -s` (required), `--app-path / -a` (optional, defaults to cwd)
  - Vérifie que le service existe via `AppAddonManager.find_service_dir(service)`
  - Vérifie que le service n'est pas déjà dans la config (sauf si `--force`)
  - Ajoute `service.{name}: {}` dans config.yml
  - Set `global.main_service` si pas encore défini
  - Appelle le hook `service/install` via `AppAddonManager.run_service_hook()`
  - S'inspirer de `v5/addons/app/command/service/install.py`
  - Note : pas besoin de gérer le merge de docker-compose (c'est le hook qui copie le fichier)
  - Note : pas besoin des dépendances de service dans un premier temps

### Étape 5 — Commande `app/init`

- [ ] Créer `commands/app/init.py` :
  - Options : `--name / -n` (required), `--services / -s` (liste, required), `--env / -e` (optional), `--app-path / -a` (optional)
  - Crée le répertoire `{app_path}/.wex/` et `{app_path}/.wex/tmp/`
  - Écrit `.wex/config.yml` avec `global.name`, `global.version: 1.0.0`, `global.type: app`
  - Écrit `.wex/.env` avec `APP_ENV={env}`
  - Pour chaque service : appelle `app/service/install`
  - Pas de git pour les helpers (option `--git` à `False` par défaut pour les helpers)
  - S'inspirer de `v5/addons/app/command/app/init.py`
  - Note : v6 n'a pas de "sample app" à copier, la structure minimale est créée directement

### Étape 6 — Refactoriser `helper/start`

- [ ] Supprimer les string literals `_PROXY_DOCKER_COMPOSE` et `_PROXY_WEX_CONF`
- [ ] Supprimer la création manuelle de fichiers dans `_create()`
- [ ] Réintroduire l'option `--name / -n` avec validation contre `HELPER_APPS_LIST`
- [ ] `_create()` devient :
  - Vérifier si `helper_app_path` existe + tourne → stop la queue (return `QueuedCollectionStopResponse`)
  - Créer le répertoire
  - Appeler `app/init` avec `name=f"wex-{name}"`, `services=[name]`, `env=env`
- [ ] `_start()` reste inchangé (appelle `app/start` sur le path calculé)
- [ ] Calculer le path via `get_helper_app_path(name, env)` (méthode centralisée)

### Étape 7 — Refactoriser `app/start._proxy()`

- [ ] Remplacer le path hardcodé `f"/var/www/{env}/wex-proxy"` par un appel à `get_helper_app_path("proxy", env)`
- [ ] Passer `name=HELPER_APP_PROXY_SHORT_NAME` à `helper/start` au lieu d'omettre l'argument

### Étape 8 — Tests

- [ ] Tester `app/service/install` sur le service proxy seul
- [ ] Tester `app/init` avec `services=["proxy"]`
- [ ] Tester `helper/start` sur une app nécessitant un proxy (crée le proxy + le démarre)
- [ ] Tester `helper/start` avec un proxy déjà lancé → doit skip sans erreur
- [ ] Tester `helper/stop` → arrête correctement
- [ ] Vérifier que `app/start` sur une app ordinaire démarre bien le proxy automatiquement
- [ ] Vérifier que `_complete` dans `app/start` ne propose pas `app::db/go` pour le proxy

---

## Points d'attention

- `run_service_hook()` dans `AppAddonManager` utilise un `app_workdir` existant.
  Pour l'appeler depuis `app/service/install`, il faut que l'app_workdir soit déjà
  créable (config.yml avec `global.version` doit exister). Donc `app/init` doit d'abord
  écrire le config.yml minimal, PUIS appeler `service/install`.

- Le hook `service/install` du proxy écrit `.wex/docker/docker-compose.yml`.
  `config/write` cherche ce fichier comme "base app compose".
  Le fichier source à copier reste dans `services/proxy/samples/docker/docker-compose.yml`,
  conformément à la convention v5/v6 : `samples/` définit les fichiers copiés ou mixés
  lors de l'install d'un service.

- `services/proxy/docker/docker-compose.yml` reste réservé au compose d'infra du service
  (ici le réseau `wex_net`) et n'est pas le fichier copié dans l'app helper.

- En v5, `service/install` merge les docker-compose YAML (pour les apps ordinaires
  qui combinent plusieurs services). En v6, `config/write` gère déjà l'assemblage runtime.
  La copie simple (sans merge) est suffisante pour l'init du helper.
  Pour les apps ordinaires avec plusieurs services, on verra quand le besoin se présente.

- `HELPER_APPS_LIST` en v5 contenait `["proxy", "ai"]`. En v6, commencer avec `["proxy"]`
  et ajouter `"ai"` quand le service sera défini.

- Ne pas ajouter `helper/start` comme dépendance dans `app/start` si le proxy est déjà
  démarré — la vérification est déjà faite dans `_proxy()`.
