#!/usr/bin/env bash

versionGenerateArgs() {
  _ARGUMENTS=(
    [0]='version v "Sub version number" false'
  )
}

versionGenerate() {
  local LAST_COMMIT_TIME=$(wex git/lastCommitTime)
  local YEAR=$(date -d @${LAST_COMMIT_TIME} +%Y)

  # Check if running.
  if [ -z "${VERSION+x}" ]; then
    VERSION=0
  fi

  echo ${VERSION}.${YEAR}.$(git rev-list --all --count)
}
