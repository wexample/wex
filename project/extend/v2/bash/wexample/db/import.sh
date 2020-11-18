#!/usr/bin/env bash

dbImportArgs() {
  _ARGUMENTS=(
    [0]='filename f "Dump file name" trues'
  )
}

dbImport() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  local CONTAINER=$(wex site/container -c="")

  # Copy mysql configuration.
  docker cp ./tmp/mysql.cnf ${CONTAINER}:./tmp/mysql.cnf
  docker exec ${CONTAINER} /bin/bash -c "mysql $(wex mysql/loginCommand) < /var/www/html/${FILENAME}"
}
