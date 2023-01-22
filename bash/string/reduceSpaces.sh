#!/usr/bin/env bash

stringReduceSpacesArgs() {
  _ARGUMENTS=(
    'text t "Text to transform" true'
  )
}

stringReduceSpaces() {
  echo "${TEXT}" | sed 's/ \{1,\}/ /g'
}
