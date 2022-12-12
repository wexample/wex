#!/usr/bin/env bash

phpConstantChangeArgs() {
 _ARGUMENTS=(
   'key k "Key" true'
   'value v "Value" true'
   'file f "File" true'
 )
}

phpConstantChange() {
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "/[ ]\{0,\}define([\'\"]"${KEY}"/s/'[^']\{0,\}'/'"${VALUE}"'/2" "${FILE}"
  rm "${FILE}${WEX_SED_I_ORIG_EXT}"
}