#!/usr/bin/env bash

_wexMigrateApp() {
  . .wex
  . .env
  # Add required .env variable for docker.
  wex config/setValue -f=.env -k=COMPOSE_PROJECT_NAME -s="=" -v=${NAME}_${SITE_ENV}
  wex site/restart --if_started
}