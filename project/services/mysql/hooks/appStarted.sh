#!/usr/bin/env bash

mysqlAppStarted() {
  . ${WEX_APP_CONFIG}

  _wexLog "Lock MySQL site.cnf access"

  docker exec "${SITE_NAME_INTERNAL}"_mysql chmod 644 /var/www/tmp/mysql.cnf
  docker exec "${SITE_NAME_INTERNAL}"_mysql chmod 644 /etc/mysql/conf.d/site.cnf

  chmod 777 ./mysql/data/auto.cnf
}
