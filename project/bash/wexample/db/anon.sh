#!/usr/bin/env bash

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