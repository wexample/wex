# Roadmap : nettoyage du système d'env

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`.

**État post-phase 3** : YAML partout côté wex.

- `<install_wex>/.env.yml` : config globale du runtime wex (chargée au boot par `AbstractKernel._init_env_file_yaml`)
- `<projet>/.wex/local/env.yml` : config wex projet, machine-local (lue par `WithEnvParametersMixin` et `kernel._init_local_env`)
- `<projet>/.wex/.env` : **legacy**, plus jamais lu, migration de cleanup prévue dans ~1 an

Hors périmètre wex : `os.environ` (POSIX), `<projet>/.env` racine (applicatif).

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

- **Pas** de `@require_local_env` tant que les phases 4 et 5 ne sont pas terminées.
- Migration de cleanup `.wex/.env` à prévoir dans ~1 an (todo futur, pas encore listé).
- La règle « `os.environ` ≠ env wex ≠ `.env` racine » s'applique aux futures
  docs / commentaires / messages d'erreur.
