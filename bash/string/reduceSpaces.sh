#!/usr/bin/env bash

stringReduceSpacesArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringReduceSpaces() {
  echo "${TEXT}" | sed 's/ \{1,\}/ /g'
}
