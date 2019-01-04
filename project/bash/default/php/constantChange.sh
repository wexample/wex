#!/usr/bin/env bash

phpConstantChangeArgs() {
 _ARGUMENTS=(
   [0]='key k "Key" true'
   [1]='value v "Value" true'
   [2]='file f "File" true'
 )
}

phpConstantChange() {
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "/[ ]\{0,\}define([\'\"]"${KEY}"/s/'[^']\{0,\}'/'"${VALUE}"'/2" ${FILE}
  rm ${FILE}"${WEX_SED_I_ORIG_EXT}"
}