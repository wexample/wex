#!/usr/bin/env bash

serverConfig() {
  docker exec ${WEX_PROXY_CONTAINER} grep -vE '^\s*$' /etc/nginx/conf.d/default.conf
}