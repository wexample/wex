# Checklist post-migration TPA prod + dev

## Contexte

Migration TPA terminée en wex 6 (prod fin mai, dev 2026-05-28). Cette todo recense les pendings techniques qu'on a contournés ou pas finalisés pendant le rush, à reprendre proprement.

## Bugs / fixes pas encore publiés dans le package apt

### 1. Hot-patch `app_readme_config_value.py`

- **Symptôme** : `TypeError: '...app_readme_config_value' is not a package` au `wex app::app/start` quand le walker README essaie de lire son template depuis un module non-package.
- **Fix** : try/except TypeError dans `_append_template_path_from_module` ([app_readme_config_value.py:32-44](/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/config_value/app_readme_config_value.py)).
- **État** : commit local, **hot-patché à la main sur dev** (`/usr/lib/wex/.venv/lib/python3.11/site-packages/...`), idem sur prod en cours de session précédente.
- **Action** : intégrer dans le prochain build apt wex (6.0.103+) pour que la prochaine install propre porte le fix.

### 2. Migrations 6.0.103 + 6.0.104 absentes du package

- `migration_6_0_103__1.py` (dedup server.ip ↔ remotes[].host) et `migration_6_0_104__1.py` (drop des skeletons `host: ''`) ont été créées dans le source local mais pas encore dans le package wex apt.
- **Action** : prochain release wex bump version + publish.
- **Conséquence actuelle** : sur dev TPA, seule la migration 6.0.90 a tourné. Les configs ont encore `server.ip` + `remotes[].host: ''` orphelins (parasites mais non-bloquants).

### 3. `python3.11-venv` pas en dépendance déclarée du paquet wex

- L'install `apt install wex` sur dev a échoué initialement parce que `python3.11-venv` n'était pas installé. Le post-install (venv creation) a foiré, package en état "iF" (installed, half-configured).
- **Action** : ajouter `python3.11-venv` comme dépendance stricte dans `debian/control` du package wex.

## Certs dev TPA — provisioning incomplet

Sur dev (152.228.175.159), 5 des 7 dev domains ont leur cert valide (dev.en, dev.de, dev.fr, dev.it, dev.nl via SAN cert restoré). Restent :

- **dev.es** : 500 (symlink supprimé pendant le cleanup, acme-companion retry en cours)
- **dev.pma** : SSL non-provisionné, Let's Encrypt fail avec 404 sur `/.well-known/acme-challenge/`

Cause probable du 404 : la location `/.well-known/acme-challenge/` dans nginx route vers `/usr/share/nginx/html` mais le fichier n'y arrive pas. Soit acme-companion ne le pose pas au bon endroit, soit nginx-proxy a une mauvaise variable de root, soit l'upstream apache attrape la requête avant nginx.

**Action** : à diagnostiquer si dev.es ou dev.pma sont vraiment nécessaires. Sinon laisser couler — le SAN cert dev.de couvre les langues principales.

## TPA prod — propagations encore à faire

### Migrations wex sur prod

- Les 6 apps TPA prod sont stampées à `6.0.101` (avant la création des migrations 103/104).
- Au prochain release apt wex, faire `git pull` + `wex app::migration/run` sur chaque app prod pour dedup `server:` et drop les skeletons restants.
- Côté serveur ssh : `ssh weeger@51.210.104.199` + boucle sur `/var/www/prod/{listmonk,baserow,matomo,gitlab,n8n,tpa}` (oscar a été viré).

### Backups prod nettoyés ✅ 2026-05-28

`/var/www/prod/_tpa_migration_backup_2026_05_27/`, `wex-proxy-legacy-2026-05-27/`, `wex-proxy-bkp-2026-05-27/` supprimés.

### Disk space prod

Le disque prod a tapé 100% pendant la session du 2026-05-28 (gitlab logs explose à 28G + journalctl 4.1G + 4 backups gitlab). On a libéré 38G en truncate logs + vacuum journal + rm vieux backups. Maintenant à **88% (273G/310G)**.

**Action** : poser une rotation propre :
- `logrotate` pour `/var/www/prod/gitlab/gitlab/logs/*.log` (max-size + 7 days)
- `journalctl` vacuum auto via systemd `SystemMaxUse=2G` dans `/etc/systemd/journald.conf`
- Politique de rétention gitlab backups : keep 7 derniers

C'est un chantier mini qui mériterait son propre todo si on veut le faire bien.

## Branche develop = master (cas particulier)

Sur le repo tpa/tpa.git, on a ff-mergé `develop` à `master` (pour propager les 3 commits wex 6). Du coup `develop == master` tip pour l'instant. Pas un bug, mais inhabituel — au prochain feature branch, develop redivergera normalement.

## Runner GitLab dev — à transformer en service wex

`/var/www/dev/runner/` est un GitLab runner CI/CD très customisé (token TPA, mount `/var/www:/var/www`, mount docker.sock). Pas migré en wex 6.

- Tree rsync vers `/home/weeger/Desktop/WIP/WEB/TPA/local/runner/` pour inspection
- À transformer en wex 6 service (chantier #2 de [master.md](master.md) — "Runner wex en remote master")
- Critique pour le chantier suivant : la pipeline CI/CD TPA passe par ce runner

## wex-proxy-legacy sur dev

`/var/www/dev/wex-proxy-legacy-2026-05-28/` a été supprimé après validation que le nouveau wex-proxy fonctionne. ✅
