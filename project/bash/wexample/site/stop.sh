#!/usr/bin/env bash

siteStop() {
  # Write config file, indicates started=stop and recreate yml file if missing.
  wex config/write -s=false
  # Use previously generated yml file.
  docker-compose -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} down
  # Execute services scripts if exists
  wex service/exec -c="stop"
  # Reload file
  wex sites/update
  # Rebuild hosts
  wex hosts/update
}
