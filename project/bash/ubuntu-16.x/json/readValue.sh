#!/usr/bin/env bash

fileJsonReadValueArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='key k "Key to read" true'
 )
}

fileJsonReadValue() {
  # Handle OS specific path
  FILE=$(wex path/safe -p="${FILE}")
  # Double slashes for windows like paths.
  FILE=$(echo "${FILE}" | sed 's/\\/\\\\/g')
  # Try with python
  if [[ $(wex package/exists -n=python) == true ]]; then
    cat ${FILE} | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["'${KEY}'"]'
  # Try with PHP
  elif [[ $(wex package/exists -n=php) == true ]]; then
    php -r 'echo (json_decode(file_get_contents("'${FILE}'"), JSON_OBJECT_AS_ARRAY))["'${KEY}'"];'
  fi
}
