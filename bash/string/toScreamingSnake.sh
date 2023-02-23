#!/usr/bin/env bash

stringToScreamingSnakeArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringToScreamingSnake() {
  TEXT=$(wex-exec string/toSnake -t="${TEXT}")

  echo "${TEXT^^}"
}
