#!/usr/bin/env bash

siteConfigYmlArgs() {
  _ARGUMENTS=(
    [0]='file_compose_yml f "Docker compose file" false',
  )
}

siteConfigYml() {
  # Allow specified file
  if [ -z "${FILE_COMPOSE_YML+x}" ]; then
    FILE_COMPOSE_YML=${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}
  fi;

  # Parse yml file built by docker compose.
  wex yml/parseFile -f=${FILE_COMPOSE_YML}
}
