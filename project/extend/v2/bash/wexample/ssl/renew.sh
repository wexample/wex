#!/usr/bin/env bash

sslRenew() {
  # Start server.
  if [ $(wex server/started) == false ];then
    wex server/start
  fi
  # SSL container may sleep.
  docker start ${WEX_WEXAMPLE_PROXY_CONTAINER}_certs
  # Force renew.
  docker exec ${WEX_WEXAMPLE_PROXY_CONTAINER}_certs /app/force_renew
}