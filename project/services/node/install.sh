#!/usr/bin/env bash

nodeAppInstall() {
  . .env

  local STARTED
  STARTED=$(wex app/started)

  if [ "${STARTED}" != true ];then
    wex app/start
  fi

  if [ -f ./project/package.json ];then
    # Yarn
    local OPTION=""
    if [ "${SITE_ENV}" = "prod" ];then
      OPTION="--production"
    fi;

    wex app/exec -l -c="yarn install "${OPTION}
  fi

  # Rebuild and clear caches.
  wex app/build

  # Give site perms
  wex app/perms

  # Stop site if not already running.
  if [ "${STARTED}" != true ];then
    wex app/stop
  fi
}