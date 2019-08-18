#!/usr/bin/env bash

# TODO Not automated for now.
laravel5LaravelInstall() {
  wex site/exec -l -c="composer require laravel/installer"
  wex site/exec -l -c="yarn"
  wex site/exec -l -c="./vendor/bin/laravel new"
}