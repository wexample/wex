#!/usr/bin/env bash

siteConfigYmlArgs() {
  _ARGUMENTS=(
    [0]='file f "Docker compose file" false',
  )
}

siteConfigYml() {
  # Allow specified file
  if [ -z "${FILE+x}" ]; then
    FILE=${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}
  fi;

  # Parse yml file built by docker compose.
  wex yml/parseFile -f=${FILE}
}
