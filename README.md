# wex

Version: 6.0.57

## Table of Contents

- [Introduction](#introduction)
- [Testing](#testing)
- [Webhooks](#webhooks)

## Check Wex Installation

Test if the core command works using these methods:

```bash
# Once installed globally
wex hi  # Returns "hi!"

# From wex directory (no global install required)
bash bin/wex hi  # Returns "hi!"
```

### Using Command

Execute all tests including core and every addon tests suite.

```bash
# Run all tests with integrated logging
bash bin/wex test::run/all
```

### Using Pytest Directly

Basic command to test only core tests.

```bash
# Run all tests
pytest

# Or using Python module
python -m pytest
```

## Testing

This project uses pytest for unit and integration testing. You can run tests using either the built-in WEX command or
pytest directly.

## Test Structure

```
tests/
├── unit/           # Unit tests (test individual components)
│   └── test_example.py
├── integration/    # Integration tests (test component interactions)
└── conftest.py     # Shared fixtures (create as needed)
```

# Système Webhook — wex

Expose des commandes wex via HTTP pour les déclencher depuis un CI/CD, un serveur distant,
ou tout outil capable de faire une requête GET.

**URL type :** `http://host:7654/webhook/{type}/{command/path}?_token=<token>&arg=val`

---

## Prise en main rapide

### 1. Démarrer le daemon

```bash
# En arrière-plan
wex core::webhook/listen --asynchronous

# En avant-plan (pour débugger)
wex core::webhook/listen

# Forcer le redémarrage si le port est déjà occupé
wex core::webhook/listen --asynchronous --force
```

### 2. Vérifier que le daemon tourne

```bash
wex core::webhook/status

# Ou directement via HTTP (pas d'auth sur /health)
curl http://localhost:7654/health
# → {"status": "ok", "uptime_seconds": 42}
```

### 3. Créer un token pour une commande app

Les tokens sont stockés **dans l'app**, pas de façon centrale.
Il faut créer le fichier manuellement avec sudo :

```bash
sudo mkdir -p /var/www/{env}/{app}/.wex/local
python3 -c "import secrets; print(secrets.token_hex(32))"
# → copier le token généré

# Écrire le fichier (clé = commande locale sous forme point)
echo "'.release/deploy': '<token>'" | sudo tee /var/www/{env}/{app}/.wex/local/webhook_tokens.yml
```

### 4. Appeler le webhook

```bash
# Token en query param
curl "http://localhost:7654/webhook/app/prod/myapp/release/deploy?_token=<token>"

# Token en header
curl -H "Authorization: Bearer <token>" \
     "http://localhost:7654/webhook/app/prod/myapp/release/deploy"

# Avec des arguments
curl "http://localhost:7654/webhook/app/prod/myapp/release/deploy?_token=<token>&env=prod"
```

### 5. Consulter les logs

```bash
# Dernières requêtes
wex core::webhook/status

# Log brut (JSON, une ligne par requête)
tail -f {workdir}/logs/webhook.log
```

### 6. Arrêter le daemon

```bash
wex core::webhook/stop
```

---

## Architecture

### Placement

- **`wex-core`** : daemon, handler HTTP, routing, `@webhook` decorator, commandes `webhook/*`
- **`wex-addon-app`** : commandes `remote/*`, intégration AppMiddleware

### Types d'URL supportés

| URL | Commande exécutée |
|-----|-------------------|
| `/webhook/app/prod/myapp/release/deploy` | `.release/deploy` dans `/var/www/prod/myapp` |
| `/webhook/app/prod/myapp/apt/publish` | `.apt/publish` dans `/var/www/prod/myapp` |

Seul le type `app` est supporté actuellement. Les types `addon` et `service` sont prévus.

### Sécurité

Chaque app gère ses propres tokens dans `{app_path}/.wex/local/webhook_tokens.yml`.

- Transmis via `Authorization: Bearer <token>` ou `?_token=<token>`
- Comparaison en temps constant (`hmac.compare_digest`)
- Absent ou invalide → 401, loggué avec IP + path
- `/health` est exempt d'authentification

### Token — format du fichier

```yaml
'.release/deploy': 'abc123...'
'.apt/publish': 'def456...'
```

La clé est la commande locale (préfixe `.`), la valeur est un hex 32 bytes (`secrets.token_hex(32)`).

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

```yaml
# .wex/commands/release/deploy.yml
decorators:
- name: webhook
- name: sudo
scripts:
  ...
```

En Python :

```python
from wexample_wex_core.decorator.webhook import webhook

@webhook()
@command(type=COMMAND_TYPE_ADDON, description="...")
def my__group__command(context: ExecutionContext) -> None:
    ...
```

Le décorateur `@webhook()` pose `webhook = True` sur le `CommandMethodWrapper`.

---

## Commandes disponibles

| Commande | Rôle |
|----------|------|
| `core::webhook/listen` | Démarrer le daemon |
| `core::webhook/stop` | Arrêter le daemon |
| `core::webhook/status` | État + dernières lignes de log |
| `core::webhook/exec` | Dispatcher interne (appelé par le daemon) |
