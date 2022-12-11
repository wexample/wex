#!/usr/bin/env bash

laravel5CacheClear() {
  wex app/exec -l -c="php artisan config:clear"
  wex app/exec -l -c="php artisan cache:clear"
  wex app/exec -l -c="php artisan route:clear"
}