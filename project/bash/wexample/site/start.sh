#!/usr/bin/env bash

siteStart() {
  if [ ! -f .env ];then
    echo "Missing .env file"
    return
  fi

  # Prepare files
  wex file/convertLinesToUnix -f=.env &> /dev/null
  wex file/convertLinesToUnix -f=wex.json &> /dev/null

  # Server must be started.
  wex server/start -n

  # Check if site is already started,
  # ignoring if containers runs or not.
  if [[ $(wex site/started -ic) == true ]];then
     # All containers exists
     # but one is not started.
     if [[ $(wex containers/exists -a) == true ]];then
       if [[ $(wex containers/started -a) != true ]];then
         # Start all containers
         wex containers/start
       fi
       # Will return, nothing to do.
     else
       # Restart will stop and
       # rebuild everything.
       wex site/restart
     fi;
     # We don't need to continue.
     return
  fi;

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

}
