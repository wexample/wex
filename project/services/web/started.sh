#!/usr/bin/env bash

webStarted() {
  # Wait mounted volumes to be available
  echo "Waiting for apache restart..."
  sleep 40
  # The reload apache (SSL certs)
  wex apache/restart >> /dev/null
}