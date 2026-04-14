# Roadmap de publication — wex 6

Objectif : packager wex-6 sous forme de paquet `.deb` distribué via un dépôt APT custom,
installable sur serveurs Ubuntu/Debian et en local (mode dev, sources directes).

---

## 1. Prérequis fonctionnels

Avant de builder le paquet, s'assurer que wex-6 tourne correctement en local.

- [ ] `bin/wex` est fonctionnel (exécution depuis les sources via venv)
- [ ] `bin/install` installe correctement le venv et les dépendances (`requirements.txt`)
- [ ] `wex core::core/install` s'exécute sans erreur post-install
- [ ] L'autocomplétion bash fonctionne après install locale
- [ ] `version.txt` est à jour (actuellement `6.0.0`)

---

## 2. Adaptations du script d'install pour le mode paquet

Le `bin/install` actuel est conçu pour une install depuis les sources.
Il faut le rendre compatible avec une install depuis `/usr/lib/wex/` (mode paquet apt).

- [ ] Créer un `bin/postinst` (ou adapter `bin/install`) qui fonctionne quand les sources sont dans `/usr/lib/wex/`
- [ ] Le script doit passer `WEX_SKIP_APT=1` (les dépendances apt sont déjà installées par dpkg)
- [ ] Le script doit éviter de demander sudo si déjà root (contexte postinst)
- [ ] Créer/adapter `bin/uninstall` pour le `postrm` Debian
- [ ] Vérifier que `DEBIAN_FRONTEND=noninteractive` est supporté (pas de prompt interactif pendant install)

---

## 3. Infrastructure de build Debian (wex-build)

Le `wex-build` existant (wex-5) est largement réutilisable. Il faut l'adapter pour wex-6.

- [ ] Créer un sous-dossier `wex-build/source-wex6/` (ou pointer `source/` vers wex-6)
- [ ] Adapter `templates/debian/control` pour wex-6 :
  - Nom du paquet : `wex` (identique)
  - Dépendances système : `python3 (>= 3.10)`, `python3-pip`, `python3-venv`, `bash`, `git`, etc.
  - Vérifier si de nouvelles dépendances sont nécessaires par rapport à wex-5
- [ ] Adapter `templates/debian/install` (mapping de fichiers) :
  - `bin/` → `usr/lib/wex/bin/` (wex-5 utilisait `cli/` → `usr/lib/wex/cli/`)
  - `src/` → `usr/lib/wex/src/`
  - `.wex/` → `usr/lib/wex/.wex/`
  - Assets divers (logo, man page, etc.)
- [ ] Adapter `templates/debian/rules` :
  - Symlink `usr/lib/wex/bin/wex` → `usr/bin/wex` (au lieu de `cli/wex`)
  - Permissions 755 sur `bin/` (au lieu de `cli/`)
- [ ] Adapter `templates/debian/postinst` pour appeler `bin/install` (au lieu de `cli/install`)
- [ ] Adapter `build.py` si nécessaire (chemins, nom du paquet)
- [ ] Tester le build en local : `python3 script/build.py -v 6.0.0 -n wex`

---

## 4. Dépôt APT (wex-apt-repo)

Le dépôt aptly existant est réutilisable tel quel pour wex-6.

- [ ] Vérifier que le serveur `wex-apt-repo` est opérationnel
- [ ] Vérifier que la clé GPG est toujours valide
- [ ] Tester `publish.sh` avec un `.deb` wex-6 en local
- [ ] Valider que `apt-get install wex` depuis le dépôt installe bien la version 6

---

## 5. Install locale en mode développement

Sur cette machine, on veut utiliser wex-6 depuis les sources (pour pouvoir les modifier),
pas depuis le paquet apt.

- [ ] Définir la stratégie : symlink `/usr/bin/wex` → `~/Desktop/WIP/.../wex-6/bin/wex` ?
- [ ] S'assurer que le venv local est actif lors de l'appel à `wex` (via le script `bin/wex`)
- [ ] Documenter la procédure d'install dev dans `.wex/knowledge/readme/`
- [ ] Vérifier que les modifications de sources sont prises en compte immédiatement (sans rebuild)

---

## 6. Tests sur VM

- [ ] Monter une VM Ubuntu (VirtualBox) propre
- [ ] Configurer la VM pour pointer sur le dépôt APT wex
- [ ] Tester `apt-get install wex` sur la VM
- [ ] Valider que `wex` fonctionne post-install (commandes de base)
- [ ] Tester la mise à jour : publier une version `6.0.1`, faire `apt-get upgrade`
- [ ] Tester `apt-get remove wex` (postrm)

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

- [ ] Créer ou adapter `.gitlab-ci.yml` pour wex-6
- [ ] Étape : bump de version (`wex core::version/new` ou équivalent)
- [ ] Étape : déclenchement du build dans `wex-build`
- [ ] Étape : upload du `.deb` vers le GitLab Package Registry
- [ ] Étape : déclenchement de la publication dans `wex-apt-repo`
- [ ] Étape optionnelle : déploiement automatique via Ansible/n8n (comme wex-5)

---

## Notes

- Le build wex-5 uploadait sur : `https://gitlab.wexample.com/api/v4/projects/{id}/packages/generic/wex/{version}/{package}`
- Le dépôt aptly utilise des distributions nommées (ex: `stable`, `beta`) extraites du numéro de version
- Le répertoire `wex-build/builds/` contient les artefacts générés — ne pas committer
- L'utilisateur `owner` est attendu par `build.py` pour le changement de propriétaire des fichiers buildés (vérifier que cet utilisateur existe sur la machine de build)
