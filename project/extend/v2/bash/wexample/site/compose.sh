#!/usr/bin/env bash

siteComposeArgs() {
  _ARGUMENTS=(
    'command c "Command to execute" true'
  )
}

siteCompose() {
  ${WEX_DIR_V3_CMD} app/compose ${@}
}
