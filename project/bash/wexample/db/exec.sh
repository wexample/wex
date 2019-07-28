#!/usr/bin/env bash

dbExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Mysql command to execute in site database" true'
  )
}

dbExec() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  local LOGIN=$(wex mysql/loginCommand)
  local QUERY="mysql --defaults-extra-file=/var/www/tmp/mysql.cnf -s -N ${SITE_NAME_INTERNAL} -e \""${COMMAND}"\""
  docker exec ${SITE_NAME}_mysql sh -c "${QUERY}"
}
