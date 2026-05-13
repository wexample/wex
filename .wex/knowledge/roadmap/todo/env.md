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
- [ ] **1.3 — Usages de `get_expected_env_keys()`** : aucun usage formel dans
  les workdirs principaux → mort ? À retirer ou à utiliser. (Voir phase 5.)
- [ ] **1.5 — Inventaire des contenus réels** : fait partiellement (doc section 8).
  À étendre aux fichiers du scope install (`<install_wex>/.env*`).
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

- [ ] Étendre le lecteur du YAML runner (`core_yaml_command_runner._build_variables`)
  pour qu'il lise le YAML en plus de `.wex/.env`.
- [ ] Aligner les commandes `app::env/var_set` / `var_get` / `var_list` / `set` / `get`
  pour qu'elles écrivent dans `.wex/local/env.yml`.
- [ ] Faire évoluer `WithEnvParametersMixin` (ou son successeur) pour lire le YAML.
- [ ] Migration des projets existants : script qui lit chaque `.wex/.env` et le
  fusionne dans `.wex/local/env.yml`, en archivant l'ancien.
- [ ] Décider du sort de `HasYamlEnvKeysFile` côté kernel : soit on garde le
  mécanisme et on le branche aussi sur `<projet>/.wex/local/env.yml` (au lieu
  de juste `<install_wex>/.env.yml`), soit on le vire et le kernel utilise
  `WithLocalDataMixin` directement.
- [ ] Mettre à jour la doc une fois la fusion faite.

---

## Phase 4 — Messages d'erreur cohérents

- [ ] Auditer tous les messages d'erreur qui mentionnent `.wex/.env` :
  pointer vers le bon fichier (post-fusion) et la bonne commande.
- [ ] Remplacer les messages « set env var X » par des consignes exploitables
  sans toucher au shell : nom de commande wex à lancer.
- [ ] Cas concret à fixer : `branch_merge_publication_strategy.py:166`
  (« or add it to .wex/.env »).

---

## Phase 5 — Faire le ménage sur `get_expected_env_keys()`

Aujourd'hui le mécanisme existe mais n'est utilisé nulle part dans les workdirs
principaux. Deux options :

- [ ] **Option A** : l'activer — chaque workdir déclare ses vars requises,
  validation au boot. Utile si on veut un check précoce sans décorateur.
- [ ] **Option B** : le retirer — code mort. Le futur `@require_local_env`
  fera le job au niveau commande, plus granulaire.

⚠️ **Chevauchement conceptuel** avec `addon.get_local_configurable_keys()`
(côté addons, déjà actif via `_auto_detect_env` + `core::env/configure`).
Trois mécanismes potentiellement concurrents pour la même idée
(déclaration de vars requises) : à arbitrer en un seul, pas en garder trois.

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
