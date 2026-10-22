# Roadmap : Publication wex via CI/CD GitLab

## Context

Today the other packages (npm, PHP/Packagist) have migrated to a model
where CI/CD performs the actual publication, not the local machine.
The local machine simply creates the merge request; the pipeline handles the rest.

For `wex` (Debian/apt package), publication is still manual: merge request
created by hand on GitLab, pipeline waited on manually, manual verification
on the apt repository.

The goal is to automate this complete cycle in `app::suite/publish` (or a
dedicated phase called from it).

---

## Phases

### Phase 1 — Publication mode detection

- [ ] Define a `publication.mode` key in the app config (`.wex/app.yml`)
  with possible values: `local` (current default) / `ci` (GitLab/GitHub pipeline)
- [ ] Read this key in `publish_bumped` / `publish` to branch on the correct mode
- [ ] Allow per-package override (some packages may have a different mode)

---

### Phase 2 — GitLab Merge Request creation

- [ ] After the `commit_and_push` of the `version-x.y.z` branch, automatically create
  an MR via the GitLab REST API (`POST /projects/:id/merge_requests`)
- [ ] MR parameters:
  - source branch: `version-x.y.z`
  - target branch: `main`
  - title: `Release x.y.z`
  - `remove_source_branch: true`
  - `squash: false`
- [ ] Store the MR IID for the following steps
- [ ] Handle the case where an MR already exists for this branch (idempotent)

---

### Phase 3 — Pre-merge pipeline wait

- [ ] After the MR is created, retrieve the associated pipeline
  (`GET /projects/:id/merge_requests/:iid/pipelines`)
- [ ] Poll until status `success` or `failed` / `canceled`
- [ ] Display progress via `io.progress` or logs
- [ ] Raise a clear exception if the pipeline fails (include a link to the pipeline in the message)

---

### Phase 4 — Automatic merge

- [ ] If pipeline `success` and no conflicts: merge via the API
  (`PUT /projects/:id/merge_requests/:iid/merge`)
- [ ] Handle merge failure cases (conflict, MR already merged, etc.)
- [ ] Retrieve the merge commit SHA to track the post-merge pipeline

---

### Phase 5 — Post-merge pipeline wait

- [ ] After the merge, retrieve the pipeline triggered on `main`
  (`GET /projects/:id/pipelines?ref=main&sha=<merge_commit>`)
- [ ] Poll until `success` or failure
- [ ] Same progress / error logic as phase 3

---

### Phase 6 — apt repository verification

- [ ] After the post-merge pipeline, verify that `wex` is available
  in the apt repository at the correct version
- [ ] Command: `apt-cache policy wex` or HTTP request against the repository
- [ ] Polling with configurable timeout (the apt repository may have a propagation delay)
- [ ] Success log with the confirmed version

---

## Abstractions to create

- `GitlabApiClient` (or helper) — lightweight wrapper around GitLab REST calls
  (token from config or env var `GITLAB_TOKEN`)
- `CiPublicationWatcher` — reusable polling logic (phases 3, 5, 6)
- Config keys:
  - `publication.mode`: `local` | `ci`
  - `publication.gitlab.project_id`
  - `publication.gitlab.token_env_var` (default: `GITLAB_TOKEN`)
  - `publication.apt.package_name` (default: `wex`)
  - `publication.apt.check_url`

---

## Notes

- The npm and PHP packages already have this pattern; draw from their implementation
  for consistency (same polling interface, same error codes)
- Phase 6 (apt verification) is specific to `wex`; the other packages have an
  equivalent (`_wait_for_registry` already exists in `repo_workdir.py`)
- Polling must be interruptible (Ctrl+C) without leaving the process in an inconsistent state
