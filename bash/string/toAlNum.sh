#!/usr/bin/env bash

stringToAlNumArgs() {
  _ARGUMENTS=(
    'text t "Text to transform" true'
    'strict s "Filter also dashes dots and underscores" true false'
  )
}

stringToAlNum() {
  local EXTRA="._-"

  if [ "${STRICT}" = "true" ];then
    local EXTRA=""
  fi

  echo "${TEXT}" | tr -cd '[:alnum:] '"${EXTRA}"
}
