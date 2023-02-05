#!/usr/bin/env bash

coreUpdateArgs() {
  _DESCRIPTION='Update core and addons.'
  _ARGUMENTS=(
    'branch b "Switch to specified branch, by default stay on current one" false'
  )
}

coreUpdate() {
  local WEX_VERSION_FROM=$(wex core/version)

  _wexLog "Updating from v${WEX_VERSION_FROM}"

  _wexLog "Pulling git changes"
  # Go to install dir.
  cd "${WEX_DIR_ROOT}../"
  # Choose branch
  if [ "${BRANCH}" == "" ];then
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
  fi;

  # Override changes and pull.
  git reset --hard
  git fetch --tags

  git pull origin "${BRANCH}"
  git update-index --chmod=+x

  _wexLog "Updating addons..."
  for ADDON in "${WEX_ADDONS[@]}"; do
    if [ -d "${WEX_DIR_ADDONS}${ADDON}" ]; then
      cd "${WEX_DIR_ADDONS}${ADDON}" && git pull
    fi
  done

  chmod -R +x "${WEX_DIR_INSTALL}"

  local WEX_VERSION_NEW=$(wex core/version)

  # Allow wex to init again.
  unset WEX_INIT

  # Proxy server exists
  if [ -d "${WEX_DIR_PROXY}" ];then
    # Update proxy server
    cd "${WEX_DIR_PROXY}"
    wex app/update
  fi

  _wexMessage "wex up-to-date at v${WEX_VERSION_NEW}"
}
