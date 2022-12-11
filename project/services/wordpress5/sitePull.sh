#!/usr/bin/env bash

wordpressSitePull() {
  . .wex
  # Access to data user
  chown -R www-data:www-data ./wordpress/
  # Do not allow to change main folders by FTP,
  # because it will be lost as mounted docker volumes.
  chmod -R 777 ./wordpress/public
  # Access for FTP transfer
  chmod -R 777 ./wordpress/public/*
}