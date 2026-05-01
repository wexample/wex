# Webhook daemon — roadmap

## Références code

- Wex 5 legacy : `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-5-legacy/addons/app/command/webhook/`
- Wex 6 core daemon : `wex-core/src/wexample_wex_core/addons/core/commands/webhook/`
- Wex 6 module : `wex-core/src/wexample_wex_core/webhook/` (handler, routing, const)
- Wex 6 décorateur : `wex-core/src/wexample_wex_core/decorator/webhook.py`
- Wex 6 addon-app : `wex-addon-app/src/wexample_wex_addon_app/`

## ✅ Phases 1–3 — Terminées

- Infrastructure : daemon HTTP threadé, commandes `listen`/`stop`/`status`/`exec`, endpoint `/health`
- Sécurité : token HMAC par commande, `Authorization: Bearer` ou `?_token`, 401 + log des échecs
- Prod : wexample.com port 7654, wex-apt-repo et tiunine opérationnels

---

## Phase 4 — Assainissement architectural

### Problème

Le daemon est dans `wex-core` mais contient du code spécifique au concept d'app :
- `const.py` : `WEBHOOK_APPS_BASE_PATH = "/var/www"` — chemin des apps hardcodé
- `routing.py` : `routing_parse_app_url` — parse `{env}/{app_name}/{command}`
- `routing_build_command` : branche `if command_type == "app"` avec logique dédiée
- `exec.py` : `os.chdir(WEBHOOK_APPS_BASE_PATH / env / app_name)` — chdir vers l'app
- `handler.py` : `_read_app_token(app_path)` — lit les tokens depuis l'app
- `handler._validate_token` : `else: return False` — addon/service jamais supportés

### Règle de séparation

```
wex core   →  daemon HTTP, routing générique, extraction du token, HMAC
wex-addon-app  →  résolution cwd app, lecture token depuis {app}/.wex/local/
```

### Solution : type handlers injectables

Le handler HTTP expose un registre de type-resolvers :

```python
class WebhookTypeResolver(Protocol):
  def resolve_cwd(self, command_path: str) -> str | None: ...
  def resolve_token(self, command_path: str, command_str: str) -> str | None: ...
  def build_command(self, command_path: str) -> str | None: ...

# Dans handler.py (core)
type_resolvers: dict[str, WebhookTypeResolver] = {}

# Dans wex-addon-app (listen override ou app_start hook)
handler.type_resolvers["app"] = AppWebhookTypeResolver(apps_base_path)
```

### Tâches

- [x] Définir `WebhookTypeResolver` (Protocol) dans `webhook/resolver.py` (core)
- [x] Vider `handler.py` de toute logique app : délégation complète au resolver
- [x] Sortir `WEBHOOK_APPS_BASE_PATH` et `routing_parse_app_url` de core vers wex-addon-app
- [x] Créer `AppWebhookTypeResolver` dans wex-addon-app
- [x] `listen.py` (core) : charge les resolvers via `_load_type_resolvers()` (import gracieux)
- [x] `exec.py` (core) : reçoit `--command-str` résolu par le handler, plus de logique app
- [x] `listen` dans wex-addon-app : `AppWebhookTypeResolver` injecté automatiquement au démarrage

---

## Phase 5 — Monitoring et gestion des tokens (wex-addon-app)

Commandes depuis le workdir d'une app (contexte `.`), déléguant au resolver :

- [x] `app::webhook/status` — statut daemon + liste commandes `@webhook()` + état tokens
- [x] `app::webhook/token-generate [--command | --all] [--force]`
- [x] `app::webhook/token-show --command`
- [x] `app::webhook/token-list`
- [x] `app::webhook/token-revoke [--command | --all]`
- [x] Section "Webhooks" dans `app::info/show`
- [x] `webhook: bool` ajouté à `RegistryCommandData` (Python + YAML)

---

## Phase 6 — Addon et service types

- [ ] Implémenter `AddonWebhookTypeResolver` (token dans workdir wex global)
- [ ] Implémenter `ServiceWebhookTypeResolver`
- [ ] Enregistrer les resolvers au démarrage du daemon

---

## Phase 7 — Robustesse et observabilité

- [ ] Timeout par worker configurable (`--worker-timeout`, défaut 30s)
- [ ] Signal handling propre : `SIGTERM` → `server.shutdown()` gracieux
- [ ] Option `--log-level` (debug/info/warning)
- [ ] Endpoint `/metrics` Prometheus : `webhook_requests_total`, `webhook_request_duration_seconds`

## Pase 8 - Test

- [ ] Marche actuellement : url http://151.80.23.108:7654/webhook/app/prod/wex-apt-repo/apt/publish?_token=Hi2gft8Fo1q4ie5-ZjNtOerjGg3CPvbgbse98sE2AtY&project=155&version=6.0.63&_async=0
- [ ] Déploiement en prod (nouvelle version wex faite par weeger)
- [ ] Retest du curl

