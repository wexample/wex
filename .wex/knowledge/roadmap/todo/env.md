# Roadmap : nettoyage du système d'env

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`.

**État post-phase 3** : YAML partout côté wex.

- `<install_wex>/.env.yml` : config globale du runtime wex (chargée au boot par `AbstractKernel._init_env_file_yaml`)
- `<projet>/.wex/local/env.yml` : config wex projet, machine-local (lue par `WithEnvParametersMixin` et `kernel._init_local_env`)
- `<projet>/.wex/.env` : **legacy**, plus jamais lu, migration de cleanup prévue dans ~1 an

Hors périmètre wex : `os.environ` (POSIX), `<projet>/.env` racine (applicatif).

---

## Phase 5 — Audit : qui doit déclarer quelles vars ?

Recenser **toutes** les classes qui consomment des vars d'env, pour produire
un inventaire exploitable en Phase 6.

**Hypothèse de travail** : `get_expected_env_keys()` est l'**intention officielle**
de centralisation. Les contournements (`os.environ.get()` direct dans une méthode
de classe, `read .env` direct via dotenv) sont des anti-patterns à proscrire.

### Les trois niveaux complémentaires (rappel)

| Niveau | Mécanisme | Déclenchement | Cas d'usage |
|---|---|---|---|
| Classe | `get_expected_env_keys()` | Au boot / `_init_*` | Besoin structurel d'une classe (`GitlabRemote` → `GITLAB_API_TOKEN`) |
| Addon | `get_local_configurable_keys()` | `_auto_detect_env` + `core::env/configure` | Var système auto-détectable (`SSH_AUTH_SOCK`) |
| Commande | `@require_local_env` (futur, Phase 7) | Avant exécution de la commande | Var nécessaire pour cette commande |

### Livrable

Une liste exhaustive sous forme de tableau :

| Classe | Var(s) | Structurel ou conditionnel ? | Niveau recommandé | À enrichir ? |
|---|---|---|---|---|

### Tâches

- [ ] Audit exhaustif des appels `get_env_parameter*` (déjà fait partiellement,
  à étendre : sous-classes concrètes de `AbstractGateway`, `AbstractExternalConnector`,
  `AbstractRemote`, stratégies de publication, etc.).
- [ ] Audit des appels `os.environ.get` qui sont dans des méthodes de classe
  (déjà fait en Phase 1.1, à raffiner si besoin).
- [ ] Classifier chaque consommation : structurelle (toujours nécessaire) vs
  conditionnelle (uniquement dans certains workflows).
- [ ] Pour chaque consommation, recommander le bon niveau (classe / addon / commande).
- [ ] Produire le livrable (tableau ci-dessus) et le sauvegarder dans la doc
  ou dans une roadmap dédiée.

---

## Phase 6 — Implémentation : doc + enrichissement des classes

Sur la base du livrable de Phase 5 :

- [ ] Ajouter à la doc env (`environment-variables.md`) une section
  « Niveaux de déclaration des vars requises » avec exemples concrets tirés
  de l'audit (pas inventés).
- [ ] Enrichir chaque classe identifiée comme « à enrichir » en Phase 5 :
  override de `get_expected_env_keys()` avec ses vars.
- [ ] S'assurer que chaque niveau a un message d'erreur clair qui pointe vers
  la commande wex à lancer pour fixer (pas vers le shell).

---

## Phase 7 — Préparer le terrain pour `@require_local_env`

Ne **rien** coder dans cette roadmap-ci : juste lister les pré-requis.

- [ ] Confirmer que `check_config_requirements()` (utilisé par `@require_app_config`)
  est réutilisable / extensible pour les env vars, ou s'il faut un mécanisme parallèle.
- [ ] Identifier où brancher le check (middleware d'addon ? hook dans le runner ?).
- [ ] Décider du contrat : la valeur saisie est-elle persistée immédiatement,
  propagée dans `env_config` (et éventuellement `os.environ`) pour la suite ?
- [ ] Créer la roadmap dédiée `require-local-env-decorator.md`.

---

## Notes

- **Pas** de `@require_local_env` tant que les phases 5 et 6 ne sont pas terminées.
- Migration de cleanup `.wex/.env` à prévoir dans ~1 an (todo futur, pas encore listé).
- La règle « `os.environ` ≠ env wex ≠ `.env` racine » s'applique aux futures
  docs / commentaires / messages d'erreur.
