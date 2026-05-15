# Roadmap : décorateur `@require_local_env`

## Statut : terminée 2026-05-15 (hors tests, reportés à un travail dédié)

Doc de référence : `.wex/knowledge/usage/environment-variables.md`, section 8.

## Objectif initial

Couvrir le **niveau commande** des trois niveaux de déclaration des vars requises :
prompter l'utilisateur dès le départ d'une commande pour ce qu'elle va consommer,
persister dans `.wex/local/env.yml`.

## Réalisations

### Phase 1 — Décorateur + fonction de check (✅)

[require_local_env.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/decorator/require_local_env.py)

API finale :
```python
@require_local_env(
    key="GITLAB_API_TOKEN",          # str | Callable -> str | None
    description="...",
    ask_question="...",
    on_missing="ask",                # "ask" | "error"
    use_suite_fallback=False,
)
```

Particularités :
- **Callable peut retourner `None`** → requirement skippé (cas conditionnel).
- **`use_suite_fallback=True`** → utilise `get_env_parameter_or_suite_fallback()`
  pour permettre une définition au niveau suite parente.

### Phase 2 — Intégration middleware (✅)

`AppMiddleware.build_execution_contexts()` lit `command_wrapper.extra["env_requirements"]`
et appelle `check_env_requirements()` juste après le check `config_requirements`.

### Phase 3 — Application sur `app::release/publish` (✅)

Deux décorateurs cumulés sur la commande :
1. `_resolve_publish_remote_token_var` — token API du remote (`GITLAB_API_TOKEN` ou
   `GITHUB_API_TOKEN`), uniquement si stratégie = `branch_merge`. Sinon skip.
2. `_resolve_publish_pipy_token_var` — `PIPY_TOKEN` uniquement pour les
   `PythonPackageWorkdir` qui publient sur PyPI public (pas de registry privée).
   `use_suite_fallback=True` pour permettre la définition au niveau suite.

Le check ad-hoc dans `branch_merge_publication_strategy._build_remote()` a été
remplacé par une assertion défensive (le token est garanti présent par le
décorateur sur la commande, qui tourne avant).

### Phase 4 — Doc (✅)

Section 8 de `environment-variables.md` enrichie : API complète + exemple réel
tiré de `app::release/publish` + usage direct de `check_env_requirements()`.

## Reporté

- **Tests unitaires** (check + middleware + callable + suite fallback) → travail
  dédié, hors périmètre de cette roadmap.
- **Tests d'intégration** `app::release/publish` sans token → prompt → continue.

## Notes pour la suite

- La règle « le prompt arrive **au départ** de la commande » est la valeur clé
  du décorateur. Toute future déclaration doit respecter ce principe.
- Si un nouveau cas nécessite la propagation `os.environ` (pour qu'un subprocess
  voie la var fraîchement saisie), c'est un sujet séparé à arbitrer — pas une
  responsabilité du décorateur lui-même.
