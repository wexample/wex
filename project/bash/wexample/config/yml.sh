#!/usr/bin/env bash

configYmlArgs() {
  _ARGUMENTS=(
    [0]='file_compose_yml f "Docker compose file" false',
    [1]='dir_site d "Site directory" false',
  )
}

configYml() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Allow specified file
  if [ "${FILE_COMPOSE_YML}" == "" ]; then
    FILE_COMPOSE_YML=${DIR_SITE}${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}
  fi;

  # Parse yml file built by docker compose.
  wex yml/parseFile -f=${FILE_COMPOSE_YML}
}
