# Checklist post-migration TPA prod + dev

## Contexte

Migration TPA terminée en wex 6 (prod fin mai, dev 2026-05-28). Cette todo recense les pendings techniques qu'on a contournés ou pas finalisés pendant le rush, à reprendre proprement.

## Bugs / fixes ✅ publiés dans wex 6.0.104

### 1. Hot-patch `app_readme_config_value.py` ✅
Le try/except TypeError sur `_append_template_path_from_module` est dans 6.0.104.

### 2. Migrations 6.0.103 + 6.0.104 ✅
Publiées dans le package. À déclencher sur les apps prod TPA pour dedup les `server.ip` orphelins (cf. plus bas).

### 3. `python3.11-venv` en dépendance ⏳
Toujours pas déclaré explicitement comme dépendance stricte de `debian/control`. Découvert pendant l'install dev TPA. À fixer.

### 4. nginx-proxy:1.3 → 1.11 ✅
Le sample compose du service proxy est passé à `:1.11` dans 6.0.104. Évite le bug de bootstrap des certs sur les nouveaux vhosts (well-known intercept conditionnel sur cert_ok dans 1.3).

## Certs dev TPA — provisioning incomplet

Sur dev (152.228.175.159), 5 des 7 dev domains ont leur cert valide (dev.en, dev.de, dev.fr, dev.it, dev.nl via SAN cert restoré). Restent :

- **dev.es** : 500 (symlink supprimé pendant le cleanup, acme-companion retry en cours)
- **dev.pma** : SSL non-provisionné, Let's Encrypt fail avec 404 sur `/.well-known/acme-challenge/`

Cause probable du 404 : la location `/.well-known/acme-challenge/` dans nginx route vers `/usr/share/nginx/html` mais le fichier n'y arrive pas. Soit acme-companion ne le pose pas au bon endroit, soit nginx-proxy a une mauvaise variable de root, soit l'upstream apache attrape la requête avant nginx.

**Action** : à diagnostiquer si dev.es ou dev.pma sont vraiment nécessaires. Sinon laisser couler — le SAN cert dev.de couvre les langues principales.

## TPA prod — propagations encore à faire

### Migrations wex sur prod ⏳

- wex CLI sur les 4 serveurs est à **6.0.104** ✅
- Mais les **apps** prod TPA (6 sur 51.210.104.199) sont stampées à `6.0.101` (pré-migrations 103/104).
- Action : `wex app::migration/run` sur chaque app prod pour appliquer les migrations 6.0.103 + 6.0.104 (dedup `server:` + drop skeletons orphelins).
- Côté serveur : `ssh weeger@51.210.104.199` + boucle sur `/var/www/prod/{listmonk,baserow,matomo,gitlab,n8n,tpa}` (oscar a été viré).
- Idem sur Wexample (151.80.23.108) et Syrtis (79.137.89.25) qui ont aussi des apps à 6.0.101.

### Symlinks acme manquants — pattern à surveiller ⚠️

Manager.thephotoacademy.com servait le SAN cert de `de.thephotoacademy.com` au lieu de son propre cert pour une seule raison : **les symlinks top-level (`<domain>.{crt,key,chain.pem,dhparam.pem}`) n'avaient jamais été créés** alors que l'acme dir avec les certs existait. Recréés à la main 2026-05-28. Cause originelle inconnue (héritage migration wex 6 ?).

À auditer : les autres apps prod TPA (listmonk, matomo, n8n, gitlab) ont-elles toutes leurs symlinks ? Si non, elles servent silencieusement le default cert. Test rapide : `ssh weeger@<serveur> "sudo ls /var/www/prod/wex-proxy/proxy/certs/*.crt"`. Si une app a sa dir acme mais pas son symlink top-level, c'est le même cas.

Aussi : Baserow était `exited+unhealthy` sur prod sans avoir alerté qui que ce soit. Crash silencieux. Si ça récidive, investiguer mémoire / DB / etc.

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
