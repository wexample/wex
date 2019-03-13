#!/usr/bin/env bash

hookExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command name" true'
  )
}

hookExec() {
  wex service/exec -c=${COMMAND}
  wex script/exec -c=${COMMAND}
}