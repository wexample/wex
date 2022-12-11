#!/usr/bin/env bash

symfony4AppBuild() {
  . .env

  # FosJs Routes
  if [ -d project/vendor/friendsofsymfony/jsrouting-bundle ];then
    wex app/exec -l -c="php bin/console fos:js-routing:dump --format=json --target=public/js/fos_js_routes.json"
  fi

  # Encore.
  if [ -f node_modules/.bin/encore ];then
    ENV_NAME="production"
    if [ "${SITE_ENV}" != "prod" ];then
      ENV_NAME=dev
    fi;
    wex app/exec -l -c="node_modules/.bin/encore ${ENV_NAME}"
  fi
}