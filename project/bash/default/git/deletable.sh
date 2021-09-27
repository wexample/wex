#!/usr/bin/env bash

gitDeletableArgs() {
  _DESCRIPTION="List all merged branches into master except master and develop"
  _ARGUMENTS=(
    'exclude e "Branch to keep even it was merged" true "master|develop"'
    'branch b "Main branch to compare to" true "master"'
  )
}

gitDeletable() {
  git branch --merged "${BRANCH}" | egrep -v "(^(\*?[[:space:]]*)(${EXCLUDE})$)"
}
