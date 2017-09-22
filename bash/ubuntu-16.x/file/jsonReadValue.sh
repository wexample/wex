#!/usr/bin/env bash

jsonReadValueArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='key k "Key to read" true'
 )
}

jsonReadValue() {
  # Try with python
  if [[ $(wexample packageExists python) == true ]]; then
   cat ${FILE} | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["'${KEY}'"]'
  # Try with PHP
  elif [[ $(wexample packageExists php) == true ]]; then
    php -r 'echo (json_decode(file_get_contents("'${FILE}'"), JSON_OBJECT_AS_ARRAY))["'${KEY}'"];'
  fi
}
