#!/usr/bin/env bash

sslEnableArgs() {
  _ARGUMENTS=(
    [0]='env e "Environment" true'
  )
}

sslEnable() {
  # Set services configuration.
  wex service/exec -c=sslEnable -d=${ENV}
  # Enable SSL in current env.
  wex config/uncomment -k="- VIRTUAL_PROTO" -f=docker/docker-compose.${ENV}.yml -s="="
}