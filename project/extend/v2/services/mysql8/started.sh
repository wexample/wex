#!/usr/bin/env bash

mysql8Started() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  _wexMessage "Lock MySQL site.cnf access"

  docker exec ${SITE_NAME_INTERNAL}_${DB_CONTAINER} chmod 644 /var/www/tmp/mysql.cnf
  docker exec ${SITE_NAME_INTERNAL}_${DB_CONTAINER} chmod 644 /etc/mysql/conf.d/site.cnf
}
