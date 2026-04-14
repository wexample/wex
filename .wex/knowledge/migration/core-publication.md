# Roadmap de publication — wex 6

Objectif : publier wex-6 via un paquet `.deb` distribué sur un dépôt APT custom,
installable sur serveurs Ubuntu/Debian. En local, on travaille depuis les sources directement.

---

## Référence : pipeline v5 (ce qui existait)

La v5 reposait sur **3 repos GitLab distincts** qui s'enchaînaient :

```
[wex repo]  →  merge request vers master
                  ↓ CI (4 stages)
               setup : installe wex depuis les sources sur le runner
               test  : lance wex test
               merge_addons : wex addons/deploy
               deploy : curl → n8n webhook ?v=<version>
                  ↓
[n8n]  reçoit le webhook, déclenche wex-api
                  ↓
[wex-build repo]  build branch
               build.py -v <version> -n wex
               → git clone source/, debuild, .deb produit
               → upload .deb sur GitLab Package Registry
                  ↓
[wex-apt-repo]  publish.sh -p <project_id> -v <version>
               → télécharge .deb depuis GitLab Registry
               → aptly repo add, snapshot, publish
               → dépôt APT exposé via nginx
                  ↓
[n8n + Ansible]  déploiement automatique sur serveurs — LEGACY DEAD
```

**Détails clés v5 :**
- Le CI tourne sur un **runner GitLab** qui a wex installé en local
- `wex-build` utilise une image Docker custom (`wex-build:build`) avec debhelper/devscripts
- La distribution aptly est dérivée du numéro de version (ex: `6-0.stable` → `stable`)
- Le `.deb` est uploadé sur le GitLab Package Registry avant d'être récupéré par wex-apt-repo

---

## Cible v6 : ce qu'on veut

Même schéma, adapté à v6 :

```
[wex repo]  →  git push sur master (ou tag)
                  ↓ CI .gitlab-ci.yml (à créer)
               stage build : déclenche wex-build via API GitLab / curl n8n
                  ↓
[wex-build repo]  build branch (existante)
               build.py -v <version> -n wex  (simplifié, sans -s/-t)
               image Docker wex-build:build (existante, à vérifier pour v6)
               → git clone source/ (symlink → ../wex), debuild, .deb
               → upload .deb sur GitLab Package Registry
                  ↓
[wex-apt-repo]  publish.sh -p <project_id> -v <version>
               → même script qu'en v5, réutilisable tel quel
                  ↓
[déploiement serveurs]  manuel pour l'instant (voir étape E)
```

**Différences v6 vs v5 :**
- Plus de `setup.py` → image Docker wex-build:build à mettre à jour (retirer dh-python, python3-setuptools, python3-all)
- `bin/install` remplace `core::core/install` (déjà fait)
- `requirements.txt` doit pointer sur les versions PyPI publiées (pas encore fait)
- Pas de tests wex en CI pour l'instant (backlog)

---

## État actuel

### Fait
- [x] Renommage `wex-6` → `wex`, `wex` → `wex-5-legacy`
- [x] `bin/wex` fonctionnel depuis les sources
- [x] `bin/install` adapté : venv, symlink, autocomplete, build registry, mode local (install-dev), compatible dpkg (WEX_SKIP_APT, DEBIAN_FRONTEND, root-aware)
- [x] `bin/uninstall` créé (prerm/postrm)
- [x] `bin/install-dev` : utilise `.venv/bin/pip` explicitement
- [x] `default::autocomplete/suggest` stub en place
- [x] `debian/control` sans dh-python/python3-setuptools/python3-all
- [x] `debian/install`, `debian/rules`, `debian/postinst`, `debian/prerm`, `debian/postrm` adaptés v6
- [x] `build.py` : cleanup artefacts dev, détection bin/ auto, fix tarball, retrait -s/-t
- [x] `wex-build/source/` → symlink `../wex`, `templates-v6/` → `templates/`, `source-v6` supprimé
- [x] `/etc/wex.conf` mis à jour (`wex-6` → `wex`)

### En cours
- [ ] Publication des packages Python sur PyPI (`app::suite/publish`)

### À faire

**Étape A — Prérequis PyPI**
- [ ] Vérifier que tous les packages sont bien publiés sur PyPI
- [ ] Mettre à jour `requirements.txt` dans `local/wex/` avec les nouvelles versions publiées (`pip-compile requirements.in`)

**Étape B — Image Docker wex-build**
- [ ] Mettre à jour `Dockerfile.build` : retirer `dh-python`, `python3-setuptools`, `python3-all` (inutiles sans setup.py)
- [ ] Builder et pousser la nouvelle image `wex-build:build` sur le registry GitLab

**Étape C — CI wex (`.gitlab-ci.yml`)**
- [ ] Créer `.gitlab-ci.yml` dans le repo `wex`
- [ ] Stage `build` : trigger wex-build via API GitLab (pipeline trigger) ou curl webhook n8n
- [ ] Passer la version (`version.txt`) en paramètre

**Étape D — Test end-to-end**
- [ ] Push sur master wex → CI déclenché → wex-build produit le `.deb`
- [ ] `publish.sh` dans wex-apt-repo avec le `.deb` produit
- [ ] `apt-get install wex` depuis le dépôt APT
- [ ] Vérifier que `bin/install` (postinst) se déroule correctement avec les packages PyPI

**Étape E — VM (validation finale)**
- [ ] VM Ubuntu propre, pointer sur le dépôt APT
- [ ] `apt-get install wex`, tester les commandes de base
- [ ] `apt-get upgrade` après publication d'une version corrective
- [ ] `apt-get remove wex` (prerm/postrm)
- [ ] Déploiement manuel sur les serveurs cibles

**Étape F — Déploiement automatique (TODO, bloqué)**
- [ ] Implémenter la réception de webhooks dans wex-6
- [ ] Brancher le CI (étape D) pour déclencher un webhook post-publication
- [ ] Valider le déploiement automatique end-to-end

> Note : n8n et Ansible sont legacy dead. Le système cible est wex lui-même comme récepteur de webhook.
> Bloqué tant que wex-6 ne supporte pas les webhooks.

---

## Notes

- Le dépôt aptly dérive la distribution du numéro de version : `6.0.0` → `stable`, `6.0.0-beta.1` → `beta`
- Upload GitLab Registry : `PUT https://gitlab.wexample.com/api/v4/projects/{id}/packages/generic/wex/{version}/{package}`
- `wex-apt-repo/script/publish.sh` est réutilisable tel quel, pas de modification nécessaire
- L'image Docker `wex-build:build` est définie dans `wex-build/.wex/docker/Dockerfile.build`
- Le runner GitLab v5 avait wex installé localement — à vérifier pour v6 (le CI v6 n'en a pas besoin si on trigger via API)
