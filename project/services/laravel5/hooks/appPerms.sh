#!/usr/bin/env bash

laravel5AppPerms() {
  wex app/exec -c="chown -R www-data:www-data /var/www/html/project/public"
  wex app/exec -c="chown -R www-data:www-data /var/www/html/project/storage"
}