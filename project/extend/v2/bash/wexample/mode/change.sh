#!/usr/bin/env bash

modeChangeArgs() {
  _DESCRIPTION="Change mode of a file or dir inside the main container if exists"
  _ARGUMENTS=(
    [0]='path_dest p "Path of file or dir to change mode" true'
    [1]='mode m "Mode to set" true'
  )
}

modeChange() {
  if [ "${RECURSIVE}" == "true" ];then
    RECURSIVE="-r"
  fi
  wex app/exec -c="([ -d ${PATH_DEST} ] || [ -f ${PATH_DEST} ]) && chmod ${RECURSIVE} ${MODE} ${PATH_DEST}"
}
