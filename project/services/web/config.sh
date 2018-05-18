#!/usr/bin/env bash

webConfig() {
  # php.ini
  wex service/templates -s=php -e=ini
  # apache.conf
  wex service/templates -s=apache -e=conf
  # cron
  wex service/templates -s=cron -e=false

  echo "\nSITE_CONTAINER=web"
}
