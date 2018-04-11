#!/usr/bin/env bash

versionGenerateArgs() {
  _ARGUMENTS=(
    [0]='subversion v "Sub version number" false'
  )
}

versionGenerate() {
  local LAST_COMMIT_TIME=$(wex git/lastCommitTime)
  local YEAR=$(date -d @${LAST_COMMIT_TIME} +%Y)

  # Check if running.
  if [ -z "${SUBVERSION+x}" ]; then
    SUBVERSION=0
  fi

  echo ${YEAR}.${SUBVERSION}.$(git rev-list --all --count)
}
