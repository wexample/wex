#!/usr/bin/env bash

symfony4Build() {
  # FosJs Routes
  wex site/exec -l -c="php bin/console fos:js-routing:dump --format=json --target=public/js/fos_js_routes.json"

  . .env

  ENV_NAME="production"
  if [ "${SITE_ENV}" != "prod" ];then
    ENV_NAME=dev
  fi;

  # Assets.
  wex site/exec -l -c="node_modules/.bin/encore ${ENV_NAME}"
}