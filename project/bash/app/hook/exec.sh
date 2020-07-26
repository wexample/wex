#!/usr/bin/env bash

hookExecArgs() {
  _ARGUMENTS=(
    'command c "Command name" true'
  )
}

hookExec() {
  wex service/exec -c=${COMMAND}
  wex script/exec -c=${COMMAND}
}