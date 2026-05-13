# Roadmap : nettoyage du système d'env

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`.

**Distinguer ce qui est wex de ce qui ne l'est pas** (établi en audit) :

### Hors périmètre

1. **`os.environ`** — espace POSIX du process, **hors sujet wex**.
   On y touche uniquement pour lire une var qu'on sait être OS-level
   (`SSH_AUTH_SOCK`, `SUDO_UID`…), avec un commentaire qui justifie le choix.

2. **Scope applicatif — `<projet>/.env`** (ou autre nom au choix de l'app).
   Consommé par l'application elle-même (Symfony, runtime Python, Docker compose).
   **Wex ne le lit jamais.** Hors sujet pour cette roadmap.

### Périmètre wex — trois scopes

3. **Scope install wex — `<install_wex>/.env` + `<install_wex>/.env.yml`.**
   Config globale du runtime wex, chargée au boot par `AbstractKernel._init_env_file`
   et `_init_env_file_yaml`. `entrypoint_path.parent` = racine de l'installation
   (`local/wex/`). Le `.env.yml` est prévu pour les structures complexes
   (un seul exemple actif côté SYRTIS, commenté).

4. **Scope workdir projet — `<projet>/.wex/.env`.**
   Config wex par projet, lue par `WithEnvParametersMixin`.

5. **Scope machine-local projet — `<projet>/.wex/local/env.yml`.**
   State par-machine du projet (gitignored).

**Piège de naming repéré** : `WithEnvParametersMixin` porte un nom générique
mais lit en réalité `<workdir>/.wex/.env`. À renommer (`WithSetupEnvParameterMixin`).

**Objectif** : avoir un système propre et cohérent **avant** d'introduire un
décorateur `@require_local_env` (déclaration en amont, prompt si manquant,
persistance dans le bon fichier).

---

## Phase 1 — Audit du code existant

- [x] **1.1 — `os.environ.get(...)` dans des méthodes de classe** : 0 violation
  réelle. Le seul cas (`repo_workdir.py:91`) est justifié par un commentaire
  « OS-level variable ». Les autres occurrences sont dans des helpers d'env,
  le kernel, ou des fonctions module-level POSIX.
- [x] **1.2 — Usages de `get_env_parameter()` et `get_env_parameter_or_suite_fallback()`** :
  7/8 OK. 1 cas à reconfirmer : `kernel_registry.py:36` lit `APP_ENV` sur
  `kernel.env_config`. Tracé : le kernel charge `<install_wex>/.env` au boot
  via `entrypoint_path = __main__.__file__`, donc `entrypoint_path.parent` =
  racine de l'install wex, qui contient `APP_ENV=local`. Donc ça marche.
- [x] **1.4 — Héritiers de `HasEnvKeysFile` / `HasYamlEnvKeysFile`** : un seul
  consommateur (`AbstractKernel`). Aucun autre code n'utilise `_init_env_file`
  ou `_init_env_file_yaml`. Les workdirs lisent leur `.wex/.env` via
  `WithEnvParametersMixin` (lecture directe, mécanisme parallèle).
- [x] **1.3 — Usages de `get_expected_env_keys()`** : pas mort, juste sous-utilisé.
  Une seule classe déclare une clé réelle (`AbstractKernel` → `["APP_ENV"]`).
  Consommé par `_validate_env_keys()` (au boot) et `core::health/check`.
  **Intention officielle** : c'est le mécanisme de **centralisation** des vars
  requises, pensé pour irriguer toute l'app. À **promouvoir** (cf. phase 5),
  pas à retirer. Les abus `os.environ.get()` direct et `read .env` direct sont
  des contournements à proscrire.
- [x] **1.5 — Inventaire des contenus réels** :
  - `<projet>/.wex/.env` : **252 instances** (ubiquitaire)
  - `<projet>/.wex/local/env.yml` : **1 seule instance** (l'install wex elle-même)
  - `<install_wex>/.env` : `APP_ENV=local` + `PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH`
  - `<install_wex>/.env.yml` : **absent en pratique**
  - `.env.yml` ailleurs : **1 seul** (SYRTIS/core, commenté)
  - Autres installs `wex-5/`, `wex-5-legacy/` : **legacy**, seule `wex/` est l'install valide.
- [x] **1.6 — Vérifier que rien dans le code Python wex ne lit `.env` racine projet**
  (audit grep confirmé : aucun appel hors `.wex/` côté workdir, et le kernel
  pointe sur l'install wex, pas sur le projet utilisateur).

---

## Phase 2 — Clarifier le naming de `WithEnvParametersMixin`

Le mixin lit `.wex/.env` mais son nom suggère un mixin générique. Convention
interne : `.wex/` est appelé le « setup ». Trois options :

- [ ] **Option A** : renommer en `WithSetupEnvParameterMixin` (aligné sur la
  convention « setup = `.wex/` », cohérent avec la constante `WORKDIR_SETUP_DIR`).
- [ ] **Option B** : laisser le nom, ajouter un commentaire de classe qui
  explicite ce qu'il fait (et ce qu'il ne fait pas).
- [ ] **Option C** : si on fusionne sur YAML (phase 3), le mixin disparaît
  ou devient `WithSetupEnvYamlMixin`.

Décision à prendre **après** la phase 3 — le naming dépend de ce qui reste.

---

## Phase 3 — Fusion `.wex/.env` + `.wex/local/env.yml` (scope projet uniquement)

**Décision validée** : fusion sur `<projet>/.wex/local/env.yml` (YAML, dans
`local/` gitignored). JSON écarté (pas de commentaires), TOML écarté
(cohérence stack > optim marginale).

⚠️ **Périmètre strict** : cette fusion concerne **uniquement les deux fichiers
du scope projet** (`<projet>/.wex/.env` et `<projet>/.wex/local/env.yml`).
- Le `<projet>/.env` racine (applicatif) reste indépendant — wex ne le touche pas.
- Les fichiers du scope install (`<install_wex>/.env` et `<install_wex>/.env.yml`)
  restent séparés — ils ont un rôle distinct (config runtime).

### Stratégie de migration

Utiliser le mécanisme de migrations existant (`wex-addon-app/migrations/`,
fichiers `migration_wex_X_Y_Z.py` héritant d'`AbstractMigration`).

**Approche progressive, non destructive** :

1. **Migration v6.0.X — copie** : pour chaque projet wex détecté, copier le
   contenu de `.wex/.env` dans `.wex/local/env.yml`. Le `.env` est **gardé
   tel quel** (legacy).
2. **Le code lit en priorité `.wex/local/env.yml`**, et tombe en fallback sur
   `.wex/.env` si une clé manque. Garantit que les vieux projets fonctionnent
   sans intervention.
3. **Migration v7.X.X de cleanup (dans ~1 an)** : supprime `.wex/.env` une
   fois que tous les projets actifs sont passés sur le YAML. Pas avant.

### Tâches

- [ ] Étendre le lecteur du YAML runner (`core_yaml_command_runner._build_variables`)
  pour qu'il lise le YAML en plus de `.wex/.env`.
- [ ] Faire évoluer `WithEnvParametersMixin` pour lire d'abord `.wex/local/env.yml`,
  puis tomber en fallback sur `.wex/.env`.
- [ ] Aligner les commandes `app::env/var_set` / `var_get` / `var_list` / `set` / `get`
  pour qu'elles **écrivent** dans `.wex/local/env.yml` (lectures depuis les deux).
- [ ] Écrire la migration `migration_wex_X_Y_Z.py` qui copie le contenu de
  `.wex/.env` vers `.wex/local/env.yml` (sans supprimer `.env`).
- [ ] Décider du sort de `HasYamlEnvKeysFile` côté kernel : soit on garde le
  mécanisme et on le branche aussi sur `<projet>/.wex/local/env.yml` (au lieu
  de juste `<install_wex>/.env.yml`), soit on le vire et le kernel utilise
  `WithLocalDataMixin` directement.
- [ ] Mettre à jour la doc une fois la fusion faite.
- [ ] Noter dans la roadmap (todo futur) : migration de cleanup `.wex/.env`
  dans ~1 an.

---

## Phase 4 — Messages d'erreur cohérents

- [ ] Auditer tous les messages d'erreur qui mentionnent `.wex/.env` :
  pointer vers le bon fichier (post-fusion) et la bonne commande.
- [ ] Remplacer les messages « set env var X » par des consignes exploitables
  sans toucher au shell : nom de commande wex à lancer.
- [ ] Cas concret à fixer : `branch_merge_publication_strategy.py:166`
  (« or add it to .wex/.env »).

---

## Phase 5 — Promouvoir `get_expected_env_keys()` et clarifier les 3 niveaux

**Décision** : `get_expected_env_keys()` **n'est pas mort, il est sous-utilisé**.
C'est l'**intention officielle** de centralisation des variables d'env requises
qui doit irriguer toute l'app. Les contournements (`os.environ.get()`
direct dans une méthode de classe, `read .env` direct via dotenv ou autre)
sont des **anti-patterns à proscrire**.

### Les trois mécanismes sont complémentaires (pas concurrents)

| Niveau | Mécanisme | Déclenchement | Cas d'usage |
|---|---|---|---|
| Classe | `get_expected_env_keys()` | Au boot / `_init_*` | Besoin structurel d'une classe (`GitlabRemote` → `GITLAB_API_TOKEN`) |
| Addon | `get_local_configurable_keys()` | `_auto_detect_env` + `core::env/configure` | Var système auto-détectable (`SSH_AUTH_SOCK`) |
| Commande | `@require_local_env` (futur) | Avant exécution de la commande | Var nécessaire pour cette commande (token pour `app::release/publish`) |

`@require_local_env` à lui seul **ne suffit pas** pour tous les usages — il
ne couvre que le niveau commande. Les besoins de bas niveau (classes, librairies)
restent du ressort de `get_expected_env_keys()`.

### Tâches

- [ ] Documenter explicitement les trois niveaux dans la doc env, avec exemples.
- [ ] Identifier les classes qui devraient déclarer leurs vars via
  `get_expected_env_keys()` (workdirs, connecteurs, gateways, addons,
  stratégies de publication…) et les enrichir.
- [ ] S'assurer que chaque niveau a un message d'erreur clair qui pointe vers
  la commande wex à lancer pour fixer (pas vers le shell).

---

## Phase 6 — Préparer le terrain pour `@require_local_env`

Ne **rien** coder dans cette roadmap-ci : juste lister les pré-requis.

- [ ] Confirmer que `check_config_requirements()` (utilisé par `@require_app_config`)
  est réutilisable / extensible pour les env vars, ou s'il faut un mécanisme parallèle.
- [ ] Identifier où brancher le check (middleware d'addon ? hook dans le runner ?).
- [ ] Décider du contrat : la valeur saisie est-elle persistée immédiatement,
  propagée dans `env_config` (et éventuellement `os.environ`) pour la suite ?
- [ ] Créer la roadmap dédiée `require-local-env-decorator.md`.

---

## Notes

- **Pas** de `@require_local_env` tant que les phases 1 à 5 ne sont pas terminées.
- Toute modification doit garder la rétro-compatibilité avec les `.wex/.env`
  existants (au moins en lecture, le temps de la migration).
- La règle « `os.environ` ≠ env wex ≠ `.env` racine » s'applique aussi aux
  futures docs / commentaires / messages d'erreur.
