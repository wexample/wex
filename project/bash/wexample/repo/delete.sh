#!/usr/bin/env bash

repoDeleteArgs() {
  _ARGUMENTS=(
    [0]='name n "Name or id of the project" false'
  )
}

repoDelete() {
  # Encode name
  NAME=$(wex url/encode -t=${NAME})
  # Delete
  wex wexample::gitlab/delete -p="projects/${NAME}"
}
