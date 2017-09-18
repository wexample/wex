#!/usr/bin/env bash

wexampleLocalUpdate() {
  GIT_EXISTS=$(wexample gitExists)
  if [ ${GIT_EXISTS} == true ];then
    cd ${WEX_LOCAL_DIR}
    git pull origin master
  fi
}
