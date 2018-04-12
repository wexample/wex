#!/usr/bin/env bash

dirExistsArgs() {
  _ARGUMENTS=(
    [0]='dir d "Directory name" true'
  )
}

dirExists() {
  if [[ -z "${DIR+x}" ]]; then
    # Get current dir.
    DIR=./
  fi;

  [ -d ${DIR} ] && echo true || echo false
}
