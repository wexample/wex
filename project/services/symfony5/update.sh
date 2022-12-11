#!/usr/bin/env bash

symfony5Update() {
  # Composer
  wex site/exec -l -c="composer update"

  # NPM
  local OPTION=""
  if [ "${SITE_ENV}" = "dev" ];then
    OPTION="--dev"
  fi;
  wex site/exec -l -c="npm update "${OPTION}

  # Rebuild and clear caches.
  wex site/build
}