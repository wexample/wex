#!/usr/bin/env bash

serverDiag() {
  # Show conf.
  wex wexample::server/exec -c="cat /etc/nginx/conf.d/default.conf"
}