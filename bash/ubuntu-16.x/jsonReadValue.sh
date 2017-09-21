#!/usr/bin/env bash

jsonReadValue() {
  FILE=${1}
  VALUE=${2}

  # Try with python
  if [[ $(wexample packageExists python) == true ]]; then
   cat ${FILE} | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["'${VALUE}'"]'
  # Try with PHP
  elif [[ $(wexample packageExists php) == true ]]; then
    php -r 'echo (json_decode(file_get_contents("'${FILE}'"), JSON_OBJECT_AS_ARRAY))["'${VALUE}'"];'
  fi
}
