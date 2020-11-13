#!/usr/bin/env bash

dirCopyArgs() {
  _ARGUMENTS=(
    [0]='from f "Source dir containing content co copy" true',
    [1]='to t "Destination dir" true',
  )
}

dirCopy() {
  # Copy files.
  cp -n -R ${FROM}/. ${TO}
}
