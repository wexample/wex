#!/usr/bin/env bash

pathPosixToWindowsArgs() {
 _ARGUMENTS=(
   [0]='path_name p "Path" true'
 )
}

pathPosixToWindows() {
  echo "${PATH_NAME}" | sed -e 's/^\///' -e 's/\//\\/g' -e 's/^./\0:/'
}
