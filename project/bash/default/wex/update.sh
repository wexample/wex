#!/usr/bin/env bash

wexUpdate() {
  # Git expected.
  GIT_EXISTS=$(wex package/exists -n=git)
  if [[ ${GIT_EXISTS} == true ]];then
    # Go to wexample install dir.
    cd ${WEX_DIR_ROOT}../
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    # Override changes and pull.
    wex git/resetHard
    # Get only last data
    git pull origin ${BRANCH} --depth=1
    git update-index --chmod=+x
    # Info
    echo "Wexample is up-to-date at v"$(wex wex/version)
  fi
}
