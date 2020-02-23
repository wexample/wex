#!/usr/bin/env bash

siteStartedArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" false'
    [1]='ignore_containers ic "Do not check if containers are also started" false'
  )
}

siteStarted() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  if [ $(wex server/started) == false ];then
    echo false
    return
  fi

  # Config file exists
  if [ -f ${DIR_SITE}${WEX_WEXAMPLE_SITE_CONFIG} ];then
    # Load config
    . ${DIR_SITE}${WEX_WEXAMPLE_SITE_CONFIG}
    # Started && into server
    if [ ${STARTED} == true ] && [ $(wex file/lineExists -f=${WEX_WEXAMPLE_DIR_PROXY_TMP}sites -l=$(realpath ${DIR_SITE})"/") == true ];then
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
  echo false
}
