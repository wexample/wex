#!/usr/bin/env bash

filesPullArgs() {
  _ARGUMENTS=(
    [0]='environment e "Environment to transfer to" true'
  )
}

filesPull() {
  FOLDERS=($(wex files/list))

  for FOLDER in ${FOLDERS[@]};do
    wex wexample::file/download -f=${FOLDER} -d=$(dirname ${FOLDER}) -e=${ENVIRONMENT}
  done
}
