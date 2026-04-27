# Roadmap : Publication wex via CI/CD GitLab

## Contexte

Aujourd'hui les autres packages (npm, PHP/Packagist) ont migré vers un modèle
où c'est le CI/CD qui effectue la publication réelle, et non la machine locale.
La machine locale crée simplement la merge request ; le pipeline se charge du reste.

Pour `wex` (paquet Debian/apt), la publication est encore manuelle : merge request
créée à la main sur GitLab, pipeline attendu manuellement, vérification manuelle
sur le dépôt apt.

L'objectif est d'automatiser ce cycle complet dans `app::suite/publish` (ou une
phase dédiée appelée depuis celui-ci).

---

## Phases

### Phase 1 — Détection du mode de publication

- [ ] Définir dans la config app (`.wex/app.yml`) une clé `publication.mode`
  avec les valeurs possibles : `local` (défaut actuel) / `ci` (pipeline GitLab/GitHub)
- [ ] Lire cette clé dans `publish_bumped` / `publish` pour brancher sur le bon mode
- [ ] Permettre la surcharge par package (certains packages peuvent avoir un mode différent)

---

### Phase 2 — Création de la Merge Request GitLab

- [ ] Après le `commit_and_push` de la branche `version-x.y.z`, créer automatiquement
  une MR via l'API GitLab REST (`POST /projects/:id/merge_requests`)
- [ ] Paramètres de la MR :
  - source branch : `version-x.y.z`
  - target branch : `main`
  - title : `Release x.y.z`
  - `remove_source_branch: true`
  - `squash: false`
- [ ] Stocker l'IID de la MR pour les étapes suivantes
- [ ] Gérer le cas où une MR existe déjà pour cette branche (idempotent)

---

### Phase 3 — Attente du pipeline pre-merge

- [ ] Après création de la MR, récupérer le pipeline associé
  (`GET /projects/:id/merge_requests/:iid/pipelines`)
- [ ] Polling jusqu'à status `success` ou `failed` / `canceled`
- [ ] Afficher la progression via `io.progress` ou logs
- [ ] Lever une exception claire si le pipeline échoue (lien vers le pipeline dans le message)

---

### Phase 4 — Merge automatique

- [ ] Si pipeline `success` et pas de conflits : merger via l'API
  (`PUT /projects/:id/merge_requests/:iid/merge`)
- [ ] Gérer les cas d'échec du merge (conflit, MR déjà mergée, etc.)
- [ ] Récupérer le commit SHA du merge pour tracker le pipeline post-merge

---

### Phase 5 — Attente du pipeline post-merge

- [ ] Après le merge, récupérer le pipeline déclenché sur `main`
  (`GET /projects/:id/pipelines?ref=main&sha=<merge_commit>`)
- [ ] Polling jusqu'à `success` ou échec
- [ ] Même logique de progression / erreur que phase 3

---

### Phase 6 — Vérification sur le dépôt apt

- [ ] Après le pipeline post-merge, vérifier que `wex` est bien disponible
  dans le dépôt apt à la bonne version
- [ ] Commande : `apt-cache policy wex` ou requête HTTP sur le dépôt
- [ ] Polling avec timeout configurable (le dépôt apt peut avoir un délai de propagation)
- [ ] Log de succès avec la version confirmée

---

## Abstractions à créer

- `GitlabApiClient` (ou helper) — wrapper léger autour des appels REST GitLab
  (token depuis config ou env var `GITLAB_TOKEN`)
- `CiPublicationWatcher` — logique de polling réutilisable (phase 3, 5, 6)
- Config keys :
  - `publication.mode` : `local` | `ci`
  - `publication.gitlab.project_id`
  - `publication.gitlab.token_env_var` (défaut : `GITLAB_TOKEN`)
  - `publication.apt.package_name` (défaut : `wex`)
  - `publication.apt.check_url`

---

## Notes

- Les packages npm et PHP ont déjà ce pattern ; s'inspirer de leur implémentation
  pour la cohérence (même interface de polling, mêmes codes d'erreur)
- La phase 6 (vérif apt) est spécifique à `wex` ; les autres packages ont un
  équivalent (`_wait_for_registry` existe déjà dans `repo_workdir.py`)
- Le polling doit être interruptible (Ctrl+C) sans laisser le process dans un état incohérent
