#!/usr/bin/env bash

nextcloudAppPerms() {
  wex app/exec -c="chown -R www-data:www-data /var/www/html/"
  wex app/exec -c="chmod 777 -R /var/www/html"
  wex app/exec -c="chmod 770 -R /var/www/html/config"
  wex app/exec -c="chmod 770 -R /var/www/html/data"
}