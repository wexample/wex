#!/usr/bin/env bash

mysqlStarted() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  _wexMessage "Set MySQL site.cnf access"

  docker exec ${SITE_NAME}_mysql chmod a-rw /var/www/tmp/mysql.cnf
  docker exec ${SITE_NAME}_mysql chmod a-rw /etc/mysql/conf.d/site.cnf
  docker exec ${SITE_NAME}_mysql service mysql restart
}
