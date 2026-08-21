# Checklist post-migration TPA prod + dev

## Context

TPA migration completed in wex 6 (prod end of May, dev 2026-05-28). This todo lists the technical pending items that were worked around or left unfinished during the rush, to be revisited properly.

## Bugs / fixes ✅ published in wex 6.0.104

### 1. Hot-patch `app_readme_config_value.py` ✅
The try/except TypeError on `_append_template_path_from_module` is in 6.0.104.

### 2. Migrations 6.0.103 + 6.0.104 ✅
Published in the package. To be triggered on the TPA prod apps to dedup the orphan `server.ip` entries (see below).

### 3. `python3.11-venv` as dependency ⏳
Still not explicitly declared as a strict dependency in `debian/control`. Discovered during the TPA dev install. To be fixed.

### 4. nginx-proxy:1.3 → 1.11 ✅
The proxy service sample compose was updated to `:1.11` in 6.0.104. Avoids the cert bootstrap bug on new vhosts (well-known intercept conditional on cert_ok in 1.3).

## Certs dev TPA — incomplete provisioning

On dev (152.228.175.159), 5 of the 7 dev domains have a valid cert (dev.en, dev.de, dev.fr, dev.it, dev.nl via restored SAN cert). Remaining:

- **dev.es** : 500 (symlink removed during cleanup, acme-companion retry in progress)
- **dev.pma** : SSL not provisioned, Let's Encrypt failing with 404 on `/.well-known/acme-challenge/`

Probable cause of the 404: the `/.well-known/acme-challenge/` location in nginx routes to `/usr/share/nginx/html` but the file doesn't land there. Either acme-companion doesn't place it in the right spot, nginx-proxy has a wrong root variable, or the upstream apache catches the request before nginx.

**Action**: to be diagnosed if dev.es or dev.pma are actually needed. Otherwise leave it — the dev.de SAN cert covers the main languages.

## TPA prod — propagations still pending

### wex migrations on prod ⏳

- wex CLI on the 4 servers is at **6.0.104** ✅
- But the TPA prod **apps** (6 on 51.210.104.199) are stamped at `6.0.101` (pre-migrations 103/104).
- Action: `wex app::migration/run` on each prod app to apply migrations 6.0.103 + 6.0.104 (dedup `server:` + drop orphan skeletons).
- Server-side: `ssh weeger@51.210.104.199` + loop over `/var/www/prod/{listmonk,baserow,matomo,gitlab,n8n,tpa}` (oscar was removed).
- Same on Wexample (151.80.23.108) and Syrtis (79.137.89.25), which also have apps at 6.0.101.

### Missing acme symlinks — pattern to watch ⚠️

Manager.thephotoacademy.com was serving the `de.thephotoacademy.com` SAN cert instead of its own cert for one reason: **the top-level symlinks (`<domain>.{crt,key,chain.pem,dhparam.pem}`) had never been created** even though the acme dir with the certs existed. Recreated by hand 2026-05-28. Original cause unknown (wex 6 migration inheritance?).

To audit: do the other TPA prod apps (listmonk, matomo, n8n, gitlab) all have their symlinks? If not, they are silently serving the default cert. Quick test: `ssh weeger@<serveur> "sudo ls /var/www/prod/wex-proxy/proxy/certs/*.crt"`. If an app has its acme dir but no top-level symlink, it's the same case.

Also: Baserow was `exited+unhealthy` on prod without alerting anyone. Silent crash. If it happens again, investigate memory / DB / etc.

### Prod backups cleaned ✅ 2026-05-28

`/var/www/prod/_tpa_migration_backup_2026_05_27/`, `wex-proxy-legacy-2026-05-27/`, `wex-proxy-bkp-2026-05-27/` removed.

### Disk space prod

The prod disk hit 100% during the 2026-05-28 session (gitlab logs ballooning to 28G + journalctl 4.1G + 4 gitlab backups). 38G was freed by truncating logs + vacuuming the journal + removing old backups. Now at **88% (273G/310G)**.

**Action**: set up a proper rotation:
- `logrotate` for `/var/www/prod/gitlab/gitlab/logs/*.log` (max-size + 7 days)
- `journalctl` vacuum auto via systemd `SystemMaxUse=2G` in `/etc/systemd/journald.conf`
- Gitlab backup retention policy: keep the last 7

This is a minor task that would deserve its own todo if done properly.

## develop branch = master (special case)

On the tpa/tpa.git repo, `develop` was ff-merged into `master` (to propagate the 3 wex 6 commits). So `develop == master` tip for now. Not a bug, but unusual — at the next feature branch, develop will diverge again normally.

## GitLab dev runner — to be turned into a wex service

`/var/www/dev/runner/` is a heavily customised GitLab CI/CD runner (TPA token, mount `/var/www:/var/www`, mount docker.sock). Not migrated to wex 6.

- Tree rsync to `/home/weeger/Desktop/WIP/WEB/TPA/local/runner/` for inspection
- To be turned into a wex 6 service (task #2 in [master.md](master.md) — "Runner wex en remote master")
- Critical for the next task: the TPA CI/CD pipeline goes through this runner

## wex-proxy-legacy on dev

`/var/www/dev/wex-proxy-legacy-2026-05-28/` was removed after validating that the new wex-proxy works. ✅
