#!/usr/bin/env bash

webAppStarted() {
  . .env

  # Wait mounted volumes to be available
  _wexLog "Waiting for apache restart..."
  sleep 5
  # Then reload apache (SSL certs)
  wex apache/restart
}