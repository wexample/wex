#!/usr/bin/env bash

phpmyadminAppConfig() {
  wex config/addTitle -t="PhpMyadmin"

  # Need php/phpmyadmin.ini even
  # if web container does not exists
  wex config/bindFiles -s=php -e=ini
}
