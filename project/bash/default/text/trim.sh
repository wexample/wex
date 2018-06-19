#!/usr/bin/env bash

textTrimArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to trim" true'
  )
}

textTrim() {
  echo -e "${TEXT}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
}
