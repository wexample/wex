#!/usr/bin/env bash

wordpress4AppConfig() {
  # Same config as web
  . ${WEX_DIR_SERVICES}web/hooks/appConfig.sh

  webAppConfig

  # WP Config constants. unreachable in wp-config.php,
  # so we use wex settings.
  . .wex
  local INI=./tmp/php.env.ini

  echo -e "\n\n[wordpress]" >> ${INI}
  # Charset.
  if [ "${WP_DB_CHARSET}" != "" ];then
    echo -e "WP_DB_CHARSET = \"${WP_DB_CHARSET}\"" >> ${INI}
  fi
  # Database prefix.
  if [ "${WP_DB_TABLE_PREFIX}" != "" ];then
    echo -e "\nWP_DB_TABLE_PREFIX = \"${WP_DB_TABLE_PREFIX}\"" >> ${INI}
  fi

  # Override default container.
  echo -e "\nSITE_CONTAINER=wordpress4" >> ${WEX_WEXAMPLE_APP_FILE_CONFIG}
}
