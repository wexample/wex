#!/usr/bin/env bash

appPull() {
  # Update GIT root.
  wex git/pullTree

  . ${WEX_APP_CONFIG}

  if [ -d ${PROJECT_DIR}/.git ];then
    cd ${PROJECT_DIR}
    # Update GIT root.
    wex git/pullTree
    cd ../
  fi

  # Execute local scripts.
  wex hook/exec -c=appPull
}