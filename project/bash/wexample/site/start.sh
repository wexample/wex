#!/usr/bin/env bash

siteStartArgs() {
  _ARGUMENTS=(
    [0]='clear_cache cc "Clear all caches" false'
    [1]='containers c "Docker containers to run" false'
  )
}

siteStart() {
  if [ ! -f .env ];then
    echo "Missing .env file"
    if [ $(wex prompt/yn -q="Would you like to create a new .env file ?") == true ];then
      select SITE_ENV in ${WEX_WEXAMPLE_ENVIRONMENTS[@]};
      do
        echo 'SITE_ENV='${SITE_ENV} > .env
        break
      done
    else
      return
    fi
  fi

  # Current site is not the server itself.
  if [ $(wex service/used -s=proxy) == false ] && [ $(wex server/started) == false ];then
    local CURRENT_DIR=$(realpath ./)
    local ARGS=${WEX_ARGUMENTS}
    # Server must be started.
    wex server/start -n

    # Relaunch manually to be sure to keep given arguments
    cd ${CURRENT_DIR}
    wex site/start ${ARGS}
    return
  fi

  # Prepare files
  wex file/convertLinesToUnix -f=.env &> /dev/null
  wex file/convertLinesToUnix -f=.wex &> /dev/null

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

  wex ci/exec -c=start
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
  # Link cron files to main cron system.
  # The script are executed outside containers.
  wex cron/reload
  # Load site config
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  . .wex
  # Update host file if user has write access.
  if [ ${SITE_ENV} == "local" ] && [ $(wex file/writable -f=/etc/hosts) == true ];then
    wex hosts/updateLocal
  fi

  wex service/exec -c=start

  local DOCKER_SERVICES=''

  for CONTAINER in ${CONTAINERS[@]}
  do
    DOCKER_SERVICES+=" "${NAME}"_"${CONTAINER}
  done;

  local OPTIONS=''
  if [ "${CLEAR_CACHE}" == true ];then
    OPTIONS=' --build'
  fi

  # Use previously generated yml file.
  docker-compose -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} up -d ${DOCKER_SERVICES} ${OPTIONS}

  wex service/exec -c=started -nw

  # Rebuild / reload configurations.
  wex site/serve
  # Bash hooks.
  wex ci/exec -c=started
  # Execute server hook for global configurations.
  wex service/exec -s=proxy -sf -c=siteStarted
}
