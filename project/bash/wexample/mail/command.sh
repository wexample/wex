#!/usr/bin/env bash

mailCommandArgs() {
  _ARGUMENTS=(
    [0]='group g "Group" true'
    [1]='action a "Action" true'
    [2]='data d "Command arguments" true'
  )
}

mailCommand() {
  # From: https://raw.githubusercontent.com/tomav/docker-mailserver/master/setup.sh
  bash ${BASH_SOURCE%/*}/_setup.sh ${GROUP} ${ACTION} "${DATA}"
}