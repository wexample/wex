#!/usr/bin/env bash

mailCommandArgs() {
  _ARGUMENTS=(
    [0]='group g "Group" true'
    [1]='action a "Action" true'
    [2]='data d "Command arguments" false'
  )
}

# From : https://raw.githubusercontent.com/tomav/docker-mailserver/master/setup.sh
# Wiki : https://github.com/tomav/docker-mailserver/wiki/Setup-docker-mailserver-using-the-script-setup.sh
mailCommand() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  # Create global config.
  CONTAINER_NAME=${SITE_NAME}_mailserver

  bash ${BASH_SOURCE%/*}/_setup.sh ${GROUP} ${ACTION} "${DATA}"
}