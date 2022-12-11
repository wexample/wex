#!/usr/bin/env bash

dbRestoreArgs() {
  _ARGUMENTS=(
    'dump d "Dump file to import, in the dumps folder only, asked if missing" false'
  )
}

dbRestore() {
  # We expect to be into site root folder.

  . ${WEX_APP_CONFIG}

  if [ -z ${DUMP+x} ];then
    # Ask user to choose a file.
    wex db/dumpChoiceList
    # Prompt does not work in the exec terminal.
    DUMP=$(wex prompt/choiceGetValue)
  fi

  local DUMP_HOST_PATH=./mysql/dumps/${DUMP}
  local LOGIN=$(wex mysql/loginCommand)

  _wexLog "Recreating database ${MYSQL_DB_NAME}"
  wex db/exec -c="DROP DATABASE IF EXISTS ${MYSQL_DB_NAME}; CREATE DATABASE ${MYSQL_DB_NAME};"

  # If file is a zip, unzip it.
  if [[ ${DUMP_HOST_PATH} =~ \.zip$ ]];then
     local DUMP_FILE_ZIP_BASE=${DUMP_HOST_PATH}
     local DUMP=$(basename  "${DUMP_HOST_PATH%.*}")
     local DUMP_DIR=$(dirname  "${DUMP_HOST_PATH%.*}")
     DUMP_HOST_PATH=${DUMP_DIR}"/"${DUMP}
     unzip -oq ${DUMP_FILE_ZIP_BASE} -d ${DUMP_DIR}
  fi;

  # Copy mysql configuration.
  docker cp ./tmp/mysql.cnf ${SITE_NAME_INTERNAL}_${DB_CONTAINER}:./tmp/mysql.cnf

  _wexLog "Importing dump ${DUMP}"
  local LOGIN=$(wex mysql/loginCommand)
  docker exec ${SITE_NAME_INTERNAL}_${DB_CONTAINER} /bin/bash -c "mysql ${LOGIN} < /var/www/dumps/${DUMP}"

  # If file was a zip, .sql file was temporary.
  if [[ ${DUMP_FILE_ZIP_BASE} =~ \.zip$ ]];then
    rm ${DUMP_HOST_PATH}
  fi
}
