#!/usr/bin/env bash

mysqlExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Mysql command to execute in site database" true'
  )
}

mysqlExec() {
  SITE_NAME=$(wex site/config -k=name)

  # We are not into the web container.
  if [[ $(wex docker/isEnv) == false ]]; then
    # Run itself into container, see below.
    docker exec ${SITE_NAME}_web sh -c "cd /var/www/html/ && wex mysql/exec -c=\"${COMMAND}\""
  else
    mysql $(wex mysql/loginCommand) -e "${COMMAND}"
  fi;
}
