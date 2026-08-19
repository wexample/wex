# Roadmap : nettoyage du système d'env

## Statut : terminée 2026-05-14

Doc de référence : `.wex/knowledge/usage/environment-variables.md`.

**Suite** : `.wex/knowledge/roadmap/todo/require-local-env-decorator.md`
(implémentation du décorateur `@require_local_env`, qui s'appuie sur cette base).

---

## Objectif initial

Avoir un système d'env propre et cohérent **avant** d'introduire un décorateur
`@require_local_env` (déclaration en amont, prompt si manquant, persistance
dans le bon fichier).

## Réalisations

### Phase 1 — Audit (✅)

- Aucun `os.environ.get()` non justifié dans le code (les cas restants ont un commentaire « OS-level »)
- 7/8 appels à `get_env_parameter` correctement alimentés ; le 8ᵉ est `kernel_registry` qui dépend du `.env` install — OK car chargé au boot par `AbstractKernel.setup()`
- `HasEnvKeysFile` / `HasYamlEnvKeysFile` : 1 seul consommateur (`AbstractKernel`)
- Audit terrain : 252 fichiers `.wex/.env` actifs, 1 seul `.wex/local/env.yml`, 1 seul `.env.yml` (commenté côté SYRTIS), 3 installs `wex*` dont une seule valide

### Phase 2 — Rename (✅)

`WithEnvParametersMixin` → `WithSetupEnvParameterMixin` (cohérent avec `WORKDIR_SETUP_DIR`).
4 fichiers touchés : le mixin lui-même + `with_runtime_config_mixin` + `core_yaml_command_runner` + doc.

### Phase 3 — Fusion sur YAML (✅)

- Migration `migration_wex_6_0_26.py` : copie `.wex/.env` → `.wex/local/env.yml` (non destructive)
- `WithSetupEnvParameterMixin` lit/écrit `.wex/local/env.yml` (plus `.wex/.env`)
- Commandes `app::env/*` alignées sur YAML
- Constante `APP_PATH_LOCAL_ENV` créée (1 seul `"env.yml"` littéral dans tout le code)
- `APP_PATH_ENV` (legacy dotenv) supprimé : 5 fichiers consommateurs migrés
- `<install_wex>/.env` → `<install_wex>/.env.yml` (kernel ne charge plus le dotenv)
- `file_env_append_as_real_user` n'est plus appelé nulle part (peut être retiré du package helpers en cleanup)

### Phase 4 — Messages d'erreur (✅)

Un seul vrai cas trouvé : `branch_merge_publication_strategy.py:166` (« or add it to .wex/.env »).
Refactor sur `io.suggestions` : message clair + commande wex à exécuter (résolue dynamiquement via `AddonCommandResolver.build_command_from_function`).

### Phase 5 — Audit niveaux (✅)

Conclusion : **aucune classe à enrichir massivement** avec `get_expected_env_keys()` au-delà de `AbstractKernel`. Les vrais besoins sont conditionnels, traités au niveau commande (Phase 7 / décorateur dédié).

### Phase 6 — Doc 3 niveaux (✅)

Section 8 ajoutée à `environment-variables.md` : classe / addon / commande, avec exemples réels.

### Phase 7 — Préparer `@require_local_env` (✅)

Architecture validée (réutilisation de l'infra `@require_app_config`).
Décisions actées :
- Lookup : `app_workdir.get_env_parameter()`
- Persistance : `app_workdir.set_env_parameters()` → YAML + `env_config`
- Pas de propagation `os.environ` (c'est un pont vers les sous-process, pas du stockage)
- `key` accepte str ou Callable (pour les cas dynamiques type token selon remote détecté)

Implémentation : roadmap dédiée `require-local-env-decorator.md`.

---

## Suite à prévoir

- **Migration de cleanup `.wex/.env`** dans ~1 an : supprimer les 252 fichiers dotenv legacy, une fois sûrs qu'ils ne contiennent plus rien d'unique par rapport au YAML.
- **`file_env_append_as_real_user`** dans `wexample_helpers/helpers/file.py` : plus appelé, à retirer du package en cleanup mineur.
