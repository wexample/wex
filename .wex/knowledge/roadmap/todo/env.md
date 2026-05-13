# Roadmap : nettoyage du système d'env

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`.

Trois stockages cohabitent (`.wex/.env`, `.wex/local/env.yml`, `os.environ`),
plusieurs mixins (`HasEnvKeys` & co.), trois moments d'init côté kernel.
Chacun a son rôle, mais des incohérences se sont accumulées :
- `get_env_parameter()` ne lit que `env_config`, pas `os.environ`
- `os.environ.get()` direct utilisé par endroits au lieu de `get_env_parameter()`
- Conventions floues sur quoi va dans `.wex/.env` vs `.wex/local/env.yml`
- Vérifications de présence parfois tardives (cf. token découvert à l'étape 7/7)
- Messages d'erreur qui pointent vers le mauvais fichier

**Objectif** : avoir un système propre et cohérent **avant** d'introduire
un décorateur `@require_local_env`. Pas de nouveau code tant que la base n'est pas saine.

---

## Phase 1 — Audit du code existant

- [ ] Lister tous les appels `os.environ.get(...)` dans des méthodes de classe
  (hors kernel et helpers d'env eux-mêmes). Décider pour chacun : remplacer par
  `self.get_env_parameter()` ou justifier l'exception.
- [ ] Lister tous les usages de `get_env_parameter()` et `get_env_parameter_or_suite_fallback()`
  pour valider que la chaîne env_config est bien alimentée en amont
  (sinon le lookup retournera systématiquement le `default`).
- [ ] Lister tous les usages de `get_expected_env_keys()` :
  - aucun → est-ce mort ? le retirer ?
  - quelques-uns → les renforcer ?
- [ ] Lister les classes qui héritent de `HasEnvKeysFile` / `HasYamlEnvKeysFile`
  et identifier où sont chargés les fichiers (`_init_env_file`).
- [ ] Lister les contenus actuels des `.wex/.env` et `.wex/local/env.yml`
  sur les projets existants : quels types de données s'y retrouvent ?

---

## Phase 2 — Convention claire `.wex/.env` vs `.wex/local/env.yml`

Aujourd'hui le placement est arbitraire. Définir une règle simple.

- [ ] Proposer une convention, à valider :
  - `.wex/.env` : vars d'app, types simples (string, port, URL), peut être commité
  - `.wex/local/env.yml` : machine-local, secrets, structures complexes, gitignored
- [ ] Lister les vars existantes qui sont mal rangées selon la convention retenue,
  et soit les migrer, soit ajuster la convention.
- [ ] Documenter la convention dans `usage/environment-variables.md` (section 8).

---

## Phase 3 — Aligner `get_env_parameter()` sur la réalité

Le piège actuel : `get_env_parameter()` ne lit que `env_config`. Si une var
n'a pas été chargée explicitement, elle est invisible — même si elle est dans `os.environ`.

Deux options à trancher :

- [ ] **Option A** : `get_env_parameter()` lit aussi `os.environ` en fallback.
  Simple, mais casse la propriété « env_config est la seule source de vérité ».
- [ ] **Option B** : laisser tel quel, mais garantir que tout `_init_*` peuple
  `env_config` depuis `os.environ` + sources fichiers. Plus de discipline mais
  comportement plus prévisible.
- [ ] Implémenter le choix retenu.
- [ ] Mettre à jour la doc en conséquence.

---

## Phase 4 — Messages d'erreur cohérents

- [ ] Auditer tous les messages d'erreur qui mentionnent `.wex/.env` ou un nom
  de var : pointent-ils vers le bon fichier selon la convention de la phase 2 ?
- [ ] Remplacer les messages qui suggèrent « set env var X » par des consignes
  exploitables sans toucher au shell : nom de commande wex à lancer.
- [ ] Cas concret à fixer : `branch_merge_publication_strategy.py:166`
  (« or add it to .wex/.env »).

---

## Phase 5 — Préparer le terrain pour `@require_local_env`

Une fois la base saine, ouvrir une nouvelle roadmap pour le décorateur.
Ne **rien** coder dans cette roadmap-ci : juste lister les pré-requis.

- [ ] Confirmer que `check_config_requirements()` (utilisé par `@require_app_config`)
  est réutilisable / extensible pour les env vars, ou s'il faut un mécanisme parallèle.
- [ ] Identifier où brancher le check (middleware d'addon ? hook dans le runner ?).
- [ ] Décider du contrat : la valeur saisie est-elle persistée immédiatement,
  propagée dans `os.environ` + `env_config` pour la suite de la commande, et/ou
  injectée dans les sous-process ?
- [ ] Créer la roadmap dédiée `require-local-env-decorator.md`.

---

## Notes

- Ne **pas** introduire `@require_local_env` tant que les phases 1 à 4 ne sont pas terminées.
- Toute modification doit garder la rétro-compatibilité avec les `.wex/.env`
  et `.wex/local/env.yml` existants des projets en cours.
