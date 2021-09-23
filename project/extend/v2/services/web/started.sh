#!/usr/bin/env bash

webStarted() {
  . .env

  # Wait mounted volumes to be available
  echo "Waiting for apache restart..."
  sleep 5
  # Then reload apache (SSL certs)
  sudo wex site/exec -c="service apache2 restart"

  # TODO for PHP FPM we should launch service.
  #  sudo wex site/exec -c="a2enmod proxy_fcgi setenvif"
  #  sudo wex site/exec -c="a2dismod php8.0"
  #  sudo wex site/exec -c="a2enconf php8.0-fpm"
  #
  #  sudo wex site/exec -c="service php8.0-fpm start"
  #  sudo wex site/exec -c="service apache2 restart"
}