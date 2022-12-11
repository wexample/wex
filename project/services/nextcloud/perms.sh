#!/usr/bin/env bash

nextcloudPerms() {
  wex site/exec -c="chown -R www-data:www-data /var/www/html/"
  wex site/exec -c="chmod 777 -R /var/www/html"
  wex site/exec -c="chmod 770 -R /var/www/html/config"
  wex site/exec -c="chmod 770 -R /var/www/html/data"
}