#!/usr/bin/env bash

stringSplitArgs() {
  _ARGUMENTS=(
    'text t "Text to transform to uppercase" true'
    'separator s "Separator, comma by default" true ,'
  )
}

stringSplit() {
  echo "${TEXT}" | tr "${SEPARATOR}" "\n"
}
