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
- `decorator/webhook.py` — `@webhook()` / `webhook: bool` sur `CommandMethodWrapper`
- Commandes : `token_show`, `token_rotate`
- Handler : `Authorization: Bearer` ou `?_token`, `hmac.compare_digest`, 401 + log des échecs

---

## Phase 3 — Mise en production (priorité immédiate)

Objectif : wex-apt-repo répond à un webhook depuis l'extérieur, en wex 6.

- [ ] **Déployer wex 6** sur le serveur (package apt)
- [ ] **Stopper le daemon wex 5** (sans doute périmé)
- [ ] **Installer wex 6** à la place de wex 5 — les apps wex 5 continuent de tourner
- [ ] **Démarrer le daemon wex 6** (`wex default::webhook/listen --asynchronous`)
- [ ] **Push wex-apt-repo en wex 6** — migration appliquée, commandes converties
- [ ] **Trigger le webhook depuis l'extérieur** — vérifier token, log, réponse
- [ ] **Boucler le CI/CD** — wex 6 se publie lui-même via webhook (wex-apt-repo déclenché depuis GitLab/GitHub)

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

## Phase 5 — Dot-commands (`.group/command` via webhook)

> Nécessite de valider `AppCommandResolver` en contexte daemon.

- [ ] Vérifier résolution contextuelle de `.group/command` depuis le workdir daemon
- [ ] Passer le `app_path` comme argument si nécessaire
- [ ] Tests de résolution app-level depuis un daemon hors workdir
