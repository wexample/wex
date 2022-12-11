#!/usr/bin/env bash

cliExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command to execute" false'
  )
}

# This methods should handle all "cli" tools for current website,
# it have to be able to detect site framework and use proper cli tool
cliExec() {
  local CLI=$(wex hook/exec -c=cliExec);
  # Pipe command to cli call.
  wex app/exec -l -c="${CLI} ${COMMAND}"
}