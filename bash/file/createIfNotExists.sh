#!/usr/bin/env bash

fileCreateIfNotExistsArgs() {
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileCreateIfNotExists() {
  if [ "$(wex-exec file/exists -f="${FILE}")" = false ];then
    touch "${FILE}"
  fi;
}
