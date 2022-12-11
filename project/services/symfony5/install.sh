#!/usr/bin/env bash

symfony5Install() {
  . .env
  . .wex

  local STARTED=$(wex site/started -ic)

  if [ ${STARTED} != true ];then
    wex site/start
  fi

  # Composer install.
  wex site/exec -l -c="composer install"${ACTION}

  # Yarn
  local OPTION=""
  if [ "${SITE_ENV}" = "prod" ];then
    OPTION="--production"
  fi;
  wex site/exec -l -c="yarn install "${OPTION}

  # Encore.
  if [ "${SITE_ENV}" = "dev" ] && [ -f ./project/node_modules/.bin/encore ];then
    wex site/exec -l -c="yarn run encore dev"
  fi

  # Copy .env file.
  if [ ! -f ./project/.env ];then
    cp ./project/.env.example ./project/.env
  fi

  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Fill up Symfony .env file with db URL
  # TODO site/install should be able to be executed on exiting site, to update packages.
  #      > TODO create wex site/configure for automatic configuration
  # wex config/setValue -f=./project/.env -k=DATABASE_URL -s="=" -v="mysql://root:${MYSQL_PASSWORD}@${SITE_NAME_INTERNAL}_mysql:3306/${NAME}"

  # Assets symlinks.
  wex cli/exec -c="assets:install --symlink public"

  # Rebuild and clear caches.
  wex site/build

  # Give site perms
  wex site/perms

  # Stop site if not already running.
  if [ ${STARTED} != true ];then
    wex site/stop
  fi

  wex site/exec -l -c="php bin/console doctrine:schema:update --force"
}