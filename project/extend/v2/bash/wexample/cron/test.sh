#!/usr/bin/env bash

cronTest() {
  echo "CRON last ran test at "$(date '+%d/%m/%Y %H:%M:%S') > /var/www/html/tmp/cron.log
}