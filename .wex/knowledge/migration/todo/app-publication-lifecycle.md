# App Publication Lifecycle — Roadmap v6

## Contexte

Deux cas d'usage distincts coexistent sous le terme "versioning/publication" :

| Cas | Exemple | Destination | État v6 |
|-----|---------|-------------|---------|
| **Package / Suite** | wexample Python packages | PyPI, npm, Packagist | Mature, migré |
| **Application** | Syrtis API, manager | Serveur/environnement | Implémenté |

Ce document traite exclusivement du second cas : la publication d'une **application déployée**.

---

## Analyse v5

### Ce que fait `version/new` + `version/new_commit` + `version/new_write`

- Bump interactif de la version dans `.wex/config.yml`
- Écriture dans `version.txt` et `README.md`
- Commit + push

### Ce que fait réellement `build.sh` (Syrtis — référence concrète)

Le script illustre que la publication d'une app est bien plus qu'un bump :

```
wex own/this                          # claim
chmod + app/start                     # prérequis
libraries/sync                        # sync dépendances locales
composer install (no-scripts)         # restore vendor
dev:setup                             # versions de dev
rm composer.lock                      # reset lock

mirror bin/ → client JS              # étape app-spécifique
mirror bin/ → client PHP             # étape app-spécifique

composer install (complet)            # install finale
cache:clear                           # Symfony cache
composer update --lock                # lock résolu

git add composer.json composer.lock   # préparation
version/new                           # bump (wex)
update registry version               # propagation registre
write version.txt                     # écriture fichier
file-state/rectify                    # rectification
git add -A + commit + push            # commit final
```

**Constat :** les étapes "métier" (composer, cache, mirror, registry) sont entièrement spécifiques à l'app. `version/new` n'est qu'un maillon parmi d'autres. Il ne faut donc pas chercher à tout absorber dans une commande générique wex.

---

## Cycle de vie cible v6

### Principe directeur

Wex v6 fournit un **squelette de pipeline** avec des points d'ancrage. L'application définit ses propres commandes et les **attache** explicitement aux étapes du pipeline via un attribut `attach`. Les tests passent en CI/CD, pas en local.

### Étapes canoniques

```
1. bump          Incrémenter la version (interactif ou --yes)
2. rectify       Mettre à jour les fichiers générés (version.txt, README, etc.)
3. commit        Committer + pousser les changements
4. tag           Créer le tag git de publication
──────────────────────────────────────────────────
5. [CI/CD]       Tests, lint, build, deploy
```

### Points d'ancrage — système `attach`

Les commandes app-spécifiques se déclarent elles-mêmes attachées à une commande du pipeline via `@attach` :

```python
# Dans la commande locale de l'app Syrtis, par exemple :
@attach(before="app::app/publish")
def syrtis_prepare_build():
    # composer install, cache:clear, update lock...

@attach(after="app::package/bump")
def syrtis_mirror_clients():
    # mirror bin/ → clients JS/PHP
    # update registry version
```

**Principe :** c'est la commande qui se déclare, pas l'orchestrateur qui cherche. Les points d'ancrage sont les commandes réelles du pipeline (`app::app/publish`, `app::package/bump`, `app::file_state/rectify`...). Aucune convention de nommage à respecter.

---

## Hiérarchie workdir

Suite à une clarification de la sémantique des workdirs, le renommage suivant a été effectué :

| Ancien nom | Nouveau nom | Rôle |
|------------|-------------|------|
| `AppWorkdir` | `ManagedWorkdir` | Répertoire géré par wex, sans hypothèse git |
| `RepoWorkdir` | `RepoWorkdir` (inchangé) | ManagedWorkdir + git |
| `CodeBaseWorkdir` | `CodeBaseWorkdir` (inchangé) | RepoWorkdir + publication (tag, merge, push) |

Les apps déployées (sites web, apps mobiles) ont toujours un repo git → elles utilisent `CodeBaseWorkdir`, qui contient toutes les méthodes nécessaires à la publication.

---

## Ce qui a été implémenté

### `CodeBaseMiddleware`

**Fichier :** `wex-addon-app/middleware/code_base_middleware.py`

Middleware qui injecte un `CodeBaseWorkdir` dans les commandes de publication d'app. Hérite de `AppMiddleware`, override uniquement `_create_app_workdir`.

### `app::app/publish`

**Fichier :** `wex-addon-app/commands/app/publish.py`

Orchestrateur de publication d'app. Pipeline en `QueuedCollectionResponse` :

```
app::app/publish [--yes] [--no-bump] [--skip-rectify]
```

1. `_bump` — `app_workdir.bump(interactive=not yes)` — stop si annulé
2. `_rectify` — `run_function(app__file_state__rectify)`
3. `_commit` — `commit_changes()` + `push_to_deployment_remote(main)`
4. `_tag` — `add_publication_tag()`

La logique git est entièrement fournie par `CodeBaseWorkdir` (bump avec branche, tag annoté, push). La commande est un orchestrateur pur (~60 lignes).

### Résolution de `version/new` (v5)

| v5 | v6 |
|----|----|
| `version/new` | `bump()` dans `CodeBaseWorkdir` via `app::app/publish` |
| `version/new_write` | `app::file_state/rectify` |
| `version/new_commit` | `commit_changes()` + `push_to_deployment_remote()` |
| orchestration | `app::app/publish` ✓ |

---

## Reste à faire

### Migration de build.sh (Syrtis, exemple concret)

Une fois l'orchestrateur en place, `build.sh` de Syrtis peut se réécrire en commandes wex locales :

```python
# .wex/commands/syrtis_build_prepare.py
@attach(before="app::app/publish")
# composer install, cache:clear, update lock

# .wex/commands/syrtis_build_mirror.py
@attach(after="app::package/bump")
# mirror bin/ → clients JS/PHP, update registry version
```

`build.sh` devient : `wex app::app/publish`

### Point ouvert — branche version pour les apps

`RepoWorkdir.bump()` crée une branche `version-x.y.z` (conçu pour les packages). Pour les apps, ce workflow de branche n'est pas forcément souhaité. À trancher : est-ce qu'`app::app/publish` doit appeler `merge_to_main()` après le tag, ou bypasser la création de branche ?

### Étape optionnelle — `app::app/publish-suite`

Si plusieurs apps d'un projet doivent publier ensemble (ex: api + manager), étendre `app::suite/publish` ou créer un orchestrateur de niveau projet.

---

## Ce qui reste hors scope wex (CI/CD)

Les éléments suivants **ne font pas partie** du cycle de vie wex local :
- Exécution des tests (pytest, phpunit, jest...)
- Lint / analyse statique
- Build d'artefacts (Docker image, dist...)
- Déploiement effectif sur serveur

Ces étapes sont déclenchées **après le push** via CI/CD (GitHub Actions, GitLab CI...).
