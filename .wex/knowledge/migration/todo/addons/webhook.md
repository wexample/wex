# Roadmap migration : Webhooks

> Référence comportementale : `wex-5-legacy/addons/app/` (commandes `webhook/*` et `remote/*`)
> Documentation de design : `../../../../readme/webhooks.md`
> Ce fichier pilote l'avancement de la migration étape par étape.

---

## Décisions architecturales

### Placement : `wex-core` et non `wex-addon-app`

Le daemon HTTP + le dispatcher sont des mécanismes génériques indépendants du concept d'app.
Un ping webhook, un hook système, doivent fonctionner sans `AppMiddleware`.

- **`wex-core`** : daemon, handler HTTP, routing, `@webhook` decorator, commandes `webhook/*`
- **`wex-addon-app`** : routes spécifiques app, commandes `remote/*`, intégration AppMiddleware

### Types de commandes supportés

Trois types d'URL supportés (dans l'ordre de priorité d'usage) :

| URL | Type | Commande exécutée |
|-----|------|-------------------|
| `/webhook/app/remote/push_receive` | app | `.remote/push_receive` |
| `/webhook/addon/app/info/show` | addon | `app::info/show` |
| `/webhook/service/nginx/status` | service | `@nginx::status` |

Le type `app` est le cas d'usage principal (dot-commands contextuelles).
Le type `addon` couvre les utilitaires globaux (ping, disk, etc.).

### Logs

Problème v5 : les logs étaient dans des fichiers task temporaires introuvables en cas d'incident.
En v6 : **un fichier de log fixe et connu**, affiché directement par `webhook/status`.

- Path fixe : `.wex/logs/webhook.log` (dans le workdir wex, pas dans /tmp)
- Format : une ligne JSON par requête (timestamp, ip, path, command, status, duration_ms)
- `webhook/status` affiche les 20 dernières entrées par défaut
- Rotation : 5 fichiers × 1 Mo max (via `RotatingFileHandler`)

### Daemon process

- Subprocess async uniquement pour Phase 1 (pas de systemd)
- systemd : évalué plus tard selon le besoin (auto-restart au reboot serveur)
- `ThreadingHTTPServer` dès Phase 1 pour éviter le blocage v5

---

## Phase 1 — Infrastructure de base

Objectif : daemon HTTP fonctionnel, routing vers addon + app + service commands.

### 1.1 Core : daemon et routing (`wex-core`)

- [ ] `webhook/const.py` — port défaut 6543, patterns de routes, regex query params
- [ ] `webhook/routing.py`
  - `routing_get_route_name(path)` — match URL → nom de route
  - `routing_is_allowed_route(path)` — validation route + query params (whitelist regex)
  - `routing_build_command(command_type, command_path, query_args)` → string commande wex
- [ ] `webhook/handler.py`
  - `ThreadingHTTPServer` (ThreadingMixIn + TCPServer)
  - `WebhookHttpRequestHandler(BaseHTTPRequestHandler)`
  - `do_GET` : valide → subprocess `wex app::webhook/exec` → JSON response
  - Log fixe : `.wex/logs/webhook.log` (JSON line par requête)
  - Endpoint `/health` → `{"status": "ok"}`

### 1.2 Core : commandes webhook (`wex-core`)

- [ ] `app::webhook/listen` — démarrer le daemon
  - Options : `--port` (défaut 6543), `--asynchronous`, `--force`, `--dry-run`
  - Mode sync (blocking, pour tests) et async (subprocess background)
  - Vérifie si port déjà occupé avant démarrage
- [ ] `app::webhook/stop` — tuer le process par port (via psutil)
- [ ] `app::webhook/status` — état daemon (psutil) + dernières lignes du log fixe
- [ ] `app::webhook/exec` — dispatcher interne
  - Parse URL → command_type + command_path + query args
  - Construit la commande wex selon le type (addon/app/service)
  - Exécute via kernel (`execute_kernel_command`)
  - Log le résultat

### 1.3 Tests Phase 1

- [ ] Test listen/stop cycle (port occupé → stop → relance)
- [ ] Test `/health` → 200
- [ ] Test `exec` addon command
- [ ] Test `exec` app command
- [ ] Test query params invalides → 404
- [ ] Test route inconnue → 404

---

## Phase 2 — Sécurité (tokens)

Objectif : aucune commande webhook ne s'exécute sans token valide.

- [ ] `@webhook()` decorator — marque une commande comme webhook-accessible
  - S'il n'existe pas de token pour cette commande → en génère un (`secrets.token_urlsafe(32)`)
  - Stocke dans `.wex/config` : `webhooks.<command_path>.token`
- [ ] Support YAML : `decorators: [{name: webhook}]`
- [ ] `app::webhook/token/show <command>` — afficher le token
- [ ] `app::webhook/token/rotate <command>` — régénérer
- [ ] Validation dans le handler : `Authorization: Bearer <token>` ou `?_token=<token>`
  - Comparaison en temps constant (`hmac.compare_digest`)
  - Absent ou invalide → 401 `{"error": "UNAUTHORIZED"}`
  - Logguer les tentatives invalides (IP + path)
- [ ] Tests : sans token → 401, token invalide → 401, token valide → 200, rotation

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

## Phase 4 — Commandes distantes (`remote/*`, dans `wex-addon-app`)

> Débloqué après Phase 1. Premiers consommateurs réels du webhook-core.

- [ ] `app::remote/push_receive` — reçoit un push git distant
- [ ] `app::remote/exec` — exécuter une commande à distance via webhook
- [ ] `app::remote/go` — ouvrir un shell distant
- [ ] `app::remote/available` — vérifier disponibilité remote
- [ ] `app::remote/push` — initier un push vers remote

---

## Phase 5 — Dot-commands (`.group/command` via webhook)

> Débloqué après Phase 1. Nécessite de valider AppCommandResolver en contexte daemon.

- [ ] Vérifier résolution contextuelle de `.group/command` depuis le workdir daemon
- [ ] Passer le `app_path` comme argument si nécessaire
- [ ] Tests de résolution app-level depuis un daemon hors workdir

---

## Dépendances

```
Phase 1 (core daemon)
    ├── Phase 2 (tokens)       ← en parallèle
    ├── Phase 3 (robustesse)   ← en parallèle
    ├── Phase 4 (remote/*)     ← débloqué après 1
    └── Phase 5 (dot-commands) ← débloqué après 1
```

---

## Notes

- Port par défaut : **6543** (compatibilité v5)
- HTTPS délégué au reverse proxy — pas de TLS natif prévu
- `status_process` de v5 absorbé dans `status` (simplification)
- Phase 1 sans token = dangereux en prod — à documenter clairement
