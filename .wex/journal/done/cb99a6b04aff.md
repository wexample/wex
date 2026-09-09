# Roadmap : décorateur `@require_local_env`

## Status: done 2026-05-15 (tests excluded, deferred to a dedicated task)

Reference doc: `.wex/knowledge/usage/environment-variables.md`, section 8.

## Initial objective

Cover the **command level** of the three declaration levels for required vars:
prompt the user at the start of a command for what it will consume,
persist to `.wex/local/env.yml`.

## Deliverables

### Phase 1 — Decorator + check function (✅)

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

Specifics:
- **Callable may return `None`** → requirement skipped (conditional case).
- **`use_suite_fallback=True`** → uses `get_env_parameter_or_suite_fallback()`
  to allow definition at the parent suite level.

### Phase 2 — Middleware integration (✅)

`AppMiddleware.build_execution_contexts()` reads `command_wrapper.extra["env_requirements"]`
and calls `check_env_requirements()` right after the `config_requirements` check.

### Phase 3 — Applied to `app::release/publish` (✅)

Two decorators stacked on the command:
1. `_resolve_publish_remote_token_var` — remote API token (`GITLAB_API_TOKEN` or
   `GITHUB_API_TOKEN`), only when strategy = `branch_merge`. Skipped otherwise.
2. `_resolve_publish_pipy_token_var` — `PIPY_TOKEN` only for
   `PythonPackageWorkdir` instances publishing to public PyPI (no private registry).
   `use_suite_fallback=True` to allow definition at the suite level.

The ad-hoc check in `branch_merge_publication_strategy._build_remote()` has been
replaced by a defensive assertion (the token is guaranteed present by the
decorator on the command, which runs first).

### Phase 4 — Docs (✅)

Section 8 of `environment-variables.md` expanded: full API + real example
taken from `app::release/publish` + direct use of `check_env_requirements()`.

## Deferred

- **Unit tests** (check + middleware + callable + suite fallback) → dedicated task,
  out of scope for this roadmap.
- **Integration tests** `app::release/publish` without token → prompt → continue.

## Notes for follow-up

- The rule "the prompt arrives **at the start** of the command" is the key value
  of the decorator. Any future declaration must respect this principle.
- If a new case requires `os.environ` propagation (so that a subprocess sees the
  freshly entered var), that is a separate topic to decide — not the decorator's
  own responsibility.
