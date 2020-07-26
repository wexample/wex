#!/usr/bin/env bash

configSetValueArgs() {
 _ARGUMENTS=(
   'key k "Target key to change" true'
   # As we edit local config file, we use = as default separator
   'separator s "Separator like space or equal sign, default space" false "="'
   # In app env, use app config file as default value.
   'file f "File" false '${WEX_WEXAMPLE_APP_FILE_CONFIG}
   'value v "New value" true'
 )
}

configSetValue() {
  wex default::config/setValue "${@}" -f=${FILE} -s=${SEPARATOR} -i
}
