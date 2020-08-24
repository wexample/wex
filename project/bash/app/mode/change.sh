#!/usr/bin/env bash

modeChangeArgs() {
  _DESCRIPTION="Change mode of a file or dir inside the main container if exists"
  _ARGUMENTS=(
    'path_dest p "Path of file or dir to change mode" true'
    'mode m "Mode to set" true'
  )
}

modeChange() {
  if [ "${RECURSIVE}" = "true" ];then
    RECURSIVE="-r"
  fi
  wex app/exec -su -c="([ -d ${PATH_DEST} ] || [ -f ${PATH_DEST} ]) && chmod ${RECURSIVE} ${MODE} ${PATH_DEST}"
}
