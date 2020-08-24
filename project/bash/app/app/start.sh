#!/usr/bin/env bash

appStartArgs() {
  _ARGUMENTS=(
    'clear_cache cc "Clear all caches" false'
    'only o "Stop all other running sites before" false'
    'port p "Port for accessing site, only allowed if not already defined" false'
  )
}

appStart() {
  # Stop other sites.
  if [ "${ONLY}" != "" ];then
    local CURRENT_DIR
    CURRENT_DIR=$(realpath ./)
    wex apps/stop
    cd ${CURRENT_DIR}
  fi

  # Create env file.
  if [ ! -f .env ];then
    if [ "$(wex prompt/yn -q="Missing .env file, would you like to create it ?")" = true ];then
      local ALLOWED_ENV="${WEX_WEXAMPLE_ENVIRONMENTS[*]}";
      ALLOWED_ENV=$(wex array/join -a="${ALLOWED_ENV}" -s=",")

      # Ask user
      wex prompt/choice -c="${ALLOWED_ENV}" -q="Choose env name"

      SITE_ENV=$(wex prompt/choiceGetValue)

      echo "SITE_ENV=${SITE_ENV}" > .env
    else
      _wexLog "Starting aborted"
      return
    fi
  fi

  local IS_PROXY_SERVER
  IS_PROXY_SERVER=$(wex service/used -s=proxy)

  # Current site is not the server itself.
  if [ "${IS_PROXY_SERVER}" = false ];then
    _wexLog "Check proxy server"

    # The server is not running.
    if [ "$(wex proxy/started)" = false ];then
      _wexLog "Starting wex server"
      _appStartRetry
      return
    # The server is running.
    else
      # Load server config.
      . ${WEX_DIR_PROXY_TMP}config
      # Asked port is not the same as currently used.
      if [ "${PORT}" != "" ] && [ "${PORT}" != "${WEX_SERVER_PORT_PUBLIC}" ];then
        local SITES_COUNT=$(wex apps/list -c);
        # Ignore server itself.
        ((SITES_COUNT--))

        # There is unexpected running sites.
        if (( ${SITES_COUNT} > 0 )); then
          _wexError "Unable to start apps on multiple ports" "Your wex server is running ${SITES_COUNT} app(s) on port ${WEX_SERVER_PORT_PUBLIC}" "Run the app on port ${WEX_SERVER_PORT_PUBLIC} or stop other apps"
          exit
        # Restart server with given new port number.
        else
          _wexMessage "Restarting wex server on port ${PORT}"
          wex proxy/stop
          _appStartRetry
          return
        fi
      fi
    fi
  fi

  # Prepare files
  wex file/convertLinesToUnix -f=.env &> /dev/null
  wex file/convertLinesToUnix -f=.wex &> /dev/null

  # Check if app is already started,
  # ignoring if containers runs or not.
  if [ "$(wex app/started -ic)" = true ];then
     # All containers exists
     # but one is not started.
     if [ "$(wex containers/exists -a)" = true ];then
       if [ "$(wex containers/started -a)" != true ];then
         _wexLog "Start all app containers"
         # Start all containers
         wex containers/start
       fi
       # Will return, nothing to do.
     else
       _wexLog "Restart app as some conainer is missing"
       # Restart will stop and
       # rebuild everything.
       wex app/restart
     fi;
     _appStartSuccess
     # We don't need to continue.
     return
  fi;

  # Load site config
  . .wex
  _wexMessage "Starting app ${WEX_COLOR_YELLOW}${NAME}${WEX_COLOR_RESET}"

  # Write new config,
  # it will also export config variables
  wex config/write -s

  . "${WEX_APP_CONFIG}"

  # Add site
  local DIR_SITE=$(realpath ./)"/"
  # Reload sites will clean up list.
  wex apps/update
  # Add new site.
  echo -e "\n"${DIR_SITE} | sudo tee -a ${WEX_PROXY_APPS_REGISTRY} > /dev/null

  # Rebuild hosts
  wex hosts/update

  # Update host file if user has write access.
  if [ ${SITE_ENV} = "local" ] && [ "$(wex file/writable -f=/etc/hosts)" = true ];then
    wex hosts/updateLocal
  fi

  wex hook/exec -c=appStart

  local DOCKER_SERVICES=''
  local CONTAINER_NAME=""

  for CONTAINER in ${CONTAINERS[@]}
  do
    CONTAINER_NAME=" ${NAME}_${CONTAINER}"
    # TODO We should build the container name including the ENV variable (testing...)
    # to allows to run the same site in several environments.
    DOCKER_SERVICES+=${CONTAINER_NAME}
    _wexLog "Use container ${CONTAINER_NAME}"
  done;

  local OPTIONS=''
  if [ "${CLEAR_CACHE}" = true ];then
    OPTIONS=' --build'
  fi

  # Use previously generated yml file.
  docker-compose -f "${WEX_APP_COMPOSE_BUILD_YML}" up -d ${DOCKER_SERVICES} ${OPTIONS}

  wex app/perms

  # Rebuild / reload configurations.
  wex app/serve
  # Services hooks
  wex hook/exec -c=appStarted

  # Execute server hook for global configurations.
  wex service/exec -s=proxy -sf -c=appStarted

  _appStartSuccess
}

# Start server on the given port number.
_appStartRetry() {
  local ARGS
  local CURRENT_DIR
  # Cache overridden vars.
  ARGS=${WEX_ARGUMENTS}
  CURRENT_DIR=$(realpath ./)

  # Server must be started.
  wex proxy/start -n -p="${PORT}"

  # Something prevent proxy server to start
  if [ "$(wex var/get -n=PROXY_ERROR)" != false ];then
    return
  fi

  # Relaunch manually to be sure to keep given arguments
  cd "${CURRENT_DIR}" || return
  wex app/start "${ARGS}"
}

_appStartSuccess() {
    . ${WEX_APP_CONFIG}
    . .wex

    # No message for proxy server.
    if [ "${NAME}" = "${WEX_PROXY_CONTAINER}" ];then
      return
    fi

    echo ""
     _wexMessage "Your site \"${NAME}\" is up in \"${SITE_ENV}\" environment" "You can access to it on these urls : "

    local DOMAINS=$(wex app/domains)
    for DOMAIN in ${DOMAINS[@]}
    do
      echo "      > http://"${DOMAIN}:${WEX_SERVER_PORT_PUBLIC}
    done;

    if [ "${SITE_ENV}" = "local" ];then
      echo ""
      echo "      You are in a local environment, so you might want"
      echo "      to run now some of this dev methods :"
      echo "        wex watcher/start"
      echo "        wex app/serve"
      echo "        wex app/go"
      echo ""
    fi
  }