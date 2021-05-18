#!/usr/bin/env bash

gitDeletableArgs() {
  _DESCRIPTION="Join array values (space separated) with given separator"
  _ARGUMENTS=(
    'exclude e "Branch to keep even it was merged" true "master|develop"'
  )
}

gitDeletable() {
  git branch --merged | egrep -v "(^(\*?[[:space:]]*)(${EXCLUDE})$)"
}
