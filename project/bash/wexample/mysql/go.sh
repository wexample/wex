#!/usr/bin/env bash

mysqlGo() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # We may merge behavior with exec.sh
  # We are not into the web container.
  if [[ $(wex docker/isEnv) == false ]]; then
    # Run itself into container, see below.
    docker exec -it ${SITE_NAME}_web sh -c "cd /var/www/html/ && wex mysql/go"
  else
    mysql $(wex mysql/loginCommand)
  fi;
}
