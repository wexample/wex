#!/usr/bin/env bash

mysqlGo() {
  SITE_NAME=$(wex site/config -k=name)

  # We may merge behavior with exec.sh
  # We are not into the web container.
  if [[ $(wex docker/isEnv) == false ]]; then
    # Run itself into container, see below.
    docker exec ${SITE_NAME}_web sh -c "cd /var/www/html/ && wex mysql/exec -c=\"${COMMAND}\""
  else
    mysql $(wex mysql/loginCommand)
  fi;
}
