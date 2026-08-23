# Roadmap : déclaration des vars d'app via `config.yml → vars:`

## Status: completed 2026-05-15

Reference doc: `.wex/knowledge/usage/environment-variables.md`, section 8.

## Initial objective

Cover **category C** identified at inspection (app-specific vars,
not covered by a service or a command) with a declarative YAML format
in `config.yml`, symmetrical to the existing `service.yml → vars:`.

## Deliverables

### Phase 1 — Refactoring + check helper (✅)

- [helpers/vars_declaration.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/helpers/vars_declaration.py)
  — function `process_vars_declarations(vars_decl, app_workdir, io)` that
  applies a `vars:` declaration (silent defaults + required prompts +
  YAML persist). Supports `use_suite_fallback`.
- [helpers/app_vars.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/helpers/app_vars.py)
  — `check_app_vars_requirements(app_workdir, io)` reads `config.yml → vars:`
  + auto-declares `${VAR}` tokens seen in `libraries:`, then calls the helper.
- [service/install.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/service/install.py)
  — refactored to use `process_vars_declarations` (duplication removed).

### Phase 2 — Hook on `app::start` (✅)

[commands/app/start.py](PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/app/start.py)
calls `check_app_vars_requirements()` right after the `APP_ENV` check, before
any docker subprocess. The existing service loop was also migrated to
`process_vars_declarations` for consistency.

### Phase 3 — `libraries:` integration (✅ — decision: no auto-declaration)

Studied then **removed**. Auto-declaring the `${VAR}` tokens seen in `libraries:`
was conceptually equivalent to the automatic compose scan that had been
explicitly ruled out earlier ("we declare what we need, we don't guess").
Final rule: any var referenced in `libraries:` must be **explicitly**
declared in `vars:`. One uniform rule, no magic.

### Phase 4 — Migration helper script (✅)

[/tmp/suggest_app_vars.py](file:///tmp/suggest_app_vars.py) — scans a
project's docker-compose, excludes built-ins and already-declared vars, and
proposes a `vars:` snippet ready to copy-paste. Displays as a comment the
value currently present in `local/env.yml` + the optional compose default.

Validated on:
- `bdo-letters` → 12 vars proposed (DOCUSIGN_*, VITE_DOCUSIGN_DEV, PACKAGE_PUBLICATION_NPM_TOKEN, etc.)
- `test` → 0 vars to declare (nothing but built-ins)

### Phase 5 — Doc (✅)

Section 8 of `environment-variables.md` updated before implementation:
- Summary table extended to **5 levels** (instead of 3)
- "Service level" sub-section documented
- "App level" sub-section documented with target example
- Anti-pattern enriched

## To do on a rolling basis (outside the roadmap)

- Migrate each existing app by running the Phase 4 script and filling in
  the `description` for each var. This is per-project work, not a single
  task of this roadmap.

## Notes for follow-up

- The mechanism **reuses** the existing YAML persistence.
- The prompt fires **at command launch** (`app::start`), not inside
  the docker subprocess.
- The `vars:` format is now **shared** between `service.yml` and `config.yml`:
  same schema, same helper, identical behaviour. Any future enhancement
  (e.g. validation, choice from a list…) will benefit both at once.
