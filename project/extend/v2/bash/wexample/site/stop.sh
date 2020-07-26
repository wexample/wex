#!/usr/bin/env bash

siteStop() {
  # Execute services scripts if exists
  wex hook/exec -c="stop"
  # Write config file, indicates started=stop and recreate yml file if missing.
  wex config/write -s=false -nr
  # Use previously generated yml file.
  docker-compose -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} down
  # Reload file
  wex sites/update
  # Rebuild hosts
  wex hosts/update
  # Execute services scripts if exists
  wex hook/exec -c="appStopped"
}
