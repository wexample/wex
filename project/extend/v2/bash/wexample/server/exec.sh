#!/usr/bin/env bash

serverExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command" true'
  )
}

serverExec() {
  EXEC="docker exec ${WEX_PROXY_CONTAINER} /bin/bash -c"

  ${EXEC} "${COMMAND}"
}
