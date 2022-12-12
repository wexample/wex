#!/usr/bin/env bash

fileCreateIfNotExistsArgs() {
  _ARGUMENTS=(
    'file f "File" true'
  )
}

fileCreateIfNotExists() {
  if [ "$(wex file/exists -f="${FILE}")" = false ];then
    touch "${FILE}"
  fi;
}
