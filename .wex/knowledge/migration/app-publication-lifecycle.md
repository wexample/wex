# App Publication Lifecycle — Roadmap v6

## Contexte

Deux cas d'usage distincts coexistent sous le terme "versioning/publication" :

| Cas | Exemple | Destination | État v6 |
|-----|---------|-------------|---------|
| **Package / Suite** | wexample Python packages | PyPI, npm, Packagist | Mature, migré |
| **Application** | Syrtis API, manager | Serveur/environnement | À construire |

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

Les commandes app-spécifiques se déclarent elles-mêmes attachées à une étape du pipeline via un attribut (pseudocode illustratif) :

```python
# Dans la commande locale de l'app Syrtis, par exemple :
@attach(before="app::app/publish::commit")
def syrtis_prepare_build():
    # composer install, cache:clear, update lock...
```

```python
@attach(after="app::app/publish::bump")
def syrtis_mirror_clients():
    # mirror bin/ → clients JS/PHP
    # update registry version
```

**Principe :** c'est la commande qui se déclare, pas l'orchestrateur qui cherche. L'orchestrateur exécute les commandes attachées à chaque point sans les connaître a priori. Aucune convention de nommage à respecter.

---

## Ce qui existe déjà en v6 (réutilisable tel quel)

- `app::package/bump` → logique de bump (détection changements, classification, branche version)
- `app::file_state/rectify` → rectification fichiers générés
- `app::package/commit_and_push` → commit + push
- `app::version/propagate` → propagation vers dépendants (utile pour mono-repos)

Ces briques sont conçues pour les packages mais leur logique est directement réutilisable pour les apps.

---

## Roadmap

### Étape 1 — Commandes app/publish

Créer `app::app/publish` comme orchestrateur de publication d'app :

```
app::app/publish [--yes] [--no-bump] [--skip-rectify]
```

Pipeline interne (points d'ancrage disponibles entre chaque étape) :
1. → `before::publish`
2. `app::package/bump` (sauf `--no-bump`) → `after::bump`
3. `app::file_state/rectify` (sauf `--skip-rectify`) → `after::rectify`
4. → `before::commit`
5. `app::package/commit_and_push` → `after::commit`
6. Tag git `{app_name}/v{version}` → `after::publish`

Les commandes attachées à chaque point sont collectées par le kernel au moment de l'exécution.

**Fichier cible :** `wex-addon-app/commands/app/publish.py`

### Étape 2 — Résolution de `version/new` (v5)

Les trois commandes v5 (`version/new`, `version/new_commit`, `version/new_write`) se dissolvent ainsi :

| v5 | v6 |
|----|----|
| `version/new` | `app::package/bump` (déjà en v6) |
| `version/new_write` | `app::file_state/rectify` (déjà en v6) |
| `version/new_commit` | `app::package/commit_and_push` (déjà en v6) |
| orchestration | `app::app/publish` (à créer) |

→ **Rien de fondamentalement nouveau à coder** sur la logique de bump/rectify/commit. La valeur ajoutée est dans l'orchestrateur et le système de hooks.

### Étape 3 — Convention hooks locaux

Définir la convention dans la doc wex-addon-app :
- Les hooks sont des commandes dans `.wex/commands/` de l'app (ou dans un addon local)
- Nommage : `app-publish-pre`, `app-publish-post`, `app-publish-pre-commit`, etc.
- L'orchestrateur utilise `kernel.run_command_if_exists()` → pas d'erreur si absent

### Étape 4 — Migration de build.sh (Syrtis, exemple concret)

Une fois l'orchestrateur + hooks en place, `build.sh` de Syrtis se réécrit en commandes wex locales :

```
# .wex/commands/app_publish_pre.py
composer install + cache:clear + update lock

# .wex/commands/app_publish_post_commit.py  
update registry version
mirror bin/ → clients JS/PHP
```

`build.sh` devient : `wex app::app/publish`

### Étape 5 (optionnel) — `app::app/publish-suite`

Si plusieurs apps d'un projet doivent publier ensemble (ex: api + manager), étendre `app::suite/publish` ou créer un orchestrateur de niveau projet.

---

## Ce qui reste hors scope wex (CI/CD)

Les éléments suivants **ne font pas partie** du cycle de vie wex local :
- Exécution des tests (pytest, phpunit, jest...)
- Lint / analyse statique
- Build d'artefacts (Docker image, dist...)
- Déploiement effectif sur serveur

Ces étapes sont déclenchées **après le push** via CI/CD (GitHub Actions, GitLab CI...). Le hook `post_publish` peut éventuellement déclencher un pipeline, mais wex ne l'exécute pas directement.

---

## Mise à jour du todo

Suite à cette analyse, `version/new`, `version/new_commit`, `version/new_write` dans `todo/addons/app.md` peuvent être **fermés** en faveur de :

- [ ] `app::app/publish` — orchestrateur publication app avec hooks
- [ ] Convention hooks locaux documentée
- [ ] `kernel.run_command_if_exists()` — mécanisme noyau requis (voir `core-mechanisms.md`)
