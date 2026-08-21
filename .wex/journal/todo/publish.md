# Roadmap : `wex app/publish` — commande générique de publication d'app

## Context

`bin/publish` is a bash script specific to wex that:
1. Optionally publishes a source lib (`PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH`)
2. Reads the version from `version.txt`
3. Increments the version via `wex core::version/increment`
4. Used to compile `requirements.in → requirements.txt` via `uv pip compile` ← **removed**
5. Commits "Release {version}" + `git push`

The generic system provides `commands/app/publish.py` in `wex-addon-app`, covering:
bump (branch `version-x.y.z`) → rectify → commit + push → annotated tag `{name}/v{version}`

The goal is for `wex app/publish` to work for any app, wex included.

---

## ✅ P1 — App manager PythonWorkdir + pyproject.toml migration (DONE)

**Created:** `.wex/python/app_manager/app_workdir.py`
- Extends `PythonWorkdir` (not Package — wex is an app, not a lib)
- Overrides `prepare_value()`: removes the enforcement of `src/{vendor}_{name}/` which does not match wex's structure
- Overrides `get_package_import_name()` / `get_package_name()` → `"wex"` (not `"wexample_wex"`)

**Migrated:** `requirements.in` → `[project] dependencies` in `pyproject.toml`, removed.

**Note:** `requirements.txt` is kept for `bin/install` (system installation). Its migration
is out of scope — `bin/install` is handled separately.

---

## ✅ P2 — version.txt synchronised by filestate (already in place)

`ManagedWorkdir` inherits from `WithAppVersionWorkdirMixin` which overrides `_get_version_default_content()`
with `VersionContentConfigValue`. `version.txt` is therefore maintained by rectify from `global.version`
in `config.yml` for all workdirs, wex included. Nothing to do.

---

## P3 — Declarative pre-publication hook (to do)

**Where:** `wex-addon-app/commands/app/publish.py` + config `config.yml`

**Problem:** `bin/publish` supports `PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH` — it publishes
the source package suite before publishing wex. This behaviour must be declarative and generic.

**Chosen design:**

In the app's `.wex/config.yml`:
```yaml
publish:
  pre_publish_suite: ${PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH}
```

- If the env variable is set: publishes the suite at the given path before the bump
- If it is not set (or empty): step is silently skipped
- Flag `--skip-pre-publish` to bypass explicitly (equivalent of the current `--no-lib`)

**Implementation in `app/publish.py`:**

Add a `_pre_publish` step at the head of `steps[]`:
```python
def _pre_publish(previous_value=None) -> None:
    suite_path = app_workdir.get_config().search(
        "publish.pre_publish_suite", default=None
    ).get_str_or_none()
    if suite_path:
        # resolve workdir suite and call suite/publish
        ...
```

---

## Migration of bin/publish (after P3)

Once P3 is in place, `bin/publish` becomes:
```bash
cd "${WEX_DIR_ROOT}"
wex app/publish --yes
```

The historical `--no-lib` is replaced by `--skip-pre-publish`.
The `uv pip compile` compilation disappears (no more `requirements.in`).
