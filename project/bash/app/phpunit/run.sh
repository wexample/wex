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

  local TMP_DIR=/var/www/html/tmp/

  mkdir -p ./tmp/phpunit

  # TODO Not working with older versions but should be tested on recent installs :
  # --log-junit ${TMP_DIR}phpunit-report.xml --coverage-html ${TMP_DIR}phpunit
  wex app/exec -l --non_interactive -c="./vendor/bin/phpunit ${FILTER} "
}