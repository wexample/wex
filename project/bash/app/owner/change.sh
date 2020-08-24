#!/usr/bin/env bash

ownerChangeArgs() {
  _DESCRIPTION="Change owner of a file or dir inside the main container if exists"
  _ARGUMENTS=(
    'path_dest p "Path of file or dir to change owner" true'
    'owner o "Owner to set" true'
    'recursive r "Recursive" false'
  )
}

ownerChange() {
  if [ "${RECURSIVE}" = "true" ];then
    RECURSIVE="-R"
  fi
  wex app/exec -su -c="([ -d ${PATH_DEST} ] || [ -f ${PATH_DEST} ]) && chown ${RECURSIVE} ${OWNER} ${PATH_DEST}"
}
