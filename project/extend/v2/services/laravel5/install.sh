#!/usr/bin/env bash

laravel5Install() {
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/storage"
}