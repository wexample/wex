#!/usr/bin/env bash

mysqlLoginCommand() {
  local BASE_PATH=''
  if [ $(wex docker/isEnv) == true ];then
    BASE_PATH='/var/www/html/'
  else
    BASE_PATH='./'
  fi
  # Load credentials stored into config
  wex config/load
  echo --defaults-extra-file=${BASE_PATH}tmp/mysql.cnf ${MYSQL_DB_NAME}
}
