#!/usr/bin/env bash

sslRenew() {
  # Start server.
  if [ $(wex server/started) == false ];then
    return
  fi
  . ${WEX_WEXAMPLE_DIR_PROXY} .env
  local PROXY_NAME=${WEX_PROXY_CONTAINER}_${SITE_ENV}
  # SSL container may sleep.
  docker start ${PROXY_NAME}_certs
  # Force renew.
  docker exec ${PROXY_NAME}_certs /app/force_renew
}