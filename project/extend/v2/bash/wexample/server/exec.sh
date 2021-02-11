#!/usr/bin/env bash

serverExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command" true'
  )
}

serverExec() {
  EXEC="docker exec ${WEX_WEXAMPLE_PROXY_CONTAINER}_prod /bin/bash -c"

  ${EXEC} "${COMMAND}"
}
