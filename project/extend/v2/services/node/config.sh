#!/usr/bin/env bash

nodeConfig() {
  # Nginx conf
  wex service/templates -s=nginx -e=conf

  echo "\nSITE_CONTAINER=node"
}
