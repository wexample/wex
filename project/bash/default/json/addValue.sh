#!/usr/bin/env bash

jsonAddValueArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='key k "Key to read" true'
   [2]='value v "Value to add" true'
 )
}

jsonAddValue() {
  # Handle OS specific path
  FILE=$(wex path/safe -p="${FILE}")
  # Double slashes for windows like paths.
  FILE=$(echo "${FILE}" | sed 's/\\/\\\\/g')
  # Allow regex patterns
  # This method is not clean, but it works with json/readValue.
  sed -i '$s/}/,\n\ \ "'${KEY}'":"'${VALUE}'"\n}/' ${FILE}
}
