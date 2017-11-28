#!/usr/bin/env bash

siteStop() {
  # Write config file, indicates started=stop and recreate yml file if missing.
  wex site/configWrite -s=false
  # Use previously generated yml file.
  docker-compose ${COMPOSE_FILES} down
  # Remove site
  wex server/siteRemove -d="./"
}
