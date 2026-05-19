# Async — Passage progressif à `asyncio`/threading pour gains de performance

## Statut

**Réouverte (2026-05-18)** : la clôture précédente couvrait uniquement le bootstrap `wex hi`. Le scope plus large (commandes longues, batch d'items de suite, FS walks récursifs) n'avait pas été traité. Voir la section **"Phase 1bis — Axes ré-introduits"** plus bas.

## Objectif

Identifier et migrer les hotspots I/O bloquants vers du parallélisme :
- `concurrent.futures.ThreadPoolExecutor` (via helper utilitaire) pour le code sync existant qu'on ne veut pas refactor en `async def` toute la chaîne — **voie par défaut**, moins invasive.
- `asyncio` (`async/await`, `asyncio.gather`, `asyncio.to_thread`, `asyncio.create_subprocess_exec`, `aiofiles`) pour le code déjà async-friendly ou nouveau code (HTTP polling, subprocess pipelines).

**Hors scope ici** : l'option CLI `--async`/`--sync` (décorateur `@async`) sur les commandes wex — à traiter dans une roadmap séparée une fois cette base posée.

## Principe

Async aide uniquement pour de l'I/O concurrent (disque, réseau, subprocess). Pas de gain sur du CPU pur (GIL). Cible : boucles séquentielles d'I/O indépendants → `asyncio.gather()`.

---

## Phase 0 — Décisions structurelles préalables

- [ ] Décider si on bascule des points d'entrée vers `async def` ou si on encapsule via `asyncio.run()` ponctuel dans des fonctions sync (impact API).
- [ ] Choisir entre `aiofiles` (vrai async disque) vs `asyncio.to_thread()` (threadpool) — `to_thread` plus simple, `aiofiles` ajoute une dep.
- [ ] Ajouter `aiofiles` (et éventuellement `aiohttp`) aux deps de `wexample-helpers` si choisi.
- [ ] Créer un helper `wexample_helpers.helpers.async_io` (ex: `gather_with_limit`, wrappers `read_text_async`, `write_text_async`) pour ne pas dupliquer.
- [ ] Définir une convention de nommage : suffixe `_async` ou conserver le nom + version sync gardée en wrapper.

---

## Phase 1 — Gains FORT (priorité haute)

### 1.1 filestate — `apply_operations` ✅ LIVRÉ (2026-05-19)

[abstract_result.py](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/result/abstract_result.py)

- [x] Refactor en deux paths : `_apply_operations_sequential` (interactive ou rollback) et `_apply_operations_parallel` (cas normal via `parallel_map`).
- [x] Logs différés en mode parallèle pour éviter l'entrelacement (subtitle/task/log replay dans l'ordre d'entrée après la fin du pool).
- [x] Dedupe par `id()` (Operations ne sont pas hashables).
- [x] `FileStateDryRunResult.apply_operations` override pour rester séquentiel (pas d'I/O réelle, pool inutile).
- [x] Dépendances : la sémantique multi-passe de filestate (1 op/item/passe puis nouvelle passe) garantit l'indépendance des ops dans un même result.operations → pas de DAG nécessaire.
- [ ] Bench réel : à mesurer sur un gros arbre via `app::state/rectify`. Hors scope tests unitaires.
- **Gain attendu : x4-x8 sur arbres conséquents (limité par taille du ThreadPool, default 8 workers).**

### 1.2 filestate — `children_filter_option` (iterdir + récursion)

[children_filter_option.py:56-90](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/option/children_filter_option.py#L56)

- [ ] Double boucle `iterdir()` + checks bloquants sur chaque entrée.
- [ ] Paralléliser avec `asyncio.gather()` les checks/builds des enfants.
- [ ] Vérifier impact sur ordre déterministe (re-trier après gather si besoin).
- **Gain attendu : x2 à x3 sur gros arbres.**

### 1.3 wex-addon-app — `_packages_execute`

[framework_packages_suite_workdir.py:530-546](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/workdir/framework_packages_suite_workdir.py#L530)

- [ ] Itération sur N packages avec subprocess/shell séquentiel.
- [ ] Bascule vers `asyncio.create_subprocess_exec` + `gather`.
- [ ] Prévoir un `gather_with_limit` (sem 4-8) pour éviter saturation CPU/réseau.
- [ ] Conserver l'ordre des logs (préfixer chaque output du nom du package).
- **Gain attendu : 10-50 packages × 1-5s → divisé par 4-8.**

### 1.4 wex-addon-app — `image/list` (docker en boucle)

[commands/image/list.py:37-56](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/image/list.py#L37)

- [ ] Boucle `subprocess.run(["docker", "images", ..., tag])` séquentielle.
- [ ] `asyncio.gather` sur `create_subprocess_exec` pour tous les tags.
- **Gain attendu : 10 builds × 100ms → ~150ms total.**

### 1.5 wex-core — Imports addons au bootstrap

[wex.py:34-82](../../../../src/common/wex.py#L34)

- [ ] 14 imports séquentiels chargent du disque + exécution module.
- [ ] `asyncio.gather(*[asyncio.to_thread(importlib.import_module, name) for name in addons])`.
- [ ] Vérifier qu'aucun addon n'a de dépendance d'ordre à l'import (sinon batcher en groupes).
- **Gain attendu : 500ms-2s au cold start, payé à chaque invocation `wex`.**

### 1.6 wex-core — Webhook subprocess

[handler.py:196-212](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/webhook/handler.py#L196)

- [ ] `subprocess.Popen` + `communicate()` bloquant par requête.
- [ ] Bascule vers `asyncio.create_subprocess_exec` + `await process.wait()`.
- [ ] Idéalement passer `ThreadingHTTPServer` → `aiohttp` ou `asgiref` (plus structurel, peut être différé).
- **Gain attendu : x2 à x10 sous charge concurrente.**

### 1.7 config — `_create_options` récursif (ABANDONNÉ après profiling)

[abstract_nested_config_option.py:136](../../../../../../../PACKAGES/PYTHON/packages/config/src/wexample_config/config_option/abstract_nested_config_option.py#L136)

**Hypothèse initiale** : les 135ms de `WexWorkdir.configure()` étaient dans l'instanciation récursive d'options → candidat parfait pour `asyncio.gather`.

**Réalité mesurée via cProfile** :

| Sous-poste | Temps | Type |
|---|---|---|
| Lecture/parse YAML (`read_parsed` + `yaml.loads`) | **~90ms** | I/O + parsing |
| Imports lazy de modules (filestate, config) | 30-50ms | I/O disque + bytecode |
| `get_allowed_options_registry/_options` | ~36ms | CPU + scan provider |
| `_create_options` (instanciation pure) | **~40ms** | **CPU pur** |
| `set_value` (cascade) | ~20ms | CPU pur |

→ **Asyncio sur `_create_options` ne gagne rien** : le code visé est CPU pur (GIL sérialise) et ne représente que 40ms sur 220ms total. Les vrais coûts sont dans le parsing YAML et les imports — pas paralélisables proprement (3 reads trop courts, overhead event loop > gain).

**Pistes alternatives non retenues** :
- **Cache structurel persisté** (sérialiser le tree configuré) → gain potentiel ~130ms, **mais** invalidation à hasher tous les `.py` contributeurs (option classes, providers, addons, workdir, env, version wex) — trop fragile pour 130ms.
- **Lazy imports** : reporter imports lourds hors du chemin critique de `setup()`. Gain ~30-50ms, faible risque. **À envisager si on veut continuer perf démarrage.**
- **Précompil YAML → JSON** au build : ~90ms → ~10ms. Mais demande un step build supplémentaire.

→ **Décision : on arrête le sujet perf démarrage ici.** Le Tier 2 actuel (gain ~100ms via configure=False + bypass shortcut) est ce qu'on peut raisonnablement obtenir sans complexification disproportionnée.

---

## Phase 2 — Gains MOYENS (priorité moyenne)

### 2.1 wex-core — Scan des commandes

[abstract_command_resolver.py:220-326](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/resolver/abstract_command_resolver.py#L220)

- [ ] N×M×P lectures `.py` (`exec_module`) + `.yml` (`yaml.safe_load`).
- [ ] Paralléliser via `asyncio.to_thread` + `gather`.
- **Gain : 200-500ms au startup avec ~100 commandes.**

### 2.2 wex-core — Parsing YAML

[yaml_command_definition.py:30-35](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/yaml/yaml_command_definition.py#L30)

- [ ] `yaml.safe_load` bloquant à chaque `from_path`.
- [ ] Couplé avec 2.1 — même refacto.

### 2.3 wex-core — Middleware path processing

[abstract_each_path_middleware.py:161-186](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/middleware/abstract_each_path_middleware.py#L161)

- [ ] `os.listdir` + checks séquentiels par item.
- [ ] Gather sur `_should_process_item` quand checks I/O.

### 2.4 filestate — `item_target_directory.build_operations`

[item_target_directory.py:54-90](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/item/item_target_directory.py#L54)

- [ ] Récursion séquentielle sur enfants.
- [ ] Paralléliser les branches indépendantes de l'arbre.

### 2.5 helpers-git — Checks parallèles

[git.py:234-251](../../../../../../../PACKAGES/PYTHON/packages/helpers-git/src/wexample_helpers_git/helpers/git.py#L234)

- [ ] `git_has_uncommitted_changes` enchaîne index_changes + working_changes.
- [ ] `gather` sur les 2 → ~50ms par appel.
- [ ] Pareil pour `git_ensure_upstream` (`git.py:81-106`).

### 2.6 helpers-git — Multi-repo state

[repo.py:10-42](../../../../../../../PACKAGES/PYTHON/packages/helpers-git/src/wexample_helpers_git/helpers/repo.py#L10)

- [ ] Si appelé sur N repos → exposer un `repo_get_state_many(paths)` avec gather.

### 2.7 wex-addon-app — Migrations YAML (rglob)

[migration_wex_6_0_17.py:154-174](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/migration/migration_wex_6_0_17.py#L154), `6_0_23`, `6_0_24`

- [ ] Pattern récurrent : `rglob("*.yml")` + read/write séquentiel.
- [ ] Factoriser un helper `migration_apply_yaml_files_async(paths, transform_fn)`.

### 2.8 wex-addon-app — Publication polling GitLab

[branch_merge_publication_strategy.py:221-252](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/publication/strategy/branch_merge_publication_strategy.py#L221)

- [ ] `time.sleep` + HTTP bloquant en boucle.
- [ ] `asyncio.sleep` + `aiohttp` → permet de poller plusieurs pipelines en parallèle.

### 2.9 wex-addon-app — `find_services_by_tag`

[app_addon_manager.py:140-159](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/app_addon_manager.py#L140)

- [ ] Lectures séquentielles de `service.yml` pour chaque service.
- [ ] Gather sur les lectures.

### 2.10 migration runner

[migration_runner.py:90-113](../../../../../../../PACKAGES/PYTHON/packages/migration/src/wexample_migration/migration_runner.py#L90)

- [ ] Migrations séquentielles. Si indépendantes → gather possible (avec prudence).

---

## Phase 3 — Gains FAIBLES / opportunistes

- [ ] **wex-addon-dev-javascript** — Polling NPM registry (`time.sleep` → `asyncio.sleep`) [javascript_package_workdir.py:195-210](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-dev-javascript/src/wexample_wex_addon_dev_javascript/workdir/javascript_package_workdir.py#L195)
- [ ] **wex-addon-dev-python** — `uv pip compile` retry/sleep [python_workdir.py:304-355](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-dev-python/src/wexample_wex_addon_dev_python/workdir/python_workdir.py#L304)
- [ ] **wex-addon-app** — `detect_ssh_socket` (peu d'itérations) [helpers/app.py:21-30](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/helpers/app.py#L21)
- [ ] **wex-addon-app** — `service_command_resolver.build_registry_data` [service_command_resolver.py:184-195](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/resolver/service_command_resolver.py#L184)
- [ ] **wex-addon-app** — `commands/config/build.py` (2 calls docker network) — gain négligeable, à skipper sauf si déjà touché.

---

## Phase 4 — Bench & validation

- [ ] Ajouter un harness de bench dans `performance/report` (commande déjà existante).
- [ ] Mesurer cold start `wex --help` avant/après Phase 1.5.
- [ ] Mesurer durée d'un `app/start` complet (Phase 1.3 + 1.4).
- [ ] Mesurer un `filestate apply` sur un gros arbre (Phase 1.1).
- [ ] Documenter les gains réels dans `.wex/knowledge/decisions/async-perf.md`.

---

## Phase 1bis — Axes ré-introduits (2026-05-18)

Suite à un audit codebase et aux retours user. Trois axes priorisés :

### Axe A — Utilitaire de parcours/map parallèle (FONDATION) ✅ LIVRÉ (2026-05-18)

**But** : factoriser le pattern "boucle séquentielle sur N items I/O-bound" qui apparaît partout. Un seul outil testé, réutilisable.

[wexample_helpers/helpers/parallel.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/helpers/parallel.py)

- [x] `parallel_map(items, fn, *, max_workers=8) -> list` — `ThreadPoolExecutor`, ordre d'entrée préservé en sortie, exceptions propagées.
- [x] `parallel_for_each(items, fn, *, max_workers=8) -> None` — variante sans retour.
- [x] Comportement vide (`items=[]`) → retour vide sans démarrer de pool.
- [x] Comportement single-item → exec directe sans pool (évite overhead).
- [x] Test unitaire (correctness + propagation d'exception). **7/7 tests passent.**

**Sites de migration restants** (à appliquer au fur et à mesure) :
- [ ] `wexample_helpers/helpers/directory.py` → `directory_list_files`, `directory_empty_dir`
- [ ] `wexample_helpers/helpers/file.py` → `file_chown_recursive`, `file_get_dir_size`, `file_copytree_merge_yaml`
- [ ] `wexample_filestate/option/children_filter_option.py:58` → `generate_children`
- [ ] `wexample_filestate/option/children_file_factory_option.py:90` → `_generate_children_recursive`
- [ ] `wexample_filestate-python/helpers/package.py:25` → `package_get_dependencies`
- [ ] `wexample_wex_addon_app/app_addon_manager.py:151` → `find_services_by_tag`

### Axe B — Batch sur items de suite (commandes `package__suite__*`)

**Pattern** : commandes qui itèrent N packages d'une suite, **sans dépendance entre items**, chaque itération = 1-2 subprocess git + lecture pyproject.toml.

- [x] `package__suite__status` : boucle migrée sur `parallel_map`. Gain wall-clock vs séquentiel = vrai mais masqué par le bootstrap (cf. Bonus session 2026-05-18). [status.py](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-package/src/wexample_wex_addon_package/commands/suite/status.py)
- [ ] `package__suite__packages` : boucle similaire avec `get_setup_version()` (lecture pyproject.toml).
- [ ] Vérifier les autres commandes du dossier (`shell.py`, `run.py`) — `shell` et `run` exécutent du code sur chaque item, **potentiellement avec logs entrelacés** : décider si parallélisation ou option `--parallel` opt-in.
- [ ] Bench sur une suite de 10-50 packages (le bench global wall-clock est dominé par d'autres facteurs ; isoler la collecte).

### Axe C — Détection de dépendances circulaires (chemin à confirmer)

**Pattern** : script qui analyse N packages pour détecter des deps circulaires. Boucle par package = parsing AST + résolution imports → indépendant entre packages.

- [ ] **Investigation** : retrouver le chemin du script (le grep `circular_dep|cyclic|find_circular` n'a remonté que des classes de test ; demander au user le chemin exact).
- [ ] Si CPU-bound (AST parse) sur N packages → considérer `ProcessPoolExecutor` (multiprocessing) plutôt que threads (GIL).
- [ ] Si I/O dominant (lecture fichiers) → Axe A suffit.

### Décisions structurelles prises (2026-05-18)

- **Publication par layers** (topo sort des packages, publier en parallèle ce qui est leaf, puis leaf+1...) : **rejeté** pour l'instant. Coûts cachés trop élevés vs gain : logs entrelacés impossibles à lire dans le shell, erreurs partielles non-rollbackables sur PyPI, reproductibilité dégradée, UI spinner non prête pour N flux concurrents. À reconsidérer si on construit une UI dédiée (1 ligne par package mise à jour en place).
- **Voie par défaut = ThreadPoolExecutor** plutôt qu'`async def` cascade : moins invasif sur le code sync existant. `asyncio` réservé aux cas qui sont déjà async-friendly (HTTP polling, subprocess pipelines).
- **50k async tasks** théoriquement OK (coroutines = quelques KB), mais throttle naturel via `ThreadPoolExecutor` (default 32 threads) + `Semaphore` explicite si gather d'asyncio. Limite réelle = `RLIMIT_NOFILE` si beaucoup d'`open()` simultanés (~1024 par défaut).

### Bonus livrés en session 2026-05-18 / 2026-05-19 (hors scope async initial)

Bien que hors du périmètre "async" strict, ces refactors ont été livrés sur le même chemin critique et ont produit l'essentiel du gain wall-clock sur les commandes de suite.

**1. Cache module-level pour YamlFile / JsonFile** ([with_yaml_files.py](../../../../../../../PACKAGES/PYTHON/packages/app/src/wexample_app/workdir/mixin/with_yaml_files.py))
- Avant : `get_yaml_file_from_path` recréait une instance fraîche à chaque appel → cache `_parsed_cache` par-instance jamais réutilisé → 4267 parses YAML pour un seul `wex package::suite/status`.
- Après : helpers `get_or_create_yaml_file` / `get_or_create_json_file` cachés par path.
- Gain mesuré : `wex package::suite/status` 78s → 23s.

**2. Lazy filestate item tree** ([item_target_directory.py](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/item/item_target_directory.py))
- Avant : `FileStateManager.configure()` déclenchait un `build_item_tree()` qui descendait récursivement → 11352 items créés systématiquement au bootstrap.
- Après : flag `_tree_built`, build à la demande via `get_children_list()`, descente récursive supprimée de `ChildrenOption.build_item_tree`. `find_all_by_type` reçoit `stop_at_match=True` pour ne pas réveiller les sous-arbres.
- Gain mesuré : `wex package::suite/status` 23s → 7.7s. `wex app::info/show` ~0.84s (était plusieurs secondes).
- Propriété acquise : le coût d'instanciation devient indépendant de la taille du workdir sur disque.

**3. Eager opt-in** (couvre les besoins fail-fast / "old school")
- `configure(config, eager=True)` et `create_from_path(path, eager=True)` forcent une matérialisation récursive complète (= comportement pre-refactor).
- Méthode publique `build_item_tree_recursive()` exposée pour les cas où on veut matérialiser explicitement.
- 1 test (`test_configure_class_unexpected`) mis à jour pour utiliser `eager=True` et préserver son intention.

**4. Fix dump lazy-aware** ([abstract_item_target.py](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/item/abstract_item_target.py))
- `dump()` déclenche le build lazy avant de dumper → sémantique "voir ce qui est configuré" préservée.

**5. Fix private_field manquants** ([file_change_mode_operation.py](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/operation/file_change_mode_operation.py))
- 3 `private_field` (`_original_uid`, `_original_gid`, `_original_octal_mode`) sans `default=` → attrs n'initialisait pas → 7 tests filestate cassés. Fix `default=None` ajouté.
- 20 → 13 tests filestate cassés (les 13 restants sont des bugs hétérogènes pré-existants, pas notre faute).

### Zones non couvertes par l'audit (à creuser avant clôture)

L'audit codebase a marqué ces zones avec "?" faute de profondeur :
- [ ] `wexample_helpers_git/helpers/git.py` — patterns git complets (au-delà des deux items déjà listés en Phase 2.5).
- [ ] `wex-core/webhook/handler.py` — subprocess en réponse à HTTP (au-delà de 1.6).
- [ ] `wex-addon-app/migration/migration_*.py` — 16 fichiers de migration avec patterns FS-walk.
- [ ] `wex-addon-dev-flutter/workdir/flutter_workdir.py` — subprocess flutter.
- [ ] `wex-addon-services-db/services/mysql/` — opérations docker/db.
- [ ] `wexample_prompt/examples/various/project_dashboard_example.py` — example avec FS-walk + subprocess.

---

## Notes finales

### Ce qui a été FAIT sur la perf démarrage

- **Tier 1** : suppression de `workdir.apply()` au démarrage (gain ~50-150ms).
- **Tier 2** : `configure=False` sur kernel workdir + bypass `get_shortcut("registry")` + suppression complète du mécanisme shortcut legacy (gain net ~80-100ms).

**Total mesuré** : `wex hi` passé de ~500ms à ~390ms (gain ~22%).

### Ce qui a été abandonné après profiling

- **Phase 1.7** (`_create_options` async) : profilé CPU pur sur 40ms / 220ms → asyncio sans gain.
- **Phase 1.5** (imports addons async) : profilé à 12-21ms réels (pas 500ms-2s comme estimé initialement) — gain max <20ms, négligeable.

### Roadmap async hors démarrage encore valide

Les phases 1.1 à 1.4 et 2.x identifient des hotspots dans des **commandes longues** (image/build, db/dump, packages_execute, etc.) où le profil "I/O concurrent" est réel et le gain potentiel mesurable. À reprendre quand le sujet "command perf" devient prioritaire.

### Pistes hors-async pour la perf démarrage (si reprise plus tard)

- **Lazy imports** : reporter les imports lourds (`wexample_filestate`, `wexample_config`) hors du chemin critique de `setup()`. Gain estimé ~30-50ms, faible risque, zéro maintenance.
- Cache structurel : écarté (invalidation trop fragile pour le gain).
- Précompil YAML→JSON au build : possible mais demande infra build.

### Lien avec la registrification

Le décorateur CLI `@async` sur les commandes (sujet initial) reste **hors scope** de cette roadmap — à traiter dans une roadmap dédiée si reprise.
