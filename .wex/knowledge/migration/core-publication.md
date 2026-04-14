# Roadmap de publication — wex 6

Objectif : publier wex-6 via un paquet `.deb` distribué sur un dépôt APT custom,
installable sur serveurs Ubuntu/Debian. En local, on travaille depuis les sources directement.

---

## Référence : pipeline v5 (architecture réelle)

Le repo wex sur GitLab a **deux branches clés** :
- `master` : le code source de wex
- `build` : le tooling de build (`script/build.py`, templates debian)

Localement : `local/wex-5/` = master, `local/wex-build/` = branche build du même repo.

```
[wex repo — merge request → master]
  stage checkup_pipeline :
    - checkup_docker   : purge images Docker du runner
    - checkup_remote   : vérifie que le serveur cible est prêt (via wex app::remote/available)

  stage build_pipeline_images :
    - build rc image   : image Docker wex/rc (wex installé dedans)
    - build test-remote image

  stage checkup_builds :
    - vérifie les images, code quality, format

  stage test :
    - wex test -vvv dans l'image rc

  stage build_apt  [on master only] :
    - image : wexample-public/docker/wex:build  (debhelper/devscripts)
    - lit version.txt → BUILD_VERSION
    - cp -r .git /var/tmp/build && git checkout build  (branche build du même repo)
    - ln -s ${CI_PROJECT_DIR} source
    - python3 script/build.py -n wex -gid ${CI_PROJECT_ID} -gtk ${WEX_BUILD_TOKEN} -v ${BUILD_VERSION}
    → produit le .deb et l'uploade sur GitLab Package Registry

  stage deploy  [on master only, after build_apt] :
    - curl "http://wexample.com:4242/webhook/app/prod/wex-apt-repo/apt/publish?p=...&v=..."
    → wex (serveur sur :4242) reçoit le webhook et forward vers wex-apt-repo
    → wex-apt-repo/script/publish.sh télécharge le .deb et publie via aptly

  stage checkup_install  [on master only, after deploy] :
    - installe wex depuis apt.wexample.com dans une image Debian et Ubuntu vierge
    - vérifie que wex hi et wex version = version attendue

  stage build_docker  [on master only, after checkup_install] :
    - trigger projet wexample-public/docker pour rebuilder l'image publique wex
```

**Points clés :**
- `build_apt` fonctionne entièrement dans le CI de wex (pas de repo séparé déclenché)
- Le webhook `:4242` = wex lui-même en mode serveur → **DEAD en v6** (wex-6 pas de serveur webhook)
- n8n n'était impliqué que pour les notifications, pas dans le pipeline principal

---

## Cible v6 : ce qu'on veut

Même repo wex, même branche `build`, pipeline simplifié :

```
[wex repo — push/merge → master]

  stage build_apt  [on master only] :
    - même logique que v5 : image wex:build, checkout branche build, build.py
    - WEX_BUILD_TOKEN à créer dans les variables CI du projet

  stage deploy  [on master only, after build_apt] :
    - curl vers wex-apt-repo  →  MANUEL pour l'instant (wex-6 pas de webhook server)

  stage checkup_install  [on master only, after deploy] :
    - même que v5 : apt install wex dans image Debian/Ubuntu vierge, vérifie version

  [déploiement serveurs]  →  MANUEL pour l'instant

  [stage build_docker]  →  TODO (image publique wex, quand pertinent)
```

**Ce qu'on ne fait PAS pour l'instant en v6 :**
- Images rc/test-remote (pas de Docker dans wex-6)
- Checkup remote (pas de wex server)
- Webhook auto vers apt-repo (pas de webhook server dans wex-6)
- Déploiement automatique serveurs (Ansible/n8n DEAD)

**Étape F (TODO, bloquée) :** quand wex-6 aura un mode serveur webhook, brancher le deploy auto.

---

## État actuel

### Fait
- [x] Renommage `wex-6` → `wex`, `wex` → `wex-5-legacy`
- [x] `bin/wex` fonctionnel depuis les sources
- [x] `bin/install` adapté : venv, symlink, autocomplete, build registry, mode local, compatible dpkg
- [x] `bin/uninstall` créé
- [x] `bin/publish` créé : bump version, pip-compile, git commit + push
- [x] `default::autocomplete/suggest` stub en place
- [x] Templates debian adaptés v6 (`control`, `install`, `rules`, `postinst`, `prerm`, `postrm`)
- [x] `build.py` : cleanup artefacts dev, détection bin/ auto, fix tarball, retrait -s/-t
- [x] Branche `build` : `source/` → symlink `../wex`, `templates-v6/` → `templates/`, `source-v6` supprimé
- [x] `/etc/wex.conf` mis à jour (`wex-6` → `wex`)
- [x] Packages Python publiés sur PyPI
- [x] `requirements.txt` mis à jour avec les versions PyPI publiées
- [x] Image Docker `wex-build:build` mise à jour (retrait dh-python/python3-setuptools/python3-all)
- [x] `.gitlab-ci.yml` créé dans wex : stages `build_apt`, `deploy` (manuel), `checkup_install`
- [x] `version-6.0.0-alpha` mergé dans `master`
- [x] Doc déploiement rédigée (`wex-build/.wex/knowledge/deployment.md`)

### À faire

**Étape A — Test end-to-end du pipeline**
- [ ] Vérifier que `build_apt` passe (pipeline en cours)
- [ ] Déclencher `deploy` manuellement → `publish.sh` sur wex-apt-repo
- [ ] Vérifier que `checkup_install` passe (apt install wex sur Debian + Ubuntu)

**Étape B — Test end-to-end**
- [ ] Push sur master wex → CI déclenché → `.deb` produit et uploadé sur Registry
- [ ] Lancer `publish.sh` manuellement sur le serveur wex-apt-repo
- [ ] `apt-get install wex` depuis apt.wexample.com
- [ ] Vérifier que `bin/install` (postinst) se déroule correctement

**Étape C — VM (validation finale)**
- [ ] VM Ubuntu propre, pointer sur apt.wexample.com
- [ ] `apt-get install wex`, tester les commandes de base
- [ ] `apt-get upgrade` après publication d'une version corrective
- [ ] `apt-get remove wex`

**Étape F — Déploiement automatique (TODO, bloqué)**
- [ ] Implémenter mode serveur webhook dans wex-6
- [ ] Brancher le stage `deploy` du CI vers ce webhook
- [ ] Déploiement automatique sur serveurs cibles

---

## Notes

- `WEX_BUILD_TOKEN` : Personal Access Token GitLab avec scope `api`, à créer et stocker dans CI/CD variables du projet wex (Settings → CI/CD → Variables)
- Le dépôt aptly dérive la distribution du numéro de version : `6.0.0` → `stable`, `6.0.0-beta.1` → `beta`
- Upload GitLab Registry : `PUT https://gitlab.wexample.com/api/v4/projects/{id}/packages/generic/wex/{version}/{package}`
- `wex-apt-repo/script/publish.sh` est réutilisable tel quel
- L'image `wexample-public/docker/wex:build` est dans le repo `wexample-public/docker` sur GitLab (pas dans wex-build local)
