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
  MESSAGE=${1};

  local MAX=$((WEX_SCREEN_WIDTH - 4))

  # Manage indentation when printing.
  echo -e "${WEX_COLOR_GRAY}  > ${MESSAGE}" | fold -s -w ${MAX} | sed '2,$s/^/    /'
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
