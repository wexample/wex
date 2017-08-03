#!/usr/bin/env bash

composerInstall() {
  # Install composer
  curl -sS https://getcomposer.org/installer | php
  # Install all project dependencies
  php composer.phar clear-cache -q
  php composer.phar install -q
}
