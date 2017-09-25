#!/usr/bin/env bash

frameworkDumpArgs() {
  _ARGUMENTS=(
    [0]='site_dir s "Root directory of site" true'
    [1]='dump_dir d "Target directory for dumps" true'
    [2]='prefix px "Prefix for final file" false'
    [3]='zip zip "Use ZIP" false'
    [4]='host H "Database host server" false'
    [5]='port P "Database host port" false'
    [6]='database db "Database name" false'
    [7]='user u "Database username" false'
    [8]='password p "Database password" false'
  )
}

frameworkDump() {

  # Get database connexion global settings.
  wex framework/settings ${SITE_DIR}

  # Get locally defined settings if not defined.
  if [[ -z "${HOST+x}" ]]; then
    HOST=${WEBSITE_SETTINGS_HOST}
  fi;

  if [[ -z "${PORT+x}" ]]; then
    PORT=${WEBSITE_SETTINGS_PORT}
  fi;

  if [[ -z "${DATABASE+x}" ]]; then
    DATABASE=${WEBSITE_SETTINGS_DATABASE}
  fi;

  if [[ -z "${USER+x}" ]]; then
    USER=${WEBSITE_SETTINGS_USERNAME}
  fi;

  if [[ -z "${PASSWORD+x}" ]]; then
    PASSWORD=${WEBSITE_SETTINGS_PASSWORD}
  fi;

  # Add -p option only if password is defined and not empty.
  # Adding empty password will prompt user instead.
  if [ "${PASSWORD}" != "" ]; then
    PASSWORD=-p"${PASSWORD}"
  fi;

  # Build dump name.
  DUMP_FULL_PATH=${DUMP_DIR}"/"${PREFIX}${DATABASE}"-"$(wex date/timeFileName)".sql"

  mysqldump -h${HOST} -P${PORT} -u${USER} ${PASSWORD} ${DATABASE} > ${DUMP_FULL_PATH}

  if [[ ${ZIP} == true ]]; then
     zip ${DUMP_FULL_PATH}".zip" ${DUMP_FULL_PATH} -q
     echo ${DUMP_FULL_PATH}".zip"
     rm -rf ${DUMP_FULL_PATH}
     return
  fi

  echo ${DUMP_FULL_PATH}
}
