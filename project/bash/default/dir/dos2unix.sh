#!/usr/bin/env bash

dirDos2unixArgs() {
  _ARGUMENTS=(
    [0]='dir d "Directory name" true'
  )
}

dirDos2unix() {
  find ${DIR} -type f -print0 | xargs -0 dos2unix
}