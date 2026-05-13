# Variables d'environnement — wex

Topo complet de tous les mécanismes liés aux « env » dans le code. Plusieurs systèmes coexistent, chacun avec un rôle propre — ils ne se recouvrent pas.

---

## Avant tout — deux univers distincts à ne pas confondre

1. **`os.environ`** — l'espace de variables d'environnement **POSIX du process**, hérité du shell parent. Géré par le système d'exploitation, pas par wex. On y touche **uniquement** quand on lit une var qu'on sait être OS-level (`SSH_AUTH_SOCK`, `SUDO_UID`, `PATH`, etc.). **Ce n'est pas le sujet de cette doc.**

2. **« env » au sens wex** — les **fichiers de config d'environnement** déclarés à la racine d'un projet (équivalent du `.env` Symfony). Aujourd'hui deux fichiers cohabitent, fonctionnellement convergents (cf. section 8).

Toute la machinerie décrite ci-dessous (`HasEnvKeys`, `get_env_parameter`, etc.) parle **uniquement** de l'univers 2. Si du code fait `os.environ.get(...)`, c'est qu'il lit une vraie var POSIX, pas une config wex — ce qui doit être **commenté explicitement**.

---

## TL;DR — les deux fichiers de config d'env wex

| Fichier | Format | Édité par | Contenu observé en pratique |
|---|---|---|---|
| `.wex/.env` | dotenv (`KEY=value`) | `app::env/var_set`, `app::env/set` | `APP_ENV`, tokens (`GITLAB_API_TOKEN`, `GITHUB_API_TOKEN`, `PIPY_TOKEN`), chemins locaux |
| `.wex/local/env.yml` | YAML | `core::env/configure`, `kernel._auto_detect_env` | Sockets et chemins auto-détectés (`SSH_AUTH_SOCK`, `PDM_BIN_DIR`) |

Les deux finissent dans `kernel.env_config` + `os.environ` après init. La séparation actuelle est un accident d'historique (dotenv v1 → YAML v2), pas une vraie séparation de responsabilités.

Tout le reste (mixins Python, décorateurs, commandes) n'est que **machinerie pour lire / écrire / valider** ces deux fichiers.

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

`.wex/local/env.yml` n'est **pas un fichier spécial réservé au core wex** : c'est juste le namespace `env` dans le système générique `.wex/local/{namespace}.yml`. Le mixin vit dans `wexample_app` et est accessible à n'importe quel code via `get_local_data("env")` / `set_local_data("env", …)`.

Ce qui rend ce namespace particulier, c'est uniquement que **`kernel._init_local_env()` le charge dans `os.environ` au démarrage**. Les autres namespaces (`webhook_tokens.yml`, etc.) n'ont pas ce traitement — ils restent du stockage YAML pur.

```
.wex/local/
├── env.yml                # namespace "env"  (chargé dans os.environ au boot)
├── webhook_tokens.yml     # namespace "webhook_tokens"
└── webhook_tokens_addon.yml
```

API : `get_local_data(ns)`, `set_local_data(ns, data)`, `get_local_data_value(ns, key)`, `set_local_data_value(ns, key, value)`, `ensure_local_token(ns, key)`, `rotate_local_token(ns, key)`.

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

## 8. État de l'art — fusion en cours, convention à finaliser

**Constat factuel** sur le contenu réel des projets (audit du `2026-05-13`) :

- `.wex/.env` contient : `APP_ENV`, `GITLAB_API_TOKEN`, `GITHUB_API_TOKEN`, `PIPY_TOKEN`, `LOCAL_*` chemins
- `.wex/local/env.yml` contient : `SSH_AUTH_SOCK`, `PDM_BIN_DIR`

**Aucun des deux fichiers** n'utilise les structures complexes du YAML — tout est `KEY: value` plat. L'argument historique « YAML pour structures complexes » n'est pas vérifié.

**Différence fonctionnelle qui reste à préserver** : le YAML runner (`core_yaml_command_runner._build_variables`) lit `.wex/.env` du `call_workdir` comme source de substitution `${VAR}` dans les scripts. Si on fusionne sur YAML, le runner doit aussi lire le YAML.

**Direction prévue** (cf. roadmap `env.md`) : fusion sur `.wex/local/env.yml` (YAML, dans `local/` gitignored). Format YAML choisi pour cohérence avec le reste de la stack wex (`config.yml`, `suite.yml`). JSON écarté (pas de commentaires, lisibilité humaine pauvre), TOML écarté (cohérence stack > optimisation marginale).

### Tableau de décision provisoire (avant fusion)

| Type de donnée | Stockage actuel | Comment l'écrire |
|---|---|---|
| `APP_ENV` (local / prod / …) | `.wex/.env` | `wex app::env/set <env>` |
| Var d'app non sensible (URL d'un service interne, port…) | `.wex/.env` | `wex app::env/var_set KEY value` |
| Secret machine (token API, mot de passe registry…) | `.wex/.env` (en pratique) ou `.wex/local/env.yml` (souhaitable) | `wex app::env/var_set` ou `wex core::env/configure` |
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

- **Deux fichiers pour le même job** : `.wex/.env` (dotenv v1) et `.wex/local/env.yml` (YAML v2). En pratique fonctionnellement convergents — les deux finissent dans `os.environ` après init, aucun ne profite des structures complexes. À fusionner (cf. roadmap `env.md`).

- **`get_env_parameter()` est volontairement séparé de `os.environ`.** Il renvoie la **config d'env wex** (chargée depuis les fichiers ci-dessus), pas une var système POSIX. Pour lire une var OS-level (`SSH_AUTH_SOCK`, `SUDO_UID`, etc.), on utilise `os.environ.get()` explicitement, avec un commentaire qui justifie le choix.

- **Aucun usage formel de `get_expected_env_keys()`** dans les workdirs principaux : la validation `_validate_env_keys()` n'est appelée qu'au moment des `_init_*`, donc rate les besoins exprimés plus tard dans le code.

- **Les checks de présence sont parfois trop tardifs** : un token absent peut n'être détecté qu'au milieu d'une commande long-running (cf. `branch_merge_publication_strategy` qui découvrait le token manquant à l'étape 7/7 d'un release). Solution prévue : décorateur `@require_local_env` (roadmap), bloqué tant que le ménage des fichiers n'est pas fait.

### Anti-pattern à éviter

- Confondre « env » au sens wex (config projet) avec `os.environ` (espace POSIX). Ce sont **deux univers distincts**.
- Lire une var de config wex via `os.environ.get()` dans une méthode de classe → toujours `self.get_env_parameter()`.
- Lire une var OS-level via `self.get_env_parameter()` → utiliser `os.environ.get()` avec un commentaire qui dit pourquoi.
- Pointer vers `.wex/.env` dans un message d'erreur pour un **secret machine**. Le secret va dans `.wex/local/env.yml` (via `core::env/configure`).
