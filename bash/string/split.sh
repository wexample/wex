#!/usr/bin/env bash

stringSplitArgs() {
  _DESCRIPTION="Split a string to array"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'text t "Text to transform to uppercase" true'
    'separator s "Separator, comma by default" true ,'
  )
}

stringSplit() {
  echo "${TEXT}" | tr "${SEPARATOR}" "\n"
}
