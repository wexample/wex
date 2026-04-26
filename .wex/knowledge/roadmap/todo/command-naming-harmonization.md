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

- [x] `app::file-state/rectify` → `app::file/rectify`

---

## Phase 4 — Simplifier les actions verbeuses ou ambiguës

- [ ] `app::package/commit_and_push` → `app::package/push`
  (le commit est implicite dans le push d'un package)
- [ ] `app::package/publish_bumped` → `app::package/release`
  (bump + publish = release ; mot plus expressif)
- [ ] `app::suite/exec_command` → `app::suite/run`
- [ ] `app::suite/exec_shell` → `app::suite/shell`
- [ ] `default::configure/env` → `default::env/configure`
  (inversion : groupe = ressource, action = verbe)
- [ ] `default::check/health` → `default::health/check`
  (même raison)

---

## Phase 5 — Résoudre doublons et ambiguïtés

**`info/show` en double** (`app` et `default`) — deux commandes différentes, noms identiques :
- [ ] `default::info/show` → `default::wex/info` (info sur wex lui-même, pas sur une app)

**Vocabulaire `registry` incohérent** — `build` vs `write` pour la même idée :
- [ ] `app::registry/write` → `app::registry/build`

**`check/hi` dans default** — nom cryptique, symétrie avec `demo::ping/pong` manquée :
- [ ] `default::check/hi` → `default::ping/pong` (ou `default::wex/ping`)

**`helper/start` et `helper/stop`** — "helper" est vague, à clarifier selon ce que ça désigne :
- [ ] Renommer selon la nature réelle : `proxy/start`, `sidecar/start`, ou `worker/start`

---

## Phase 6 — Réflexion sur le découpage de l'addon `app`

L'addon `app` concentre ~55 commandes sur des domaines distincts (lifecycle, infra, packages, migrations, tests…).
À évaluer avant d'implémenter — ne découper que si le couplage est faible.

- [ ] Évaluer l'extraction d'un addon `pkg` : `package/*` + `suite/*` + `dependency/*` + `library/*`
- [ ] Évaluer l'extraction d'un addon `infra` : `container/*` + `image/*` + `runtime/*` + `performance/*`
- [ ] Garder `app` pour le pur lifecycle : `start`, `stop`, `restart`, `init`, `go`, `setup`, `perms`, `publish`
- [ ] Ne pas découper si les commandes partagent fortement le contexte app (services, config, env)
