#!/usr/bin/env bash

dbRestoreArgs() {
  _ARGUMENTS=(
  [0]='dump d "Dump file to import, in the dumps folder only, asked if missing" false'
  [1]='environment e "Remote environment name" false'
  )
}

dbRestore() {
  # We expect to be into site root folder.

  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Remote restoration.
  if [ ! -z ${ENVIRONMENT+x} ];then
    # Restore
    wex wexample::remote/exec -e=${ENVIRONMENT} -s="wex db/restore -d=${DUMP}"
    return
  fi;

  if [ -z ${DUMP+x} ];then
    # Ask user to choose a file.
    wex db/dumpChooseList
    # Prompt does not work in the exec terminal.
    DUMP=$(wex db/dumpChoose)
  fi

  local DUMP_HOST_PATH=./mysql/dumps/${DUMP}
  local LOGIN=$(wex mysql/loginCommand)

  wex db/exec -c="DROP DATABASE IF EXISTS ${SITE_DB_NAME}; CREATE DATABASE ${SITE_DB_NAME};"

  # If file is a zip, unzip it.
  if [[ ${DUMP_HOST_PATH} =~ \.zip$ ]];then
     local DUMP_FILE_ZIP_BASE=${DUMP_HOST_PATH}
     local DUMP=$(basename  "${DUMP_HOST_PATH%.*}")
     local DUMP_DIR=$(dirname  "${DUMP_HOST_PATH%.*}")
     DUMP_HOST_PATH=${DUMP_DIR}"/"${DUMP}
     unzip -oq ${DUMP_FILE_ZIP_BASE} -d ${DUMP_DIR}
  fi;

  # Copy mysql configuration.
  docker cp ./tmp/mysql.cnf ${SITE_NAME}_mysql:./tmp/mysql.cnf

  local LOGIN=$(wex mysql/loginCommand)
  docker exec ${SITE_NAME}_mysql /bin/bash -c "mysql ${LOGIN} < /var/www/dumps/${DUMP}"

  # If file was a zip, .sql file was temporary.
  if [[ ${DUMP_FILE_ZIP_BASE} =~ \.zip$ ]];then
    rm ${DUMP_HOST_PATH}
  fi
}
