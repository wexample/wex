#!/usr/bin/env bash

siteConfigYml() {
  # Parse yml file built by docker compose.
  wex yml/parseFile -f=${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}
}
