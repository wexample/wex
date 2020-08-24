#!/usr/bin/env bash

appContainerArgs() {
  _ARGUMENTS=(
    'container c "User container" true'
  )
}

appContainer() {
  . ${WEX_APP_CONFIG}

  # Default container name.
  if [ "${CONTAINER}" = "" ]; then
    if [ "${SITE_CONTAINER}" != "" ]; then
      CONTAINER=${SITE_CONTAINER}
    else
      CONTAINER=web
    fi
  fi

  echo "${SITE_NAME_INTERNAL}_${CONTAINER}"
}