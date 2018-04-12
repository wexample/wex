#!/usr/bin/env bash

siteStart() {
  if [ ! -f .env ];then
    echo "Missing .env file"
    return
  fi
  # Server must be started.
  wex server/start -n
  # Check if site is stopped, ignoring if containers runs or not
  if [ $(wex site/started -ic) == false ];then
    # Write new config,
    # it will also export config variables
    wex site/configWrite -s
    # Add site
    wex server/siteStart -d=$(realpath ./)"/"
    # Use previously generated yml file.
    docker-compose -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} up -d --build
  # Site is marked as started but containers
  # are totally or partially stopped.
  elif [[ $(wex site/containersStarted -a) == false ]];then
    # All containers exists
    if [[ $(wex site/containersExists -a) == true ]];then
      # Start all
      wex site/containersStart
    else
      # Restart will build everything.
      wex site/restart
    fi;
  fi;
  # Open web page
  local DOMAINS=($(wex site/domains))
  wex web/open -u=http://${DOMAINS[0]}
}
