#!/usr/bin/env bash

symfony4Perms() {
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/src"
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/var"
  wex site/exec -c="chown -R www-data:www-data /var/www/html/project/public/uploads"
  # Allow tcpdf to write new fonts.
  wex site/exec -c="chmod -R 777 /var/www/html/project/vendor/tecnickcom/tcpdf/fonts"
}