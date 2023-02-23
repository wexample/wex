#!/usr/bin/env bash

coreVersionArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION='Returns current wex core version'
  _REQUIREMENTS=(
    'nano'
  )
}

coreVersion() {
  echo "${WEX_CORE_VERSION}"
}
