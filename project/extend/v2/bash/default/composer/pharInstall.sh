#!/usr/bin/env bash

composerPharInstall() {
  # Install composer
  curl -sS https://getcomposer.org/installer | php
  # Move to PATH
  mv composer.phar /usr/local/bin/composer
}
