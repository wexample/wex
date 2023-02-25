#!/usr/bin/env bash

stringToKebabArgs() {
  _DESCRIPTION="Convert text to kebab_case"
  # shellcheck disable=SC2034
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
