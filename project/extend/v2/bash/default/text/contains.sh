#!/usr/bin/env bash

textContainsArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to colorize" true'
    [1]='search s "Searched string" true'
  )
}

textContains() {
  if echo "${TEXT}" | grep -q "${SEARCH}"; then
    echo true
  else
    echo false
  fi
}
