#!/usr/bin/env bash

mailComposeArgs() {
  _ARGUMENTS=(
    [0]='command c "Command to execute" true'
  )
}

mailCompose() {
  # Create temp dit if not exists.

  docker-compose -f ${WEX_DIR_ROOT}docker/containers/mail/docker-compose.yml ${COMMAND}
}
