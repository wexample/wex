#!/usr/bin/env bash

pathWindowsToPosixArgs() {
  _ARGUMENTS=(
    [0]='path_name p "Path" true'
  )
}

pathWindowsToPosix() {
  echo "/${PATH_NAME}" | sed -e 's/\\/\//g' -e 's/://'
}
