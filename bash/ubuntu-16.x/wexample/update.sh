#!/usr/bin/env bash

wexampleUpdate() {
  # Git expected.
  GIT_EXISTS=$(wex packageExists git)
  if [ ${GIT_EXISTS} == true ];then
    # Go to wexample install dir.
    cd ${WEX_LOCAL_DIR}
    # Override changes and pull.
    wexample git/resetHard
    git pull origin master
    # Git all needed wrights.
    chown root:root -R *
    chmod -R 755 *
  fi
}
