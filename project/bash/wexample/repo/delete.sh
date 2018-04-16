#!/usr/bin/env bash

repoDeleteArgs() {
  _ARGUMENTS=(
    [0]='name n "Name or id of the project" false'
  )
}

repoDelete() {
  local REPO_NAME=$(wex repo/name)
  # Delete
  wex wexample::gitlab/delete -p="projects/${REPO_NAME}"
}
