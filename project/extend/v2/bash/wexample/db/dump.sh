#!/usr/bin/env bash

dbDumpArgs() {
  _ARGUMENTS=(
    [0]='site_name n "Website name (internal usage for container execution)" false'
    [1]='site_env se "Website environment (internal usage for container execution)" false'
    [2]='latest l "Save latest copy file" false'
    [3]='environment e "Remote environment name" false'
    [4]='pull p "Pull remote dump locally" false'
    [5]='tag t "Tag name append as a suffix" false'
    [6]='filename f "Dump file name" false'
  )
}

dbDump() {
  # We expect to be into site root folder.

  # Remote dump.
  if [ ! -z ${ENVIRONMENT+x} ];then
    # Dump
    wex wexample::remote/exec -e=${ENVIRONMENT} -s="wex db/dump"
    return
  fi

  . ${WEX_APP_CONFIG}

  # Filename is specified
  if [ "${FILENAME}" != "" ];then
    local DUMP_FILE_NAME=${FILENAME}
  else
    # Build dump name.
    local DUMP_FILE_NAME=${SITE_ENV}'-'${MYSQL_DB_NAME}"-"$(wex date/timeFileName)
    if [ "${TAG}" != "" ];then
      DUMP_FILE_NAME+="-"${TAG}
    fi
    DUMP_FILE_NAME+=".sql"
  fi

  local DUMP_FULL_PATH="./mysql/dumps/"${DUMP_FILE_NAME}

  # Copy mysql configuration.
  docker cp ./tmp/mysql.cnf ${SITE_NAME_INTERNAL}_mysql:./tmp/mysql.cnf
  docker exec ${SITE_NAME_INTERNAL}_mysql /bin/bash -c "mysqldump $(wex mysql/loginCommand) > /var/www/dumps/${DUMP_FILE_NAME}"

  if [[ ${ZIP} == true ]]; then
    zip ${DUMP_FULL_PATH}".zip" ${DUMP_FULL_PATH} -q -j
  fi

  local LATEST_DUMP_FILE="./mysql/dumps/"${SITE_ENV}"-"${SITE_NAME}"-latest.sql"
  # Clone to latest
  cp ${DUMP_FULL_PATH} ${LATEST_DUMP_FILE}
  # Create zip.
  zip ${LATEST_DUMP_FILE}".zip" ${LATEST_DUMP_FILE} -q -j
  # No more usage of source files.
  rm -f ${LATEST_DUMP_FILE}

  if [[ ${ZIP} == true ]]; then
    # No more usage of source files.
    rm -f ${DUMP_FULL_PATH}
  fi
  # Echo name without zip extension
  echo ${DUMP_FULL_PATH}

}
