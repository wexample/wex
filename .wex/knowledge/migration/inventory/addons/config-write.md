# config/write — État v6

## ✅ Validé et fonctionnel sur l'app `network`

`config/write` produit trois fichiers dans `.wex/tmp/` :

```
1. config.runtime.wex6.yml   — runtime complet, toutes contributions mergées
2. docker.env                — flatten mécanique du runtime, namespaces APP_*/BIND_*/SERVICE_*
3. docker-compose.runtime.yml — résultat de `docker compose config` sur tous les fichiers mergés
```

---

## Architecture

### Namespaces docker.env
```
APP_*        — métadonnées de l'app (APP_NAME, APP_ENV, APP_PATH, APP_SETUP_PATH, APP_HOST_IP, APP_STARTED, ...)
BIND_*       — chemins de fichiers bindés (BIND_WEB_PHP_INI, BIND_WEB_APACHE_CONF, ...)
SERVICE_*_*  — données des services (SERVICE_MYSQL_HOST, SERVICE_MYSQL_COMPOSE, ...)
```
Le `.env` de l'app est chargé en base (variables utilisateur), le runtime flatten par-dessus (priorité wex).

### Résolution en couches des fichiers bindés
```
.wex/env/{env}/php/web.ini   ← prioritaire si existe
.wex/php/web.ini             ← fallback
→ FileNotFoundError explicite si aucun n'existe
```

### Contributions des services
Deux mécanismes cumulatifs :
1. `AppService.get_runtime_contribution()` — statique : config.yml + bind + compose
2. `AppMiddleware.call_service_hook("runtime/contribution", ...)` — commande `@{service}::runtime/contribution` si elle existe

`call_service_hook` est générique — utilisable pour tous les hooks de service (stop-pre, start-post, etc.).

### Services intégrés dans `wex-addon-app`
| Service | Rôle |
|---|---|
| `proxy` | Déclare `wex_net` (réseau Docker externe partagé avec le proxy) |
| `letsencrypt` | Produit `DOMAINS_STRING` via `@letsencrypt::runtime/contribution` |

Ces services sont activés en ajoutant `proxy: {}` et `letsencrypt: {}` sous `service:` dans `config.yml`.

### Config env-spécifique
- Override de config : `.wex/env/{env}/config.yml` (remplace l'ancien `config.{env}.yml`)
- Le bloc `env.{env}.*` du `config.yml` est résolu et fusionné dans `app.*` du runtime

---

## Fichiers clés

| Fichier | Rôle |
|---|---|
| `wex-addon-app/.../commands/config/write.py` | Orchestrateur (`_runtime`, `_env`, `_docker`) |
| `wex-addon-app/.../service/app_service.py` | `get_runtime_contribution()` |
| `wex-addon-app/.../middleware/app_middleware.py` | `get_services()` + `call_service_hook()` |
| `wex-addon-app/.../services/proxy/` | Service proxy (wex_net) |
| `wex-addon-app/.../services/letsencrypt/` | Service letsencrypt (DOMAINS_STRING) |
| `wex-addon-*/services/*/service.yml` | Déclarations bind/compose par service |

---

## TODO restants

- Réseau proxy (`wex_net` créé par le proxy) — service proxy à implémenter dans un addon dédié ultérieurement
- `user`/`group`/`uid`/`gid` — gestion des permissions, hors scope config/write
- `app/start` est le prochain chantier — dépend de `docker-compose.runtime.yml` valide ✅
