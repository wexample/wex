#!/usr/bin/env bash

laravel5Perms() {
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/public"
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/storage"
}