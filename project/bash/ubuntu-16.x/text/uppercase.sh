#!/usr/bin/env bash

textUppercaseArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to transform to uppercase" true'
  )
}

textUppercase() {
  echo ${TEXT} | tr '[:lower:]' '[:upper:]'
}
