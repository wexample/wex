#!/usr/bin/env bash

dbAnonArgs() {
  _MIGRATED_TO_V3=true
}

# Make current database anonymous (dev usage)
dbAnon() {
  . .env

  # Prevent big mistakes.
  if [ "${SITE_ENV}" == 'prod' ];then
    echo "You don't want to do that.";
    exit;
  fi;

  wex hook/exec -c=dbAnon
}