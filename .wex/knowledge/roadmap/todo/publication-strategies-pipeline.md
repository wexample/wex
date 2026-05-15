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

## Phase 1 — Refactoring AbstractPublicationStrategy ✅

- [x] Remplacer `ensure_tag_triggers_ci()` par `run_post_publish_pipeline()`
- [x] Déclarer les hooks dans la classe abstraite : `post_push()`, `wait_for_ci()`, `wait_for_deployment()`
- [x] `from_workdir()` lit `git.publication_strategy` dans `.wex/config.yml`
- [x] Mettre à jour `_do_publish()` dans `repo_workdir.py`

---

## Phase 2 — GitlabRemote enrichi ✅

Intégré dans `filestate-git/remote/` (pas de doublon dans `wex-addon-app`) :

- [x] `AbstractRemote` — interface MR/pipeline : `create_merge_proposal`, `get_merge_proposal_pipelines`,
  `merge_merge_proposal`, `get_pipeline`, `poll_pipeline` (concret), hooks `_extract_pipeline_status` /
  `_is_pipeline_terminal`
- [x] `GitlabRemote` — implémentation avec `_project_endpoint(namespace, name)` → `projects/{ns}%2F{name}`
- [x] `GithubRemote` — implémentation (PRs, check-runs, workflow runs, override `_extract_pipeline_status`)
- [x] Config keys : `git.gitlab_url`, `git.gitlab_project_id`, `git.gitlab_token_env_var`

---

## Phase 3 — BranchMergePublicationStrategy complète ✅

- [x] `post_push()` — créer MR idempotente, stocker `_mr_iid`
- [x] `wait_for_ci()` — attendre pipeline MR, lever exception si `failed`, merger si `success`
- [x] `_wait_for_mr_pipeline()` — retry si pipeline pas encore créé
- [x] Timeout configurable (`git.ci_poll_timeout`, défaut 600s)
- [x] Exception claire avec URL pipeline en cas d'échec

---

## Phase 4 — Application à syrtis-react-ui ✅

- [x] Config `.wex/config.yml` : `publication_strategy: branch_merge`, `gitlab_project_id: "73"`,
  `gitlab_url: https://gitlab.syrtis.ai`, `gitlab_token_env_var: GITLAB_API_TOKEN`
- [ ] Tester un cycle complet `wex app::release/publish`
- [ ] Vérifier publication npm après merge

---

## Phase 5 — wait_for_deployment (optionnel)

- [ ] Implémentation : poll `deployment.health_check_url` jusqu'à version attendue
- [ ] Config : `deployment.health_check_url`, `deployment.version_json_path`, `deployment.timeout`

---

## Phase 6 — Extension stack

- [ ] Appliquer `branch_merge` à tous les packages concernés
- [ ] Migration 6.0.25 pose `main_push` par défaut — override manuel si `branch_merge` voulu
- [ ] Packages purement locaux (pas de GitLab CI) → rester sur `main_push`
