#!/usr/bin/env bash

configWriteArgs() {
  _ARGUMENTS=(
    [0]='started s "Set the site is started or not" false'
    [1]='no_recreate nr "No recreate if files exists" false'
  )
}

configWrite() {
  ${WEX_DIR_V3_CMD} config/write "${@}"
}
