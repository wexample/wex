#!/usr/bin/env bash

pathSafeArgs() {
  _ARGUMENTS=(
    'path_name p "Path" true'
  )
}

pathSafe() {
  # Os is windows
  if [ "$(wex system/os)" = "windows" ];then
    local FIRST_LETTER
    FIRST_LETTER="$(echo "${PATH_NAME}" | head -c 1)"

    # Path is not already converted.
    if [ "${FIRST_LETTER}" = "/" ];then
      wex path/posixToWindows -p="${PATH_NAME}";
      return
    fi;
  fi;

  echo "${PATH_NAME}";
}
