# Roadmap migration : Webhooks (`wex-addon-app`)

> Référence comportementale : `wex-5-legacy/addons/app/` (commandes `webhook/*` et `remote/*`)
> Documentation de design : `../../../../readme/webhooks.md`
> Ce fichier pilote l'avancement de la migration étape par étape.

---

## Périmètre

Le système webhook permet d'exposer des commandes wex via HTTP pour un déclenchement distant.
La v6 reprend le principe de v5 avec des améliorations ciblées sur : sécurité (tokens),
stabilité du daemon (threading + watchdog), et observabilité (health + metrics).

---

## Phase 1 — Infrastructure de base (webhook-core)

Objectif : avoir un daemon HTTP fonctionnel en v6 avec le même comportement qu'en v5.

### 1.1 Décorateur et marquage

- [ ] Créer `@webhook()` dans `wexample_wex_addon_app/decorator/webhook.py`
  - Enregistre la commande comme webhook-accessible (`set_extra_value("webhook")`)
  - Support équivalent en YAML (`webhook: true`)
- [ ] Ajouter le scan des commandes marquées dans `AppAddonManager`

### 1.2 Routes map et routing

- [ ] Porter `const/webhook.py` → routes map v6 (pattern + is_async + script_command)
- [ ] Porter `src/helper/routing.py` → `helpers/webhook_routing.py` dans wex-addon-app
  - `routing_build_webhook_route_map()`
  - `routing_get_route_name()` / `routing_get_route_info()`
  - `routing_is_allowed_route()` avec validation regex query params

### 1.3 Handler HTTP

- [ ] Porter `WebhookHttpRequestHandler` → v6
  - Remplacer `HTTPServer` par `ThreadingHTTPServer` (stabilité)
  - Conserver le pattern : sync/async selon `is_async` de la route
  - Ajouter endpoint `/health` → `{"status": "ok", "uptime_seconds": N}`
  - Ajouter logging structuré par requête (timestamp, command, status, duration, IP)

### 1.4 Commandes webhook

- [ ] `app::webhook/listen` — démarrer le daemon
  - Options : `--port` (défaut 6543), `--dry-run`, `--asynchronous`, `--force`
  - Modes : sync / subprocess async / systemd daemon (hors Docker)
  - Healthcheck du port avant démarrage
- [ ] `app::webhook/stop` — arrêt propre (SIGTERM → kill, systemd disable si applicable)
- [ ] `app::webhook/status` — état daemon + table des enfants (pid, command, timestamp, status)
- [ ] `app::webhook/exec` — dispatcher interne appelé par le daemon
  - Parse URL pattern `/webhook/{type}/{path}?args`
  - Validation des query params (regex whitelist)
  - Délègue au resolver de commandes correspondant (`command_type`)

### 1.5 Tests

- [ ] Porter `AbstractWebhookTestCase` → v6
- [ ] Test listen/stop cycle
- [ ] Test requête sync (status endpoint)
- [ ] Test requête async (exec endpoint)
- [ ] Test query params invalides → 404

---

## Phase 2 — Sécurité (tokens)

Objectif : aucune commande webhook ne s'exécute sans token valide.

### 2.1 Génération et stockage

- [ ] À la registration d'une commande `@webhook`, générer un token via `secrets.token_urlsafe(32)`
- [ ] Stocker dans `.wex/config` : `webhooks.<command_path>.token = <token>`
- [ ] Commande `app::webhook/token/show <command>` — afficher le token d'une commande
- [ ] Commande `app::webhook/token/rotate <command>` — régénérer le token

### 2.2 Validation au moment de la requête

- [ ] Dans `WebhookHttpRequestHandler.do_GET` : extraire token depuis
  - Header `Authorization: Bearer <token>`, **ou**
  - Query param `_token=<token>`
- [ ] Comparer en temps constant (`hmac.compare_digest`) avec le token stocké
- [ ] Si absent ou invalide → 401 JSON `{"error": "UNAUTHORIZED"}`
- [ ] Logger les tentatives invalides (IP + path) avec un rate-limit warning

### 2.3 Tests sécurité

- [ ] Test requête sans token → 401
- [ ] Test requête avec token invalide → 401
- [ ] Test requête avec token valide → 200
- [ ] Test rotation token → ancien token refusé, nouveau accepté

---

## Phase 3 — Robustesse et observabilité

Objectif : le daemon ne se bloque plus silencieusement ; son état est monitorable.

### 3.1 Stabilité daemon

- [ ] `ThreadingHTTPServer` + timeout par worker configurable (`--worker-timeout`, défaut 30s)
- [ ] Signal handling propre : `SIGTERM` → `server.shutdown()` gracieux
- [ ] Watchdog optionnel : thread superviseur détecte les workers bloqués et les relance
- [ ] Option `--log-level` pour contrôler verbosité (debug/info/warning)

### 3.2 Métriques

- [ ] Endpoint `/metrics` → format texte Prometheus-compatible
  - `webhook_requests_total{command, status}` counter
  - `webhook_request_duration_seconds{command}` histogram
  - `webhook_daemon_uptime_seconds` gauge
- [ ] Endpoint `/status` → JSON structuré machine-readable (pour healthcheck externe)

### 3.3 Tests observabilité

- [ ] Test `/health` retourne 200 quand daemon actif
- [ ] Test `/metrics` retourne du texte valide
- [ ] Test `/status` retourne JSON structuré

---

## Phase 4 — Commandes distantes (`remote/*`)

> Ces commandes sont les premiers consommateurs du webhook-core. Elles constituent un
> chantier distinct, débloqué après Phase 1.

- [ ] `app::remote/push_receive` — recoit un push git distant (décorée `@webhook`)
- [ ] `app::remote/exec` — exécuter une commande à distance via webhook
- [ ] `app::remote/go` — ouvrir un shell distant
- [ ] `app::remote/available` — vérifier disponibilité remote
- [ ] `app::remote/push` — initier un push vers remote

---

## Phase 5 — Commandes locales contextuelles (dot-commands)

- [ ] Vérifier que `AppCommandResolver` v6 dispatche correctement les commandes préfixées `.`
  - Via `wex .groupe/commande` depuis le dossier d'une app
  - Via `wex .groupe/commande` depuis un sous-dossier de l'app
- [ ] Exposer les dot-commands via webhook (URL `/webhook/app/.groupe/commande`)
- [ ] Tests de résolution contextuelle

---

## Dépendances inter-phases

```
Phase 1 (core)
    └── Phase 2 (tokens)
    └── Phase 3 (robustesse)
            └── Phase 4 (remote/*)
            └── Phase 5 (dot-commands)
```

Phases 2 et 3 peuvent être traitées en parallèle après Phase 1.

---

## Notes et décisions

- Le port par défaut reste **6543** (compatibilité v5)
- L'authentification par token remplace la validation regex seule — c'est un breaking change
  assumé (v6 n'est pas rétrocompatible avec les clients v5)
- Le HTTPS reste délégué au reverse proxy en amont (nginx/caddy) — pas de TLS natif prévu
- `status_process` peut être absorbé dans `status` en v6 (simplification)
- systemd daemon : conserver la logique v5 (copie service file + enable/start)
- En Docker (pas de systemd) : subprocess async comme en v5
