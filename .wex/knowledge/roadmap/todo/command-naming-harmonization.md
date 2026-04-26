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
- [x] `core::configure/env` → `core::env/configure`
- [x] `core::check/health` → `core::health/check`

---

## Phase 5 — Renommer l'addon `default` en `core`

`default` est un détail d'implémentation sans sens métier. `core` dit ce que c'est : les commandes fondamentales de wex. Toutes les commandes `core::*` deviennent `core::*`.

**Fichiers et classes à renommer dans `wex-core` :**
- [x] Dossier `addons/default/` → `addons/core/`
- [x] Fichier `default_addon_manager.py` → `core_addon_manager.py`
- [x] Classe `DefaultAddonManager` → `CoreAddonManager`
- [x] Import dans `wex.py` mis à jour

**Noms de fonctions** — `default__*__*` → `core__*__*` dans tous les fichiers de commandes :
- [x] `default__autocomplete__suggest` → `core__autocomplete__suggest`
- [x] `default__check__hi` → `core__check__hi`
- [x] `default__command__create` → `core__command__create`
- [x] `default__env__configure` → `core__env__configure`
- [x] `default__health__check` → `core__health__check`
- [x] `default__info__show` → `core__info__show`
- [x] `default__logo__show` → `core__logo__show`
- [x] `default__registry__build` → `core__registry__build`
- [x] `default__self__upgrade` → `core__self__upgrade`
- [x] `default__version__get` → `core__version__get`
- [x] `default__version__increment` → `core__version__increment`
- [x] `default__webhook__*` → `core__webhook__*` (6 commandes)

**Références string** — partout où `"default"` désigne l'addon (docs, YMLs, code) :
- [x] `default::` → `core::` dans tous les `.md`, `.yml`, `.py`
- [x] Appels string vérifiés (webhook/listen.py, webhook/handler.py, webhook_tokens.yml)

---

## Phase 5.2 — Résoudre doublons et ambiguïtés restants

**`info/show` en double** (`app` et `core`) — résolu par le renommage de l'addon :
- [x] `core::info/show` — ok tel quel, plus de doublon depuis que l'addon s'appelle `core`

**Vocabulaire `registry` incohérent** — `build` vs `write` pour la même idée :
- [ ] `app::registry/write` → `app::registry/build`

**`check/hi` dans core** — ping de vitalité de wex, alias `hi` :
- [ ] `core::check/hi` → `core::wex/ping`

**`helper/start` et `helper/stop`** — app compagnon pré-configurée (ex: proxy) lancée en sidecar :
- [ ] `app::helper/start` → `app::sidecar/start`
- [ ] `app::helper/stop` → `app::sidecar/stop`

---

## Phase 6 — Réflexion sur le découpage de l'addon `app`

L'addon `app` concentre ~55 commandes sur des domaines distincts (lifecycle, infra, packages, migrations, tests…).
À évaluer avant d'implémenter — ne découper que si le couplage est faible.

- [ ] Évaluer l'extraction d'un addon `pkg` : `package/*` + `suite/*` + `dependency/*` + `library/*`
- [ ] Évaluer l'extraction d'un addon `infra` : `container/*` + `image/*` + `runtime/*` + `performance/*`
- [ ] Garder `app` pour le pur lifecycle : `start`, `stop`, `restart`, `init`, `go`, `setup`, `perms`, `publish`
- [ ] Ne pas découper si les commandes partagent fortement le contexte app (services, config, env)
