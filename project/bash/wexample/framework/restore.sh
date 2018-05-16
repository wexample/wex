#!/usr/bin/env bash

frameworkRestoreArgs() {
  _ARGUMENTS=(
    [0]='dump_file f "Target directory for dumps" true'
    [1]='zip zip "Use ZIP" false'
    [2]='host h "Database host server" false'
    [3]='port P "Database host port" false'
    [4]='database db "Database name" false'
    [5]='user u "Database username" false'
  )
}

frameworkRestore() {
  wex db/exec -c="DROP DATABASE IF EXISTS ${DATABASE}; CREATE DATABASE ${DATABASE};"

  # If file is a zip, unzip it.
  if [[ ${DUMP_FILE} =~ \.zip$ ]];then
     DUMP_FILE_BASE=${DUMP_FILE}
     DUMP_DIR=$(dirname  "${DUMP_FILE%.*}")
     DUMP_FILE=${DUMP_DIR}"/"$(basename  "${DUMP_FILE%.*}")
     unzip -oq ${DUMP_FILE} -d ${DUMP_DIR}
  fi;

  # Import
  mysql $(wex mysql/loginCommand) < ${DUMP_FILE}

  # If file was a zip, .sql file was temporary.
  if [[ ${DUMP_FILE_BASE} =~ \.zip$ ]];then
    rm ${DUMP_FILE}
  fi
}
