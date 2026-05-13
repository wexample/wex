# Variables d'environnement — wex

Topo complet de tous les mécanismes liés aux « env » dans le code. Plusieurs systèmes coexistent, avec des rôles distincts ou parfois redondants.

---

## TL;DR — les trois stockages physiques

| Fichier / source | Format | Portée | Gitignored | Usage canonique |
|---|---|---|---|---|
| `.wex/.env` | dotenv (`KEY=value`) | par projet | non (souvent commit) | `APP_ENV`, vars app non-sensibles |
| `.wex/local/env.yml` | YAML | par machine | oui (`.wex/local/` gitignored) | Secrets, sockets, tokens API, vars de dev |
| `os.environ` | — | process / shell | — | Hérité du shell + injecté par les deux ci-dessus au démarrage |

Tout le reste (mixins Python, décorateurs, commandes) n'est que **machinerie pour lire / écrire / valider** ces trois sources.

---

## 1. Couche Python — la famille `HasEnvKeys`

Mixins génériques, vivent dans `wexample_helpers` / `wexample_helpers_yaml`. Ils stockent les vars en mémoire dans un dict `env_config` porté par l'instance.

### `HasEnvKeys` (base)

`packages/helpers/src/wexample_helpers/classes/mixin/has_env_keys.py`

| Membre | Rôle |
|---|---|
| `env_config: dict[str, str \| None]` | Dict en mémoire, source de vérité pour cette instance |
| `get_env_parameter(key, default=UNSET)` | Lit dans `env_config` uniquement. **Ne lit pas `os.environ`.** Raise `KeyNotFoundError` si manquant et pas de `default` |
| `set_env_parameter(key, value)` / `set_env_parameters(dict)` | Écrit dans `env_config` (en mémoire seulement) |
| `get_expected_env_keys()` | À override : liste des clés requises pour cette classe |
| `_get_missing_env_keys(required)` | Compare aux clés requises **en regardant `os.environ` ET `env_config`** |
| `_init_env(env_dict)` | Remplace `env_config` puis valide |
| `_validate_env_keys()` | Raise `MissingRequiredEnvVarError` si une clé requise manque |

**Piège** : `get_env_parameter` ne regarde **pas** `os.environ`. Pour qu'une var du shell soit lisible via cette méthode, il faut qu'un autre mécanisme l'ait préalablement copiée dans `env_config`.

### `HasEnvKeysFile`

`packages/helpers/src/wexample_helpers/classes/mixin/has_env_keys_file.py`

Ajoute `_init_env_file(file_path)` :
1. `load_dotenv(file_path)` → vars **dans `os.environ`**
2. `dotenv_values(file_path)` → vars **dans `self.env_config`**
3. `_validate_env_keys()`

Format dotenv classique. Utilisé pour charger `.wex/.env`.

### `HasYamlEnvKeysFile`

`packages/helpers-yaml/src/wexample_helpers_yaml/classes/mixin/has_yaml_env_keys_file.py`

Variante YAML : charge un YAML, met les clés dans `env_config` ET propage dans `os.environ`.

### Extension : `get_env_parameter_or_suite_fallback`

`wex/wex-addon-app/src/wexample_wex_addon_app/workdir/mixin/with_suite_tree_workdir_mixin.py:106`

Lookup avec fallback sur la suite parente : si la var n'est pas trouvée dans le workdir courant, on remonte au `package_suite` parent. Utilisé pour des tokens partagés entre packages d'une même suite (CI vars, token PyPI…).

---

## 2. Couche kernel — initialisation au démarrage

`wex/wex-core/src/wexample_wex_core/common/kernel.py`

Le kernel orchestre, au démarrage (`setup()`), deux opérations sur les env :

### `_init_local_env()` — ligne 506

Lit `.wex/local/env.yml` du workdir courant via `get_local_data("env")` :
- Tout son contenu est **copié dans `kernel.env_config`**
- Tout son contenu est **propagé dans `os.environ`**

C'est le chemin par lequel un secret stocké en local devient disponible globalement dans le process.

### `_auto_detect_env()` — ligne 205

Pour chaque addon, regarde `addon.get_local_configurable_keys()` (liste de dicts `{key, description, detect, on_apply, default_candidates}`). Pour chaque entrée :

1. Si la var est déjà dans `os.environ` → on appelle juste `on_apply()` (effets de bord, ex. ajustement du `PATH`).
2. Sinon, si un callable `detect` est fourni, on l'appelle. Si on trouve une valeur :
   - Écrit dans `os.environ`
   - Écrit dans `.wex/local/env.yml` (persisté via `set_local_data("env", …)`)
   - Appel `on_apply()`

**Exemple** (`wex-addon-app/app_addon_manager.py:209`) :
```python
def get_local_configurable_keys(self) -> list[dict]:
    return [{
        "key": "SSH_AUTH_SOCK",
        "description": "SSH agent socket — required for git push/pull over SSH",
        "detect": detect_ssh_socket,
        "default_candidates": ["/run/user/1000/keyring/ssh", ...],
    }]
```

---

## 3. Couche commande — `core::env/configure`

`wex/wex-core/src/wexample_wex_core/addons/core/commands/env/configure.py`

Commande **interactive** qui parcourt les `get_local_configurable_keys()` de tous les addons et, pour chaque var manquante :
- Affiche la `description`
- Propose un `default_value` auto-détecté si un des `default_candidates` est un socket existant
- Prompte l'utilisateur
- Si une valeur est saisie : écrit dans `os.environ` + persiste dans `.wex/local/env.yml`

→ Même registre que `_auto_detect_env()` (mêmes clés), mais déclenché manuellement et explicite.

---

## 4. Couche app — `.wex/.env` (per-projet, `APP_ENV` et compagnie)

Fichier dotenv classique. Sa raison d'être historique : héberger `APP_ENV` (`local`, `dev`, `prod`…) et toute var spécifique au projet.

### Chargement

- Constante : `APP_PATH_ENV = WORKDIR_SETUP_DIR / ".env"` (`packages/app/src/wexample_app/const/globals.py:16`)
- Lu par le workdir via `HasEnvKeysFile._init_env_file`
- Référence : `core_yaml_command_runner.py:36` — `.wex/.env` est utilisé comme **base de variables** pour la substitution dans les scripts YAML, surchargée par `os.environ`, surchargée par les options de commande.

### Commandes dédiées (`wex-addon-app`)

| Commande | Action |
|---|---|
| `app::env/set` | Définit `APP_ENV` dans `.wex/.env` |
| `app::env/get` | Lit `APP_ENV` depuis `.wex/.env` |
| `app::env/var_set` | Set une var arbitraire dans `.wex/.env` |
| `app::env/var_get` | Get une var depuis `.wex/.env` |
| `app::env/var_list` | Liste toutes les vars de `.wex/.env` |

### Accès par code

`managed_workdir.py:240` :
```python
def get_app_env(self) -> str | None:
    # APP_ENV is always set via .wex/.env — never in config.yml
    return self.get_env_parameter("APP_ENV") or ENV_NAME_PROD
```

---

## 5. Couche `local/` — `WithLocalDataMixin` (généralisation)

`packages/app/src/wexample_app/workdir/mixin/with_local_data_mixin.py`

`.wex/local/env.yml` n'est qu'**un namespace parmi d'autres** dans `.wex/local/`. Le mixin offre un stockage YAML générique :

```
.wex/local/
├── env.yml                # namespace "env"
├── webhook_tokens.yml     # namespace "webhook_tokens"
└── webhook_tokens_addon.yml
```

API : `get_local_data(ns)`, `set_local_data(ns, data)`, `get_local_data_value(ns, key)`, `set_local_data_value(ns, key, value)`, `ensure_local_token(ns, key)`, `rotate_local_token(ns, key)`.

Toute la couche kernel pour les env (`_init_local_env`, `_auto_detect_env`) utilise simplement `get_local_data("env")` / `set_local_data("env", …)`.

---

## 6. Cas particulier — `@require_app_config` (pour `config.yml`, pas pour les env)

`wex/wex-addon-app/src/wexample_wex_addon_app/decorator/require_app_config.py`

**N'agit pas sur les vars d'env**, mais sur les clés de `config.yml`. Mentionné ici parce que c'est l'autre mécanisme « check une config en amont, demande à l'utilisateur si manquante, persiste ».

```python
@require_app_config(
    path="git.publication_strategy",
    type=str,
    values=["main_push", "branch_merge"],
    description="Publication strategy",
    ask_question="Which publication strategy should be used?",
    on_missing="ask",   # "error" | "ask"
)
```

Comportement :
- Si la clé existe dans `config.yml` → validation (présence dans `values` si fourni)
- Sinon, si un `default` est passé → écrit silencieusement dans `config.yml`
- Sinon, `on_missing="ask"` → prompt utilisateur, persiste dans `config.yml`
- Sinon, `on_missing="error"` → raise `ValueError`

Le check tourne **avant** l'exécution de la commande, donc plus de surprise au milieu d'un pipeline.

---

## 7. Substitution dans les scripts YAML

`wex/wex-core/src/wexample_wex_core/runner/core_yaml_command_runner.py:_build_variables`

Quand une commande YAML s'exécute, le runner construit un dict `variables` par ordre de priorité croissante :

1. **Plus bas** : `.wex/.env` du `call_workdir` (où `wex` a été invoqué)
2. `os.environ` (qui inclut déjà `.wex/local/env.yml` chargé par `_init_local_env`)
3. Built-ins (`PATH_CURRENT`, etc.)
4. **Plus haut** : options passées à la commande (`--key=value`)

Donc dans un YAML, `${VAR}` résout dans cet ordre.

---

## 8. Tableau de décision — où ranger quoi ?

| Type de donnée | Stockage | Comment l'écrire |
|---|---|---|
| `APP_ENV` (local / prod / …) | `.wex/.env` | `wex app::env/set <env>` |
| Var d'app non sensible (URL d'un service interne, port…) | `.wex/.env` | `wex app::env/var_set KEY value` |
| Secret machine (token API GitLab/GitHub, mot de passe registry…) | `.wex/local/env.yml` | `wex core::env/configure` ou édition manuelle |
| Socket / chemin machine (`SSH_AUTH_SOCK`, etc.) | `.wex/local/env.yml` | Auto-détecté au `setup()`, ou `wex core::env/configure` |
| Choix structurel du projet (stratégie de publication, branche principale…) | `config.yml` | `@require_app_config` au niveau commande |
| Token webhook tournant | `.wex/local/{namespace}.yml` | `rotate_local_token()` |

---

## 9. État des lieux — ce qui marche, ce qui pue

### Justifié et propre

- Pile `HasEnvKeys` / `HasEnvKeysFile` / `HasYamlEnvKeysFile` : utilitaires génériques, pas de redondance entre eux.
- Trio `_init_local_env` / `_auto_detect_env` / `core::env/configure` : cohérent, mêmes clés (`get_local_configurable_keys`), trois moments d'usage (auto au démarrage, auto-détection passive, interactif).
- `@require_app_config` : périmètre clair (`config.yml` uniquement), pré-check propre.
- `WithLocalDataMixin` : abstraction propre pour tout `.wex/local/*.yml`.

### Sources de confusion

- **Deux fichiers, deux formats** pour des env :
  - `.wex/.env` (dotenv) pour le projet
  - `.wex/local/env.yml` (YAML) pour la machine
  
  Cohabitent légitimement (portées différentes), mais c'est facile de se tromper. Les messages d'erreur doivent pointer **vers le bon**.

- **`get_env_parameter` ne lit pas `os.environ`** directement, seulement `env_config`. Une var purement shell (sans passage par un init) n'est pas visible via cette méthode. Toute classe qui veut « la var où qu'elle soit » doit s'assurer que `_init_env_file` ou `_init_local_env` a tourné en amont.

- **Aucun usage formel de `get_expected_env_keys()`** dans les workdirs principaux : la validation `_validate_env_keys()` n'est appelée qu'au moment des `_init_*`, donc rate les besoins exprimés plus tard dans le code.

- **Les checks de présence sont parfois trop tardifs** : un token absent peut n'être détecté qu'au milieu d'une commande long-running (cf. `branch_merge_publication_strategy` qui découvrait le token manquant à l'étape 7/7 d'un release). Solution : déclarer la var dans `get_local_configurable_keys()` de l'addon, **ou** ajouter un `@require_app_config` sur la commande (pour le nom de var, à défaut de la valeur elle-même).

### Anti-pattern à éviter

- `os.environ.get(...)` **directement** dans une méthode de classe. Toujours passer par `self.get_env_parameter()` pour respecter la chaîne `env_config` (et permettre l'override en test, le fallback suite, etc.).
- Pointer vers `.wex/.env` dans un message d'erreur pour un **secret machine**. Le secret va dans `.wex/local/env.yml` (via `core::env/configure`).
