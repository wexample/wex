#!/usr/bin/env bash

serviceList() {
  # From config.
  . .wex
  . .env

  # Add env specific services.
  local ENV_SERVICES+=$(eval 'echo ${'${SITE_ENV^^}'_SERVICES}')
  if [ "${ENV_SERVICES}" != "" ];then
    SERVICES+=,${ENV_SERVICES}
  fi

  # Split
  SERVICES=($(wex text/split -t=${SERVICES} -s=","))
  # Return
  echo "${SERVICES[*]}"
}
