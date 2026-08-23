# Roadmap master post-migration wex 6

## Context

Wexample / Syrtis / TPA have moved to wex 6 (May 2026). First pass done — all apps are running. What remains: consolidate master tooling + bring TPA CI/CD back up + clean up self-hosted services.

## Work streams

### 1. Add missing remotes to the master

- **TPA dev** ✅ done (`wex master::info/show --remotes dev` shows tpa)
- **wex runner** ⏳ not done — CI/CD runner to expose as master remote to pilot/observe from the dashboard. Local rsync to `/home/weeger/Desktop/WIP/WEB/TPA/local/runner/` for inspection.

Spec: `wex master::info/show --remotes <name>` must show Local Version / Wex / Git for each app on the remote.

### 2. Restore TPA CI/CD (modern version)

Builds have historically been very slow. Goals:

- Get TPA pipelines onto the new wex 6 stack (direct push already works since the manual migration, but gitlab-ci jobs must follow)
- Look for build time optimisations (Docker layer cache, multi-stage, BuildKit, registry mirror, pre-baked base images…)
- Criterion: a commit on `master` must deploy to dev in < X min (to be defined after baseline)

### 3. Update all self-hosted apps

Move each service to its latest stable:

- gitlab-ce (actuellement pin `17.6.1-ce.0`)
- listmonk
- baserow
- matomo
- n8n
- postgres / mysql (par service)
- nginx-proxy / acme-companion

For each app: check changelog → bump image → test locally/in dev → push to prod.

### 4. Improve `wex master::info/*`

Dashboard command to enrich:

- **Service** versions (docker image + tag) per app, not just the app version
- **Multi-env** view: prod + dev + local side by side
- Explicit diff when one env lags behind another
- "Update available" indicator (compare with dockerhub)

### 5. "Update service" workflow

A command like `wex app::service/update <service>` that:

1. Service-specific backup (gitlab-backup, n8n export, mysqldump, pg_dump… each with its own protocol)
2. Fetch latest version from dockerhub (or specified tag)
3. Apply (rebuild + restart)
4. Commit + push the version bump
5. Pull + apply on all other envs (dev → prod)

Goal: zero manual steps, zero forgotten backup.

### 6. "Everything up-to-date in N commands" workflow

Vision: from the master, in a few commands:

- All wex apps up to date (wex CLI)
- All envs up to date
- All self-hosted services on their latest stable

This comes naturally once (1), (4), (5) are in place.

### 6.5. `wex upgrade` everywhere

Currently doable manually: `for srv in ...; do ssh weeger@$srv "wex upgrade"; done`. Done for 4 servers in 6.0.104 on 2026-05-28.

To industrialise: `wex master::servers/upgrade` which ssh into each remote (declared in the remotes of known apps), runs `apt update && apt install -y wex`, reports before/after version per host. Bonus: compatibility check (if the CLI moves to 6.X.Y, apps stamped at 6.X-1.Z must remain compatible or be migrated at the same time).

Prerequisite: have a host registry at master level (see friction #8 below).

### 7. App maintenance commands

Set of cross-env operations done manually today that should be scriptable:

- **Sync data prod → dev**: dump prod DB, restore in dev (typical use case: test a migration on real data, refresh a stale staging)
- **Sync data dev → prod**: rarer but useful for initial seed
- **Punctual backup**: trigger a named backup (before a risky migration), not the auto cron
- **Restore from backup**: select a backup, restore it in a given env

Prerequisite: each app/service must know how to describe its "persistent resources" (DB, volumes, secrets) and expose its dump/restore primitives. See task (5) — already touched for service updates.

Target ergonomic spec: `wex app::data/sync --from prod --to dev` (or similar).

### 8. Master "host registry" + ephemeral provisioning

Today the `host:` (IPs) are declared **per app, per env, in `.wex/env/<env>/config.yml`**. No central registry. To add an env or change an IP, N app files must be edited. Friction noted several times during the 2026-05-28 session (TPA dev integration, plausible deployment).

À ajouter dans `master.local.yml` :
```yaml
hosts:
  tpa_prod: 51.210.104.199
  tpa_dev: 152.228.175.159
  wexample_prod: 151.80.23.108
  syrtis_prod: 79.137.89.25
```
And allow apps to reference: `remotes[].host: ${HOST_TPA_PROD}`.

**Prerequisite for the `wex upgrade everywhere` task (#6.5) AND for ephemeral provisioning (#9).**

### 9. Master orchestration & auto-provisioning

Discussion 2026-05-28. The underlying promise: from the master, **provision / deploy / destroy** complete environments in a single command, on ephemeral hosts paid by the hour. Three use cases.

#### Use case A — Client demos / temporary staging

The user schedules their demos. At T-10 min, runs `wex master::stack/deploy --stack tpa --remote demo-laurius`. The master:
1. Provisions a host via cloud API
2. Cloud-init/ansible minimal makes it ready (wex CLI, Docker daemon, network)
3. Ephemeral DNS `demo-laurius.thephotoacademy.com` via Cloudflare API (provider we just implemented)
4. Pulls the TPA stack from git, `wex app::app/start --remote` each app
5. Seeded DB snapshot (see task #7)
6. Returns the demo URL

After the demo, `wex master::stack/destroy --remote demo-laurius` → DNS removed + host destroyed. Total cost: ~€0.05 per 2h demo on Hetzner.

#### Use case B — Ephemeral CI/CD runner

The €80/month runner sits idle 23 hours a day. Alternative: a tiny permanent manager runner (~€3/month) that, on each heavy pipeline, requests an ad-hoc host, runs the job, then destroys it. Standard mechanics on the GitLab side = fleeting plugin (`fleeting-plugin-aws`, `fleeting-plugin-hetzner`) — no need to reinvent, just integrate into the master to manage credentials and scaling from a single place.

Latency trade-off: cold-start ~30s (Hetzner) to 1-2 min (OVH). Possible optimisation via **pre-baked template/snapshot** (Docker + tools already installed) → cold-start reduced to ~30s. Packer + Hetzner snapshots, or OVH Public Cloud custom images.

#### Use case C — Syrtis deployment (multi-service interdependent stack)

The original stretch goal. Now clearer thanks to the two previous use cases: if we can spawn a host + deploy N apps that depend on each other (postgres before api before manager…), we can deploy Syrtis. The "stack" primitive must handle **inter-app dependencies** (see `stacks:` in `project.yml`, which already exists but only groups, not orchestrates).

#### Technical building blocks (to investigate)

| Building block | Default choice | Alternative |
|---|---|---|
| Cloud provider | Hetzner Cloud (best price/perf EU, ~€5/month vs OVH €80/month) | OVH Public Cloud (stay in France), Scaleway, AWS EC2 Spot (worldwide top) |
| Infrastructure provisioning | Terraform (declares what exists) | OpenTofu, Pulumi, or direct Python API client |
| Host provisioning | Cloud-init via user-data | Ansible (more powerful but heavier) |
| Host template | Packer to pre-bake snapshot (Docker + wex CLI already installed) | Cloud-init from scratch each time (1-2 min cold-start) |
| Ephemeral DNS | Cloudflare API (provider already implemented) | Manual via UI (not scalable) |
| CI runner pipeline | GitLab Runner Autoscaler + fleeting-plugin-hetzner | BuildJet/Buildkite (SaaS, but requires leaving GitLab CI) |

#### Breakdown into sub-tasks

1. **Host registry at master level** — prerequisite (task #8 above): declare hosts at master level, apps reference them by name
2. **Abstract `HostProvider`** in wex-addon-master, as done for DNS — Hetzner implementation first
3. **`wex master::host/spawn --provider hetzner --type cpx21`** → returns IP, ssh OK
4. **`wex master::host/destroy <name>`** → symmetric
5. **`wex master::stack/deploy --stack <name> --remote <host>`** → loops over stack apps respecting dependency order
6. **Ephemeral DNS** → Cloudflare provider wrapper for create A record + cleanup
7. **Use case B (CI runner)** — fleeting-plugin-hetzner integration via the manager runner
8. **Templating / Packer image** — accelerates cold-start
9. **Use case A (demo)** — combines spawn + DNS + deploy into a single command
10. **Use case C (Syrtis)** — applies the pattern to the Syrtis stack

This will probably be a multi-week task. Incremental approach: start with 1+2+3 (provision an empty host from the master), then add layers.

### 9.5. Webhook listener: boot persistence

The `wex core::webhook/listen --port 7654` daemon (CI → `app::release/deploy` deploy trigger) is started **manually** on TPA prod (51.210.104.199) and Syrtis prod (79.137.89.25, added 2026-06-12 for bdo-letters). No systemd unit, no `@reboot` cron, nothing in wex-core nor in the debian package → **a server reboot silently breaks all automatic deployments**.

Already addressed several times in the past without reaching a conclusion (worth investigating why before reimplementing). Target fix: the wex debian package installs a `wex-webhook.service` unit (enabled by default or via a command like `core::webhook/install`).

### 10. New services to install

- ✅ **Plausible TPA** (`plausible.thephotoacademy.com`) — deployed to prod 2026-05-28
- ⏳ **Plausible Wex** — web analytics for the Wexample unit
- ⏳ **PostHog** on Syrtis (product analytics)
- ⏳ **OpenClaw #2** on Syrtis for Gabriel
- ⏳ **OpenClaw #3** on Syrtis for Simon

Each install = new wex 6 app, to be set up following the standard template.

## Architectural overhaul in progress

A cross-cutting **master overhaul** task is being designed — it covers several structural frictions (host registry #8 included, but also: apps self-described by name and tags, stacks by name or tag rather than by path, app registry, auto-enrollment, etc.). Dedicated document: [master-architecture-refactor.md](master-architecture-refactor.md).

To be addressed before or in parallel with (4), (5), (6), (6.5), (8), (9) — all tasks that benefit from or depend on the overhaul.

## Notes

- Non-exhaustive list — to be fleshed out as things progress
- Default priority: (2) TPA CI/CD first (blocking for daily TPA prod, dedicated agent already briefed via [ci-cd-agent-brief.md](/home/weeger/Desktop/WIP/WEB/TPA/local/tpa/.wex/knowledge/ci-cd-agent-brief.md)), then master overhaul ([master-architecture-refactor.md](master-architecture-refactor.md)) which unblocks the rest, then (1) runner remote, then (4)/(5)/(7) tooling, then (3) updates and (10) new services in parallel.
