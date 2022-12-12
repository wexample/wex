#!/usr/bin/env bash

_wexMethodName() {
  local SPLIT=(${1//// })
  echo ${SPLIT[0]}$(_wexUpperCaseFirstLetter "${SPLIT[1]}")
}

_wexTruncate() {
  local MAX_MIDTH
  MAX_WIDTH=$(("${WEX_SCREEN_WIDTH}" - "${WEX_TRUCATE_SPACE}" - ${2}))

  if [ "${#1}" -gt "${MAX_WIDTH}" ];then
    echo "$(echo "${1}" | cut -c -"${MAX_WIDTH}")${WEX_COLOR_GRAY}...${WEX_COLOR_RESET} "
  else
    echo "${1}"
  fi
}

_wexUpperCaseFirstLetter() {
  echo $(tr '[:lower:]' '[:upper:]' <<< ${1:0:1})${1:1}
}