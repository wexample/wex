#!/usr/bin/env bash

fileLineRemoveArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='line l "New line" true'
 )
}

fileLineRemove() {
  LINE=$(echo "${LINE}" | sed 's/\//\\\//g')
  sed -i"${WEX_SED_I_ORIG_EXT}" -e '/'${LINE}'/d' ${FILE}
  rm ${FILE}"${WEX_SED_I_ORIG_EXT}"
}