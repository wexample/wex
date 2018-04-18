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
    wex config/write -s
    # Add site
    local DIR_SITE=$(realpath ./)"/"
    # Reload sites will clean up list.
    wex sites/update
    # Add new site.
    echo -e "\n"${DIR_SITE} >> ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites
    # Rebuild hosts
    wex hosts/update
    # Load site config
    . ${SITE_PATH}${WEX_WEXAMPLE_SITE_CONFIG}
      # Update host file if user has write access.
    if [ ${SITE_ENV} == "local" ] && [ $(wex file/writable -f=/etc/hosts) == true ];then
      wex hosts/updateLocal
    fi
    # Use previously generated yml file.
    docker-compose -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} up -d --build
  # Site is marked as started but containers
  # are totally or partially stopped.
  elif [[ $(wex containers/started -a) == false ]];then
    # All containers exists
    if [[ $(wex containers/exists -a) == true ]];then
      # Start all
      wex containers/start
    else
      # Restart will build everything.
      wex site/restart
    fi;
  fi;
}
