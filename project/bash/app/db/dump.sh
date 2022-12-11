#!/usr/bin/env bash

dbDumpArgs() {
  _ARGUMENTS=(
    'site_name n "Website name (internal usage for container execution)" false'
    'site_env se "Website environment (internal usage for container execution)" false'
    'latest l "Save latest copy file" false'
    'pull p "Pull remote dump locally" false'
    'tag t "Tag name append as a suffix" false'
    'filename f "Dump file name" false'
  )
}

dbDump() {
  # We expect to be into site root folder.

  . ${WEX_APP_CONFIG}

  # Filename is specified
  if [ "${FILENAME}" != "" ];then
    local DUMP_FILE_NAME=${FILENAME}
  else
    # Build dump name.
    local DUMP_FILE_NAME
    DUMP_FILE_NAME=${SITE_ENV}'-'${MYSQL_DB_NAME}"-"$(wex date/timeFileName)
    if [ "${TAG}" != "" ];then
      DUMP_FILE_NAME+="-"${TAG}
    fi
    DUMP_FILE_NAME+=".sql"
  fi

  local DUMP_FULL_PATH="./mysql/dumps/"${DUMP_FILE_NAME}

  # Copy mysql configuration.
  docker cp ./tmp/mysql.cnf ${SITE_NAME_INTERNAL}_${DB_CONTAINER}:./tmp/mysql.cnf
  docker exec ${SITE_NAME_INTERNAL}_${DB_CONTAINER} /bin/bash -c "mysqldump $(wex mysql/loginCommand) > /var/www/dumps/${DUMP_FILE_NAME}"

  if [ "${ZIP}" = true ]; then
    zip ${DUMP_FULL_PATH}".zip" ${DUMP_FULL_PATH} -q -j
    # No more usage of source files.
    rm -f ${DUMP_FULL_PATH}
  fi

  # Echo name without zip extension
  echo ${DUMP_FULL_PATH}
}
