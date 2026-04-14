# Déploiement wex

## Architecture

3 repos impliqués :
- **wex** — le code source (branches `master` et `version-6.x.x-alpha`)
- **wex** branche `build` — le tooling de build (= `local/wex-build/`)
- **wex-apt-repo** — le dépôt APT (aptly + nginx)

## Pipeline CI (déclenché sur master)

```
push master
  └─ build_apt       : produit le .deb et l'uploade sur GitLab Package Registry
  └─ deploy          : MANUEL — déclenche publish.sh sur wex-apt-repo
  └─ checkup_install : vérifie apt install wex sur Debian + Ubuntu
```

## Publier une nouvelle version

**1. Depuis la branche de dev :**
```bash
bin/publish   # bumpe version.txt, pip-compile, commit, push
```

**2. Merger dans master via MR GitLab**

Le CI se déclenche automatiquement.

**3. Une fois build_apt terminé, déclencher deploy manuellement dans GitLab**

Le bouton "play" sur le stage `deploy` dans le pipeline.

Cela appelle `wex-apt-repo/script/publish.sh` qui :
- télécharge le `.deb` depuis le GitLab Package Registry
- l'ajoute au repo aptly
- publie le snapshot sur le dépôt APT

**4. Le stage `checkup_install` se déclenche automatiquement**

Installe wex depuis `apt.wexample.com` dans une image Debian et Ubuntu vierge et vérifie que la version correspond.

---

## Image Docker de build

`gitlab-docker.wexample.com/wexample/wex/wex-build:build`

Définie dans `wex-build/.wex/docker/Dockerfile.build`. Contient debhelper/devscripts pour faire tourner `debuild`.

Se rebuild automatiquement à chaque push sur la branche `build` de wex.

---

## Distribution aptly

Dérivée du numéro de version :
- `6.0.0` → `stable`
- `6.0.0-beta.1` → `beta`

---

## Cibles d'installation

| Plateforme | Méthode |
|---|---|
| Serveur Linux / Ubuntu dev | `apt install wex` depuis apt.wexample.com |
| macOS | Homebrew tap (à venir) |

---

## TODO

- `bin/publish` déclenche la MR automatiquement (pas encore fait)
- Stage `deploy` automatique quand wex-6 aura un serveur webhook
- Homebrew tap pour macOS
