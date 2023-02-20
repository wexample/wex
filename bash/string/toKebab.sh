#!/usr/bin/env bash

stringToKebabArgs() {
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringToKebab() {
  TEXT=$(echo "${TEXT}" | tr "_" " ")
  TEXT=$(wex-exec string/reduceSpaces -t="${TEXT}")
  TEXT=$(wex-exec string/toAlNum -t="${TEXT}")
  echo "${TEXT// /-}"
}
