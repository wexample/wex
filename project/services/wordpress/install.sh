#!/usr/bin/env bash

wordpressInstall() {
  # Get MySQL configuration
  eval $(echo -e $(wex service/exec -c=config -s=mysql -p))

  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_NAME -v="${MYSQL_DB_NAME}"
  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_USER -v="${MYSQL_DB_USER}"
  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_PASSWORD -v="${MYSQL_DB_PASSWORD}"
  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_HOST -v="${MYSQL_DB_HOST}"
}
