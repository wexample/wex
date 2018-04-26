#!/usr/bin/env bash

serviceRemoveArgs() {
  _ARGUMENTS=(
    [0]='service s "Service" true'
  )
}

serviceRemove() {
  local SERVICE_PATH=${WEX_WEXAMPLE_DIR_SERVICES_STANDALONE}${SERVICE}/

  if [ -d ${SERVICE_PATH} ] && [ -f ${SERVICE_PATH}.wex ];then
    # Go to new temporary website.
    cd ${SERVICE_PATH}
    # Stop
    wex site/stop
    # Remove
    rm -rf ${SERVICE_PATH}
  fi
}