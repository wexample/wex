#!/usr/bin/env bash

fileTextAppendOnceArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='line l "New line" true'
 )
}

fileTextAppendOnce() {
  findExactLine=$(wex file/lineExists -f=${FILE} -l="${LINE}")

  if [ "${findExactLine}" != true ]; then
    wex file/textAppend -f=${FILE} -l="${LINE}"
  fi
}
