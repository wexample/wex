#!/usr/bin/env bash

dbExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Mysql command to execute in site database" true'
    [1]='options o "Options" false'
  )
}

dbExec() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # We are not into the web container.
  if [[ $(wex docker/isEnv) == false ]]; then
    # Run itself into container, see below.
    docker exec ${SITE_NAME}_web sh -c "cd /var/www/html/ && wex db/exec -c=\"${COMMAND}\""
  else
    mysql $(wex mysql/loginCommand) -e "${COMMAND}" ${OPTIONS}
  fi;
}
