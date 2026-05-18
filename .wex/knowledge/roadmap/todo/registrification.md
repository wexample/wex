# Registrification — Standardisation du pattern Registry

## Objectif

Unifier toutes les collections de type "liste de classes / singletons" derrière `Registry[T]` + `RegistryContainerMixin` ([registry.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/service/registry.py), [registry_container_mixin.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/service/mixins/registry_container_mixin.py)), et y centraliser :
1. **L'init** (sync ou async).
2. **La résolution de dépendances** entre items.

---

## Audit (FAIT)

Critères retenus (cumulatifs, ≥3/4) : collection d'items même type, remplie à l'init puis read-only, lookup par clé OU itération, sources multiples possibles.

### Vrais candidats à migrer

| # | Nom | Fichier | État | Criticité | Source des items |
|---|-----|---------|------|-----------|------------------|
| 1 | `ScriptRunnerRegistry._runners` | [yaml/script_runner_registry.py:17](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/yaml/script_runner_registry.py#L17) | CUSTOM | HAUTE | 4 defaults hard-codés + addons |
| 2 | `StepGuardRegistry._guards` | [yaml/step_guard_registry.py:18](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/yaml/step_guard_registry.py#L18) | CUSTOM (list!) | HAUTE | Addons via `get_step_guard_classes()` |
| 3 | `RunnerRegistry._runners` | [packages/runner/runner_registry.py:16](../../../../../../../PACKAGES/PYTHON/packages/runner/src/wexample_runner/runner_registry.py#L16) | CUSTOM | MOYENNE | `register(name, runner)` |
| 4 | `EventDispatcher._event_listeners` | [packages/event/common/dispatcher.py:44](../../../../../../../PACKAGES/PYTHON/packages/event/src/wexample_event/common/dispatcher.py#L44) | HYBRID | HAUTE | `add_event_listener()` (dynamique) |
| 5 | Webhook `type_resolvers` | [webhook/handler.py:96](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/webhook/handler.py#L96) | INLINE | MOYENNE | `_load_type_resolvers()` (listen.py:138) |
| 6 | `SpinnerPool._spinners` | [packages/prompt/common/spinner_pool.py:98](../../../../../../../PACKAGES/PYTHON/packages/prompt/src/wexample_prompt/common/spinner_pool.py#L98) | CUSTOM | BASSE | `get(key)` lazy |
| 7 | `WithConfigRegistry._registry` | [packages/pseudocode/common/with_config_registry.py:17](../../../../../../../PACKAGES/PYTHON/packages/pseudocode/src/wexample_pseudocode/common/with_config_registry.py#L17) | INLINE | BASSE | Hard-codé `__init__` |

### Déjà conformes (STANDARD)

- ✅ Kernel `addons` (`REGISTRY_KERNEL_ADDON`) — [kernel.py:150](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/common/kernel.py#L150)
- ✅ Kernel `middlewares` — [kernel.py:548](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/common/kernel.py#L548)
- ✅ `RegistryContainerMixin._registries` — le méta-registre lui-même.

### Cas spéciaux à traiter à part

- **`KernelRegistry`** [registry/kernel_registry.py:28](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/registry/kernel_registry.py#L28) — HYBRID, HAUTE. Spécifique : persistance fichier (`registry.json`), hydratation via resolvers. **À garder isolé** car son cycle de vie diffère. Pourra implémenter le Protocol `Registrable` sans casser sa persistance.
- **Options nested dans `wexample_config`** [config_option/abstract_nested_config_option.py:32](../../../../../../../PACKAGES/PYTHON/packages/config/src/wexample_config/config_option/abstract_nested_config_option.py#L32) — plutôt **composition d'options typées** qu'un registre. Décision reportée → audit ciblé Phase 1bis.

### Faux positifs (NE PAS migrer)

- ❌ Webhook `_counters` / `_duration_sum` / `_duration_count` — métriques runtime mutables.
- ❌ `_REGISTRY_CACHE` (abstract_nested_config_option.py:7) — cache de perf, pas registre.
- ❌ `AbstractResult.operations` (filestate) — résultat de build, accumulé puis consommé.
- ❌ App registry (`with_app_registry_mixin.py`) — config sérialisée vers/depuis YAML.

### Pattern récurrent identifié

Motif `for addon in kernel.get_addons().values(): collect addon.get_X_classes()` présent dans :
- `_init_middlewares` ✅ déjà standard
- `_init_step_guard_registry` ❌ #2
- `_init_resolvers` → à vérifier
- `_load_type_resolvers` (webhook) ❌ #5

→ Un seul mécanisme générique `Registry.populate_from_addons(method_name)` pourrait remplacer ces 4+ boucles.

---

## Phase 1bis — Audits restants

- [ ] Trancher : `wexample_config` options nested = registre ou composition ?
- [ ] Vérifier `_init_resolvers` du kernel (STANDARD ou pas ?).
- [ ] Re-grep `wex-addon-app` : services, builds, containers.

### Candidat additionnel — Suite packages

**[FrameworkPackagesSuiteWorkdir](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/workdir/framework_packages_suite_workdir.py)** : la liste de packages d'une suite est un registre déguisé.

- Items même type (workdirs de packages), itérations multiples (build, publish, version bump...).
- **Dépendances inter-packages** existent → tri topologique utile pour ordre de build/publish.
- Découverte par filesystem (paths), pas par `register()` explicite.

→ Possible nouvelle variante **`FilesystemDiscoveredRegistry`** OU méthode `populate_from_paths(paths, item_class)` sur `SingletonRegistry`. À décider au moment de la migration.

---

## Phase 2 — Protocol `Registrable` avec dépendances

`RegistrableType = TypeVar("RegistrableType")` est aujourd'hui vide. À remplacer par un Protocol explicite (fallback Mixin si trop restrictif à l'usage).

- [ ] Créer `Registrable` Protocol dans `wexample_helpers/service/registrable.py` :
  ```python
  @runtime_checkable
  class Registrable(Protocol):
      @classmethod
      def get_registry_key(cls) -> str: ...
      @classmethod
      def dependencies(cls) -> list[type[Registrable]]: ...
      def init_sync(self) -> None: ...
      async def init_async(self) -> None: ...
  ```
- [ ] `Registry.register(item)` : signature simplifiée, dérive la clé via `item.get_registry_key()`. **Pas de rétro-compat** sur `register(key, item)`.
- [ ] `Registry.resolve_init_order()` → tri topologique des items selon `dependencies()`.
- [ ] Détection des cycles → exception explicite avec la chaîne fautive.

## Phase 2ter — `SharedRegistry` (accès singleton par classe)

Variante orthogonale qui ajoute un mode "instance partagée accessible globalement", sans renoncer au mode instance-based standard. Utile quand un registre doit être atteint depuis n'importe où sans passer une référence (cas typique : registres de niveau process comme runners de packages externes).

- ✅ Créé dans `wexample_helpers/service/shared_registry.py`.
- API : `MyRegistry.shared()` retourne l'instance partagée (lazy-créée, isolée par sous-classe).
- Mode instance dédiée préservé : `MyRegistry()` crée toujours une instance neuve.
- `reset_shared()` exposé pour les tests.

## Phase 2bis — `DiskPersistedRegistry` (FAIT)

- ✅ Créé `DiskPersistedRegistry(Registry[T])` dans `wexample_helpers/service/disk_persisted_registry.py`.
- ✅ Accepte un duck-typed file avec `read_parsed()`/`write_parsed()`/`get_local_file().is_empty()` — compatible avec `JsonFile`/`YamlFile` de filestate.
- ✅ `is_persisted()` tolère fichier inexistant.
- ✅ `load()` no-op si fichier absent.
- ✅ Validé via `AppsRegistry` (cf Phase 4 #candidat additionnel).

## Phase 2quater — `WithFileLockMixin` (FAIT)

- ✅ Créé dans `wexample_helpers/service/with_file_lock_mixin.py`.
- ✅ Context manager `file_lock()` via `fcntl.flock` cross-process.
- ✅ `_get_locked_resource_path()` à implémenter par la classe utilisatrice (sinon NotImplementedError explicite).
- ✅ Validé via `AppsRegistry` (composition `WithFileLockMixin + SharedRegistry + DiskPersistedRegistry`).

---

## Phase 3 — Init async dans Registry

Lien direct avec [async.md](async.md) Phase 1.5.

- [ ] `Registry.init_all_async()` :
  - Résolution topologique via `dependencies()`.
  - Calcul des **couches indépendantes** → `await asyncio.gather(*layer)`.
  - Couches enchaînées séquentiellement.
- [ ] `Registry.init_all_sync()` (fallback / debug).
- [ ] `RegistryContainerMixin.init_all_registries_async()` qui parallélise entre registres indépendants.
- [ ] Mesurer le gain sur bootstrap kernel.

---

## Phase 4 — Migration des registres (1 commit par item)

Ordre proposé (par criticité + indépendance) :

- [x] **#1 ScriptRunnerRegistry** — `AbstractScriptRunner` implémente `Registrable`, `kernel._init_script_runner_registry` utilise `SingletonRegistry[AbstractScriptRunner]`, 4 defaults inline dans le kernel (à déplacer dans `core_addon_manager.get_script_runner_classes()` plus tard). Classe custom supprimée. Validé via `wex demo::yaml/hello`.
- [x] **#2 StepGuardRegistry** — `AbstractStepGuard` implémente `Registrable`. `StepGuardRegistry` hérite désormais de `SingletonRegistry[AbstractStepGuard]` et conserve ses méthodes métier (`should_skip_step`, `get_all_step_options`). Passage **list → dict** sans casse (any() court-circuite, get_all_step_options agrège). Validé via `wex demo::yaml/hello`.
- [x] **#5 Webhook type_resolvers** — `_load_type_resolvers` retourne désormais un `Registry[WebhookTypeResolver]`, `WebhookHttpRequestHandler.type_resolvers` typé Registry. API consumer (`.get(command_type)`) inchangée. Validé via `wex core::webhook/listen --dry-run`.
- [x] **#3 RunnerRegistry** (packages/runner) — hérite désormais de `SharedRegistry[AbstractRunner]` (mode singleton via `.shared()` préservé + mode instance dédiée disponible), garde `get_or_raise` et `status` comme méthodes métier. Validé via test direct (shared singleton, instance dédiée, reset, isolation entre sous-classes).
- [~] **#4 EventDispatcher** — **HORS SCOPE** (faux candidat) : c'est un pattern Pub/Sub (`dict<event, list<listener>>` avec mutations runtime, tri par priorité, bubbling, async dispatch), pas un Registry. Mériterait sa propre roadmap si on veut le standardiser.
- [x] **#6 SpinnerPool** — hérite désormais de `SharedRegistry[Spinner]`. Méthodes classmethod ad-hoc remplacées par méthodes d'instance avec `get_or_create()` pour la lazy creation. RLock préservé. 2 call sites mis à jour (`SpinnerPool.next()` → `SpinnerPool.shared().next()`).
- [x] **#7 WithConfigRegistry** (pseudocode) — Refacto `is-a` → `has-a` : `CodeGenerator` instancie un `Registry[type]` au lieu d'hériter d'un mixin. Mixin `WithConfigRegistry` supprimé. Validé via génération YAML → Python.
- [ ] **Cas spécial KernelRegistry** — laissé tel quel (modèle métier persisté distinct du pattern dict<key,item>, `SerializableMixin` suffit). À revisiter seulement si refacto de fond.
- [x] **Candidat additionnel — AppsRegistry** (apps_registry.py de wex-addon-app) — réécrit comme `AppsRegistry(WithFileLockMixin, SharedRegistry[dict], DiskPersistedRegistry[dict])`. Lock cross-process pour writes, format on-disk `{"apps": ...}` préservé. Validé via `wex app/list` + tests directs (load/add/remove/format on-disk).

---

## Phase 5 — Documentation & garde-fous

- [ ] Décision écrite dans `.wex/knowledge/decisions/registry-pattern.md`.
- [ ] Grep CI : interdire toute nouvelle classe `*Registry` qui ne dérive pas de `Registry[T]`.
- [ ] Doc auteurs d'addons : "comment créer un nouveau type de registre".

---

## Décisions actées

- ✅ **Protocol** pour `Registrable`, fallback Mixin si trop restrictif à l'usage.
- ✅ **Ordre d'attaque** : registrification → async sur `_create_options` (Phase 1.7 d'[async.md](async.md)) → migration des autres registres.
- ✅ **`KernelRegistry`** → réécrit en tant que `DiskPersistedRegistry` (Phase 2bis).
- ✅ **Pas de rétro-compat** : cassure directe, on corrige tous les call sites en même temps.

---

## Liens

- [async.md](async.md) Phase 1.5 (imports addons) — pourra être réécrit comme cas particulier d'init de registre.
- [publication-strategies-pipeline.md](publication-strategies-pipeline.md) — stratégies de publication = cas typique de registre, à vérifier.

## Notes

- Prérequis pour rendre l'init async propre et généralisable. Sans cette base, on disperse l'async dans N classes custom.
- Effort estimé : Phases 2-3 ≈ 1-2 jours focus, Phase 4 ≈ 2-4h par registre migré, Phase 5 ≈ 1-2h.
- Risque principal : casser des call sites externes → atténué par déprécation douce + tests.
