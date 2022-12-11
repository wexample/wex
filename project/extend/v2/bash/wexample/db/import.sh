#!/usr/bin/env bash

dbImportArgs() {
  _ARGUMENTS=(
    [0]='filename f "Dump file name" trues'
  )
}

dbImport() {
  . ${WEX_APP_CONFIG}

  local CONTAINER=$(wex app/container -c="")

  # Copy mysql configuration.
  docker cp ./tmp/mysql.cnf ${CONTAINER}:./tmp/mysql.cnf
  docker exec ${CONTAINER} /bin/bash -c "mysql $(wex mysql/loginCommand) < /var/www/html/${FILENAME}"
}
