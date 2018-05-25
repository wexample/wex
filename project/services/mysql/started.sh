#!/usr/bin/env bash

mysqlStarted() {
  # On windows toolbox we need to set proper file access.
  if [ $(wex system/osName) == 'windows' ] && [ $(wex docker/isToolBox) == true ];then
    . ${WEX_WEXAMPLE_SITE_CONFIG}

    echo "Set MySQL site.cnf access"

    docker exec ${SITE_NAME}_mysql chmod -rw /etc/mysql/conf.d/site.cnf
    docker exec ${SITE_NAME}_mysql service mysql restart
  fi
}
