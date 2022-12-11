#!/usr/bin/env bash

appStop() {
  # Already stopped
  if [ "$(wex app/started -ic)" = false ];then
    return
  fi
  # Execute services scripts if exists
  wex hook/exec -c="appStop"
  # Write config file, indicates started=stop and recreate yml file if missing.
  wex config/write -s=false -nr
  # Use previously generated yml file.
  docker-compose -f "${WEX_APP_COMPOSE_BUILD_YML}" down
  # Reload file
  wex app/update
  # Rebuild hosts
  wex hosts/update
  # Execute services scripts if exists
  wex hook/exec -c="appStopped"
}
