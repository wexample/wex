#!/usr/bin/env bash

configSetValueArgs() {
 _ARGUMENTS=(
   'key k "Target key to change" true'
   # As we edit local config file, we use = as default separator
   'separator s "Separator like space or equal sign, default space" false "="'
   # In app env, use app config file as default value.
   'file f "File" false '${WEX_WEXAMPLE_APP_FILE_CONFIG}
   'ignore_duplicates i "Do not check if variable exists or is commented" false false'
   'value v "New value" true'
 )
}

configSetValue() {
  wex default::config/setValue -k="${KEY}" -v="${VALUE}" -f="${FILE}" -s="${SEPARATOR}" -i="${IGNORE_DUPLICATES}"
}
