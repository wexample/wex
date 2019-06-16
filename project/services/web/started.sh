#!/usr/bin/env bash

webStarted() {
  . .env

  # Wait mounted volumes to be available
  echo "Waiting for apache restart..."
  sleep 5
  # Then reload apache (SSL certs)
  wex apache/restart
}