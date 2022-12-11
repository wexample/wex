#!/usr/bin/env bash

mysqlGo() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  docker exec -it ${SITE_NAME_INTERNAL}_${DB_CONTAINER} sh -c "mysql $(wex mysql/loginCommand -i)"
}