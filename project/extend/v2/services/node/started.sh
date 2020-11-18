#!/usr/bin/env bash

nodeStarted() {
  . .env
  # Then reload apache (SSL certs)
  wex site/exec -c="service nginx restart"
}