#!/usr/bin/env bash

serviceUsedArgs() {
  _ARGUMENTS=(
    [0]='service s "Service to install" true',
  )
}

serviceUsed() {
  local SERVICES=($(wex service/list))
  wex array/contains -a="${SERVICES}" -i=${SERVICE}
}