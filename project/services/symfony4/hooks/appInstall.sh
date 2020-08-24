#!/usr/bin/env bash

symfony4Install() {
  . .env
  . .wex

  local STARTED=$(wex app/started -ic)

  if [ "${STARTED}" != true ];then
    wex app/start
  fi

  # Composer install.
  wex app/exec -l -c="composer install"

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