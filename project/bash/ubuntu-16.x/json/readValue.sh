#!/usr/bin/env bash

jsonReadValueArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='key k "Key to read" true'
 )
}

jsonReadValue() {
  # Handle OS specific path
  FILE=$(wex path/safe -p="${FILE}")
  # Double slashes for windows like paths.
  FILE=$(echo "${FILE}" | sed 's/\\/\\\\/g')
  # Allow regex search patterns
  sed -n "s/^[ ]*\"${KEY}\":[ ]*\"\(.*\)\",*/\1/p" ${FILE}
}
