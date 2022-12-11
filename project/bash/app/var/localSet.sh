#!/usr/bin/env bash

varLocalSetArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'value v "Variable value" true'
  )
}

varLocalSet() {
  wex var/set -n="${NAME}" -v="${VALUE}" -f="${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}"
}
