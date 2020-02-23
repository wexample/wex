#!/usr/bin/env bash

symfony4Install() {
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
  if [ "${SITE_ENV}" = "dev" ] && [ -f ./project/node_modules/.bin/encore ];then
    wex site/exec -l -c="yarn run encore dev"
  fi

  # Copy .env file.
  if [ ! -f ./project/.env ];then
    cp ./project/.env.example ./project/.env
  fi

  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Fill up Symfony .env file with db URL
  wex config/setValue -f=./project/.env -k=DATABASE_URL -s="=" -v="mysql://root:${MYSQL_PASSWORD}@${SITE_NAME_INTERNAL}_mysql:3306/${NAME}"

  # Assets symlinks.
  wex cli/exec -c="assets:install --symlink public"

  # CKEditor install
  # TODO modularize..
  if [ $(wex dir/exists -d="project/vendor/friendsofsymfony/ckeditor-bundle") == true ];then
    wex cli/exec -c="ckeditor:install"
  fi

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