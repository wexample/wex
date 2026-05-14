# Roadmap : décorateur `@require_local_env`

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`, section 8 (« Déclarer les vars requises — les trois niveaux complémentaires »).

Ce décorateur couvre le **niveau commande** : déclarer qu'une commande wex a besoin
d'une variable d'env précise pour s'exécuter, prompter l'utilisateur si manquante,
persister la valeur dans `.wex/local/env.yml`.

C'est le pendant de `@require_app_config` (qui couvre les clés de `config.yml`).
Cibles différentes, architecture identique.

**Use-cases prioritaires** (issus de l'audit Phase 5) :
- `app::release/publish` → token de publication (PyPI, GitLab, GitHub…)
- Toute commande avec un pré-requis ponctuel non auto-détectable

---

## Architecture cible (réutilisation maximale)

Calquée sur `@require_app_config` :

```
@require_local_env(...)  →  command_wrapper.extra["env_requirements"]
                                        ↓
                          AppMiddleware (étendu)
                                        ↓
                          check_env_requirements()
                                        ↓
                          app_workdir.get_env_parameter / set_env_parameters
```

3 pièces à produire :
- `decorator/require_local_env.py` — le décorateur + `check_env_requirements()`
- Extension de `middleware/app_middleware.py` — appeler le check après celui de config
- Doc env (section 8 déjà prête, à enrichir avec un exemple concret)

---

## Décisions actées

| Sujet | Décision |
|---|---|
| Lookup | `app_workdir.get_env_parameter(key, default=None)` |
| Persistance | `app_workdir.set_env_parameters({key: value})` → écrit dans `.wex/local/env.yml` + maj `env_config` |
| Propagation `os.environ` | **Non.** `os.environ` n'est pas un stockage wex, c'est juste un pont vers les sous-process. Si une commande lance un subprocess qui a besoin de la var, c'est au moment du lancement qu'elle prépare son env. |
| Clé dynamique | **Oui.** `key: str \| Callable[[ctx], str]`. Le callable reçoit le contexte d'exécution et retourne le nom de la var. Couvre le cas `branch_merge_publication_strategy` (token dont le nom dépend du remote détecté). |
| `on_missing` | `"ask"` (défaut) → prompt + persiste. `"error"` → raise. Pas de `"default"` automatique : un secret n'a pas de default raisonnable. |
| Message d'erreur | Via `io.suggestions` avec une commande wex à exécuter (cf. pattern `branch_merge_publication_strategy.py`). |

---

## Phase 1 — Décorateur + fonction de check

- [ ] Créer `wex-addon-app/decorator/require_local_env.py`
- [ ] API du décorateur :
  ```python
  @require_local_env(
      key="GITLAB_API_TOKEN",                    # str | Callable
      description="GitLab API token",
      ask_question="Paste your GitLab API token:",
      on_missing="ask",                          # "ask" | "error"
  )
  ```
- [ ] Implémenter `check_env_requirements(requirements, app_workdir, io, function_kwargs)` :
  - Résoudre `key` (si callable, l'appeler avec le contexte)
  - Lookup via `app_workdir.get_env_parameter(resolved_key, default=None)`
  - Si trouvé → continue
  - Si manquant + `on_missing="ask"` → prompt user via `io.input`, persiste via `set_env_parameters`
  - Si manquant + `on_missing="error"` → `io.suggestions` + raise

---

## Phase 2 — Intégration middleware

- [ ] Étendre `AppMiddleware.build_execution_contexts()` pour lire
  `command_wrapper.extra["env_requirements"]` et appeler `check_env_requirements()`
  juste après le check `config_requirements`.
- [ ] Tester l'ordre : les deux checks tournent avant que la commande s'exécute.
  En cas d'échec sur l'un, l'autre n'est pas tenté (fail-fast).

---

## Phase 3 — Application aux commandes existantes

Sur la base de l'audit Phase 5 :

- [ ] `app::release/publish` :
  ```python
  @require_local_env(
      key=lambda ctx: _detect_remote_token_var(ctx),  # dynamique selon le remote
      description="Remote API token for publishing",
      ask_question="Paste your remote API token:",
  )
  ```
- [ ] Retirer le check ad-hoc dans `branch_merge_publication_strategy._build_remote()` :
  le token est garanti présent quand on arrive dans `_build_remote()` car le
  middleware a déjà tourné. On garde une assertion défensive.
- [ ] Cas PyPI (`python_package_workdir.py:445`) : audit du flow pour décider
  si le décorateur s'applique à `app::release/publish` (cas couvert) ou à un
  point d'entrée plus spécifique.

---

## Phase 4 — Doc + tests

- [ ] Compléter la section 8 de `environment-variables.md` avec un exemple
  réel utilisant `@require_local_env`.
- [ ] Tests unitaires : check + middleware + cas dynamique (clé callable).
- [ ] Tests d'intégration : `app::release/publish` sans token → prompt, avec
  token → continue.

---

## Notes

- Pas de validation `values=[...]` (contrairement à `@require_app_config`) :
  un secret est libre, pas dans une liste fermée. Si un jour on a besoin, on
  ajoute.
- Si `app_workdir` n'est pas disponible (commande hors `AppMiddleware`),
  le décorateur lève une erreur explicite à la définition de la commande.
