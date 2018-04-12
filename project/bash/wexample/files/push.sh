#!/usr/bin/env bash

filesPushArgs() {
  _ARGUMENTS=(
    [0]='environment e "Environment to transfer to" true'
  )
}

filesPush() {
  FOLDERS=($(wex files/list))

  for FOLDER in ${FOLDERS[@]};do
    wex wexample::file/upload -f=${FOLDER} -d=${FOLDER} -e=${ENVIRONMENT}
  done
}
