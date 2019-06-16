#!/usr/bin/env bash

symfony4WatcherStart() {
  . .env

  ENV_NAME="production"
  if [ "${SITE_ENV}" != "prod" ];then
    ENV_NAME=dev
  fi;

  wex site/exec -l -c="node_modules/.bin/encore ${ENV_NAME} --watch"
}