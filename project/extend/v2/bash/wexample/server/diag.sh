#!/usr/bin/env bash

serverDiag() {
  # Show conf.
  wex wexample::server/exec -c="cat /etc/nginx/conf.d/default.conf"
  echo -e "\n\n\nLOG"
  # Show log
  docker logs ${WEX_WEXAMPLE_PROXY_CONTAINER}_prod --tail 20
  echo -e "\n\n\nACCESS"
  docker exec -ti ${WEX_WEXAMPLE_PROXY_CONTAINER}_prod tail /var/log/nginx/access.log
}