# Système Webhook — wex

Expose des commandes wex via HTTP pour les déclencher depuis un CI/CD, un serveur distant,
ou tout outil capable de faire une requête GET.

**URL type :** `http://host:6543/webhook/{type}/{command/path}?_token=<token>&arg=val`

---

## Prise en main rapide

### 1. Démarrer le daemon

```bash
# En arrière-plan
wex default::webhook/listen --asynchronous

# En avant-plan (pour débugger)
wex default::webhook/listen

# Forcer le redémarrage si le port est déjà occupé
wex default::webhook/listen --asynchronous --force
```

### 2. Vérifier que le daemon tourne

```bash
wex default::webhook/status

# Ou directement via HTTP (pas d'auth sur /health)
curl http://localhost:6543/health
# → {"status": "ok", "uptime_seconds": 42}
```

### 3. Obtenir le token d'une commande

```bash
wex default::webhook/token-show --command-name "app::info/show"
# → affiche le token, le génère s'il n'existe pas encore
```

### 4. Appeler le webhook

```bash
# Token en query param
curl "http://localhost:6543/webhook/addon/app/info/show?_token=<token>"

# Token en header
curl -H "Authorization: Bearer <token>" \
     "http://localhost:6543/webhook/addon/app/info/show"

# Avec des arguments
curl "http://localhost:6543/webhook/addon/app/info/show?_token=<token>&env=prod"
```

### 5. Consulter les logs

```bash
# Dernières requêtes (20 par défaut)
wex default::webhook/status

# Log brut (JSON, une ligne par requête)
tail -f {workdir}/logs/webhook.log
```

### 6. Renouveler un token

```bash
wex default::webhook/token-rotate --command-name "app::info/show"
# → affiche le nouveau token — l'ancien est immédiatement invalide
```

### 7. Arrêter le daemon

```bash
wex default::webhook/stop
```

---

## Architecture

### Placement

- **`wex-core`** : daemon, handler HTTP, routing, `@webhook` decorator, commandes `webhook/*`
- **`wex-addon-app`** : commandes `remote/*`, intégration AppMiddleware

### Types d'URL supportés

| URL | Commande exécutée |
|-----|-------------------|
| `/webhook/addon/app/info/show` | `app::info/show` |
| `/webhook/app/remote/push_receive` | `.remote/push_receive` |
| `/webhook/service/nginx/status` | `@nginx::status` |

Le type `addon` est le plus courant (commandes globales wex).
Le type `app` est pour les dot-commands contextuelles.

### Sécurité

Chaque commande a un token indépendant stocké dans `{workdir}/webhook_tokens.yml`.

- Transmis via `Authorization: Bearer <token>` ou `?_token=<token>`
- Comparaison en temps constant (`hmac.compare_digest`)
- Absent ou invalide → 401, loggué avec IP + path
- `/health` est exempt d'authentification

### Logs

Fichier fixe : `{workdir}/logs/webhook.log`
Format : une ligne JSON par requête — `ts`, `ip`, `path`, `command_type`, `status`, `duration_ms`
Rotation : 5 fichiers × 1 Mo max.

### Daemon

- `ThreadingHTTPServer` : un thread par requête, daemon non bloquant
- Mode async : subprocess background, détection du port avant retour
- `--force` : tue l'éventuel process existant sur le port avant démarrage
- `--dry-run` : bind le socket sans servir (utile pour les tests)

---

## Marquer une commande comme accessible

```python
from wexample_wex_core.decorator.webhook import webhook

@webhook()
@command(type=COMMAND_TYPE_ADDON, description="...")
def my__group__command(context: ExecutionContext) -> None:
    ...
```

Le décorateur `@webhook()` pose `webhook = True` sur le `CommandMethodWrapper`.
Le token doit ensuite être explicitement généré via `webhook/token-show`.

---

## Commandes disponibles

| Commande | Rôle |
|----------|------|
| `default::webhook/listen` | Démarrer le daemon |
| `default::webhook/stop` | Arrêter le daemon |
| `default::webhook/status` | État + dernières lignes de log |
| `default::webhook/exec` | Dispatcher interne (appelé par le daemon) |
| `default::webhook/token-show` | Afficher / générer le token d'une commande |
| `default::webhook/token-rotate` | Régénérer le token d'une commande |
