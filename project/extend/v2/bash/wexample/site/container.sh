#!/usr/bin/env bash

siteContainerArgs() {
  _ARGUMENTS=(
    [0]='container c "User container" true'
  )
}

siteContainer() {
  . ${WEX_APP_CONFIG}

  # Default container name.
  if [ "${CONTAINER}" == "" ]; then
    if [ "${SITE_CONTAINER}" != "" ]; then
      CONTAINER=${SITE_CONTAINER}
    else
      CONTAINER=web
    fi
  fi

  echo ${SITE_NAME_INTERNAL}_${CONTAINER}
}