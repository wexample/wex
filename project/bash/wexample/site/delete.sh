#!/usr/bin/env bash

siteDeleteArgs() {
  _ARGUMENTS=(
    [0]='site s "Site name" true'
  )
}

siteDelete() {
  # We store all standalone websites in the default sites location.
  local SERVICE_PATH=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${SERVICE}/

  if [ -d ${SERVICE_PATH} ] && [ -f ${SERVICE_PATH}.wex ];then
    # Go to new temporary website.
    cd ${SERVICE_PATH}
    # Stop
    wex site/stop
    # Remove
    rm -rf ${SERVICE_PATH}
  fi
}