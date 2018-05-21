#!/usr/bin/env bash

wordpressSitePull() {
  . .wex

  chown -R www-data:www-data ./wordpress/
}