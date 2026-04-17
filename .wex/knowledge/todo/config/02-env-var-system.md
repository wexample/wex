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

## Tâches

### Étendre le pattern de déclaration des env vars

- [ ] Créer une dataclass `EnvVarSpec` dans `packages/helpers/src/wexample_helpers/const/env.py`
  - Champs : `key: str`, `description: str`, `required: bool = True`, `default: str | None = None`
- [ ] Modifier `get_expected_env_keys()` → accepter optionnellement une liste de `EnvVarSpec` (compatibilité rétrograde avec `list[str]`)
- [ ] Modifier `_validate_env_keys()` → utiliser `EnvVarSpec` pour afficher description + valeur par défaut si disponible

### Permettre aux addons de déclarer leurs env vars

- [ ] Créer un mixin `HasAddonEnvKeys` pour les addons wex
  - Méthode `get_addon_expected_env_keys()` → `list[EnvVarSpec]`
- [ ] Le kernel collecte les déclarations de tous les addons chargés au boot
  - Dans `Kernel._init_addons()` ou un nouveau `_collect_env_requirements()`
- [ ] Fusionner et valider l'ensemble des déclarations

### Support de la config locale `.wex/local/`

- [ ] Définir le format : `.wex/local/env.yaml` (par machine, gitignored)
  ```yaml
  SSH_AUTH_SOCK: /run/user/1000/keyring/ssh
  MY_CUSTOM_VAR: value
  ```
- [ ] Charger `.wex/local/env.yaml` dans `AbstractKernel.setup()` après les autres env files
- [ ] Les valeurs de `.wex/local/env.yaml` peuvent satisfaire les `EnvVarSpec` requis

### Déclaration SSH dans `helpers-git`

- [ ] Créer `packages/helpers-git/src/wexample_helpers_git/const/env.py`
  ```python
  SSH_AUTH_SOCK_SPEC = EnvVarSpec(
      key="SSH_AUTH_SOCK",
      description="Path to SSH agent socket. Required for git push/pull via SSH.",
      required=False,  # warn seulement, auto-détection possible
  )
  ```
- [ ] `HasSshCheck` (niveau 1) déclare `SSH_AUTH_SOCK_SPEC` via `get_addon_expected_env_keys()`

### Documentation et guidage utilisateur

- [ ] Message d'erreur enrichi quand une var est manquante :
  - Afficher description de la var
  - Afficher commande pour la setter dans `.wex/local/env.yaml`
  - Afficher valeur détectée automatiquement si applicable

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
