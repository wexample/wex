#!/usr/bin/env bash

repoDelete() {
  local REPO_NAME=$(wex repo/name)
  # Delete
  wex wexample::gitlab/delete -p="projects/${REPO_NAME}"
}
