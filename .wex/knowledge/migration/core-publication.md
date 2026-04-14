# Roadmap de publication — wex 6

Objectif : packager wex-6 sous forme de paquet `.deb` distribué via un dépôt APT custom,
installable sur serveurs Ubuntu/Debian et en local (mode dev, sources directes).

---

## 0. Renommage des répertoires (prérequis oublié)

wex-6 a vocation à remplacer wex. Ce renommage aurait dû être fait en premier.
Tout le travail des étapes suivantes référence encore `wex-6` — à corriger une fois cette étape faite.

- [ ] Désinstaller wex-5 en local (supprimer symlink `/usr/local/bin/wex`, `/etc/bash_completion.d/wex`, venv)
- [ ] Renommer `local/wex` → `local/wex-5-legacy`
- [ ] Renommer `local/wex-6` → `local/wex`
- [ ] Vérifier que `wex` en ligne de commande appelle bien le nouveau binaire (wex-6)

---

## 1. Prérequis fonctionnels

Avant de builder le paquet, s'assurer que wex tourne correctement en local.

- [x] `bin/wex` est fonctionnel (exécution depuis les sources via venv)
- [x] `bin/install` installe correctement le venv et les dépendances (`requirements.txt`)
- [x] Post-install : symlink `/usr/local/bin/wex`, handler autocomplete, build registry (intégré dans `bin/install`, remplace le défunt `core::core/install` de v5)
- [x] `default::autocomplete/suggest` existe (stub vide — suggestions à implémenter, voir TODO dans le fichier)
- [x] L'autocomplétion bash est branchée (`/etc/bash_completion.d/wex` → `bin/autocomplete-handler`)
- [x] `version.txt` est à jour (actuellement `6.0.0`)

---

## 2. Adaptations du script d'install pour le mode paquet

Le `bin/install` actuel est conçu pour une install depuis les sources.
Il faut le rendre compatible avec une install depuis `/usr/lib/wex/` (mode paquet apt).

- [x] `bin/install` fonctionne depuis `/usr/lib/wex/bin/` (chemins résolus via `BASH_SOURCE[0]`)
- [x] `WEX_SKIP_APT=1` : skip `apt-get update` si déjà géré par dpkg
- [x] Root-aware : `INSTALL_USER="${SUDO_USER:-${USER:-root}}"` — fonctionne en postinst sans `$USER`
- [x] `sudo` supprimé des appels internes (script déjà garanti root par `_init_sudo.sh`)
- [x] `DEBIAN_FRONTEND` : skip du sourcing `~/.bashrc` en mode non-interactif
- [x] `pip install -q` : output propre en postinst
- [x] `bin/uninstall` créé — supprime symlink + handler ; purge le venv si appelé avec `purge`

---

## 3. Infrastructure de build Debian (wex-build)

À simplifier suite à la décision de casser la compatibilité wex-5 :
- `source/` et `templates/` remplacés directement pour v6 (plus de `-v6` suffixe)
- Le symlink `source/` local sert uniquement aux tests de build manuels ; en CI/CD, c'est un `git clone` du repo wex depuis GitLab
- Les params `-s` / `-t` ajoutés à `build.py` sont à retirer (surcharge inutile)

**À défaire / simplifier :**
- [ ] Retirer les args `-s` et `-t` de `build.py` — revenir à `source/` et `templates/` fixes
- [ ] Supprimer `wex-build/source-v6` (symlink local inutile en CI/CD)
- [ ] Supprimer `wex-build/templates-v6/` et déplacer son contenu dans `wex-build/templates/` (remplacement direct)
- [ ] Mettre à jour `wex-build/source/` pour pointer vers le nouveau `../wex` (après renommage étape 0)

**Déjà fait (contenu correct, à déplacer) :**
- [x] `debian/control` — suppression `dh-python`/`python3-setuptools`/`python3-all` (plus de setup.py en v6)
- [x] `debian/install` — `wex/* usr/lib/wex/` + `.wex/*`, sans le `wexd.service` supprimé en v6
- [x] `debian/rules` — `dh $@` sans `--with python3`, symlink `bin/wex` → `usr/bin/wex`, chmod sur tous les scripts `bin/`
- [x] `debian/postinst` — appelle `bin/install` avec `WEX_SKIP_APT=1` et `DEBIAN_FRONTEND=noninteractive`
- [x] `debian/prerm` — appelle `bin/uninstall` avant la suppression des fichiers
- [x] `debian/postrm` — purge les fichiers hors dpkg (symlink, completion, venv) sur `purge`
- [x] `build.py` — cleanup des artefacts dev (`.venv`, `tests/`, etc.) ; `step_set_permissions` détecte `bin/` automatiquement ; fix du tarball hardcodé `/wex` → `self.name`
- [ ] Tester le build en local : `python3 script/build.py -v 6.0.0 -n wex` (une fois simplifié)

---

## 4. Dépôt APT (wex-apt-repo)

Le dépôt aptly existant est réutilisable tel quel pour wex-6.

- [ ] Vérifier que le serveur `wex-apt-repo` est opérationnel
- [ ] Vérifier que la clé GPG est toujours valide
- [ ] Tester `publish.sh` avec un `.deb` wex en local
- [ ] Valider que `apt-get install wex` depuis le dépôt installe bien la version 6

---

## 5. Install locale en mode développement

Sur cette machine, on travaille depuis les sources (pas depuis le paquet apt).
Le symlink `/usr/local/bin/wex` → `local/wex/bin/wex` suffit — c'est ce que fait `bin/install`.

- [ ] Lancer `bin/install` depuis le nouveau `local/wex` (après renommage étape 0)
- [ ] Vérifier que les modifications de sources sont prises en compte immédiatement (sans rebuild)
- [ ] Documenter la procédure d'install dev dans `.wex/knowledge/readme/`

---

## 6. Tests sur VM

- [ ] Monter une VM Ubuntu (VirtualBox) propre
- [ ] Configurer la VM pour pointer sur le dépôt APT wex
- [ ] Tester `apt-get install wex` sur la VM
- [ ] Valider que `wex` fonctionne post-install (commandes de base)
- [ ] Tester la mise à jour : publier une version `6.0.1`, faire `apt-get upgrade`
- [ ] Tester `apt-get remove wex` (prerm/postrm)

---

## 7. Compatibilité macOS (à planifier, non bloquant)

- [ ] Identifier les dépendances Linux-only dans `bin/install` (apt, dpkg, etc.)
- [ ] Créer un script d'install alternatif pour macOS (Homebrew ?)
- [ ] Tester sur une VM macOS (image VirtualBox existante)
- [ ] Décider si on cible Homebrew Formula ou install script uniquement

---

## 8. Tests unitaires (backlog, non bloquant)

Les tests unitaires de wex-6 ne sont pas une priorité pour la première publication.

- [ ] (Todo) Porter les tests unitaires de wex-5 vers wex-6
- [ ] (Todo) Intégrer les tests dans le pipeline CI/CD

---

## 9. Pipeline CI/CD

- [ ] Créer ou adapter `.gitlab-ci.yml` pour wex (repo source)
- [ ] Étape : bump de version (`default::version/increment` ou équivalent)
- [ ] Étape : déclenchement du build dans `wex-build` (le CI clone `source/` depuis GitLab, pas un symlink local)
- [ ] Étape : upload du `.deb` vers le GitLab Package Registry
- [ ] Étape : déclenchement de la publication dans `wex-apt-repo`
- [ ] Étape optionnelle : déploiement automatique via Ansible/n8n (comme wex-5)

---

## Notes

- Le build wex-5 uploadait sur : `https://gitlab.wexample.com/api/v4/projects/{id}/packages/generic/wex/{version}/{package}`
- Le dépôt aptly utilise des distributions nommées (ex: `stable`, `beta`) extraites du numéro de version
- Le répertoire `wex-build/builds/` contient les artefacts générés — ne pas committer
- L'utilisateur `owner` est attendu par `build.py` pour le changement de propriétaire des fichiers buildés (vérifier que cet utilisateur existe sur la machine de build)
- En CI/CD, `wex-build/source/` est alimenté par un `git clone` du repo wex depuis GitLab — le symlink local `source/` n'est utile que pour les tests de build manuels
