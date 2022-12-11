#!/usr/bin/env bash

serverDiag() {
  # Show conf.
  wex wexample::server/exec -c="cat /etc/nginx/conf.d/default.conf"
  echo -e "\n\n\nLOG"
  # Show log
  docker logs ${WEX_PROXY_CONTAINER} --tail 20
  echo -e "\n\n\nACCESS"
  docker exec -ti ${WEX_PROXY_CONTAINER} tail /var/log/nginx/access.log
}