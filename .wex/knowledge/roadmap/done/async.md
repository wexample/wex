# Async — Passage progressif à `asyncio` pour gains de performance

## Objectif

Identifier et migrer les hotspots I/O bloquants vers `asyncio` (`async/await`, `asyncio.gather`, `asyncio.to_thread`, `asyncio.create_subprocess_exec`, `aiofiles`).

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

### 1.1 filestate — `apply_operations` (le plus gros gain)

[abstract_result.py:33-69](../../../../../../../PACKAGES/PYTHON/packages/filestate/src/wexample_filestate/result/abstract_result.py#L33)

- [ ] Boucle séquentielle sur `operations` → chaque op fait du disque (create/write/remove).
- [ ] Refactor : `await asyncio.gather(*[op.apply_async() for op in operations])` avec `asyncio.to_thread` pour les ops disque.
- [ ] Identifier les ops avec dépendances (ex: créer dossier avant fichier) → batcher par phase de dépendance.
- [ ] Bench avant/après sur un gros arbre (>500 ops).
- **Gain attendu : x2 à x5 sur arbres conséquents.**

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
