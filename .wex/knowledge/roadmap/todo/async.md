# Async — Parallélisme ciblé sur les hotspots safe

## Règle qu'on grave (2026-05-20)

**Async SAFE** :
- Subprocess (chacun isolé, son propre Python)
- FS I/O pure (lecture/écriture fichier sans passer par filestate)
- HTTP requests (asyncio + aiohttp)
- Calcul CPU pur **avec `ProcessPoolExecutor`** (pas thread, à cause du GIL)

**Async FOIREUX (interdit)** :
- Tout ce qui touche au tree **filestate** (`AbstractItemTarget`, `ChildrenOption`, options batch, caches d'options) — state mutable partagé, non thread-safe
- `importlib.import_module` / `exec_module` — modifie `sys.modules` global + side effects au import
- Registries partagés (`SingletonRegistry`, `SharedRegistry`, etc.) sans audit lock
- `IoManager` / prompt response renderers (non thread-safe par design)

Heuristique de validation avant de paralléliser :
> *"Est-ce que les workers partagent un objet Python mutable ?"* — si oui → STOP, faire séquentiel ou passer en subprocess/ProcessPool.

---

## État acquis (à conserver)

### ✅ Livrés et safe (gardés)

**Helper `parallel_map` / `parallel_for_each`** ([wexample_helpers/helpers/parallel.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/helpers/parallel.py))
- ThreadPoolExecutor, ordre préservé, exceptions propagées, default `PARALLEL_DEFAULT_MAX_WORKERS=32`
- 7/7 tests passent

**Usages safe en place** :
- `wex-addon-package/commands/suite/status.py:55` — subprocess git ✅
- `wex-addon-master/commands/info/show.py:73` — subprocess git ✅
- `wex-addon-master/commands/stack/show.py:87` — subprocess git ✅
- `wex-addon-master/workdir/master_workdir.py:146` — subprocess ✅

**Lazy filestate item tree** ([item_target_directory.py](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/item/item_target_directory.py))
- Flag `_tree_built`, build à la demande sur `get_children_list()`. Pas async en soi, mais condition technique pour beaucoup d'optims FS.
- Gain : `package::suite/status` 78s → 7.7s (combiné avec cache YAML/JSON).

**Eager opt-in** : `configure(config, eager=True)`, `create_from_path(eager=True)`, `build_item_tree_recursive()` pour matérialisation forcée.

**Cache module-level YamlFile/JsonFile** ([with_yaml_files.py](../../../../../../../PACKAGES/PYTHON/packages/app/src/wexample_app/workdir/mixin/with_yaml_files.py))
- 4267 parses YAML → cache par path. Gain massif.

### 💀 Rollback (2026-05-20)

| Item | Pourquoi |
|------|----------|
| Phase 1.1 filestate `apply_operations` parallèle | Touche au tree filestate (options, batch caches, IoManager) — silent exits, "trous" dans la sortie, dette debug ingérable. |
| Phase 2.4 filestate `build_operations` parallèle | Même cause. Inspection items = traversée du tree mutable partagé. |

Code revenu à `_apply_operations` séquentiel pur et `build_operations` récursif simple. Helper `inspect_for_operation` (ajouté pour Phase 2.4) supprimé : son commentaire "safe for parallel" était trompeur (la chaîne d'inspection touche au tree filestate) et personne d'autre ne l'appelait.

---

## Roadmap — uniquement les optims SAFE

### A. Subprocess parallel (gain ×N, zéro risque)

Pattern : on lance N subprocess indépendants via `parallel_map`.

- [ ] **wex-addon-app `_packages_execute`** ([framework_packages_suite_workdir.py:530-546](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/workdir/framework_packages_suite_workdir.py#L530)) — N packages × subprocess. Gain : 10-50 packages × 1-5s → ÷4-8. **Attention** : logs entrelacés si modes verbeux → batch en mode quiet ou tampon par package.
- [ ] **wex-addon-app `image/list`** ([commands/image/list.py:37-56](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/image/list.py#L37)) — `docker images` en boucle. Gain : 10 × 100ms → ~150ms.
- [ ] **wex-core webhook subprocess** ([handler.py:196-212](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/webhook/handler.py#L196)) — `subprocess.Popen` par requête HTTP. Gain ×2 à ×10 sous charge.
- [ ] **helpers-git checks parallèles** ([git.py:234-251](../../../../../../../PACKAGES/PYTHON/packages/helpers-git/src/wexample_helpers_git/helpers/git.py#L234)) — `git_has_uncommitted_changes` (index + working en gather). ~50ms par appel.
- [ ] **helpers-git multi-repo state** ([repo.py:10-42](../../../../../../../PACKAGES/PYTHON/packages/helpers-git/src/wexample_helpers_git/helpers/repo.py#L10)) — exposer `repo_get_state_many(paths)` pour appels N repos.
- [ ] **wex-addon-package `suite/packages`** — `get_setup_version()` (lecture pyproject) sur N packages.
- [ ] **wex-addon-dev-javascript polling NPM** ([javascript_package_workdir.py:195-210](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-dev-javascript/src/wexample_wex_addon_dev_javascript/workdir/javascript_package_workdir.py#L195)) — polling registry, HTTP/CLI subprocess.
- [ ] **wex-addon-dev-python `uv pip compile`** ([python_workdir.py:304-355](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-dev-python/src/wexample_wex_addon_dev_python/workdir/python_workdir.py#L304)) — retry/sleep parallèle si plusieurs packages.
- [ ] **wex-addon-app `detect_ssh_socket`** ([helpers/app.py:21-30](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/helpers/app.py#L21)) — subprocess (gain modeste).

### B. FS I/O pure (gain × cores I/O)

Pattern : lecture/écriture fichiers sans passer par filestate (`open()` / `Path.read_text()` direct).

- [ ] **`directory_list_files`, `directory_empty_dir`** ([wexample_helpers/helpers/directory.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/helpers/directory.py)) — scan FS direct.
- [ ] **`file_chown_recursive`, `file_get_dir_size`, `file_copytree_merge_yaml`** ([wexample_helpers/helpers/file.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/helpers/file.py)) — opérations FS récursives directes.

### C. HTTP requests (asyncio + aiohttp)

- [ ] **wex-addon-app polling GitLab pipelines** ([branch_merge_publication_strategy.py:221-252](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/publication/strategy/branch_merge_publication_strategy.py#L221)) — `time.sleep` + HTTP bloquant → `asyncio.sleep` + `aiohttp`. Permet de poller N pipelines en parallèle.

### D. CPU pur avec ProcessPool (PAS thread)

Pattern : AST parse / analyse code → CPU-bound, GIL bloque les threads.

- [ ] **Détection deps circulaires sur N packages** (chemin à confirmer avec user). Si AST parse → `ProcessPoolExecutor`. Si I/O dominant → `parallel_map` standard.

---

## ⚠️ À auditer avant de paralléliser

Ces items semblent safe **mais touchent à des zones où il faut vérifier qu'aucun appel ne passe par filestate / registry partagé**. À profiler/lire avant d'agir, pas attaquer en aveugle.

- [ ] **wex-core middleware path processing** ([abstract_each_path_middleware.py:161-186](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/middleware/abstract_each_path_middleware.py#L161)) — `os.listdir` OK ; `_should_process_item` à auditer.
- [ ] **wex-addon-app migrations YAML rglob** ([migration_wex_6_0_17.py:154-174](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/migration/migration_wex_6_0_17.py#L154), `6_0_23`, `6_0_24`) — OK si lecture/écriture fichier directe, foireux si la migration passe par filestate.
- [ ] **wex-addon-app `find_services_by_tag`** ([app_addon_manager.py:140-159](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/app_addon_manager.py#L140)) — lecture `service.yml` par service. OK si pas via filestate.
- [ ] **migration runner** ([migration_runner.py:90-113](../../../../../../../PACKAGES/PYTHON/packages/migration/src/wexample_migration/migration_runner.py#L90)) — dépend de ce que font les migrations individuelles.
- [ ] **`package_get_dependencies`** ([wexample_filestate-python/helpers/package.py:25](../../../../../../../PACKAGES/PYTHON/packages/filestate-python/src/wexample_filestate_python/helpers/package.py#L25)) — lecture pyproject.toml ; OK si pas via filestate tree.
- [ ] **wex-addon-package `shell.py`, `run.py`** — exécutent code sur chaque item d'une suite. Audit avant de paralléliser (logs entrelacés + potentiel state partagé).

### Zones non explorées par l'audit initial (à creuser si besoin)

- [ ] `wexample_helpers_git/helpers/git.py` — patterns git au-delà de la Phase 2.5.
- [ ] `wex-core/webhook/handler.py` — subprocess au-delà du point déjà identifié.
- [ ] `wex-addon-app/migration/migration_*.py` — 16 fichiers de migration avec patterns FS-walk.
- [ ] `wex-addon-dev-flutter/workdir/flutter_workdir.py` — subprocess flutter.
- [ ] `wex-addon-services-db/services/mysql/` — opérations docker/db.

---

## Bench & validation

- [ ] Harness de bench dans `performance/report`.
- [ ] Mesurer chaque optim avant/après (sinon on ne sait pas si ça vaut le coup).
- [ ] Documenter gains réels dans `.wex/knowledge/decisions/async-perf.md`.

---

## Phase 0 — Décisions structurelles à figer si on attaque les blocs C/D

- [ ] Choisir `asyncio.to_thread()` (simple) vs `aiofiles` (vrai async disque, ajoute dep) pour le bloc B.
- [ ] Décider point d'entrée : `async def` propagé ou `asyncio.run()` ponctuel ?
- [ ] Helper `wexample_helpers.helpers.async_io` (`gather_with_limit`, etc.) si on s'engage sur aiohttp/asyncio.
- [ ] Convention de nommage suffixe `_async` ou wrapper sync.

---

## Pour mémoire — pistes hors async

(documentées pour ne pas refaire les mêmes analyses)

- **Lazy imports** pour reporter imports lourds hors du chemin critique de `setup()` — gain ~30-50ms, faible risque, zéro maintenance.
- **Cache structurel persisté** : écarté, invalidation trop fragile pour le gain (~130ms vs hasher tous les `.py` contributeurs).
- **Précompil YAML→JSON au build** : possible mais demande infra build.
- **Décorateur CLI `@async`** sur les commandes wex : hors scope de cette roadmap, à traiter séparément si reprise.
