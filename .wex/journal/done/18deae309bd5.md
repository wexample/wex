# Registrification — Standardisation du pattern Registry

## Objective

Unify all collections of the "list of classes / singletons" type behind `Registry[T]` + `RegistryContainerMixin` ([registry.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/service/registry.py), [registry_container_mixin.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/service/mixins/registry_container_mixin.py)), and centralise there:
1. **Init** (sync or async).
2. **Dependency resolution** between items.

---

## Audit (DONE)

Retained criteria (cumulative, ≥3/4): collection of same-type items, populated at init then read-only, lookup by key OR iteration, multiple sources possible.

### True migration candidates

| # | Name | File | Status | Criticality | Item source |
|---|------|------|--------|-------------|-------------|
| 1 | `ScriptRunnerRegistry._runners` | [yaml/script_runner_registry.py:17](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/yaml/script_runner_registry.py#L17) | CUSTOM | HIGH | 4 hard-coded defaults + addons |
| 2 | `StepGuardRegistry._guards` | [yaml/step_guard_registry.py:18](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/yaml/step_guard_registry.py#L18) | CUSTOM (list!) | HIGH | Addons via `get_step_guard_classes()` |
| 3 | `RunnerRegistry._runners` | [packages/runner/runner_registry.py:16](../../../../../../../PACKAGES/PYTHON/packages/runner/src/wexample_runner/runner_registry.py#L16) | CUSTOM | MEDIUM | `register(name, runner)` |
| 4 | `EventDispatcher._event_listeners` | [packages/event/common/dispatcher.py:44](../../../../../../../PACKAGES/PYTHON/packages/event/src/wexample_event/common/dispatcher.py#L44) | HYBRID | HIGH | `add_event_listener()` (dynamic) |
| 5 | Webhook `type_resolvers` | [webhook/handler.py:96](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/webhook/handler.py#L96) | INLINE | MEDIUM | `_load_type_resolvers()` (listen.py:138) |
| 6 | `SpinnerPool._spinners` | [packages/prompt/common/spinner_pool.py:98](../../../../../../../PACKAGES/PYTHON/packages/prompt/src/wexample_prompt/common/spinner_pool.py#L98) | CUSTOM | LOW | `get(key)` lazy |
| 7 | `WithConfigRegistry._registry` | [packages/pseudocode/common/with_config_registry.py:17](../../../../../../../PACKAGES/PYTHON/packages/pseudocode/src/wexample_pseudocode/common/with_config_registry.py#L17) | INLINE | LOW | Hard-coded `__init__` |

### Already compliant (STANDARD)

- ✅ Kernel `addons` (`REGISTRY_KERNEL_ADDON`) — [kernel.py:150](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/common/kernel.py#L150)
- ✅ Kernel `middlewares` — [kernel.py:548](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/common/kernel.py#L548)
- ✅ `RegistryContainerMixin._registries` — the meta-registry itself.

### Special cases to handle separately

- **`KernelRegistry`** [registry/kernel_registry.py:28](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/registry/kernel_registry.py#L28) — HYBRID, HIGH. Specific: file persistence (`registry.json`), hydration via resolvers. **Keep isolated** as its lifecycle differs. Can implement the `Registrable` Protocol without breaking its persistence.
- **Nested options in `wexample_config`** [config_option/abstract_nested_config_option.py:32](../../../../../../../PACKAGES/PYTHON/packages/config/src/wexample_config/config_option/abstract_nested_config_option.py#L32) — more **typed option composition** than a registry. Decision deferred → targeted audit Phase 1bis.

### False positives (DO NOT migrate)

- ❌ Webhook `_counters` / `_duration_sum` / `_duration_count` — mutable runtime metrics.
- ❌ `_REGISTRY_CACHE` (abstract_nested_config_option.py:7) — perf cache, not a registry.
- ❌ `AbstractResult.operations` (filestate) — build result, accumulated then consumed.
- ❌ App registry (`with_app_registry_mixin.py`) — config serialised to/from YAML.

### Recurring pattern identified

Pattern `for addon in kernel.get_addons().values(): collect addon.get_X_classes()` present in:
- `_init_middlewares` ✅ already standard
- `_init_step_guard_registry` ❌ #2
- `_init_resolvers` → to be verified
- `_load_type_resolvers` (webhook) ❌ #5

→ A single generic `Registry.populate_from_addons(method_name)` mechanism could replace these 4+ loops.

---

## Phase 1bis — Remaining audits

- [ ] Decide: `wexample_config` nested options = registry or composition?
- [ ] Verify `_init_resolvers` in the kernel (STANDARD or not?).
- [ ] Re-grep `wex-addon-app`: services, builds, containers.

### Additional candidate — Suite packages

**[FrameworkPackagesSuiteWorkdir](../../../../../../../PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/workdir/framework_packages_suite_workdir.py)**: the list of packages in a suite is a disguised registry.

- Same-type items (package workdirs), multiple iterations (build, publish, version bump...).
- **Inter-package dependencies** exist → topological sort useful for build/publish order.
- Discovered via filesystem (paths), not via explicit `register()`.

→ Possible new variant **`FilesystemDiscoveredRegistry`** OR a `populate_from_paths(paths, item_class)` method on `SingletonRegistry`. To be decided at migration time.

---

## Phase 2 — `Registrable` Protocol with dependencies

`RegistrableType = TypeVar("RegistrableType")` is currently empty. To be replaced by an explicit Protocol (fallback Mixin if too restrictive in practice).

- [ ] Create `Registrable` Protocol in `wexample_helpers/service/registrable.py`:
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
- [ ] `Registry.register(item)`: simplified signature, key derived via `item.get_registry_key()`. **No backward compat** on `register(key, item)`.
- [ ] `Registry.resolve_init_order()` → topological sort of items according to `dependencies()`.
- [ ] Cycle detection → explicit exception with the offending chain.

## Phase 2ter — `SharedRegistry` (singleton access per class)

Orthogonal variant that adds a "globally accessible shared instance" mode, without giving up the standard instance-based mode. Useful when a registry must be reachable from anywhere without passing a reference (typical case: process-level registries such as external package runners).

- ✅ Created in `wexample_helpers/service/shared_registry.py`.
- API: `MyRegistry.shared()` returns the shared instance (lazily created, isolated per subclass).
- Dedicated instance mode preserved: `MyRegistry()` always creates a new instance.
- `reset_shared()` exposed for tests.

## Phase 2bis — `DiskPersistedRegistry` (DONE)

- ✅ Created `DiskPersistedRegistry(Registry[T])`. Moved on 2026-05-20 from `wexample_helpers/service/disk_persisted_registry.py` to `wexample_filestate/service/disk_persisted_registry.py` to resolve a dependency cycle (the class is intrinsically coupled to `StructuredContentFile` which lives in filestate).
- ✅ Accepts a duck-typed file with `read_parsed()`/`write_parsed()`/`get_local_file().is_empty()` — compatible with `JsonFile`/`YamlFile` from filestate.
- ✅ `is_persisted()` tolerates missing file.
- ✅ `load()` is a no-op if the file is absent.
- ✅ Validated via `AppsRegistry` (see Phase 4 #additional candidate).

## Phase 2quater — `WithFileLockMixin` (DONE)

- ✅ Created in `wexample_helpers/service/with_file_lock_mixin.py`.
- ✅ Context manager `file_lock()` via cross-process `fcntl.flock`.
- ✅ `_get_locked_resource_path()` to be implemented by the consumer class (otherwise explicit NotImplementedError).
- ✅ Validated via `AppsRegistry` (composition `WithFileLockMixin + SharedRegistry + DiskPersistedRegistry`).

---

## Phase 3 — Async init in Registry

Direct link with [async.md](async.md) Phase 1.5.

- [ ] `Registry.init_all_async()`:
  - Topological resolution via `dependencies()`.
  - Compute **independent layers** → `await asyncio.gather(*layer)`.
  - Layers chained sequentially.
- [ ] `Registry.init_all_sync()` (fallback / debug).
- [ ] `RegistryContainerMixin.init_all_registries_async()` that parallelises across independent registries.
- [ ] Measure the gain on kernel bootstrap.

---

## Phase 4 — Registry migration (1 commit per item)

Proposed order (by criticality + independence):

- [x] **#1 ScriptRunnerRegistry** — `AbstractScriptRunner` implements `Registrable`, `kernel._init_script_runner_registry` uses `SingletonRegistry[AbstractScriptRunner]`, 4 inline defaults in the kernel (to be moved into `core_addon_manager.get_script_runner_classes()` later). Custom class removed. Validated via `wex demo::yaml/hello`.
- [x] **#2 StepGuardRegistry** — `AbstractStepGuard` implements `Registrable`. `StepGuardRegistry` now inherits from `SingletonRegistry[AbstractStepGuard]` and keeps its business methods (`should_skip_step`, `get_all_step_options`). **list → dict** switch without breakage (any() short-circuits, get_all_step_options aggregates). Validated via `wex demo::yaml/hello`.
- [x] **#5 Webhook type_resolvers** — `_load_type_resolvers` now returns a `Registry[WebhookTypeResolver]`, `WebhookHttpRequestHandler.type_resolvers` typed Registry. Consumer API (`.get(command_type)`) unchanged. Validated via `wex core::webhook/listen --dry-run`.
- [x] **#3 RunnerRegistry** (packages/runner) — now inherits from `SharedRegistry[AbstractRunner]` (singleton mode via `.shared()` preserved + dedicated instance mode available), keeps `get_or_raise` and `status` as business methods. Validated via direct test (shared singleton, dedicated instance, reset, isolation between subclasses).
- [~] **#4 EventDispatcher** — **OUT OF SCOPE** (false candidate): it is a Pub/Sub pattern (`dict<event, list<listener>>` with runtime mutations, priority sorting, bubbling, async dispatch), not a Registry. Would deserve its own roadmap if standardisation is wanted.
- [x] **#6 SpinnerPool** — now inherits from `SharedRegistry[Spinner]`. Ad-hoc classmethod methods replaced by instance methods with `get_or_create()` for lazy creation. RLock preserved. 2 call sites updated (`SpinnerPool.next()` → `SpinnerPool.shared().next()`).
- [x] **#7 WithConfigRegistry** (pseudocode) — Refactoring `is-a` → `has-a`: `CodeGenerator` instantiates a `Registry[type]` instead of inheriting from a mixin. `WithConfigRegistry` mixin removed. Validated via YAML → Python generation.
- [ ] **Special case KernelRegistry** — left as-is (persisted business model distinct from the dict<key,item> pattern, `SerializableMixin` suffices). To revisit only on a deep refactoring.
- [x] **Additional candidate — AppsRegistry** (apps_registry.py from wex-addon-app) — rewritten as `AppsRegistry(WithFileLockMixin, SharedRegistry[dict], DiskPersistedRegistry[dict])`. Cross-process lock for writes, on-disk format `{"apps": ...}` preserved. Validated via `wex app/list` + direct tests (load/add/remove/format on-disk).

---

## Phase 5 — Documentation & guardrails

- [ ] Decision written in `.wex/knowledge/decisions/registry-pattern.md`.
- [ ] CI grep: disallow any new `*Registry` class that does not derive from `Registry[T]`.
- [ ] Addon author doc: "how to create a new registry type".

---

## Agreed decisions

- ✅ **Protocol** for `Registrable`, fallback Mixin if too restrictive in practice.
- ✅ **Order of attack**: registrification → async on `_create_options` (Phase 1.7 of [async.md](async.md)) → migration of the remaining registries.
- ✅ **`KernelRegistry`** → rewritten as `DiskPersistedRegistry` (Phase 2bis).
- ✅ **No backward compat**: direct break, all call sites fixed at the same time.

---

## Links

- [async.md](async.md) Phase 1.5 (addon imports) — may be rewritten as a special case of registry init.
- [publication-strategies-pipeline.md](publication-strategies-pipeline.md) — publication strategies = typical registry case, to be verified.

## Closing notes

### What was delivered

- `Registrable` Protocol (`get_registry_key`, `dependencies`, `init_sync`, `init_async`).
- **4 Registry variants** in `wexample_helpers/service/`:
  - `Registry[T]` — generic base, `register(item, key=None)` with auto-derive.
  - `SingletonRegistry[T]` — classes instantiated with topological sync/async init.
  - `SharedRegistry[T]` — shared instance per class via `.shared()`, isolated between subclasses.
  - `DiskPersistedRegistry[T]` — persistence via `StructuredContentFile` (JsonFile/YamlFile).
- 1 composable mixin: `WithFileLockMixin` (cross-process fcntl).
- **6 validated migrations**: ScriptRunner #1, StepGuard #2, Runner #3, Webhook type_resolvers #5, SpinnerPool #6, WithConfigRegistry #7.
- **1 bonus**: `AppsRegistry` (composition of the 3 variants + mixin, demonstrates composability).
- #4 EventDispatcher: classified OUT OF SCOPE (Pub/Sub pattern, not Registry).

### Deferred remainders (non-blocking)

- Phase 1bis audits (config nested options, `_init_resolvers`, services/builds/containers wex-addon-app).
- Phase 3 (async init in Registry): `SingletonRegistry.init_all_async()` is delivered, but the `RegistryContainerMixin.init_all_registries_async()` hook was not added — only useful if a concrete use case calls for it.
- Phase 5 (doc + CI lint + decision file): the doc emerges from the already-written roadmaps; a decision file and a CI lint can wait for a real need.
- Additional candidate "Suite packages" (`FrameworkPackagesSuiteWorkdir`): to be explored in a dedicated roadmap if needed.
- KernelRegistry: intentionally left as-is (persisted business model ≠ dict<key,item> pattern).
