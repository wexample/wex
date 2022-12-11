#!/usr/bin/env bash

mysqlStarted() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  _wexMessage "Lock MySQL site.cnf access"

  docker exec ${SITE_NAME_INTERNAL}_mysql chmod 644 /var/www/tmp/mysql.cnf
  docker exec ${SITE_NAME_INTERNAL}_mysql chmod 644 /etc/mysql/conf.d/site.cnf
}
