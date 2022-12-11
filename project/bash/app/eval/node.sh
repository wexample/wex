#!/usr/bin/env bash

evalNodeArgs() {
  _ARGUMENTS=(
    [0]='command c "Command to eval" true'
  )
}

evalNode() {
  local CONTAINER=$(docker run -d -ti wexample/node)
  docker exec ${CONTAINER} node -e "${COMMAND}"
  docker stop ${CONTAINER} &> /dev/null
  docker rm ${CONTAINER} &> /dev/null
}