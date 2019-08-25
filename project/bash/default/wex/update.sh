#!/usr/bin/env bash

wexUpdateArgs() {
  _DESCRIPTION="Update core"
  _ARGUMENTS=(
    [0]='branch b "Switch to specified branch, by default stay on current one" false'
  )
}

wexUpdate() {
  # Git expected.
  GIT_EXISTS=$(wex package/exists -n=git)

  if [[ ${GIT_EXISTS} == true ]];then

    # Go to wexample install dir.
    cd ${WEX_DIR_ROOT}../
    # Choose branch
    if [ "${BRANCH}" == "" ];then
      BRANCH=$(git rev-parse --abbrev-ref HEAD)
    fi;

    # Override changes and pull.
    wex git/resetHard
    git fetch --tags

    # Get only last data
    git pull origin ${BRANCH}
    git update-index --chmod=+x

    # Info
    echo "Wexample is up-to-date at v"$(wex wex/version)
  fi
}
