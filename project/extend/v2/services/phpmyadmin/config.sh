#!/usr/bin/env bash

phpmyadminConfig() {
  # Need php/phpmyadmin.ini even
  # if web container does not exists
  wex service/templates -s=php -e=ini
}
