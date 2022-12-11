#!/usr/bin/env bash

sonarqubeAppPerms() {
  wex app/exec -c="chown -R www-data:www-data /var/www/html/project/src"
}