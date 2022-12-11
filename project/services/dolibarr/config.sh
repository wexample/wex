#!/usr/bin/env bash

dolibarrConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=dolibarr"
  echo "\nDOLIBARR_VERSION="${DOLIBARR_VERSION}
}
