#!/usr/bin/env bash

sslRenew() {
  # Start server.
  if [ $(wex server/started) == false ];then
    wex server/start
  fi
  # Force renew.
  docker exec wex_reverse_proxy_certs /app/force_renew
}