#!/usr/bin/env bash

configProcessSeparatorArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'separator s "Separator like space or equal sign, default space" false'
  )
}

configProcessSeparator() {
  # Empty separator
  if [ "${SEPARATOR}" = "" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  # One or more separator in a group
  # Non capturing group does not exists in bash
  # So final regex should increment captured indexes +1
  echo "\(${SEPARATOR}\)\{1,\}"
}