#!/usr/bin/env bash

siteStartArgs() {
  _ARGUMENTS=(
    [0]='clear_cache cc "Clear all caches" false'
    [1]='containers c "Docker containers to run" false'
    [2]='only o "Stop all other running sites before" false'
    [3]='port p "Port for accessing site, only allowed if not already defined" false'
  )
}

siteStart() {
  # Stop other sites.
  if [ "${ONLY}" != "" ];then
    local CURRENT_DIR=$(realpath ./)
    wex sites/stop
    cd ${CURRENT_DIR}
  fi

  # Create env file.
  if [ ! -f .env ];then
    echo "Missing .env file"
    if [ $(wex prompt/yn -q="Would you like to create a new .env file ?") == true ];then
      select SITE_ENV in ${WEX_WEXAMPLE_ENVIRONMENTS[@]};
      do
        echo 'SITE_ENV='${SITE_ENV} > .env
        . .wex
        # Set SITE_NAME_INTERNAL equivalent.
        # Used by docker-compose to isolate docker services with the same name,
        # useful when running two instance of the same app (eg: dev and prod).
        echo 'COMPOSE_PROJECT_NAME='${NAME}_${SITE_ENV} >> .env
        break
      done
    else
      return
    fi
  fi

  local IS_PROXY_SERVER=$(wex service/used -s=proxy)

  # Current site is not the server itself.
  if [ ${IS_PROXY_SERVER} == false ];then
    # Start server on the given port number.
    _siteStartRetry() {
      # Cache overridden vars.
      local CURRENT_DIR=$(realpath ./)
      local ARGS=${WEX_ARGUMENTS}

      # Server must be started.
      wex server/start -n -p=${PORT}

      # Relaunch manually to be sure to keep given arguments
      cd ${CURRENT_DIR}
      wex site/start ${ARGS}
    }

    # The server is not running.
    if [ $(wex server/started) == false ];then
      _wexMessage "Starting wex server"
      _siteStartRetry
      return
    # The server is running.
    else
      # Load server config.
      . ${WEX_WEXAMPLE_DIR_PROXY_TMP}config
      # Asked port is not the same as currently used.
      if [ "${PORT}" != "" ] && [ "${PORT}" != "${WEX_SERVER_PORT_PUBLIC}" ];then
        local SITES_COUNT=$(wex sites/list -c);
        # Ignore server itself.
        ((SITES_COUNT--))

        # There is unexpected running sites.
        if (( ${SITES_COUNT} > 0 )); then
          _wexError "Unable to start apps on multiple ports" "Your wex server is running ${SITES_COUNT} app(s) on port ${WEX_SERVER_PORT_PUBLIC}" "Run the app on port ${WEX_SERVER_PORT_PUBLIC} or stop other apps"
          exit
        # Restart server with given new port number.
        else
          _wexMessage "Restarting wex server on port ${PORT}"
          wex server/stop
          _siteStartRetry
          return
        fi
      fi
    fi
  fi

  _siteStartSuccess() {
    . ${WEX_WEXAMPLE_SITE_CONFIG}
    . .wex

    # No message for proxy server.
    if [ ${NAME} == ${WEX_WEXAMPLE_PROXY_CONTAINER} ];then
      return
    fi

    echo ""
     _wexMessage "Your site \"${NAME}\" is up in \"${SITE_ENV}\" environment" "You can access to it on these urls : "

    local DOMAINS=$(wex site/domains)
    for DOMAIN in ${DOMAINS[@]}
    do
      echo "      > http://"${DOMAIN}:${WEX_SERVER_PORT_PUBLIC}
    done;

    if [ ${SITE_ENV} == "local" ];then

      echo ""
      echo "      You are in a local environment, so you might want"
      echo "      to run now some of this dev methods :"
      echo "        wex watcher/start"
      echo "        wex site/serve"
      echo "        wex site/go"
      echo ""

    fi
  }

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
     _siteStartSuccess
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
  echo -e "\n"${DIR_SITE} | sudo tee -a ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites > /dev/null

  # Rebuild hosts
  wex hosts/update
  # Link cron files to main cron system.
  # The script are executed outside containers.
  # TODO rm as we are now able to run internal crons in containers.
  # wex cron/reload
  # Load site config
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  . .wex
  # Update host file if user has write access.
  if [ ${SITE_ENV} == "local" ] && [ $(wex file/writable -f=/etc/hosts) == true ];then
    wex hosts/updateLocal
  fi

  wex hook/exec -c=start

  local DOCKER_SERVICES=''

  for CONTAINER in ${CONTAINERS[@]}
  do
    # TODO We should build the container name including the ENV variable
    # to allows to run the same site in several environments.
    DOCKER_SERVICES+=" "${NAME}"_"${CONTAINER}
  done;

  local OPTIONS=''
  if [ "${CLEAR_CACHE}" == true ];then
    OPTIONS=' --build'
  fi

  # Use previously generated yml file.
  docker-compose -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} up -d ${DOCKER_SERVICES} ${OPTIONS}

  wex site/perms
  wex service/exec -c=started -nw
  # Rebuild / reload configurations.
  wex site/serve
  # Bash hooks TODO remove ci/exec, use script/exec instead
  wex ci/exec -c=started
  wex hook/exec -c=siteStarted
  # Execute server hook for global configurations.
  wex service/exec -s=proxy -sf -c=siteStarted

  _siteStartSuccess
}
