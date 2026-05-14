# Roadmap : nettoyage du système d'env

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`.

**État post-phase 3** : YAML partout côté wex.

- `<install_wex>/.env.yml` : config globale du runtime wex (chargée au boot par `AbstractKernel._init_env_file_yaml`)
- `<projet>/.wex/local/env.yml` : config wex projet, machine-local (lue par `WithEnvParametersMixin` et `kernel._init_local_env`)
- `<projet>/.wex/.env` : **legacy**, plus jamais lu, migration de cleanup prévue dans ~1 an

Hors périmètre wex : `os.environ` (POSIX), `<projet>/.env` racine (applicatif).

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
