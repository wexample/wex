#!/usr/bin/env bash

symfony4AppPerms() {
  wex owner/change -r -o="www-data:www-data" -p="/var/www/html/project/src"
  wex owner/change -r -o="www-data:www-data" -p="/var/www/html/project/var"
  wex owner/change -r -o="www-data:www-data" -p="/var/www/html/project/public/uploads"
  wex owner/change -r -o="www-data:www-data" -p="/var/www/html/project/public/uploads"
  # Allow tcpdf to write new fonts.
  wex mode/change -m="0777" -p="/var/www/html/project/vendor/tecnickcom/tcpdf/fonts"
}