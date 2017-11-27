#!/usr/bin/env bash

fileLinesCountArgs() {
  _ARGUMENTS=(
    [0]='file f "File" true'
  )
}

fileLinesCount() {
  cat ${FILE} | wc -l
}
