#!/usr/bin/env bash

stringToKebabArgs() {
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringToKebab() {
  TEXT=$(echo "${TEXT}" | tr "_" " ")
  TEXT=$(wex string/reduceSpaces -t="${TEXT}")
  TEXT=$(wex string/toAlNum -t="${TEXT}")
  echo "${TEXT// /-}"
}
