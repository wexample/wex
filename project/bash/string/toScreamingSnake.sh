#!/usr/bin/env bash

stringToScreamingSnakeArgs() {
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringToScreamingSnake() {
  TEXT=$(wex string/toSnake -t="${TEXT}")

  echo "${TEXT^^}"
}
