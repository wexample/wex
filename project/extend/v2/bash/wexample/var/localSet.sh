#!/usr/bin/env bash

varLocalSetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='value v "Variable value" true'
  )
}

varLocalSet() {
  wex default::var/localSet ${WEX_ARGUMENTS} -f="${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}"
}
