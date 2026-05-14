# Variables d'environnement — wex

Topo complet de tous les mécanismes liés aux « env » dans le code. Plusieurs systèmes coexistent, chacun avec un rôle propre — ils ne se recouvrent pas.

---

## Avant tout — distinguer ce qui est wex de ce qui ne l'est pas

### Hors périmètre wex

1. **`os.environ`** — espace POSIX du process, hérité du shell parent. Géré par l'OS. On y touche **uniquement** quand on lit une var qu'on sait être OS-level (`SSH_AUTH_SOCK`, `SUDO_UID`, `PATH`, etc.). **Pas le sujet de cette doc.**

2. **Scope applicatif — `<projet_user>/.env`** à la racine du projet. Équivalent du `.env` Symfony : consommé directement par l'application elle-même (PHP, Python, Docker compose, runtime…). **Wex ne le lit jamais.** Le projet le gère lui-même, et peut d'ailleurs utiliser n'importe quel nom de fichier (`.env`, `.env.local`, `.trilili-vars`, etc.) — c'est l'app qui décide.

### Périmètre wex (2 scopes, YAML partout)

3. **Scope install wex — `<install_wex>/.env.yml`.** Config **globale du runtime wex**, à la racine de l'installation (`local/wex/`). Chargée au boot par `AbstractKernel._init_env_file_yaml`. Wex étant lui-même un projet python, son `APP_ENV` vit ici, ainsi que toute config globale du runtime (chemins, structures complexes…).

4. **Scope projet (machine-local) — `<projet_user>/.wex/local/env.yml`.** Config wex **par projet, par machine** (gitignored). Lue par `WithEnvParametersMixin` et `kernel._init_local_env`. Contient typiquement `APP_ENV` du projet, tokens API, chemins locaux, sockets, etc. Rempli par les commandes `app::env/*`, `core::env/configure`, ou auto-détecté par les addons.

> **Note legacy** : avant la migration `wex 6.0.26`, le scope projet vivait dans `<projet>/.wex/.env` (dotenv). Ces fichiers existent encore physiquement sur les projets non encore migrés, mais ne sont **plus lus** par wex. Une migration de cleanup les supprimera dans ~1 an.

⚠️ **Piège de naming** : `WithEnvParametersMixin` porte un nom générique. Il gère en réalité le scope projet (`<workdir>/.wex/local/env.yml`). À renommer (`WithSetupEnvParameterMixin`, cf. roadmap).

---

## TL;DR — les deux fichiers du périmètre wex

| Fichier | Scope | Format | Géré par |
|---|---|---|---|
| `<install_wex>/.env.yml` | Install (config runtime wex) | YAML | `AbstractKernel._init_env_file_yaml` |
| `<projet>/.wex/local/env.yml` | Projet, machine-local | YAML | `WithEnvParametersMixin` + `kernel._init_local_env` + `WithLocalDataMixin` |

Les deux sont chargés au boot par le kernel et alimentent `kernel.env_config` + `os.environ`. **YAML partout**, plus de dotenv côté wex.

> Les fichiers `.env` à la racine d'un projet utilisateur restent du ressort de l'application elle-même (Symfony, runtime…). Wex ne les lit jamais.

---

## 1. Couche Python — la famille `HasEnvKeys`

Mixins génériques, vivent dans `wexample_helpers` / `wexample_helpers_yaml`. Ils stockent les vars en mémoire dans un dict `env_config` porté par l'instance.

### `HasEnvKeys` (base)

`packages/helpers/src/wexample_helpers/classes/mixin/has_env_keys.py`

| Membre | Rôle |
|---|---|
| `env_config: dict[str, str \| None]` | Dict en mémoire, source de vérité pour cette instance |
| `get_env_parameter(key, default=UNSET)` | Lit dans `env_config` uniquement (volontaire : voir « À retenir » plus bas). Raise `KeyNotFoundError` si manquant et pas de `default` |
| `set_env_parameter(key, value)` / `set_env_parameters(dict)` | Écrit dans `env_config` (en mémoire seulement) |
| `get_expected_env_keys()` | À override : liste des clés requises pour cette classe |
| `_get_missing_env_keys(required)` | Compare aux clés requises **en regardant `os.environ` ET `env_config`** |
| `_init_env(env_dict)` | Remplace `env_config` puis valide |
| `_validate_env_keys()` | Raise `MissingRequiredEnvVarError` si une clé requise manque |

**À retenir** :
- `get_env_parameter()` (sur le mixin de base) ne renvoie que ce qu'il y a dans `env_config`. Il ne lit pas `os.environ` — c'est volontaire, les deux univers sont séparés. Les sous-classes (`WithEnvParametersMixin`, etc.) peuvent étendre la lecture vers d'autres sources.
- **`get_expected_env_keys()` est le mécanisme officiel de centralisation** des vars requises pensé pour irriguer toute l'app. À override sur chaque classe qui dépend d'une var d'env. Aujourd'hui sous-utilisé (seul `AbstractKernel` déclare `["APP_ENV"]`), mais l'intention de design est de l'employer partout — pas de le contourner avec des `os.environ.get()` ad hoc. Validation au boot via `_validate_env_keys()`, et liste exposée par la commande `core::health/check`.

### `HasEnvKeysFile`

`packages/helpers/src/wexample_helpers/classes/mixin/has_env_keys_file.py`

Ajoute `_init_env_file(file_path)` :
1. `load_dotenv(file_path)` → vars **dans `os.environ`**
2. `dotenv_values(file_path)` → vars **dans `self.env_config`**
3. `_validate_env_keys()`

Format dotenv classique.

### `HasYamlEnvKeysFile`

`packages/helpers-yaml/src/wexample_helpers_yaml/classes/mixin/has_yaml_env_keys_file.py`

Variante YAML : charge un YAML, met les clés dans `env_config` ET propage dans `os.environ`.

### À retenir sur ces deux mixins

**Un seul consommateur** : `AbstractKernel`. Aucun workdir, aucun addon n'utilise `_init_env_file` ou `_init_env_file_yaml` ailleurs. Les workdirs lisent leur `.wex/.env` via un mécanisme parallèle (`WithEnvParametersMixin`, ci-dessous), pas via cette chaîne.

### `WithEnvParametersMixin` — accès workdir vers `.wex/.env`

`packages/app/src/wexample_app/workdir/mixin/with_env_parameters_mixin.py`

Hérite de `HasEnvKeys`. Spécialise `get_env_parameter()` pour qu'il :
1. Lise **d'abord directement le fichier `.wex/local/env.yml`** via `YamlFile.create_from_path()`
2. Tombe en fallback sur `super().get_env_parameter()` (donc `env_config`)

Fournit aussi `set_env_parameters(dict)` qui **écrit dans `.wex/local/env.yml`** (en plus de mettre à jour `env_config`).

**Naming trompeur** : le nom suggère un mixin générique d'env, mais le chemin construit est `path / ".wex" / "local" / "env.yml"`. C'est en fait le mixin du **scope projet wex** (machine-local), pas du scope applicatif. À renommer (`WithSetupEnvParameterMixin`, cf. roadmap).

### Extension : `get_env_parameter_or_suite_fallback`

`wex/wex-addon-app/src/wexample_wex_addon_app/workdir/mixin/with_suite_tree_workdir_mixin.py:106`

Lookup avec fallback sur la suite parente : si la var n'est pas trouvée dans le workdir courant, on remonte au `package_suite` parent. Utilisé pour des tokens partagés entre packages d'une même suite (CI vars, token PyPI…).

---

## 2. Couche kernel — initialisation au démarrage

`packages/app/src/wexample_app/common/abstract_kernel.py` + `wex/wex-core/src/wexample_wex_core/common/kernel.py`

Le kernel orchestre, au démarrage (`setup()`), **trois** opérations sur les env :

### `AbstractKernel.setup()` — `.env.yml` de l'install

`abstract_kernel.py` :
```python
env_dir_path = Path(self.entrypoint_path).parent  # par défaut
self._init_env_file_yaml(env_dir_path / FILE_NAME_ENV_YAML)  # .env.yml
```

`entrypoint_path` est défini à l'instanciation du kernel par `__main__.py` :
```python
Wex(entrypoint_path=__file__).exec()
```

Donc `entrypoint_path.parent` = **racine de l'installation wex** (ex. `local/wex/`). C'est là que vit le `.env.yml` (config globale du runtime). Avant la migration 6.0.26, un `.env` (dotenv) était aussi chargé à ce niveau ; il a été retiré au profit du YAML uniquement.

### `Kernel._init_local_env()` — ligne 506

Lit `.wex/local/env.yml` du workdir courant via `get_local_data("env")` :
- Tout son contenu est **copié dans `kernel.env_config`**
- Tout son contenu est **propagé dans `os.environ`**

C'est le chemin par lequel un secret stocké en local devient disponible globalement dans le process.

### `Kernel._auto_detect_env()` — ligne 205

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

## 4. Couche app — `.wex/local/env.yml` (per-projet, `APP_ENV` et compagnie)

Fichier YAML, gitignored. Héberge `APP_ENV` (`local`, `dev`, `prod`…) et toute var spécifique au projet (tokens API, chemins locaux, etc.).

> **Legacy** : le fichier dotenv `.wex/.env` existait avant la migration 6.0.26. Il n'est plus lu — ses contenus sont copiés vers `.wex/local/env.yml` par la migration. Le `.env` reste sur disque tant qu'une migration de cleanup ne l'a pas supprimé (~1 an).

### Chargement

- Chemin : `<projet>/.wex/local/env.yml`
- Lu directement par `WithEnvParametersMixin` (qui hérite de `HasEnvKeys`)
- Aussi propagé dans `os.environ` au boot par `kernel._init_local_env()` (via `WithLocalDataMixin`)
- Référence : `core_yaml_command_runner._build_variables` utilise ce fichier comme **base de variables** pour la substitution dans les scripts YAML, surchargée par `os.environ`, surchargée par les options de commande.

### Commandes dédiées (`wex-addon-app`)

| Commande | Action |
|---|---|
| `app::env/set` | Définit `APP_ENV` dans `.wex/local/env.yml` |
| `app::env/get` | Lit `APP_ENV` depuis `.wex/local/env.yml` |
| `app::env/var_set` | Set une var arbitraire dans `.wex/local/env.yml` |
| `app::env/var_get` | Get une var depuis `.wex/local/env.yml` |
| `app::env/var_list` | Liste toutes les vars de `.wex/local/env.yml` |

### Accès par code

`managed_workdir.py` :
```python
def get_app_env(self) -> str | None:
    # APP_ENV is always set via .wex/local/env.yml — never in config.yml
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

1. **Plus bas** : `.wex/local/env.yml` du `call_workdir` (où `wex` a été invoqué)
2. `os.environ` (qui inclut déjà `<install_wex>/.env.yml` et `.wex/local/env.yml` chargés au boot)
3. Built-ins (`PATH_CURRENT`, etc.)
4. **Plus haut** : options passées à la commande (`--key=value`)

Donc dans un YAML, `${VAR}` résout dans cet ordre.

---

## 8. Tableau de décision — où ranger quoi

Post-migration `wex 6.0.26` — **YAML partout** côté wex.

| Type de donnée | Stockage | Comment l'écrire |
|---|---|---|
| `APP_ENV` du runtime wex (l'install) | `<install_wex>/.env.yml` | Édition manuelle |
| Config globale du runtime wex (chemins, structures complexes) | `<install_wex>/.env.yml` | Édition manuelle |
| `APP_ENV` du projet | `<projet>/.wex/local/env.yml` | `wex app::env/set <env>` |
| Var d'app non sensible (URL service, port…) | `<projet>/.wex/local/env.yml` | `wex app::env/var_set KEY value` |
| Secret machine (token API, mot de passe registry…) | `<projet>/.wex/local/env.yml` | `wex app::env/var_set` ou `wex core::env/configure` |
| Socket / chemin machine (`SSH_AUTH_SOCK`…) | `<projet>/.wex/local/env.yml` | Auto-détecté au boot, ou `wex core::env/configure` |
| Choix structurel du projet (stratégie de publication…) | `config.yml` | `@require_app_config` au niveau commande |
| Token webhook tournant | `<projet>/.wex/local/{namespace}.yml` | `rotate_local_token()` |

---

## 9. État des lieux — ce qui marche, ce qui pue

### Justifié et propre

- Pile `HasEnvKeys` / `HasEnvKeysFile` / `HasYamlEnvKeysFile` : utilitaires génériques, pas de redondance entre eux.
- Trio `_init_local_env` / `_auto_detect_env` / `core::env/configure` : cohérent, mêmes clés (`get_local_configurable_keys`), trois moments d'usage (auto au démarrage, auto-détection passive, interactif).
- `@require_app_config` : périmètre clair (`config.yml` uniquement), pré-check propre.
- `WithLocalDataMixin` : abstraction propre pour tout `.wex/local/*.yml`.

### Sources de confusion résiduelles

- **Naming de `WithEnvParametersMixin`** : nom générique qui cache le scope réel (`<workdir>/.wex/local/env.yml`). À renommer en `WithSetupEnvParameterMixin` (cf. roadmap).

- **Deux mécanismes parallèles** pour charger un fichier de config wex :
  - Côté kernel : `HasYamlEnvKeysFile._init_env_file_yaml()` → `<install_wex>/.env.yml`
  - Côté workdir : `WithEnvParametersMixin` → `<workdir>/.wex/local/env.yml` (lecture directe)
  
  Pas une duplication fonctionnelle (cibles différentes), mais deux chemins de code qui font la même chose mécaniquement.

- **Fichiers `.wex/.env` legacy** : encore présents physiquement sur les 252 projets pré-migration. Plus jamais lus par wex. Seront supprimés par une migration de cleanup (~1 an).

- **`get_env_parameter()` est volontairement séparé de `os.environ`.** Il renvoie la **config d'env wex** (chargée depuis les fichiers ci-dessus), pas une var système POSIX. Pour lire une var OS-level (`SSH_AUTH_SOCK`, `SUDO_UID`, etc.), on utilise `os.environ.get()` explicitement, avec un commentaire qui justifie le choix.

- **Usage formel de `get_expected_env_keys()` minimal** : seul `AbstractKernel` déclare une clé (`["APP_ENV"]`). Le mécanisme est en place mais sous-utilisé. C'est l'**intention officielle** : chaque classe qui a besoin d'une var devrait la déclarer ici. Voir roadmap phase 5.

- **Trois niveaux de déclaration complémentaires** (pas concurrents) :
  - **Classe** : `get_expected_env_keys()` — besoin structurel d'une classe, validation au boot
  - **Addon** : `get_local_configurable_keys()` — auto-détection au boot + prompt via `core::env/configure`
  - **Commande** : `@require_local_env` (à venir) — prompt avant exécution d'une commande spécifique
  
  Chaque niveau couvre un cas d'usage distinct. Aucun ne remplace les autres.

- **`.env.yml` au niveau install est quasi-mort** : un seul exemple (commenté) dans tout le code. Le mécanisme `HasYamlEnvKeysFile` n'est utilisé que par le kernel et n'a presque jamais servi.

- **Les checks de présence sont parfois trop tardifs** : un token absent peut n'être détecté qu'au milieu d'une commande long-running (cf. `branch_merge_publication_strategy` qui découvrait le token manquant à l'étape 7/7 d'un release). Solution prévue : décorateur `@require_local_env` (roadmap), bloqué tant que le ménage des fichiers n'est pas fait.

### Anti-pattern à éviter

- Confondre la **config du gestionnaire wex** (`.wex/.env`, `.wex/local/env.yml`) avec `os.environ` (espace POSIX). **Deux univers distincts.**
- Confondre la **config du gestionnaire wex** (`.wex/.env`) avec le **`.env` applicatif** à la racine du projet. **Deux univers distincts.** Wex ne lit jamais le `.env` racine.
- Lire une var de config wex via `os.environ.get()` dans une méthode de classe → toujours `self.get_env_parameter()`.
- Lire une var OS-level via `self.get_env_parameter()` → utiliser `os.environ.get()` avec un commentaire qui dit pourquoi.
- Pointer vers un fichier de config wex dans un message d'erreur sans préciser **quelle commande wex utiliser** pour le configurer.
- **Contourner la centralisation** des vars requises. Toute classe qui a besoin d'une var d'env doit la déclarer via `get_expected_env_keys()` (intention officielle de centralisation). Lire `os.environ` à la volée ou ouvrir un `.env` manuellement avec `dotenv`/`open()`/`read_text()`/etc. **dans une méthode de classe** contourne ce dispositif et casse la promesse de check au boot.
