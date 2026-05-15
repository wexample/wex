# Roadmap : déclaration des vars d'app via `config.yml → vars:`

## Statut : terminée 2026-05-15

Doc de référence : `.wex/knowledge/usage/environment-variables.md`, section 8.

## Objectif initial

Couvrir la **catégorie C** identifiée à l'inspection (vars spécifiques app,
non couvertes par un service ni par une commande) avec un format YAML
déclaratif dans `config.yml`, symétrique au `service.yml → vars:` existant.

## Réalisations

### Phase 1 — Factorisation + helper de check (✅)

- [helpers/vars_declaration.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/helpers/vars_declaration.py)
  — fonction `process_vars_declarations(vars_decl, app_workdir, io)` qui
  applique une déclaration `vars:` (defaults silencieux + prompts required +
  persist YAML). Support `use_suite_fallback`.
- [helpers/app_vars.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/helpers/app_vars.py)
  — `check_app_vars_requirements(app_workdir, io)` qui lit `config.yml → vars:`
  + auto-déclare les `${VAR}` vues dans `libraries:`, et appelle le helper.
- [service/install.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/service/install.py)
  — refactor pour utiliser `process_vars_declarations` (duplication supprimée).

### Phase 2 — Hook sur `app::start` (✅)

[commands/app/start.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/app/start.py)
appelle `check_app_vars_requirements()` juste après le check `APP_ENV`, avant
tout subprocess docker. La boucle services existante a aussi été migrée sur
`process_vars_declarations` pour cohérence.

### Phase 3 — Intégration `libraries:` (✅ — décision : pas d'auto-déclaration)

Étudié puis **retiré**. Auto-déclarer les `${VAR}` vues dans `libraries:`
était conceptuellement équivalent au scan automatique du compose qu'on avait
explicitement écarté plus tôt (« on déclare ce dont on a besoin, on ne devine pas »).
Règle finale : toute var référencée dans `libraries:` doit être **explicitement**
déclarée dans `vars:`. Une seule règle uniforme, pas de magie.

### Phase 4 — Script d'aide à la migration (✅)

[/tmp/suggest_app_vars.py](file:///tmp/suggest_app_vars.py) — scanne le
docker-compose d'un projet, exclut built-ins et vars déjà déclarées, propose
un snippet `vars:` à copier-coller. Affiche en commentaire la valeur
actuellement présente dans `local/env.yml` + le default éventuel du compose.

Validé sur :
- `bdo-letters` → 12 vars proposées (DOCUSIGN_*, VITE_DOCUSIGN_DEV, PACKAGE_PUBLICATION_NPM_TOKEN, etc.)
- `test` → 0 var à déclarer (rien que des built-ins)

### Phase 5 — Doc (✅)

Section 8 de `environment-variables.md` mise à jour avant l'implémentation :
- Tableau récapitulatif passé à **5 niveaux** (au lieu de 3)
- Sous-section « Niveau service » documentée
- Sous-section « Niveau app » documentée avec exemple cible
- Anti-pattern enrichi

## À faire au fil de l'eau (hors roadmap)

- Migrer chaque app existante en lançant le script de Phase 4 et en complétant
  la `description` de chaque var. C'est un travail par projet, pas une tâche
  unique de cette roadmap.

## Notes pour la suite

- Le mécanisme **réutilise** la persistance YAML existante.
- Le prompt arrive **au lancement de la commande** (`app::start`), pas dans
  le subprocess docker.
- Le format `vars:` est désormais **partagé** entre `service.yml` et `config.yml` :
  même schéma, même helper, comportement identique. Tout enrichissement futur
  (ex. validation, choix dans une liste…) bénéficiera aux deux d'un coup.
