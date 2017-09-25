#!/usr/bin/env bash

wexampleUpdate() {
  # Git expected.
  GIT_EXISTS=$(wex package/exists -n=git)
  if [[ ${GIT_EXISTS} == true ]];then
    # Go to wexample install dir.
    cd ${WEX_LOCAL_DIR}
    # Override changes and pull.
    wex git/resetHard
    git pull origin master
    # Git all needed wrights.
    chown root:root -R *
    chmod -R 755 *
    # Info
    echo "Wexample is up-to-date at v"$(wex wexample/version)
  fi
}
