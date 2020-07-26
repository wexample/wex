#!/usr/bin/env bash

portsOpenedArgs() {
  _ARGUMENTS=(
    [0]='separator s "Separator" false'
  )
}

portsOpened() {
  ${WEX_DIR_V3_CMD} app::ports/opened -s=${SEPARATOR}
}
