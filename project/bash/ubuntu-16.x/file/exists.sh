#!/usr/bin/env bash

fileExistsArgs() {
  _ARGUMENTS=(
    [0]='file f "File" true'
  )
}

fileExists() {
  [ -f ${FILE} ] && echo true || echo false
}
