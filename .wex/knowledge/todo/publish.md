# Roadmap : `wex app/publish` — commande générique de publication d'app

## Contexte

`bin/publish` est un script bash spécifique à wex qui :
1. Publie optionnellement une lib source (`PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH`)
2. Lit la version depuis `version.txt`
3. Incrémente la version via `wex default::version/increment`
4. Compilait `requirements.in → requirements.txt` via `uv pip compile` ← **supprimé**
5. Commit "Release {version}" + `git push`

Le système générique dispose de `commands/app/publish.py` dans `wex-addon-app` qui couvre :
bump (branche `version-x.y.z`) → rectify → commit + push → tag annoté `{name}/v{version}`

L'objectif est que `wex app/publish` soit valable pour n'importe quelle app, wex inclus.

---

## ✅ P1 — App manager PythonWorkdir + migration pyproject.toml (FAIT)

**Créé :** `.wex/python/app_manager/app_workdir.py`
- Étend `PythonWorkdir` (pas Package — wex est une app, pas une lib)
- Override `prepare_value()` : retire l'enforcement de `src/{vendor}_{name}/` qui ne correspond pas à la structure de wex
- Override `get_package_import_name()` / `get_package_name()` → `"wex"` (pas `"wexample_wex"`)

**Migré :** `requirements.in` → `[project] dependencies` dans `pyproject.toml`, supprimé.

**Note :** `requirements.txt` reste pour `bin/install` (installation système). Sa migration
est hors scope — `bin/install` est traité séparément.

---

## ✅ P2 — version.txt synchronisé par filestate (déjà en place)

`ManagedWorkdir` hérite de `WithAppVersionWorkdirMixin` qui overrides `_get_version_default_content()`
avec `VersionContentConfigValue`. `version.txt` est donc maintenu par rectify depuis `global.version`
dans `config.yml` pour tous les workdirs, y compris wex. Rien à faire.

---

## P3 — Hook de pré-publication déclaratif (à faire)

**Où :** `wex-addon-app/commands/app/publish.py` + config `config.yml`

**Problème :** `bin/publish` supporte `PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH` — il publie
la suite de packages source avant de publier wex. Ce comportement doit être déclaratif et générique.

**Design retenu :**

Dans `.wex/config.yml` de l'app :
```yaml
publish:
  pre_publish_suite: ${PROGRAM_PUBLICATION_SOURCE_LIBRARY_PATH}
```

- Si la variable d'env est définie : publie la suite au chemin indiqué avant le bump
- Si elle n'est pas définie (ou vide) : step silencieusement skippé
- Flag `--skip-pre-publish` pour bypasser explicitement (équivalent de `--no-lib` actuel)

**Implémentation dans `app/publish.py` :**

Ajouter une étape `_pre_publish` en tête de `steps[]` :
```python
def _pre_publish(previous_value=None) -> None:
    suite_path = app_workdir.get_config().search(
        "publish.pre_publish_suite", default=None
    ).get_str_or_none()
    if suite_path:
        # resolve workdir suite et appeler suite/publish
        ...
```

---

## Migration de bin/publish (après P3)

Une fois P3 en place, `bin/publish` devient :
```bash
cd "${WEX_DIR_ROOT}"
wex app/publish --yes
```

Le `--no-lib` historique est remplacé par `--skip-pre-publish`.
La compilation `uv pip compile` disparaît (plus de `requirements.in`).
