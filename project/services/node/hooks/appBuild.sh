#!/usr/bin/env bash

nodeAppBuild() {
  . .env

  if [ -f ./project/package.json ];then
    ENV_NAME="production"
    if [ "${SITE_ENV}" != "prod" ];then
      ENV_NAME="dev"
    fi;

    # Assets.
    wex app/exec -l -c="npm run ${ENV_NAME}"
  fi
}