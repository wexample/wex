#!/usr/bin/env bash

wexampleLocalUpdate() {
  GIT_EXISTS=$(wexample gitExists)
  if [ ${GIT_EXISTS} == true ];then
    # Go to wexample install dir.
    cd ${WEX_LOCAL_DIR}
    # Override changes and pull.
    wexample gitResetHard
    git pull origin master
    # Git all needed wrights.
    chown root:root -R *
    chmod 755 -r *
  fi
}
