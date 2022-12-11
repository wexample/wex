#!/usr/bin/env bash

mysqlAppStop() {
  . ${WEX_APP_CONFIG}

  _wexMessage "Release MySQL site.cnf access"

  docker exec "${SITE_NAME_INTERNAL}_mysql" chmod 777 /var/www/tmp/mysql.cnf
  docker exec "${SITE_NAME_INTERNAL}_mysql" chmod 777 /etc/mysql/conf.d/site.cnf
}
