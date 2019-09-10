#!/usr/bin/env bash

_wexMigrateApp() {
  # Replace ${SITE_NAME} by ${SITE_NAME_INTERNAL}
  # into docker compose files.
  if [ -d ./docker/ ];then
    local YMLS=($(ls ./docker/*.yml))

    for YML in "${YMLS[@]}"
    do
      wex file/textReplace -f=${YML} -r=s/\$\{SITE_NAME\}/\$\{SITE_NAME_INTERNAL\}/g
    done
  fi
}