#!/usr/bin/env bash

pathPosixToWindows() {
  echo "${1}" | sed -e 's/^\///' -e 's/\//\\/g' -e 's/^./\0:/'
}
