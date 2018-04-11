#!/usr/bin/env bash

gitTagExistsArgs() {
  _ARGUMENTS=(
    [0]='tag t "Tag name" true'
  )
}

gitTagExists() {
  if GIT_DIR=.git git rev-parse ${TAG} >/dev/null 2>&1
  then
      echo true
  else
      echo false
  fi
}
