#!/usr/bin/env bash

configProcessSeparatorArgs() {
  _ARGUMENTS=(
    [0]='separator s "Separator like space or equal sign, default space" false'
  )
}

configProcessSeparator() {
  # Empty separator
  if [ "${SEPARATOR}" == "" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  # Space separator to regex
  if [ "${SEPARATOR}" == " " ];then
    # Protect separator
    SEPARATOR="[ ]"
  fi;

  echo ${SEPARATOR}
}