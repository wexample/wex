#!/usr/bin/env bash

siteContainerArgs() {
  _ARGUMENTS=(
    [0]='container c "User container" true'
  )
}

siteContainer() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Default container name.
  if [ "${CONTAINER}" == "" ]; then
    if [ ${SITE_CONTAINER} != "" ]; then
      CONTAINER=${SITE_CONTAINER}
    else
      CONTAINER=web
    fi
  fi

  echo ${SITE_NAME}_${CONTAINER}
}