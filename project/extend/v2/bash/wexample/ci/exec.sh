#!/usr/bin/env bash

# May be replaced by script/exec.

ciExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command name, ex : "command" to execute ci/command.sh" true'
  )
}

ciExec() {
  local FILE_PATH=ci/${COMMAND}.sh
  # Execute custom script for site.
  if [ -f ${FILE_PATH} ];then
    . ${FILE_PATH}
  fi
}
