# Roadmap : Stratégies de publication — pipeline complet

## Context

Currently `AbstractPublicationStrategy` covers only one micro-step post-publish
(`ensure_tag_triggers_ci`). The goal is for each strategy to own the **complete release
pipeline**: push branch → MR → poll CI → poll prod deployment.

Standard strategies to implement:

| Strategy | Description |
|----------|-------------|
| `main_push` | direct push to main + tag → CI on tag (current, no-op) |
| `branch_merge` | version branch → push → MR → auto merge → poll CI → poll prod |
| `tag_only` | tag pushed on existing commit, without branch (lib case without CI) |

**Priority target:** `branch_merge` applied to `syrtis-react-ui`, then the full stack.

Overlap with `publication-pipeline-ci-cd.md`: this roadmap covers the generic pattern;
the other covers the implementation specific to the `wex` package (apt).

---

## Phase 1 — Refactoring AbstractPublicationStrategy ✅

- [x] Replace `ensure_tag_triggers_ci()` with `run_post_publish_pipeline()`
- [x] Declare hooks in the abstract class: `post_push()`, `wait_for_ci()`, `wait_for_deployment()`
- [x] `from_workdir()` reads `git.publication_strategy` from `.wex/config.yml`
- [x] Update `_do_publish()` in `repo_workdir.py`

---

## Phase 2 — GitlabRemote enrichi ✅

Integrated into `filestate-git/remote/` (no duplicate in `wex-addon-app`):

- [x] `AbstractRemote` — MR/pipeline interface: `create_merge_proposal`, `get_merge_proposal_pipelines`,
  `merge_merge_proposal`, `get_pipeline`, `poll_pipeline` (concrete), hooks `_extract_pipeline_status` /
  `_is_pipeline_terminal`
- [x] `GitlabRemote` — implementation with `_project_endpoint(namespace, name)` → `projects/{ns}%2F{name}`
- [x] `GithubRemote` — implementation (PRs, check-runs, workflow runs, override `_extract_pipeline_status`)
- [x] Config keys: `git.gitlab_url`, `git.gitlab_project_id`, `git.gitlab_token_env_var`

---

## Phase 3 — BranchMergePublicationStrategy complète ✅

- [x] `post_push()` — create idempotent MR, store `_mr_iid`
- [x] `wait_for_ci()` — wait for MR pipeline, raise exception if `failed`, merge if `success`
- [x] `_wait_for_mr_pipeline()` — retry if pipeline not yet created
- [x] Configurable timeout (`git.ci_poll_timeout`, default 600s)
- [x] Clear exception with pipeline URL on failure

---

## Phase 4 — Application à syrtis-react-ui ✅

- [x] Config `.wex/config.yml` : `publication_strategy: branch_merge`, `gitlab_project_id: "73"`,
  `gitlab_url: https://gitlab.syrtis.ai`, `gitlab_token_env_var: GITLAB_API_TOKEN`
- [ ] Test a complete `wex app::release/publish` cycle
- [ ] Verify npm publication after merge

---

## Phase 5 — wait_for_deployment (optional)

- [ ] Implementation: poll `deployment.health_check_url` until expected version
- [ ] Config: `deployment.health_check_url`, `deployment.version_json_path`, `deployment.timeout`

---

## Phase 6 — Extension stack

- [ ] Apply `branch_merge` to all relevant packages
- [ ] Migration 6.0.25 sets `main_push` by default — manual override if `branch_merge` is desired
- [ ] Purely local packages (no GitLab CI) → stay on `main_push`
