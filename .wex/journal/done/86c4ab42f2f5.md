# Roadmap : nettoyage du système d'env

## Status: completed 2026-05-14

Reference doc: `.wex/knowledge/usage/environment-variables.md`.

**Follow-up**: `.wex/knowledge/roadmap/todo/require-local-env-decorator.md`
(implementation of the `@require_local_env` decorator, built on top of this foundation).

---

## Initial objective

Have a clean and consistent env system **before** introducing a
`@require_local_env` decorator (upfront declaration, prompt if missing, persistence
in the right file).

## Achievements

### Phase 1 — Audit (✅)

- No unjustified `os.environ.get()` in the code (remaining cases have an "OS-level" comment)
- 7/8 calls to `get_env_parameter` correctly fed; the 8th is `kernel_registry` which depends on the install `.env` — OK since loaded at boot by `AbstractKernel.setup()`
- `HasEnvKeysFile` / `HasYamlEnvKeysFile`: 1 single consumer (`AbstractKernel`)
- Field audit: 252 active `.wex/.env` files, 1 single `.wex/local/env.yml`, 1 single `.env.yml` (commented out on SYRTIS side), 3 `wex*` installs of which only one is valid

### Phase 2 — Rename (✅)

`WithEnvParametersMixin` → `WithSetupEnvParameterMixin` (consistent with `WORKDIR_SETUP_DIR`).
4 files touched: the mixin itself + `with_runtime_config_mixin` + `core_yaml_command_runner` + doc.

### Phase 3 — YAML merge (✅)

- Migration `migration_wex_6_0_26.py`: copies `.wex/.env` → `.wex/local/env.yml` (non-destructive)
- `WithSetupEnvParameterMixin` reads/writes `.wex/local/env.yml` (no longer `.wex/.env`)
- `app::env/*` commands aligned on YAML
- `APP_PATH_LOCAL_ENV` constant created (1 single `"env.yml"` literal throughout the code)
- `APP_PATH_ENV` (legacy dotenv) removed: 5 consumer files migrated
- `<install_wex>/.env` → `<install_wex>/.env.yml` (kernel no longer loads the dotenv)
- `file_env_append_as_real_user` is no longer called anywhere (can be removed from the helpers package in cleanup)

### Phase 4 — Error messages (✅)

One real case found: `branch_merge_publication_strategy.py:166` ("or add it to .wex/.env").
Refactored on `io.suggestions`: clear message + wex command to execute (resolved dynamically via `AddonCommandResolver.build_command_from_function`).

### Phase 5 — Level audit (✅)

Conclusion: **no class to enrich massively** with `get_expected_env_keys()` beyond `AbstractKernel`. Real needs are conditional, handled at the command level (Phase 7 / dedicated decorator).

### Phase 6 — 3-level doc (✅)

Section 8 added to `environment-variables.md`: class / addon / command, with real examples.

### Phase 7 — Prepare `@require_local_env` (✅)

Architecture validated (reuse of the `@require_app_config` infrastructure).
Decisions made:
- Lookup: `app_workdir.get_env_parameter()`
- Persistence: `app_workdir.set_env_parameters()` → YAML + `env_config`
- No `os.environ` propagation (it is a bridge to sub-processes, not storage)
- `key` accepts str or Callable (for dynamic cases such as a token depending on the detected remote)

Implementation: dedicated roadmap `require-local-env-decorator.md`.

---

## Follow-up items

- **`.wex/.env` cleanup migration** in ~1 year: remove the 252 legacy dotenv files, once certain they no longer contain anything unique compared to YAML.
- **`file_env_append_as_real_user`** in `wexample_helpers/helpers/file.py`: no longer called, to be removed from the package in a minor cleanup.
