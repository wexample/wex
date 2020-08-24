#!/usr/bin/env bash

wordpressUpdate() {
  wex app/exec -l -c="wp core update --allow-root"
  wex app/exec -l -c="wp plugin update --all --allow-root"
  wex app/exec -l -c="wp core update-db --allow-root"
  wex app/exec -l -c="wp theme update --all --allow-root"
  wex app/exec -l -c="wp language core update --allow-root"
  # Woo commerce db
  # wex app/exec -l -c="wp wc update --allow-root"
}