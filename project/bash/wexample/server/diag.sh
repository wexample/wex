#!/usr/bin/env bash

serverDiag() {
  # Show conf.
  wex wexample::server/exec -c="cat /etc/nginx/conf.d/default.conf"
  echo -e "\n\n\nLOG"
  # Show log
  docker logs wex_server --tail 20
  echo -e "\n\n\nACCESS"
  docker exec -ti wex_server tail /var/log/nginx/access.log
}