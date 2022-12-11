#!/usr/bin/env bash

dolibarrInit() {
  # Override default container.
  echo "DOLIBARR_VERSION=13.0.3-php7.4" >> .wex
}
