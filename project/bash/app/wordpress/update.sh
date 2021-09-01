#!/usr/bin/env bash

wordpressUpdate() {
  wex site/exec -l -c="wp core update --allow-root"
  wex site/exec -l -c="wp plugin update --all --allow-root"
  wex site/exec -l -c="wp core update-db --allow-root"
  wex site/exec -l -c="wp core update-db --network --allow-root"
  wex site/exec -l -c="wp theme update --all --allow-root"
  wex site/exec -l -c="wp language core update --allow-root"
}