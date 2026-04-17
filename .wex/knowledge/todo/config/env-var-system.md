# Niveau 2 — Système structuré de gestion des variables d'env

Étendre le système existant `get_expected_env_keys()` pour permettre aux addons
et features de déclarer leurs propres variables requises, avec support
de la config locale `.wex/local/`.

---

## Contexte actuel

Le système existe déjà mais est rudimentaire :
- `HasEnvKeys` mixin → `get_expected_env_keys()` retourne `[]`
- `AbstractKernel` surcharge → retourne `["APP_ENV"]` seulement
- `_validate_env_keys()` vérifie `os.environ` et `self.env_config`
- `.wex/local/` existe dans plusieurs packages mais ne contient que des `.gitkeep`

---

## ✅ Fait

- `_init_env_file_yaml()` injecte dans `os.environ` (les subprocesses héritent maintenant)
- `Kernel._init_local_env()` charge `.wex/local/env.yml` dans `os.environ` + `env_config`

## ⬜ YAGNI — supprimé du scope

- `EnvVarSpec` dataclass — aucun addon ne déclare de vars aujourd'hui
- `HasAddonEnvKeys` mixin — idem
- Collecte des env vars des addons au boot

---

## Fichiers concernés

| Fichier | Action |
|---|---|
| `packages/helpers/src/wexample_helpers/classes/mixin/has_env_keys.py` | Étendre avec `EnvVarSpec` |
| `packages/app/src/wexample_app/common/abstract_kernel.py` | Charger `.wex/local/env.yaml` |
| `wex/wex-core/src/wexample_wex_core/common/kernel.py` | Collecter env vars des addons |
| `packages/helpers-git/src/wexample_helpers_git/const/env.py` | Nouveau — specs SSH |

---

## Contraintes

- Rétrocompatible : `get_expected_env_keys()` retournant `list[str]` doit continuer à fonctionner
- `.wex/local/` doit être dans `.gitignore` de chaque package qui l'utilise
- Les addons ne doivent pas avoir à connaître le kernel directement pour déclarer leurs vars
