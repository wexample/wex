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
| `/webhook/addon/app/info/show` | addon | `app::info/show` |
| `/webhook/app/remote/push_receive` | app | `.remote/push_receive` |
| `/webhook/service/nginx/status` | service | `@nginx::status` |

### Logs

Path fixe : `{workdir}/logs/webhook.log` — JSON line par requête, rotation 5 × 1 Mo.
Affiché directement par `webhook/status`.

---

## ✅ Phases 1 et 2 — Terminées

**Phase 1 — Infrastructure**
- `webhook/const.py`, `webhook/routing.py`, `webhook/handler.py` (`ThreadingHTTPServer`)
- Commandes : `listen` (sync/async/force/dry-run), `stop`, `status`, `exec`
- Endpoint `/health` sans auth → `{"status":"ok","uptime_seconds":...}`

**Phase 2 — Sécurité**
- `webhook/token_store.py` — stockage YAML (`webhook_tokens.yml` dans workdir)
- `decorator/webhook.py` — `@webhook()` marque une commande comme accessible
- Commandes : `token_show`, `token_rotate`
- Handler : `Authorization: Bearer` ou `?_token`, `hmac.compare_digest`, 401 + log des échecs

---

## Phase 3 — Robustesse et observabilité

- [ ] Timeout par worker configurable (`--worker-timeout`, défaut 30s)
- [ ] Signal handling propre : `SIGTERM` → `server.shutdown()` gracieux
- [ ] Option `--log-level` (debug/info/warning)
- [ ] Endpoint `/metrics` → format Prometheus-compatible
  - `webhook_requests_total{command_type, status}` counter
  - `webhook_request_duration_seconds` histogram
  - `webhook_daemon_uptime_seconds` gauge

---

## Phase 4 — Dot-commands (`.group/command` via webhook)

> Nécessite de valider `AppCommandResolver` en contexte daemon.

- [ ] Vérifier résolution contextuelle de `.group/command` depuis le workdir daemon
- [ ] Passer le `app_path` comme argument si nécessaire
- [ ] Tests de résolution app-level depuis un daemon hors workdir
