#!/usr/bin/env bash

postgresGo() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  docker exec -it ${SITE_NAME_INTERNAL}_mysql sh -c "psql $(wex mysql/loginCommand)"
}
