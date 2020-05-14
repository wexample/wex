#!/usr/bin/env bash

laravel5CacheClear() {
  wex site/exec -l -c="php artisan config:clear"
  wex site/exec -l -c="php artisan cache:clear"
  wex site/exec -l -c="php artisan route:clear"
}