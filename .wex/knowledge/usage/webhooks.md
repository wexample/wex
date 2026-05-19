# Système Webhook — wex

Expose des commandes wex via HTTP pour les déclencher depuis un CI/CD, un serveur distant,
ou tout outil capable de faire une requête GET.

**URL type :** `http://host:6543/webhook/{type}/{path}?_token=<token>&arg=val`

---

## Prise en main rapide

### 1. Démarrer le daemon

```bash
# En arrière-plan
wex core::webhook/listen --async

# En avant-plan (pour débugger)
wex core::webhook/listen

# Forcer le redémarrage si le port est déjà occupé
wex core::webhook/listen --async --force

# Timeout custom (défaut 300s, 0 = pas de limite)
wex core::webhook/listen --worker-timeout 600
```

### 2. Vérifier que le daemon tourne

```bash
wex core::webhook/status

# Directement via HTTP — pas d'auth sur /health
curl http://localhost:6543/health
# → {"status": "ok", "uptime_seconds": 42}
```

### 3. Arrêter le daemon

```bash
wex core::webhook/stop
```

---

## Types d'URL supportés

| Type | URL | Commande exécutée |
|------|-----|-------------------|
| `app` | `/webhook/app/{env}/{app}/{cmd}` | `.{cmd}` dans `/var/www/{env}/{app}` |
| `addon` | `/webhook/addon/{addon}/{cmd}` | `{addon}::{cmd}` |
| `service` | `/webhook/service/{service}/{cmd}` | `@{service}::{cmd}` |

---

## Type `app` — commandes dans une application

### Marquer une commande comme accessible

YAML :
```yaml
# .wex/commands/release/deploy.yml
decorators:
  - name: webhook
scripts:
  ...
```

Python :
```python
from wexample_wex_core.decorator.webhook import webhook

@webhook()
@command(type=COMMAND_TYPE_ADDON, description="...")
def my__group__command(context: ExecutionContext) -> None:
    ...
```

### Gérer les tokens (depuis le workdir de l'app)

```bash
# Générer un token pour une commande
wex app::webhook/token-generate --command-name .release/deploy

# Générer pour toutes les commandes @webhook de l'app d'un coup
wex app::webhook/token-generate --all

# Regénérer (écraser l'existant)
wex app::webhook/token-generate --command-name .release/deploy --force

# Voir le token complet d'une commande
wex app::webhook/token-show --command-name .release/deploy

# Lister tous les tokens enregistrés (préfixe seulement)
wex app::webhook/token-list

# Révoquer un token
wex app::webhook/token-revoke --command-name .release/deploy

# Révoquer tous les tokens de l'app
wex app::webhook/token-revoke --all
```

Les tokens sont stockés dans `{app_path}/.wex/local/webhook_tokens.yml`.

### Statut webhooks de l'app

```bash
wex app::webhook/status
```

Affiche : état du daemon, nombre de commandes `@webhook`, nombre de tokens présents.
Ce résumé apparaît également dans `wex app::info/show`.

### Appeler le webhook

```bash
# Token en query param
curl "http://localhost:6543/webhook/app/prod/myapp/release/deploy?_token=<token>"

# Token en header
curl -H "Authorization: Bearer <token>" \
     "http://localhost:6543/webhook/app/prod/myapp/release/deploy"

# Avec des arguments passés à la commande
curl "http://localhost:6543/webhook/app/prod/myapp/release/deploy?_token=<token>&version=1.2.3"

# Forcer l'exécution synchrone (attend la fin, retourne la sortie)
curl "http://...?_token=<token>&_async=0"
```

---

## Type `addon` — commandes addon globales

### Gérer les tokens

```bash
# Générer un token pour une commande addon
wex core::webhook/token-generate --type addon --command-name app::info/show

# Générer pour toutes les commandes @webhook addon
wex core::webhook/token-generate --type addon --all

# --force, --all, token-show, token-list, token-revoke : mêmes options que pour app
wex core::webhook/token-show   --type addon --command-name app::info/show
wex core::webhook/token-list   --type addon
wex core::webhook/token-revoke --type addon --command-name app::info/show
wex core::webhook/token-revoke --type addon --all
```

Les tokens sont stockés dans `{wex_workdir}/.wex/local/webhook_tokens_addon.yml`.

### Appeler le webhook

```bash
curl "http://localhost:6543/webhook/addon/app/info/show?_token=<token>"
```

---

## Type `service` — commandes service

Identique au type `addon`, remplacer `--type addon` par `--type service`.

Tokens stockés dans `{wex_workdir}/.wex/local/webhook_tokens_service.yml`.

```bash
curl "http://localhost:6543/webhook/service/nginx/status?_token=<token>"
```

---

## Observabilité

### Logs

```bash
# Dernières requêtes (20 par défaut)
wex core::webhook/status

# Log brut — JSON, une ligne par requête
tail -f {wex_workdir}/logs/webhook.log
```

Champs : `ts`, `ip`, `path`, `command_type`, `command_path`, `status`, `duration_ms`, `pid`.
Rotation : 5 fichiers × 1 Mo max.

### Métriques Prometheus

```bash
curl http://localhost:6543/metrics
```

Expose (sans authentification) :
- `webhook_requests_total{command_type, status}` — compteur par type et statut
- `webhook_request_duration_seconds_sum{command_type}` — durée cumulée
- `webhook_request_duration_seconds_count{command_type}` — nombre de requêtes mesurées

---

## Sécurité

- Token transmis via `Authorization: Bearer <token>` ou `?_token=<token>`
- Comparaison en temps constant (`hmac.compare_digest`)
- Token absent ou invalide → **401**, loggué avec IP + path
- `/health` et `/metrics` sont exempts d'authentification

---

## Architecture

### Séparation des responsabilités

```
wex-core       →  daemon HTTP, routing générique, validation HMAC, résolveurs addon/service
wex-addon-app  →  AppWebhookTypeResolver, commandes app::webhook/*
```

### Résolveurs de type (`WebhookTypeResolver` Protocol)

Chaque type d'URL délègue à un résolveur qui implémente :

```python
def build_command(command_path: str) -> str | None  # construit la commande wex
def resolve_cwd(command_path: str) -> str | None    # répertoire de travail du subprocess
def resolve_token(command_path: str, command_str: str) -> str | None  # lit le token attendu
```

Résolveurs enregistrés au démarrage du daemon dans `listen.py` :

| Type | Classe | Token |
|------|--------|-------|
| `app` | `AppWebhookTypeResolver` (wex-addon-app) | `{app}/.wex/local/webhook_tokens.yml` |
| `addon` | `AddonWebhookTypeResolver` (wex-core) | `{wex_workdir}/.wex/local/webhook_tokens_addon.yml` |
| `service` | `ServiceWebhookTypeResolver` (wex-core) | `{wex_workdir}/.wex/local/webhook_tokens_service.yml` |

### Daemon

| Option | Défaut | Description |
|--------|--------|-------------|
| `--port` | `6543` | Port d'écoute |
| `--async` | `false` | Lance en subprocess background |
| `--force` | `false` | Tue le process existant sur le port |
| `--worker-timeout` | `300` | Timeout subprocess sync en secondes (0 = infini) |
| `--dry-run` | `false` | Bind le socket sans servir (tests) |

- **SIGTERM** → arrêt gracieux : les workers en cours terminent avant la fermeture
- Dépassement du timeout → HTTP **504**, process tué proprement

---

## Référence des commandes

| Commande | Rôle |
|----------|------|
| `core::webhook/listen` | Démarrer le daemon |
| `core::webhook/stop` | Arrêter le daemon |
| `core::webhook/status` | État + dernières lignes de log |
| `core::webhook/exec` | Dispatcher interne (appelé par le daemon) |
| `core::webhook/token-generate` | Générer un token addon/service |
| `core::webhook/token-show` | Afficher un token addon/service |
| `core::webhook/token-list` | Lister les tokens addon/service |
| `core::webhook/token-revoke` | Révoquer un token addon/service |
| `app::webhook/status` | Statut webhooks de l'app courante |
| `app::webhook/token-generate` | Générer un token pour une commande app |
| `app::webhook/token-show` | Afficher un token app |
| `app::webhook/token-list` | Lister les tokens app |
| `app::webhook/token-revoke` | Révoquer un token app |
