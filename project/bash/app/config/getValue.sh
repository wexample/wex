#!/usr/bin/env bash

configGetValueArgs() {
  _ARGUMENTS=(
    'target_key k "Target key to get" true'
    'separator s "Separator like space or equal sign, default space" false'
    'file f "File" true'
  )
}

configGetValue() {
  wex default::config/getValue "${@}"
}
