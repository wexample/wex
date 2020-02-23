#!/usr/bin/env bash

laravel5CacheClear() {
  wex site/exec -l -c="php artisan cache:clear"
}