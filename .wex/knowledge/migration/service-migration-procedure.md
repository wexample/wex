# Service Migration Procedure

Reference procedure for creating a v6 service addon package and migrating v5 services into it.

## Goal

- Keep package naming coherent
- Migrate services with the same v6 structure
- Avoid re-inventing patterns service by service

## 1. Choose the target addon package

Create or reuse a package only when the grouping is clear.

Current target groups:

- `wex-addon-services-db`
- `wex-addon-dev-php`
- `wex-addon-services-platform`
- `wex-addon-services-collab`
- `wex-addon-services-monitoring`

Rule:

- if the package contains only services of one family, prefer `wex-addon-services-*`
- if the package contains broader language tooling, keep a wider name such as `wex-addon-dev-php`

## 2. Create the addon package

Minimum package layout:

```text
wex-addon-<name>/
  pyproject.toml
  src/wexample_wex_addon_<name>/
    __init__.py
    <name>_addon_manager.py
    services/
```

Checklist:

- distribution name aligned with folder name
- Python module aligned with distribution name
- addon manager name aligned with package purpose
- package wired in `wex-6/src/common/wex.py`
- package installed in `wex-6/.venv`

## 3. Inventory the v5 service

For each v5 service, review:

- `service.config.yml`
- `docker/docker-compose.yml`
- `samples/.wex/*`
- `command/service/*`
- `command/config/*`
- `command/db/*` or other service-specific commands
- old `command/app/*` hooks

Then classify each item:

- required in v6
- useful but can be simplified
- obsolete / no longer matching v6 patterns

## 4. Create the v6 service skeleton

Minimum service layout:

```text
services/<service>/
  service.yml
  docker/docker-compose.yml
  samples/
```

Add commands only when the service really needs them:

```text
commands/
  service/install.py
  service/ready.py
  config/runtime.py
  db/*
  url/*
  helpers/*
```

Rules:

- put pure helper code in `helpers/`
- keep service-specific commands under the service itself
- reuse an existing v6 service pattern before inventing a new one

## 5. Map v5 concepts to v6

Preferred mapping:

- `service.config.yml` -> `service.yml`
- `extends` / `dependencies` -> declarative v6 service manifest
- service compose -> `docker/docker-compose.yml`
- samples -> `samples/...`
- `command/service/install.py` -> `commands/service/install.py`
- `command/service/ready.py` -> `commands/service/ready.py`
- `command/config/runtime.py` -> `commands/config/runtime.py`

Important rule:

- old v5 `command/app/*` hooks are not ported automatically by default
- only reintroduce them when there is a clean v6 execution point

## 6. Reuse existing patterns

Current reference services:

- DB family:
  `mysql`, `postgres`, `mongo`, `sqlserver`, `redis`
- PHP family:
  `php`, `symfony`, `laravel`, `wordpress`, `phpmyadmin`

Guideline:

- clone the closest v6 service pattern
- change only the service-specific parts
- avoid adding one-off abstractions too early

## 7. Validate the migrated service

Minimum validation:

1. `python3 -m compileall <package-or-service-path>`
2. install the package in `wex-6/.venv` if renamed or newly created
3. verify the package is wired in `wex.py`
4. if possible, test:
   `service/install -> config/write -> app start -> service/ready`

Runtime validation is preferred, but compile validation is the minimum accepted step.

## 8. Update migration docs

After each migrated service or service family:

- update the relevant `todo/addons/*.md`
- move a fully migrated lane from `todo/` to `done/`
- update `_index.md` and `todo/backlog.md` if the global picture changed

## 9. Naming convention decisions

Current conventions validated during migration:

- service-only family package: `wex-addon-services-*`
- broader tooling package: purpose-driven name such as `wex-addon-dev-php`
- service-local helpers: `services/<service>/helpers/*`

## 10. Stop conditions

Do not force a 1:1 v5 port when:

- the old behavior depends on a dead v5 hook model
- the v6 equivalent would be hacky
- the feature is only historical comfort and not required for functional parity

In that case:

- migrate the clean functional core
- note the gap in migration docs
- keep the package/service structure ready for a later second pass
