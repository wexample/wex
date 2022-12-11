#!/usr/bin/env bash

dbAnonArgs() {
  _DESCRIPTION="Update database with anonymization and optimization scripts for local work"
}

dbAnon() {
  . .env

  # Prevent big mistakes.
  if [ "${SITE_ENV}" = 'prod' ];then
    echo "You don't want to do that.";
    exit;
  fi;

  wex hook/exec -c=dbAnon
}