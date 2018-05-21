#!/usr/bin/env bash

gitHasChangesArgs() {
  _ARGUMENTS=(
    [0]='path_git p "File or directory path" false'
  )
}

gitHasChanges() {
    if [ -z "$(git status --porcelain ${PATH_GIT})" ]; then
      echo false
    else
      echo true
    fi
}