#!/usr/bin/env bash

fileJsonReadValueArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='key k "Key to read" true'
   [2]='separator s "Used separator by string" false'
 )
}

fileJsonReadValue() {
  if [ -z "${SEPARATOR+x}" ]; then
    SEPARATOR=
  fi;

  # Try with PHP
  if [[ $(wex package/exists -n=php) == true ]]; then
  # TODO ...
  php ${WEX_DIR_ROOT}"php/fileJsonReadValue.php" ${FILE} ${KEY} {$SEPARATOR}
#    echo $(php ${WEX_DIR_ROOT}"php/fileJsonReadValue.php" "$@");
    #php -r 'echo (json_decode(file_get_contents("'${FILE}'"), JSON_OBJECT_AS_ARRAY))["'${KEY}'"];'
  fi
}
