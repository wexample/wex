#!/usr/bin/env bash

roundcubeConfig() {
  # php.ini
  wex service/templates -s=roundcube -e=inc
}
