#!/usr/bin/env bash

nodeInstall() {
  . .env

  local STARTED=$(wex site/started)

  if [ ${STARTED} != true ];then
    wex site/start
  fi

  if [ -f ./project/package.json ];then
    # Yarn
    local OPTION=""
    if [ "${SITE_ENV}" = "prod" ];then
      OPTION="--production"
    fi;

    wex site/exec -l -c="yarn install "${OPTION}
  fi

  # Rebuild and clear caches.
  wex site/build

  # Give site perms
  wex site/perms

  # Stop site if not already running.
  if [ ${STARTED} != true ];then
    wex site/stop
  fi
}