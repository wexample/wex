#!/usr/bin/env bash

sslRenew() {
  # Start server.
  if [ $(wex server/started) == false ];then
    wex server/start
  fi
  # SSL container may sleep.
  docker start wex_server_certs
  # Force renew.
  docker exec wex_server_certs /app/force_renew
}