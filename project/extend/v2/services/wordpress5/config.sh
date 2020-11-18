#!/usr/bin/env bash

wordpress5Config() {
  # Same config as web
  . ${WEX_DIR_ROOT}services/web/config.sh

  webConfig

  # WP Config constants. unreachable in wp-config.php,
  # so we use wex settings.
  . .wex
  local INI=./tmp/php.env.ini
  echo '[wordpress]' >> ${INI}
  # Charset.
  if [ "${WP_DB_CHARSET}" != "" ];then
    echo 'WP_DB_CHARSET = "'${WP_DB_CHARSET}'"' >> ${INI}
  fi
  # Database prefix.
  if [ "${WP_DB_TABLE_PREFIX}" != "" ];then
    echo 'WP_DB_TABLE_PREFIX = "'${WP_DB_TABLE_PREFIX}'"' >> ${INI}
  fi

  # Override default container.
  echo "\nSITE_CONTAINER=wordpress5"
}
