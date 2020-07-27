#!/usr/bin/env bash

siteGoArgs() {
  _ARGUMENTS=(
    [0]='container_name c "Container name suffix like site_name_suffix. Default is web" false'
  )
}

siteGo() {
  ${WEX_DIR_V3_CMD} app/go ${@}
}
