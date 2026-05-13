# Roadmap : nettoyage du système d'env

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`.

**Trois univers à ne pas confondre** (établi en audit) :

1. **`os.environ`** — espace POSIX du process, **hors sujet wex**.
   On y touche uniquement pour lire une var qu'on sait être OS-level
   (`SSH_AUTH_SOCK`, `SUDO_UID`…), avec un commentaire qui justifie le choix.

2. **Scope applicatif — `.env` à la racine du projet.** Équivalent du `.env`
   Symfony, consommé par l'application elle-même (Symfony, runtime Python,
   Docker compose). **Wex ne le lit jamais.** Hors sujet pour cette roadmap.

3. **Scope wex — `.wex/.env` + `.wex/local/env.yml`.** La config d'env du
   gestionnaire wex (le `.wex/` est son répertoire). C'est cet univers qu'on
   nettoie. Aujourd'hui deux fichiers cohabitent, fonctionnellement convergents,
   à fusionner.

**Piège de naming repéré** : `WithEnvParametersMixin` porte un nom générique
mais lit en réalité `.wex/.env`. Conçu probablement à l'origine pour le
scope applicatif, dévié vers le scope wex. À renommer ou clarifier.

**Objectif** : avoir un système propre et cohérent **avant** d'introduire un
décorateur `@require_local_env` (déclaration en amont, prompt si manquant,
persistance dans le bon fichier).

---

## Phase 1 — Audit du code existant

- [x] Lister tous les appels `os.environ.get(...)` dans des méthodes de classe
  → **0 violation réelle**. Le seul cas (`repo_workdir.py:91`) est justifié
  par un commentaire « OS-level variable ». Les autres occurrences sont dans
  des helpers d'env, le kernel, ou des fonctions module-level POSIX.
- [ ] Lister tous les usages de `get_env_parameter()` et
  `get_env_parameter_or_suite_fallback()` pour valider que la chaîne `env_config`
  est bien alimentée en amont (sinon le lookup retourne systématiquement le `default`).
- [ ] Lister tous les usages de `get_expected_env_keys()` : aucun → est-ce mort ?
  À retirer ou à utiliser ?
- [ ] Lister les classes qui héritent de `HasEnvKeysFile` / `HasYamlEnvKeysFile`
  et identifier où sont chargés les fichiers (`_init_env_file`).
- [ ] Inventaire des contenus réels de `.wex/.env` et `.wex/local/env.yml` sur
  les projets existants (déjà partiellement fait : voir doc section 8).
- [ ] Vérifier que **rien dans le code Python wex ne lit `.env` racine**
  (audit grep confirme déjà : aucun appel hors `.wex/`). Documenter le fait.

---

## Phase 2 — Clarifier le naming de `WithEnvParametersMixin`

Le mixin lit `.wex/.env` mais son nom suggère un mixin générique. Trois options :

- [ ] **Option A** : renommer en `WithWexEnvParametersMixin` ou
  `WithWexDotEnvMixin` pour expliciter le scope.
- [ ] **Option B** : laisser le nom, ajouter un commentaire de classe qui
  explicite ce qu'il fait (et ce qu'il ne fait pas).
- [ ] **Option C** : si on fusionne sur YAML (phase 3), le mixin disparaît
  ou devient `WithWexEnvYamlMixin`.

Décision à prendre **après** la phase 3 — le naming dépend de ce qui reste.

---

## Phase 3 — Fusion `.wex/.env` + `.wex/local/env.yml` (scope wex uniquement)

**Décision validée** : fusion sur `.wex/local/env.yml` (YAML, dans `local/`
gitignored). JSON écarté (pas de commentaires), TOML écarté (cohérence stack
> optim marginale).

⚠️ Cette fusion concerne **uniquement le scope wex**. Le `.env` racine
(applicatif) reste indépendant, on n'y touche pas.

- [ ] Étendre le lecteur du YAML runner (`core_yaml_command_runner._build_variables`)
  pour qu'il lise le YAML en plus de `.wex/.env`.
- [ ] Aligner les commandes `app::env/var_set` / `var_get` / `var_list` / `set` / `get`
  pour qu'elles écrivent dans `.wex/local/env.yml`.
- [ ] Faire évoluer `WithEnvParametersMixin` (ou son successeur) pour lire le YAML.
- [ ] Migration des projets existants : script qui lit chaque `.wex/.env` et le
  fusionne dans `.wex/local/env.yml`, en archivant l'ancien.
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
