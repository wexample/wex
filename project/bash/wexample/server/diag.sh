#!/usr/bin/env bash

serverDiag() {
  # Show conf.
  wex wexample::server/exec -c="cat /etc/nginx/conf.d/default.conf"
  # Show log
  docker logs wex_reverse_proxy --tail 20
}