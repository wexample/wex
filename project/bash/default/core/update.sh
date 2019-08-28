#!/usr/bin/env bash

coreUpdateArgs() {
  _DESCRIPTION="Update core"
  _ARGUMENTS=(
    [0]='branch b "Switch to specified branch, by default stay on current one" false'
  )
}

coreUpdate() {
  local WEX_VERSION_FROM=$(wex core/version)

  # Go to wexample install dir.
  cd ${WEX_DIR_ROOT}../
  # Choose branch
  if [ "${BRANCH}" == "" ];then
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
  fi;

  # Override changes and pull.
  git reset --hard
  git fetch --tags

  git pull origin ${BRANCH}
  git update-index --chmod=+x

  chmod -R +x ${WEX_DIR_INSTALL}

  local WEX_VERSION_NEW=$(wex core/version)

  # Allow wex to init again.
  unset WEX_INIT

  wex core/migrate --from ${WEX_VERSION_FROM} --to ${WEX_VERSION_NEW} --command core

  _wexMessage "wex up-to-date at v"${WEX_VERSION_NEW}
}
