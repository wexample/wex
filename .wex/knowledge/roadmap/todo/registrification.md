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

## Phase 2bis — `DiskPersistedRegistry` (abstraction du cas KernelRegistry)

Plutôt que de garder `KernelRegistry` à part, créer une abstraction réutilisable.

- [ ] Créer `DiskPersistedRegistry(Registry[T])` dans `wexample_helpers/service/disk_persisted_registry.py` :
  ```python
  class DiskPersistedRegistry(Registry[T]):
      def __init__(self, container: Any, file: StructuredFile):
          super().__init__(container)
          self._file = file
      def save(self) -> None: ...    # serialize items → file.write_parsed()
      def load(self) -> None: ...    # file.read_parsed() → hydrate items
      def is_persisted(self) -> bool: return not self._file.get_local_file().is_empty()
  ```
- [ ] Le `StructuredFile` (alias générique pour `YamlFile | JsonFile`) est passé en construction.
- [ ] Sérialisation/hydratation déléguée aux items (méthodes `serialize()`/`hydrate(data)` sur Registrable).
- [ ] **Bénéfice** : KernelRegistry devient un `DiskPersistedRegistry[CommandData](file=KernelRegistryFile)`. Ouvre la porte à d'autres caches persistés (apps_registry, autocomplete cache, etc.).

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
- [ ] **#2 StepGuardRegistry** — idem. ⚠️ passage **list → dict** : vérifier qu'aucun call site ne dépend de l'ordre d'insertion.
- [ ] **#5 Webhook type_resolvers** — dict rebuilt à chaque démarrage daemon → bon candidat.
- [ ] **#3 RunnerRegistry** (packages/runner) — singleton statique à exposer via container.
- [ ] **#4 EventDispatcher** — plus complexe (registration dynamique, priorité via `_ORDER_ATTR`, thread-safety). À évaluer après les autres.
- [ ] **#6 SpinnerPool** — BASSE priorité, à faire en passant.
- [ ] **#7 WithConfigRegistry** (pseudocode) — BASSE priorité.
- [ ] **Cas spécial KernelRegistry** — implémente `Registrable` mais garde sa persistance fichier.

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
