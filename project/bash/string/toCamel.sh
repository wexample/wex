#!/usr/bin/env bash

stringToCamelArgs() {
  _ARGUMENTS=(
    'text t "Text to work on" true'
  )
}

stringToCamel() {
  echo -e ${TEXT} | sed -E 's/-([a-zA-Z0-9])/\U\1/g' | sed -E 's/^([A-Z])/\l\1/'
}