# Virtual Environments

## Principe : un seul venv partagé

Tous les projets et packages utilisent un unique venv situé à :

```
wex-6/.venv/
```

Tous les packages wexample sont installés en mode éditable (`-e`) dans ce venv.
Cela évite la multiplication des venvs (un par projet = cauchemar IDE + disque),
et permet aux packages de se référencer mutuellement sans config spéciale.

---

## app-manager : deux racines distinctes

Chaque projet a son propre code `app_manager` dans `.wex/python/app_manager/`,
mais le Python qui l'exécute vient toujours du venv partagé de wex-6.

Le script `wex-6/.wex/bin/app-manager` gère ça avec deux variables séparées :

```bash
# Résout le symlink → donne toujours wex-6, quel que soit le projet appelant
SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
WEX_ROOT="$(cd "$(dirname "$SCRIPT_REAL")/../.." && pwd)"

# Ne résout PAS le symlink → donne le projet appelant (manager, api, network…)
APP_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AM_DIR="$APP_ROOT/.wex/python/app_manager"
```

- `WEX_ROOT` → racine de wex-6 → `$WEX_ROOT/.venv/bin/python` (venv partagé)
- `APP_ROOT` → racine du projet appelant → `AM_DIR` pointe vers son `app_manager`

---

## Symlinks app-manager

Les projets ne contiennent pas le script `app-manager`, ils ont un symlink vers wex-6 :

```
projet/.wex/bin/app-manager -> wex-6/.wex/bin/app-manager
```

C'est ce comportement symlink (non résolu) qui permet à `APP_ROOT` de pointer
vers le bon projet appelant.

---

## Prérequis pour qu'un projet fonctionne

Chaque projet doit avoir son répertoire `app_manager` initialisé :

```
projet/.wex/python/app_manager/
    __main__.py      ← déclare les addons wex à charger
    pyproject.toml   ← dépendances du projet
```

Ce répertoire est créé par la commande d'init wex-6 (checkup/setup).
Sans lui, l'app-manager plante même si le venv partagé est en place.

---

## Contextes dev vs déploiement

**Dev (machine locale) :**
- wex-6 accédé via son chemin complet ou un alias, pas via `which wex` (qui pointe encore sur wex-5 legacy)
- Le venv partagé est alimenté manuellement avec les packages en `-e`
- `/etc/wex.conf` peut exister comme outil pratique local, mais n'est pas requis par le système

**Déploiement (apt ou autre) :**
- wex-6 installé proprement, `which wex` pointe dessus
- Le venv est créé par le postinstall du package
- Pas de `/etc/wex.conf`, pas de chemins hardcodés — `readlink -f` suffit
