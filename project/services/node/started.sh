#!/usr/bin/env bash

nodeAppStarted() {
  . .env
  # Then reload apache (SSL certs)
  wex app/exec -c="service nginx restart"
}