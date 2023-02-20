#!/usr/bin/env bash

stringToSnakeArgs() {
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringToSnake() {
  TEXT=$(echo "${TEXT}" | tr "-" "_")
  TEXT=$(wex-exec string/reduceSpaces -t="${TEXT}")
  TEXT=$(wex-exec string/toAlNum -t="${TEXT}")
  echo "${TEXT// /_}"
}
