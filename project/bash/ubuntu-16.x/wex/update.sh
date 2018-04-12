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
    git pull origin ${BRANCH}
    # Git all needed wrights.
    chown root:root -R *
    chmod -R 755 *
    # Info
    echo "Wexample is up-to-date at v"$(wex wex/version)
  fi
}
