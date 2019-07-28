#!/usr/bin/env bash

sonarqubePerms() {
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/src"
}