# Virtual Environments — config actuelle

## Venv partagé

Un seul venv pour tous les projets et packages, situé à :

```
wex-6/.venv/
```

Tous les packages wexample/syrtis sont installés en mode éditable (`-e`) dans ce venv.

## Localisation du venv par les scripts

Le binaire `wex` installé système (`/usr/local/bin/wex`) pointe vers `wex-6/bin/wex`.

Le script `app-manager` de chaque projet trouve le venv via `/etc/wex.conf` (hack temporaire) :

```
CORE_BIN=/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-6/bin/wex
```

## app-manager par projet

Chaque projet (manager, api, core…) a son propre `app_manager` dans `.wex/python/app_manager/`
avec son `__main__.py` et `pyproject.toml`. Le venv partagé est utilisé pour l'exécuter.

## Symlinks app-manager

- `syrtis/local/*` → `wex-6/.wex/bin/app-manager`
- Autres packages → `wex-addon-app/resources/app-manager.sh` (version modifiée, lit `/etc/wex.conf`)

## Problème ouvert

`/etc/wex.conf` est un hack machine-specific. Si le chemin vers `wex-6` change ou sur une nouvelle machine, il faut le mettre à jour manuellement.
