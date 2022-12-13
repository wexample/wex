#!/usr/bin/env bash

coreVersionArgs() {
  _DESCRIPTION='Returns current wex core version'
  _REQUIREMENTS=(
    'nano'
  )
}

coreVersion() {
  echo "${WEX_CORE_VERSION}"
}
