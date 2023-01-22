#!/usr/bin/env bash

stringToPascalArgs() {
  _ARGUMENTS=(
    'text t "Text to work on" true'
  )
}

stringToPascal() {
  echo -e ${TEXT} | sed -r 's/(^|-)(\w)/\U\2/g'
}