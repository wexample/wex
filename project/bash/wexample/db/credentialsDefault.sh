#!/usr/bin/env bash

dbCredentialsDefault() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  export SITE_DB_HOST=${SITE_NAME}_mysql
  export SITE_DB_PORT=3306
  export SITE_DB_NAME=${SITE_NAME}
  export SITE_DB_USER=root
  export SITE_DB_PASSWORD="thisIsAReallyNotSecurePassword!"
}
