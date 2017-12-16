#!/usr/bin/env bash

siteStart() {
  if [ ! -f .env ];then
    echo "Missing .env file"
    return
  fi
  # Server must be started.
  wex server/start -n
  if [ $(wex site/started) == false ];then
    # Write new config,
    # it will also export config variables
    wex site/configWrite -s
    # Add site
    wex server/siteStart -d=$(realpath ./)"/"
    # Use previously generated yml file.
    docker-compose -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} up -d --build
  fi;
}
