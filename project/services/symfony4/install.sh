#!/usr/bin/env bash

# TODO Not tested
symfony4Install() {
  . .env
  . .wex

  local STARTED=$(wex site/started)

  if [ ${STARTED} != true ];then
    wex site/start
  fi

  wex site/perms

  # Composer install / update.
  local ACTION="update"
  if [ "${SITE_ENV}" = "prod" ];then
    ACTION="install"
  fi;
  wex site/exec -l -c="composer "${ACTION}

  # NPM
  local OPTION=""
  if [ "${SITE_ENV}" = "prod" ];then
    OPTION="--production"
  fi;
  wex site/exec -l -c="npm install "${OPTION}

  # Encore.
  if [ "${SITE_ENV}" = "dev" ] && [ $(wex site/exec -c="wex file/exists -f=/var/www/html/project/node_modules/.bin/encore") == true ];then
    wex site/exec -l -c="yarn run encore dev"
  fi

  # Fill up Symfony .env file with db URL
  wex config/setValue -f=./project/.env -k=DATABASE_URL -s="=" -v="mysql://root:${MYSQL_PASSWORD}@${NAME}_mysql:3306/${NAME}"

  # Assets symlinks.
  wex cli/exec -c="assets:install --symlink public"

  # CKEditor install
  if [ $(wex dir/exists -d="project/vendor/friendsofsymfony/ckeditor-bundle") == true ];then
    wex cli/exec -c="ckeditor:install"
  fi

  # Rebuild and clear caches.
  wex site/build

  # Stop site if not already running.
  if [ ${STARTED} != true ];then
    wex site/stop
  fi
}