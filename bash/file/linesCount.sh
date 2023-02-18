#!/usr/bin/env bash

fileLinesCountArgs() {
  _DESCRIPTION='Count number of lines in a file'
  _ARGUMENTS=(
    'file f "File" true'
    'ignore_empty i "Ignore empty lines" false'
  )
}

fileLinesCount() {
  if [ "${IGNORE_EMPTY}" = "true" ];then
    cat "${FILE}" | sed '/^[[:space:]]*$/d' | wc -l
  else
    cat "${FILE}" | wc -l | sed 's/^ *//'
  fi
}
