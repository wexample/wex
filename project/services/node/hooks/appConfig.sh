#!/usr/bin/env bash

nodeAppConfig() {
  # Nginx conf
  wex config/bindFiles -s=nginx -e=conf

  echo -e "\nSITE_CONTAINER=node" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}

  # Copy .env file.
  if [ ! -f ./project/.env ];then
    cp ./project/.env.example ./project/.env
  fi

  . "${WEX_APP_CONFIG}"

  # Fill up Symfony .env file with db URL
  wex config/setValue -f=./project/.env -k=DATABASE_URL -s="=" -v="mysql://root:${MYSQL_PASSWORD}@${SITE_NAME_INTERNAL}_mysql:3306/${NAME}"

  # Assets symlinks.
  wex cli/exec -c="assets:install --symlink public"

}
