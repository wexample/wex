#!/usr/bin/env bash

mysqlLoginCommand() {
  # Load credentials stored into config
  wex config/load
  echo --defaults-extra-file=./tmp/mysql.cnf ${MYSQL_DB_NAME}
}
