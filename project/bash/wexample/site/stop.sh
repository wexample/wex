#!/usr/bin/env bash

siteStop() {
  # Write config file, indicates started=stop and recreate yml file if missing.
  wex site/configWrite -s=false
  # Use previously generated yml file.
  docker-compose ${COMPOSE_FILES} down
  # Execute services scripts if exists
  wex service/exec -c="stop"
  # Remove site
  wex server/siteStop -d=$(realpath ./)
}
