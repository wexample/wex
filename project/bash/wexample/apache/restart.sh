#!/usr/bin/env bash

apacheRestart() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  CONTAINER=web
  docker exec ${SITE_NAME}_${CONTAINER} service apache2 restart
}
