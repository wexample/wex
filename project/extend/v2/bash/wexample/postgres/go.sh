#!/usr/bin/env bash

postgresGo() {
  . ${WEX_APP_CONFIG}
  docker exec -it ${SITE_NAME_INTERNAL}_postgres sh -c "psql ${SITE_NAME}"
}
