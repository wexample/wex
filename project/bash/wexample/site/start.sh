#!/usr/bin/env bash

siteStart() {
  # Server must be started.
  wex server/start -n

  if [ $(wex site/started) == false ];then
    # Execute services scripts if exists
    wex service/exec -c="start"
    # Write new config,
    # it will also export config variables
    wex site/configWrite -s
    # Add site
    wex server/siteStart -d=$(realpath ./)"/"
    # Use previously generated yml file.
    docker-compose ${COMPOSE_FILES} up -d --build
    # Show domains.
    echo $(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts)
  fi;
}
