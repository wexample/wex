#!/usr/bin/env bash

containerDefaultArgs() {
  _DESCRIPTION="Return the full name of current app container"
  _ARGUMENTS=(
    'container c "User container" false "web"'
  )
}

containerDefault() {
  . ${WEX_WEXAMPLE_APP_CONFIG}

  # Default container name.
  if [ "${CONTAINER}" == "" ]; then
    if [ "${SITE_CONTAINER}" != "" ]; then
      CONTAINER=${SITE_CONTAINER}
    else
      CONTAINER=web
    fi
  fi

  echo ${APP_NAME_INTERNAL}_${CONTAINER}
}