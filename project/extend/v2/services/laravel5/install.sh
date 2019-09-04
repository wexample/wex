#!/usr/bin/env bash

laravel5Install() {
  . .env
  . .wex

  local STARTED=$(wex site/started)

  if [ ${STARTED} != true ];then
    wex site/start
  fi

  # Composer install / update.
  local ACTION="update"
  if [ "${SITE_ENV}" = "prod" ];then
    ACTION="install"
  fi;
  wex site/exec -l -c="composer "${ACTION}

  # Yarn
  local OPTION=""
  if [ "${SITE_ENV}" = "prod" ];then
    OPTION="--production"
  fi;
  wex site/exec -l -c="yarn install "${OPTION}

  # Encore.
  if [ "${SITE_ENV}" = "dev" ] && [ $(wex site/exec -c="wex file/exists -f=/var/www/html/project/node_modules/.bin/encore") == true ];then
    wex site/exec -l -c="yarn run encore dev"
  fi

  # Copy .env file.
  if [ ! -f ./project/.env ];then
    cp ./project/.env.example ./project/.env
  fi

  # Fill up laravel file with db URL
  wex config/setValue -f=./project/.env -k=DATABASE_URL -s="=" -v="mysql://root:${MYSQL_PASSWORD}@${NAME}_mysql:3306/${NAME}"

  # Rebuild and clear caches.
  wex site/build

  # Give site perms
  wex site/perms

  # Stop site if not already running.
  if [ ${STARTED} != true ];then
    wex site/stop
  fi
}