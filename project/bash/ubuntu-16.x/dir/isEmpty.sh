#!/usr/bin/env bash

dirIsEmptyArgs() {
  _ARGUMENTS=(
    [0]='dir d "Directory name" true'
  )
}

dirIsEmpty() {
  [ -z "$(ls -A ${DIR})" ] && echo true || echo false
}
