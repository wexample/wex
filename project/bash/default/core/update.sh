#!/usr/bin/env bash

coreUpdateArgs() {
  _AS_NON_SUDO=false
  _DESCRIPTION="Update core and proxy server. Proxy may be restarted."
  _ARGUMENTS=(
    'branch b "Switch to specified branch, by default stay on current one" false'
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

  wex core::migration/exec --from ${WEX_VERSION_FROM} --to ${WEX_VERSION_NEW} --command core

  # Proxy server exists
  if [ -d ${WEX_WEXAMPLE_DIR_PROXY} ];then
    # Update proxy server
    cd ${WEX_WEXAMPLE_DIR_PROXY}
    wex app/update
  fi

  _wexMessage "wex up-to-date at v"${WEX_VERSION_NEW}
}
