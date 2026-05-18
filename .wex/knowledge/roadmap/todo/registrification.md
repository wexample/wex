# Registrification — Standardisation du pattern Registry

## Objectif

Unifier toutes les collections de type "liste de classes / singletons" derrière le pattern standard `Registry[T]` + `RegistryContainerMixin`, et y centraliser :
1. **L'init** (sync ou async).
2. **La résolution de dépendances** entre items.

## Constat

Le pattern standard existe :
- [registry.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/service/registry.py) — `Registry[T]` : dict + `get/has/register/get_all/all_keys`.
- [registry_container_mixin.py](../../../../../../../PACKAGES/PYTHON/packages/helpers/src/wexample_helpers/service/mixins/registry_container_mixin.py) — Container avec `_registries: dict[str, Registry]`.
- [service_container_mixin.py](../../../../../../../PACKAGES/PYTHON/packages/app/src/wexample_app/service/mixins/service_container_mixin.py) — Extension pour services.

**Bon élève** : `kernel._init_addons` et `kernel._init_middlewares` passent par `register_items("addons", ...)` / `register_items("middlewares", ...)`.

**Mauvais élèves** :
- [kernel.py:577 _init_script_runner_registry](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/common/kernel.py#L577) → instancie une classe custom [script_runner_registry.py](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/yaml/script_runner_registry.py) avec `dict[str, runner]` ad-hoc + `_register_defaults()` qui hard-code les runners par défaut.
- [kernel.py:582 _init_step_guard_registry](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/common/kernel.py#L582) → instancie [step_guard_registry.py](../../../../../../../PACKAGES/PYTHON/wex/wex-core/src/wexample_wex_core/yaml/step_guard_registry.py) qui est en plus une **liste** (pas un dict), avec `register(guard)` signature différente.

Conséquences :
- Deux interfaces parallèles à maintenir (`all()` vs `get_all()`, `register(item)` vs `register(key, item)`).
- Aucun accès uniforme via `kernel.get_item("script_runners", "bash")`.
- L'init async (roadmap [async.md](async.md)) doit être pensé deux fois si on garde le double pattern.

---

## Phase 1 — Audit complet des "registres cachés"

- [ ] Lister tous les `dict[str, X]` ou `list[X]` du kernel + addons qui ont une sémantique "registre" (collection de classes/instances enregistrées à l'init).
- [ ] Candidats déjà connus :
  - [ ] `ScriptRunnerRegistry`
  - [ ] `StepGuardRegistry`
  - [ ] `KernelRegistry` (cas spécial : persistance fichier — peut-être à laisser à part)
  - [ ] `resolvers` (kernel) — vérifier comment c'est stocké
  - [ ] `webhook type_resolvers` (handler.py:160) — `dict[str, AddonWebhookTypeResolver]` construit ad-hoc
  - [ ] Dans wex-addon-app : registries de services, builds, containers
- [ ] Établir critère explicite : "qu'est-ce qui mérite d'être un Registry ?"
  - Plusieurs items du même type
  - Enregistrés à l'init (pas mutables après usage normal)
  - Lookup par clé string
  - Peuvent provenir de plusieurs sources (core + addons)

---

## Phase 2 — Mixin `Registrable` avec dépendances

Aujourd'hui `RegistrableType = TypeVar("RegistrableType")` est juste un TypeVar, donc aucun contrat sur les items. À remplacer par un **mixin/Protocol** explicite :

- [ ] Créer `Registrable` (mixin ou Protocol) dans `wexample_helpers/service/registrable.py` avec :
  ```python
  class Registrable:
      @classmethod
      def get_registry_key(cls) -> str: ...
      @classmethod
      def dependencies(cls) -> list[type[Registrable]]: return []
      def init_sync(self) -> None: ...
      async def init_async(self) -> None: ...  # default = run sync in thread
  ```
- [ ] `Registry.register(item)` (signature simplifiée) → dérive la clé via `item.get_registry_key()`.
- [ ] `Registry.resolve_init_order()` → tri topologique des items selon `dependencies()`.
- [ ] Détection des cycles → exception explicite avec la chaîne fautive.
- [ ] Conserver l'API actuelle `register(key, item)` en surcharge pour rétro-compat (déprécation douce).

Discussion :
- **Protocol** (PEP 544) plus souple : pas d'héritage forcé, juste duck typing.
- **Mixin** plus explicite : `class BashScriptRunner(Registrable, AbstractScriptRunner)`.
- → On part sur **Protocol** par défaut pour ne pas forcer la hiérarchie, sauf si on a besoin d'attributs partagés.

---

## Phase 3 — Init async dans Registry

Le registre devient le point d'entrée pour l'init async (lien direct avec [async.md](async.md) Phase 1.5).

- [ ] Méthode `Registry.init_all_async()` :
  - Résout l'ordre topologique via `dependencies()`.
  - Calcule les **couches indépendantes** (items sans deps entre eux → même couche).
  - Pour chaque couche : `await asyncio.gather(*[item.init_async() for item in layer])`.
  - Les couches s'enchaînent séquentiellement (dep avant dépendant).
- [ ] Méthode `Registry.init_all_sync()` (fallback / mode debug) : init dans l'ordre topologique sans parallélisme.
- [ ] `RegistryContainerMixin.init_all_registries_async()` qui parallélise aussi entre registres indépendants.
- [ ] Mesurer : sur le bootstrap kernel, combien de % du temps est gagné ?

---

## Phase 4 — Migration des registres existants

Une fois la base prête, on bascule un par un (chacun en un commit séparé pour pouvoir bisecter) :

- [ ] **ScriptRunnerRegistry** :
  - Faire hériter `AbstractScriptRunner` du Protocol `Registrable`.
  - Supprimer la classe `ScriptRunnerRegistry`, remplacer par `kernel.get_registry("script_runners", Registry[AbstractScriptRunner])`.
  - Les 4 runners par défaut (bash, docker, exec, python) sont enregistrés dans `core_addon_manager.get_script_runner_classes()` (à créer) au lieu de `_register_defaults()`.
  - Adapter les call sites (grep `script_runner_registry`).
- [ ] **StepGuardRegistry** :
  - Idem. Note : passage **list → dict** — vérifier que personne ne dépend de l'ordre d'insertion (sinon préserver via `OrderedDict` ou `dependencies()`).
- [ ] **Webhook type_resolvers** (handler.py:160) :
  - Le dict est rebuilt à chaque démarrage du daemon. Bonne occasion d'en faire un registre proper.
- [ ] **Autres candidats identifiés en Phase 1** : un par un.

---

## Phase 5 — Documentation & garde-fous

- [ ] Décision écrite dans `.wex/knowledge/decisions/registry-pattern.md` : pourquoi tout registre passe par `Registry[T]` + `Registrable` Protocol.
- [ ] Linter custom (ou simple grep CI) : interdire toute nouvelle classe `*Registry` qui ne dérive pas de `Registry[T]`.
- [ ] Documenter l'API pour les auteurs d'addons : "comment créer un nouveau type de registre dans ton addon".

---

## Liens avec autres roadmaps

- [async.md](async.md) **Phase 1.5** (imports addons) — pourra être réécrit comme un cas particulier d'init de registre une fois la base posée. À voir lequel des deux on attaque en premier.
- [publication-strategies-pipeline.md](publication-strategies-pipeline.md) — les stratégies de publication sont aussi un cas typique de registre (déjà ?).

---

## Décisions encore ouvertes

- [ ] **Protocol vs Mixin** pour `Registrable` ? (penche Protocol)
- [ ] **Ordre d'attaque** entre cette roadmap et async.md ? (Faire d'abord registrification permet de centraliser l'async dans Registry — plus propre. Mais plus long avant de voir un gain.)
- [ ] **`KernelRegistry`** (commands) — cas spécial avec persistance fichier — on l'embarque ou on le laisse à part ?
- [ ] **Rétro-compat** : on garde `register(key, item)` en plus de `register(item)` ou on casse direct ?

---

## Notes

- Ce refacto est **prérequis** pour rendre l'init async propre et généralisable. Sans lui, on disperse la logique async dans N classes Registry custom.
- Effort estimé : Phases 1-3 ≈ 1-2 jours focus, Phase 4 ≈ 2-4 heures par registre migré, Phase 5 ≈ 1-2h.
- Risque principal : casser des call sites externes (addons tiers, code utilisateur). À atténuer via dépréciation douce et tests.
