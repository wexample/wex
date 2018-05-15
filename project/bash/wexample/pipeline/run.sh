#!/usr/bin/env bash

pipelineRun() {
  # Repo name
  local REPO_NAME=$(wex repo/name);
  wex wexample::gitlab/post -p="projects/${REPO_NAME}/pipeline" -d="ref=master"
}