#!/usr/bin/env bash

_wexError() {
  printf "${WEX_COLOR_RED}[wex] Error : ${1}${WEX_COLOR_RESET}\n"

  # Complementary information or description for extra text
  if [ "${2}" != "" ];then
    printf "      ${WEX_COLOR_CYAN}${2}${WEX_COLOR_RESET}\n"
  fi

  # Extra text
  if [ "${3}" != "" ];then
    printf "      ${3}\n"
  fi
}

_wexLog() {
  local MESSAGE;
  MESSAGE=$(_wexTruncate "${1}" 4)

  printf "${WEX_COLOR_GRAY}  > ${WEX_COLOR_LIGHT_GRAY}${MESSAGE}${WEX_COLOR_RESET}\n"
}

_wexMessage() {
  printf "${WEX_COLOR_CYAN}[wex]${WEX_COLOR_RESET} ${1}${WEX_COLOR_RESET}\n"

  # Complementary information or description for extra text
  if [ "${2}" != "" ];then
    printf "      ${WEX_COLOR_CYAN}${2}${WEX_COLOR_RESET}\n"
  fi

  # Extra text
  if [ "${3}" != "" ];then
    printf "      ${3}\n"
  fi
}

export -f _wexError
export -f _wexLog
export -f _wexMessage
