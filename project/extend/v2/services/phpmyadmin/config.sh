#!/usr/bin/env bash

phpmyadminConfig() {
  # Need php/phpmyadmin.ini even
  # if web container does not exists
  wex service/templates -s=php -e=ini

  . .env
  . .wex

  local SITE_ENV_MAJ=${SITE_ENV^^}
  local DOMAIN=$(eval 'echo ${'${SITE_ENV_MAJ}'_DOMAIN_PMA}')

  if [ "${DOMAIN}" = '' ] && [ "${SITE_ENV}" = "local" ];then
    DOMAIN=pma.${SITE_NAME}.wex
  fi

  echo "\nDOMAIN_PMA=${DOMAIN}"
}
