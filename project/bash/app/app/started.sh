#!/usr/bin/env bash

appStartedArgs() {
  _ARGUMENTS=(
    'dir_site d "Root site directory" false'
    'ignore_containers ic "Do not check if containers are also started" false'
  )
}

appStarted() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Config file exists
  if [ -f ${DIR_SITE}${WEX_APP_CONFIG} ];then
    # Load config
    . ${DIR_SITE}${WEX_APP_CONFIG}
    # Started && into server
    if [ "${STARTED}" = true ] && [ "$(wex file/lineExists -f="${WEX_PROXY_APPS_REGISTRY}" -l="$(realpath ${DIR_SITE})/")" = true ];then
      # Check if containers are started if expected.
      if [ "${IGNORE_CONTAINERS}" != true ];then
        # At least on container should run.
        # Return true or false.
        wex containers/started
        return
      fi
      # Do not check containers.
      echo true
      return
    fi
  fi

  # Check if proxy runs at end, for performance.
  if [ "$(wex proxy/started)" = false ];then
    echo false
    return
  fi

  echo false
}
