#!/usr/bin/env bash

textSplitArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to transform to uppercase" true'
    [1]='separator s "Separator" true'
  )
}

textSplit() {
  echo ${TEXT} | tr "${SEPARATOR}" "\n"
}
