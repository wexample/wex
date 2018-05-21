#!/usr/bin/env bash

wordpressSitePull() {
  . .wex
  # Access to data user
  chown -R www-data:www-data ./wordpress/
  # Access for FTP transfer
  chmod -R 777 ./wordpress/public
}