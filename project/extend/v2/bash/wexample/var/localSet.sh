#!/usr/bin/env bash

varLocalSetArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'value v "Variable value" true'
  )
}

varLocalSet() {
  wex default::var/localSet -n="${NAME}" -v="${VALUE}" -f="${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}"
}
