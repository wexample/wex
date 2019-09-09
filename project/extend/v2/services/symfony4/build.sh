#!/usr/bin/env bash

symfony4Build() {
  . .env

  # FosJs Routes
  # TODO Modularize...
  if [ -d project/vendor/friendsofsymfony/jsrouting-bundle ];then
    wex site/exec -l -c="php bin/console fos:js-routing:dump --format=json --target=public/js/fos_js_routes.json"
  fi

  # Encore.
  # TODO Modularize...
  if [ -f node_modules/.bin/encore ];then
    ENV_NAME="production"
    if [ "${SITE_ENV}" != "prod" ];then
      ENV_NAME=dev
    fi;
    wex site/exec -l -c="node_modules/.bin/encore ${ENV_NAME}"
  fi
}