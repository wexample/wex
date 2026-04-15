# Système Webhook — wex

> Ce document décrit l'architecture du système webhook wex : comment il fonctionnait en v5,
> ce qui doit changer en v6, et les principes de conception retenus.
> La roadmap de migration détaillée est dans `migration/todo/addons/webhook.md`.

---

## Principe général

Les webhooks permettent d'exposer des commandes wex (internes à une app) via HTTP, pour qu'elles
soient déclenchables depuis un serveur distant ou un CI/CD.

**URL type :** `https://monserveur.com:6543/webhook/{command_type}/{command_path}?arg1=val1`

**Exemple :** `https://deploy.myapp.com:6543/webhook/app/remote/push_receive?app=myapi&env=prod`

---

## Architecture v5 (référence)

### Marquage des commandes

Une commande Python est déclarée comme webhook-accessible via le décorateur `@app_webhook()` :

```python
# addons/app/decorator/app_webhook.py
@app_webhook()
@command(help="Receive a remote push")
def app__remote__push_receive(kernel, ...):
    ...
```

En YAML, la propriété `app_webhook: true` joue le même rôle.

### Daemon HTTP

La commande `app::webhook/listen` démarre un serveur HTTP (`http.server.HTTPServer`)
sur le port **6543** (configurable via `--port`).

Trois modes de lancement :
- **sync** (blocking) — utile pour les tests
- **async subprocess** — pour Docker (pas de systemd disponible)
- **async daemon** — via systemd (machines Linux bare-metal)

La classe `WebhookHttpRequestHandler` hérite de `BaseHTTPRequestHandler`.

### Routes déclarées

```python
# addons/app/const/webhook.py
WEBHOOK_LISTENER_ROUTES_MAP = {
    "exec": {
        "is_async": True,
        "pattern": r"^/webhook/([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-\/]+)$",
        "script_command": app__webhook__exec,
    },
    "status": {
        "is_async": False,
        "pattern": r"^/status$",
        "script_command": app__webhook__status,
    },
    "status_process": {
        "is_async": False,
        "pattern": r"^/status/process/([0-9\-]+)$",
        "script_command": app__webhook__status_process,
    },
}
```

À l'initialisation du serveur, `routing_build_webhook_route_map()` convertit chaque
`script_command` en liste de commandes shell réelles (avec placeholders `__URL__` et `__PORT__`).

### Dispatch d'une requête (`do_GET`)

1. Validation de la route contre les patterns (`routing_is_allowed_route`)
2. Validation stricte des query params (whitelist regex)
3. Spawn d'un subprocess qui exécute `app::webhook/exec`
4. Pour les routes **sync** : attente, capture stdout/stderr, retour JSON
5. Pour les routes **async** : retour immédiat avec PID

### Sécurité (v5)

- Validation des query params par regex (chars autorisés uniquement)
- Pas d'authentification par token — c'est le principal manque identifié
- Aucun HTTPS natif (suppose un reverse proxy TLS en amont)

### Commandes disponibles

| Commande | Rôle |
|----------|------|
| `app::webhook/listen` | Démarrer le daemon |
| `app::webhook/stop` | Arrêter le daemon |
| `app::webhook/status` | État du daemon + log des enfants |
| `app::webhook/status_process` | État d'un process enfant par PID |
| `app::webhook/exec` | Dispatcher interne (appelé par le daemon) |

### Gestion des processus (v5)

- Détection port ouvert avant démarrage (`system_is_port_open`)
- `--force` pour tuer l'existant
- Logs via `RotatingFileHandler` + task files (`webhook-stdout`, `webhook-stderr`)
- Tracking via `task_id` pour associer les logs daemon ↔ enfants

---

## Problèmes identifiés en v5

### Stabilité du daemon

- Le daemon avait tendance à se bloquer silencieusement sans mécanisme de détection
- Pas de healthcheck automatique ni de watchdog
- Restart manuel uniquement

### Sécurité insuffisante

- Aucun token d'authentification — n'importe qui atteignant le port peut déclencher une commande
- Pas de signature de requête (HMAC ou autre)
- Validation query params basique (regex seule)

### Observabilité limitée

- Pas d'endpoint de santé standardisé
- Status lisible mais non structuré pour du monitoring externe (Prometheus, etc.)
- Les logs enfants sont liés au task_id du daemon, difficile à corréler sans tooling

---

## Design cible v6

### Placement dans le code

Le mécanisme webhook est **générique** — il n'a pas besoin du concept d'app pour fonctionner.
Un ping webhook, un hook système, doivent marcher sans `AppMiddleware`.

- **`wex-core`** : daemon HTTP, handler, routing, `@webhook` decorator, commandes `webhook/*`
- **`wex-addon-app`** : commandes `remote/*`, intégration AppMiddleware, routes app-spécifiques

### Sécurité — tokens d'accès

Chaque commande marquée `@webhook` reçoit un **token** généré à la registration.
Le token est stocké dans la config de l'app (`.wex/config`).

L'appelant doit passer ce token dans le header `Authorization: Bearer <token>`
ou dans un query param `_token=<token>`.

Génération : `secrets.token_urlsafe(32)` — renouvelable via `app::webhook/token/rotate`.

### Robustesse du daemon

- Utiliser `ThreadingHTTPServer` ou `asyncio` au lieu de `HTTPServer` mono-thread
- Ajouter un endpoint `/health` retournant `{"status": "ok", "uptime": ...}`
- Watchdog optionnel : le daemon se redémarre lui-même si un worker se bloque (timeout configurable)
- Signal handling propre (`SIGTERM`, `SIGINT`) pour arrêt gracieux

### Observabilité

- Métriques exposées sur `/metrics` (format texte Prometheus-compatible)
- Chaque requête webhook loguée avec : timestamp, command, status, duration, source IP
- Endpoint `/status` retourne JSON structuré prêt pour healthcheck externe

### Logs

Problème v5 : logs dans des fichiers task temporaires introuvables en cas d'incident.
En v6 : **chemin fixe `.wex/logs/webhook.log`**, JSON line par requête, affiché par `webhook/status`.

### Commandes locales contextuelles (`.command`)

Les commandes préfixées `.` (dot-commands) doivent être accessibles depuis le webhook
via la même URL pattern `webhook/app/.command/path`.

Le `AppCommandResolver` v6 doit gérer le dispatch contextuellement selon l'app déclarée.

### Commandes distantes (`remote/*`)

Les commandes `remote/push_receive`, `remote/exec`, `remote/go` etc. sont les premiers
consommateurs naturels du système webhook. Elles restent dans le périmètre v6 mais
constituent un chantier séparé post-webhook-core.

---

## Fichiers v5 de référence

```
addons/app/
├── WebhookHttpRequestHandler.py        # Handler HTTP principal
├── decorator/app_webhook.py            # Décorateur @app_webhook
├── decorator/option_webhook_listener.py
├── const/webhook.py                    # Routes map
├── typing/webhook.py                   # Types (WebhookRoute, RoutesMap)
├── command/webhook/
│   ├── listen.py                       # Démarrer le daemon
│   ├── exec.py                         # Dispatcher interne
│   ├── status.py                       # État daemon + logs enfants
│   ├── status_process.py               # État d'un process
│   └── stop.py                         # Arrêter
└── tests/AbstractWebhookTestCase.py    # Infrastructure de test

src/helper/routing.py                   # routing_build_webhook_route_map, validation
```
