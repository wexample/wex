#!/usr/bin/env bash

fileLineRemoveArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Remove a line from a file."
  _ARGUMENTS=(
    'file f "File" true'
    'line l "New line" true'
  )
}

fileLineRemove() {
  LINE=$(printf '%s\n' "${LINE}" | sed 's/[[\.*^$/]/\\&/g')
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "/${LINE}/d" ${FILE}
  rm "${FILE}${WEX_SED_I_ORIG_EXT}"
}
