# Roadmap : Harmonisation du nommage des commandes wex

Réorganisation du naming pour cohérence, lisibilité et maintenabilité.

**Règles adoptées :**
- Groupe (avant `/`) : toujours **singulier** — il désigne la ressource
- Action (après `/`) : **verbe court** — ce qu'on fait à la ressource
- Pas de répétition du nom de l'addon dans le groupe

---


## Phase 1 — Singulier/pluriel : uniformiser

Actuellement mélangé (`container/list` vs `hosts/clean`, `services/exec` vs `service/install`).

- [x] `app::apps/list` → `app::app/list`
- [x] `app::dependencies/check` → `app::dependency/check`
- [x] `app::dependencies/publish` → `app::dependency/publish`
- [x] `app::hosts/clean` → `app::host/clean`
- [x] `app::hosts/update` → `app::host/update`
- [x] `app::libraries/sync` → `app::library/sync`
- [x] `app::services/exec` → `app::service/exec`

---

## Phase 2 — Supprimer les préfixes redondants avec l'addon

Le groupe ne doit pas répéter le nom de l'addon.

- [x] `docker::docker/ip` → `docker::network/ip`
- [x] `docker::docker/stop_all` → `docker::container/stop_all`
- [x] `system::system/ip` → `system::network/ip`
- [x] `system::system/is_docker` → `system::runtime/is_docker`

---

## Phase 3 — Simplifier file_state

`file_state` est trop technique et utilise un underscore au lieu d'un `/`.
Le concept : rectifier des fichiers selon un état attendu.

- [x] `app::file-state/rectify` → `app::state/rectify`

---

## Phase 4 — Simplifier les actions verbeuses ou ambiguës

- [x] `app::package/commit-and-push` → `app::package/push`
- [x] `app::package/publish-bumped` → `app::package/release`
- [x] `app::suite/exec-command` → `app::suite/run`
- [x] `app::suite/exec-shell` → `app::suite/shell`
- [x] `default::configure/env` → `default::env/configure`
- [x] `default::check/health` → `default::health/check`

---

## Phase 5 — Renommer l'addon `default` en `core`

`default` est un détail d'implémentation sans sens métier. `core` dit ce que c'est : les commandes fondamentales de wex. Toutes les commandes `default::*` deviennent `core::*`.

**Fichiers et classes à renommer dans `wex-core` :**
- [ ] Dossier `addons/default/` → `addons/core/`
- [ ] Fichier `default_addon_manager.py` → `core_addon_manager.py`
- [ ] Classe `DefaultAddonManager` → `CoreAddonManager`
- [ ] Import dans `wex.py` : `from ...addons.default.default_addon_manager import DefaultAddonManager`

**Noms de fonctions** — `default__*__*` → `core__*__*` dans tous les fichiers de commandes :
- [ ] `default__autocomplete__suggest` → `core__autocomplete__suggest`
- [ ] `default__check__hi` → `core__check__hi`
- [ ] `default__command__create` → `core__command__create`
- [ ] `default__env__configure` → `core__env__configure`
- [ ] `default__health__check` → `core__health__check`
- [ ] `default__info__show` → `core__info__show`
- [ ] `default__logo__show` → `core__logo__show`
- [ ] `default__registry__build` → `core__registry__build`
- [ ] `default__self__upgrade` → `core__self__upgrade`
- [ ] `default__version__get` → `core__version__get`
- [ ] `default__version__increment` → `core__version__increment`
- [ ] `default__webhook__*` → `core__webhook__*` (6 commandes)

**Références string** — partout où `"default"` désigne l'addon (docs, YMLs, code) :
- [ ] `default::` → `core::` dans tous les `.md`, `.yml`, `.py`
- [ ] Vérifier les appels par string comme dans `app_should_run_step_guard.py`

---

## Phase 5.2 — Résoudre doublons et ambiguïtés restants

**`info/show` en double** (`app` et `core`) — deux commandes différentes, noms identiques :
- [ ] `core::info/show` → `core::info/show` (à préciser : décrit wex lui-même, pas une app — ok tel quel une fois l'addon renommé)

**Vocabulaire `registry` incohérent** — `build` vs `write` pour la même idée :
- [ ] `app::registry/write` → `app::registry/build`

**`check/hi` dans core** — nom cryptique :
- [ ] `core::check/hi` → à clarifier (test de connectivité ? ping ?)

**`helper/start` et `helper/stop`** — "helper" est vague :
- [ ] Renommer selon la nature réelle : `proxy/start`, `sidecar/start`, ou `worker/start`

---

## Phase 6 — Réflexion sur le découpage de l'addon `app`

L'addon `app` concentre ~55 commandes sur des domaines distincts (lifecycle, infra, packages, migrations, tests…).
À évaluer avant d'implémenter — ne découper que si le couplage est faible.

- [ ] Évaluer l'extraction d'un addon `pkg` : `package/*` + `suite/*` + `dependency/*` + `library/*`
- [ ] Évaluer l'extraction d'un addon `infra` : `container/*` + `image/*` + `runtime/*` + `performance/*`
- [ ] Garder `app` pour le pur lifecycle : `start`, `stop`, `restart`, `init`, `go`, `setup`, `perms`, `publish`
- [ ] Ne pas découper si les commandes partagent fortement le contexte app (services, config, env)
