#!/usr/bin/env bash

siteDeleteArgs() {
  _ARGUMENTS=(
    [0]='site s "Site name" true'
  )
}

siteDelete() {
  # We store all standalone websites in the default sites location.
  local SITE_PATH=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${SITE}/

  if [ -d ${SITE_PATH} ] && [ -f ${SITE_PATH}.wex ];then
    # Go to new temporary website.
    cd ${SITE_PATH}
    # Stop
    wex app/stop
    # Remove
    rm -rf ${SITE_PATH}
  fi
}