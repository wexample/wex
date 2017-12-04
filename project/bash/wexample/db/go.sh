#!/usr/bin/env bash

dbGo() {
  # We may merge behavior with exec.sh
  # We are not into the web container.
  if [[ $(wex docker/isEnv) == false ]]; then
    . ${WEX_WEXAMPLE_SITE_CONFIG}
    # Run itself into container, see below.
    docker exec -it ${SITE_NAME}_web sh -c "cd /var/www/html/ && wex db/go"
  else
    mysql $(wex mysql/loginCommand)
  fi;
}
