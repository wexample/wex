#!/usr/bin/env bash

githubTagLatestArgs() {
  _ARGUMENTS=(
    [0]='name n "Name of Github repo" true'
  )
}

githubTagLatest() {
  # Local temp json storage.
  local TMP_JSON_PATH=${WEX_DIR_TMP}githubTagLatest.json
  # Get list of tags.
  curl -s https://api.github.com/repos/${NAME}/tags > ${TMP_JSON_PATH}
  # Get all "names" (tags).
  local NAMES=($(wex json/readValue -f=${TMP_JSON_PATH} -k=name))
  # Get first one.
  echo ${NAMES[0]}
}
