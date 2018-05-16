#!/usr/bin/env bash

wordpressConfig() {
  wex db/config

  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_NAME -v="${SITE_DB_NAME}"
  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_USER -v="${SITE_DB_USER}"
  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_PASSWORD -v="${SITE_DB_PASSWORD}"
  wex php/constantChange -f=./wordpress/wp-config.php -k=DB_HOST -v="${SITE_DB_HOST}"

  echo "\nSITE_CONTAINER=wordpress"
}
