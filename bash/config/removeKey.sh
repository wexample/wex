#!/usr/bin/env bash

configRemoveKeyArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'target_key k "Target key to get (line beginning by ... regex)" true'
    'file f "File" true'
    'separator s "Separator like space or equal sign, default space" false " "'
  )
}

configRemoveKey() {
  sed -i"${WEX_SED_I_ORIG_EXT}" -e '/^[ ]\{0,\}'"${TARGET_KEY}"'/d' "${FILE}"
  rm "${FILE}${WEX_SED_I_ORIG_EXT}"
}
