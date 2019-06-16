#!/usr/bin/env bash

phpunitRunArgs() {
  _ARGUMENTS=(
    [0]='file f "File name" false'
    [1]='class c "Class name" false'
    [2]='method m "Method name" false'
  )
}

phpunitRun() {
  local FILTER=""
  if [ "${FILE}" != "" ];then
    if [ "${CLASS}" == "" ];then
      local CLASS=$(basename ${FILE})
      CLASS="${CLASS%.*}"
    fi
    # Adjust file path to site root,
    # allows user to use auto completion when calling method.
    local FILTER="--filter ${METHOD} ${CLASS} ../${FILE}"
  fi

  wex site/exec -c="cd /var/www/html/project && ./vendor/bin/phpunit ${FILTER}"
}