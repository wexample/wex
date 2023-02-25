#!/usr/bin/env bash

stringReduceSpacesArgs() {
  _DESCRIPTION="Remove two or more consecutive spaces in a text"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringReduceSpaces() {
  echo "${TEXT}" | sed 's/ \{1,\}/ /g'
}
