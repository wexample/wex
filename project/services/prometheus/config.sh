#!/usr/bin/env bash

prometheusConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=prometheus"
  echo "\nPROMETHEUS_VERSION="${PROMETHEUS_VERSION}

  local DOMAIN=$(eval 'echo ${'${SITE_ENV^^}'_DOMAIN_PROMETHEUS}')

  if [ "${DOMAIN}" = '' ] && [ "${SITE_ENV}" = "local" ];then
    DOMAIN=pma.${SITE_NAME}.wex
  fi

  echo "\nDOMAIN_PROMETHEUS=${DOMAIN}"
}
