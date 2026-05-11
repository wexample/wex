# Roadmap : Stratégies de publication — pipeline complet

## Contexte

Actuellement `AbstractPublicationStrategy` ne couvre qu'une micro-étape post-publish
(`ensure_tag_triggers_ci`). L'objectif est que chaque stratégie soit propriétaire
du **pipeline complet de release** : push branche → MR → poll CI → poll déploiement prod.

Stratégies standard à implémenter :

| Stratégie | Description |
|-----------|-------------|
| `main_push` | push direct sur main + tag → CI sur tag (actuel, no-op) |
| `branch_merge` | branche version → push → MR → merge auto → poll CI → poll prod |
| `tag_only` | tag poussé sur commit existant, sans branche (cas lib sans CI) |

**Cible prioritaire :** `branch_merge` appliquée à `syrtis-react-ui`, puis stack complète.

Overlap avec `publication-pipeline-ci-cd.md` : ce roadmap couvre le pattern générique ;
l'autre couvre l'implémentation spécifique au package `wex` (apt).

---

## Phase 1 — Refactoring AbstractPublicationStrategy

- [ ] Remplacer `ensure_tag_triggers_ci()` par `run_post_publish_pipeline()`
- [ ] Déclarer les hooks optionnels dans la classe abstraite :
  - `post_push()` — après push branche (ex : créer MR)
  - `wait_for_ci()` — poll pipeline CI
  - `wait_for_deployment()` — poll prod (optionnel)
- [ ] `from_workdir()` lit `git.publication_strategy` dans `.wex/config.yml`
- [ ] Mettre à jour `_do_publish()` dans `repo_workdir.py` pour appeler `run_post_publish_pipeline()`

---

## Phase 2 — GitlabApiClient

- [ ] Créer `wex-addon-app/gitlab/gitlab_api_client.py`
  - Token via env var (clé config `git.gitlab_token_env_var`, défaut `GITLAB_TOKEN`)
  - `create_merge_request(project_id, source_branch, target_branch, title)` — idempotent
  - `get_merge_request_pipelines(project_id, mr_iid)`
  - `merge_merge_request(project_id, mr_iid)`
  - `get_pipeline_status(project_id, pipeline_id)`
- [ ] Config keys :
  - `git.gitlab_project_id`
  - `git.gitlab_token_env_var` (défaut : `GITLAB_TOKEN`)

---

## Phase 3 — BranchMergePublicationStrategy complète

Pipeline de `run_post_publish_pipeline()` :

1. Push branche `version-x.y.z` sur GitLab (déjà fait dans `version/push`)
2. Créer MR `version-x.y.z → main` (titre : `Release x.y.z`)
3. Poller pipeline pre-merge jusqu'à `success` / `failed`
4. Merger la MR via API
5. Poller pipeline post-merge sur `main`
6. (Optionnel) `wait_for_deployment()` si configuré

- [ ] Implémenter les étapes 2–5 dans `BranchMergePublicationStrategy`
- [ ] Afficher progression via `io.progress` (lien pipeline dans les logs)
- [ ] Lever exception claire si pipeline `failed` (avec URL)
- [ ] Polling interruptible (Ctrl+C propre)
- [ ] Timeout configurable (`git.ci_poll_timeout`, défaut 600s)

---

## Phase 4 — Application à syrtis-react-ui

- [ ] Ajouter dans `.wex/config.yml` de `syrtis-react-ui` :
  ```yaml
  git:
    publication_strategy: branch_merge
    gitlab_project_id: <ID>
  ```
- [ ] Tester un cycle complet `wex app::release/publish`
- [ ] Vérifier publication npm après merge

---

## Phase 5 — wait_for_deployment (optionnel)

- [ ] Interface `wait_for_deployment()` dans `AbstractPublicationStrategy` (no-op par défaut)
- [ ] Implémentation : poll `deployment.health_check_url` jusqu'à version attendue
- [ ] Config : `deployment.health_check_url`, `deployment.version_json_path`, `deployment.timeout`

---

## Phase 6 — Extension stack

- [ ] Appliquer `branch_merge` à tous les packages concernés
- [ ] Migration 6.0.25 pose `main_push` par défaut — override manuel si `branch_merge` voulu
- [ ] Packages purement locaux (pas de GitLab CI) → rester sur `main_push`
