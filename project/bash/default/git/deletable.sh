#!/usr/bin/env bash

gitDeletableArgs() {
  _DESCRIPTION="List all merged branches into master except master and develop"
  _ARGUMENTS=(
    'exclude e "Branch to keep even it was merged" true "master|develop"'
  )
}

gitDeletable() {
  git branch --merged master | egrep -v "(^(\*?[[:space:]]*)(${EXCLUDE})$)"
}
