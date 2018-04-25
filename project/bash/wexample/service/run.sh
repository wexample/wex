#!/usr/bin/env bash

serviceRunArgs() {
  _ARGUMENTS=(
    [0]='service s "Service" true'
  )
}

# Start stand alon service without site folder.
# This first version does not care about environments.
serviceRun() {
  local SERVICE_PATH=${WEX_WEXAMPLE_DIR_SERVICES_STANDALONE}${SERVICE}/
  local SITE_NAME=${SERVICE}Standalone

  # Create folders.
  mkdir -p ${SERVICE_PATH}

  # Go to new temporary website.
  cd ${SERVICE_PATH}

  if [ $(wex site/started) == false ];then
    if [ $(wex site/isset) == false ];then
      # Create site with only one service
      wex site/init -n=${SITE_NAME} -s=${SERVICE} --git=false
    fi

    wex site/start
  fi
}