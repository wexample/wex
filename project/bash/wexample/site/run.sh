#!/usr/bin/env bash

siteRunArgs() {
  _ARGUMENTS=(
    [0]='site_name n "Service" true'
    [1]='environment e "Environment" true'
    [2]='services s "Services" true'
    [3]='clear_content cc "Delete service files if exists" false'
  )
}

# Start a standalone site without version control.
siteRun() {
  # We store all standalone websites in the default sites location.
  local SITE_PATH=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${SITE_NAME}/

  if [ "${CLEAR_CONTENT}" == true ];then
    wex wexample::service/remove -s=${SITE_NAME}
  fi

  # Create folders.
  mkdir -p ${SITE_PATH}

  # Go to new temporary website.
  cd ${SITE_PATH}

  if [ $(wex site/started) == false ];then
    # Init only if not exists.
    if [ $(wex site/isset) == false ];then
      # Create site with only one service
      wex site/init -n=${SITE_NAME} -s=${SERVICES} -e=${ENVIRONMENT} --git=false
    fi

    wex site/start
  fi
}