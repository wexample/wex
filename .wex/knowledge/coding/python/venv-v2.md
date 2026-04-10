# Virtual Environments — proposition v2 (uv)

## Principe

Remplacer `/etc/wex.conf` par une mécanique où le venv est toujours trouvé
de manière reproductible, sans config machine-specific manuelle.

## Outil : uv

`uv` remplace pip/pdm. Il gère un workspace monorepo avec un seul `uv.lock` et un seul venv.

```
wex-6/.venv/        ← venv unique (inchangé)
wex-6/uv.lock       ← source de vérité, commité dans git
wex-6/pyproject.toml ← déclare tous les packages membres du workspace
```

## Déclaration des packages (pyproject.toml racine)

```toml
[tool.uv.workspace]
members = [
    "../../PACKAGES/PYTHON/packages/app",
    "../../PACKAGES/PYTHON/packages/helpers",
    "../../PACKAGES/PYTHON/wex/wex-core",
    # ... tous les packages
]
```

Tous sont automatiquement installés en `-e` (editable) dans le venv partagé.

## Bootstrap nouvelle machine

```bash
cd wex-6
uv sync --all-packages   # recrée .venv depuis uv.lock, installe tout en -e
sudo bin/install         # installe wex dans /usr/local/bin
```

Pas de `/etc/wex.conf`. Le venv est toujours à `$(dirname $(readlink -f $(which wex)))/../../.venv`.

## app-manager

```bash
WEX_ROOT="$(cd "$(dirname "$(readlink -f "$(which wex")")")/../.." && pwd)"
VENV_PATH="$WEX_ROOT/.venv"
exec "$VENV_PATH/bin/python" "$AM_DIR/__main__.py" ...
```

## Avantages vs config actuelle

| | Actuel | v2 |
|---|---|---|
| Nouvelle machine | éditer `/etc/wex.conf` manuellement | `uv sync` |
| Versions reproductibles | non | oui (`uv.lock`) |
| `/etc/wex.conf` | requis | supprimé |
| Outil | pip/pdm mixte | uv seul |

## Risque / coût

Migration : réécrire le `pyproject.toml` racine, tester que tous les packages
s'installent proprement, mettre à jour les scripts `app-manager`.
Non trivial si beaucoup de dépendances croisées non déclarées.
