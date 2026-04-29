# Roadmap migration : Webhooks

> Documentation de design et prise en main : `../../../../readme/webhooks.md`

---

## Décisions architecturales

### Placement

- **`wex-core`** : daemon HTTP, handler, routing, `@webhook` decorator, commandes `webhook/*`
- **`wex-addon-app`** : commandes `remote/*`, intégration AppMiddleware

### Types de commandes supportés

| URL | Type | Commande exécutée |
|-----|------|-------------------|
| `/webhook/app/prod/myapp/release/deploy` | app | `.release/deploy` |
| `/webhook/addon/app/info/show` | addon | `app::info/show` (non implémenté) |
| `/webhook/service/nginx/status` | service | `@nginx::status` (non implémenté) |

### Tokens

Un token par app, stocké dans `{app_path}/.wex/local/webhook_tokens.yml`.
Pas de registre central — chaque app gère ses propres tokens.
Création manuelle avec `sudo` (voir readme).

Les commandes `token-show` et `token-rotate` ont été supprimées : elles écrivaient dans
le workdir wex (`/usr/lib/wex/.wex/local/`) que le daemon ne lit pas.

### Logs

Path fixe : `{workdir}/logs/webhook.log` — JSON line par requête, rotation 5 × 1 Mo.
Affiché directement par `webhook/status`.

---

## ✅ Phases 1, 2 et 3 — Terminées

**Phase 1 — Infrastructure**
- `webhook/const.py`, `webhook/routing.py`, `webhook/handler.py` (`ThreadingHTTPServer`)
- Commandes : `listen` (sync/async/force/dry-run), `stop`, `status`, `exec`
- Endpoint `/health` sans auth → `{"status":"ok","uptime_seconds":...}`

**Phase 2 — Sécurité**
- Handler : `Authorization: Bearer` ou `?_token`, `hmac.compare_digest`, 401 + log des échecs
- `decorator/webhook.py` — `@webhook()` / `webhook: bool` sur `CommandMethodWrapper`
- Tokens stockés par app dans `{app_path}/.wex/local/webhook_tokens.yml`

**Phase 3 — Production**
- wex 6 déployé sur wexample.com (port 7654)
- wex-apt-repo et tiunine opérationnels avec webhook

---

## Phase 4 — Robustesse et observabilité

- [ ] Timeout par worker configurable (`--worker-timeout`, défaut 30s)
- [ ] Signal handling propre : `SIGTERM` → `server.shutdown()` gracieux
- [ ] Option `--log-level` (debug/info/warning)
- [ ] Endpoint `/metrics` → format Prometheus-compatible
  - `webhook_requests_total{command_type, status}` counter
  - `webhook_request_duration_seconds` histogram
  - `webhook_daemon_uptime_seconds` gauge

---

## Phase 5 — Addon et service types

- [ ] Implémenter `_validate_token` pour `addon` et `service` (actuellement `return False`)
- [ ] Décider du stockage : workdir wex central ou par addon ?

---

## Phase 6 — Commande de gestion des tokens (wex-addon-app)

- [ ] Créer `app::webhook/token-show --command-name ".release/deploy"` dans wex-addon-app
  - Détecte l'app workdir courant, écrit dans `{app_path}/.wex/local/webhook_tokens.yml`
  - Pas de dépendance inversée core→app
