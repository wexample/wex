# Refonte de l'architecture master

## Context

The current master (May 2026) is functional but has several structural frictions that have accumulated over the sessions:

- `project.yml > stacks > apps` lists **app paths** (`${LOCAL}/tpa`, `${LOCAL}/oscar`…). If an app is renamed, moved or deleted, the YAML file breaks. Seen this session: oscar removed, but the tpa stack still referenced `${LOCAL}/oscar` until a manual fix.
- `master.local.yml > MASTER_APP_PATHS` mixes the *definition of folders to scan* and the *explicit list of apps*. Implicit behaviour.
- No host registry: IPs are scattered across N `.wex/env/<env>/config.yml` files in apps. Friction noted in workstream #8 of `master.md`.
- No app registry either: every `master::info/show` call re-scans the disk, redoes discovery. No memory between runs.
- Appearance/disappearance of an app handled silently by the scan — no alert if an app disappears from disk.

The idea is to rebuild the master on more solid principles, while keeping backward compatibility during the transition.

## Target principles

### 1. Self-describing apps

An app = a folder containing a `.wex/config.yml` with:
```yaml
global:
  name: tpa           # app identity, independent of the folder
  version: 3.5.82
  ...
```

The **name** in the config is the canonical identifier. The **folder** is an organisational detail (can move without breaking references).

### 2. Stacks by name or tag, not by path

Today:
```yaml
stacks:
  tpa:
    apps:
      - ${LOCAL}/tpa
      - ${LOCAL}/oscar       # ← hard-coded path, fragile
```

Target:
```yaml
stacks:
  tpa:
    apps: [tpa, oscar]       # ← canonical names
    # OR
    tags: [tpa-core]         # ← apps declare `tags: [tpa-core]` in their config
```

An app can carry multiple tags (`tags: [tpa-core, web, php]`). A stack can combine an explicit list and tag-based filters.

### 3. Centralised discovery

Today `apps:` at the top of `project.yml` mixes discovery and declaration. To separate:

- **`master.local.yml`** defines where to look for apps (varies by machine — local vs server, etc.):
  ```yaml
  app_discovery_paths:
    - ${LOCAL}/*
    - ${PACKAGES}/*
    - ${PROJECT}/*/*
  ```
- **`project.yml`** no longer declares the list — it describes the logical structure (stacks, DNS, etc.) — this is versioned and identical between machines.

### 4. Auto-enrolment & registries

Master maintains two registries:

#### App registry (`apps.yml`, versioned)

Updated on every scan. Sample format:
```yaml
apps:
  tpa:
    name: tpa
    path_hint: local/tpa             # informational, for reference
    version: 3.5.82
    tags: [tpa-core, web]
    enrolled_at: 2026-05-28
  plausible:
    name: plausible
    path_hint: local/plausible
    version: 1.0.0
    tags: [analytics]
    enrolled_at: 2026-05-28
```

#### Host/remote registry (`hosts.yml`, partially versioned, secrets kept local)

```yaml
hosts:
  tpa_prod:
    ip: 51.210.104.199
    type: ovh-vps
    discovered_via: tpa/.wex/env/prod/config.yml
  tpa_dev:
    ip: 152.228.175.159
    discovered_via: tpa/.wex/env/dev/config.yml
  wexample_prod:
    ip: 151.80.23.108
  syrtis_prod:
    ip: 79.137.89.25
```

Note: the `remotes[].host` values in app configs are the **primary sources of truth**. The master registry only aggregates them.

#### Enrolment behaviour

- `wex master::scan` (or `master::enroll`) walks the discovery paths
- Reads each `.wex/config.yml` found
- For each new app: adds it to the versioned `apps.yml` + optionally adds the path to a non-versioned local cache (`apps.cache.yml`)
- For each new remote seen in `.wex/env/*/config.yml`: adds it to `hosts.yml`
- **Disappearance**: if an app/host disappears from disk, **do not remove it from the registry automatically** — emit a warning (`WARNING: app 'oscar' was enrolled but no longer found in discovery paths; run 'master::registry/clear oscar' to remove`)

The registry is resilient to glitches — a folder accidentally removed does not erase the memory.

### 5. Cross-referencing

With registries in place:

- An app can reference a host by name: `remotes[].host: ${HOST_TPA_PROD}` (unblocks #6.5 and #9 from [master.md](master.md))
- A stack can compose apps by tag or name
- Master commands take names (`wex master::host/spawn --based-on tpa_prod`) instead of paths

## Workflow for adding a new app

Today (May 2026):
1. Create the folder `local/myapp/`
2. Initialise `.wex/config.yml`
3. Edit `project.yml` to add the path to `apps:` (often forgotten — the `${MASTER_APP_PATHS}` glob fortunately handles it)
4. If deploying: create `.wex/env/prod/config.yml` with `remotes[].host: <ip>` (hard-coded IP)
5. Repeat for each env

Target:
1. Create the folder `local/myapp/`
2. Initialise `.wex/config.yml` with `global.name + tags`
3. `wex master::scan` (or auto-trigger via watch?)
   - Detects the new app → registry + cache
   - Finds a `.wex/env/prod/config.yml` → adds the host to the registry if new
4. To attach to a stack: `wex master::stack/add tpa myapp` or edit `project.yml > stacks > tpa > apps: [..., myapp]`
5. That's it.

## Open topics (to clarify later)

- **Watch vs manual scan?** A filesystem watcher (inotify) that re-enrols on the fly would be great, but adds a layer of complexity. Probably start with manual scan + scheduled.
- **How to version `apps.yml`** without turning it into a merge conflict bottleneck? At master level = yes (it is the identity of the project). Within the TPA master it should be fine because only one operator edits at a time in practice.
- **The local cache (`apps.cache.yml`)** — should it store full paths, or just a `name → relative_path` mapping?
- **How to handle `discovered_via`** when an app has multiple envs on multiple hosts? List of origins?
- **Integration with `master::info/show`**: does the command now pull data from the registry, or keep scanning to stay in sync? Probably registry by default + a `--rescan` flag to force.
- **What determines "an app has disappeared"?** The path no longer exists? The `global.name` no longer found in the discovered apps? Edge case if a folder is renamed without changing the `name`.
- **The "stack" concept** deserves to be enriched: today it is just a named group of apps. With orchestration (#9 of master.md), it needs a dependency order and constraints (cf. Syrtis example).
- **Backward compatibility**: during the transition, the current `apps:` paths must continue to work during the migration. Bridge mechanism.

## Links

- [master.md](master.md) workstreams #1, #4, #6.5, #8, #9 depend on or benefit from this refactor
- [post-tpa-migration-checklist.md](post-tpa-migration-checklist.md) — not directly related, but touches the same files
