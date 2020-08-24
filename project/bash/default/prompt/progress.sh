#!/usr/bin/env bash

promptProgressArgs() {
  _ARGUMENTS=(
    'percentage p "Percentage" true'
    'width w "Width" false 30'
    'description d "Description" false'
    'status s "Status" false'
    'new_line nl "New line at end" false'
  )
}

# See : https://stackoverflow.com/questions/18362837/how-to-display-and-refresh-multiple-lines-in-bash
# See : https://www.fileformat.info/info/unicode/char/25a0/index.htm
promptProgress() {
  local MESSAGE="    ${WEX_COLOR_RESET}["
  local PRECISION=100;

  # Manage cursor position
  if [ "${NEW_LINE}" != "true" ];then
    local PROGRESS_BAR_RUNNING=$(wex var/get -n=PROGRESS_BAR_RUNNING -d=false)

    if [ "${PROGRESS_BAR_RUNNING}" = true ];then
      # Move cursor up
      printf "\033[1A"
    fi

    wex var/set -n=PROGRESS_BAR_RUNNING -v=true
  fi

  if [ "${DESCRIPTION}" != "" ];then
    MESSAGE=${DESCRIPTION}"\n"${MESSAGE}
  fi

  # Compute progress position
  for ((i=0;i<=WIDTH;i++));
  do
     if [ $(((((i * PRECISION) / WIDTH) * 100) / PRECISION)) -le "${PERCENTAGE}" ];then
       MESSAGE+="${WEX_COLOR_CYAN}"
     else
       MESSAGE+="${WEX_COLOR_GRAY}"
     fi

     MESSAGE+='■'
  done

  MESSAGE+="${WEX_COLOR_RESET}] "${PERCENTAGE}'%'"\n"

  if [ "${STATUS}" != "" ];then
    MESSAGE+="     ${WEX_COLOR_GRAY}> ${WEX_COLOR_CYAN}${STATUS}${WEX_COLOR_RESET}"
  fi

  printf "%b          \r" "${MESSAGE}"

  # Complete
  if [ "${PERCENTAGE}" = "100" ];then
    echo ""
    echo ""

    if [ "${NEW_LINE}" != "true" ];then
      wex var/set -n=PROGRESS_BAR_RUNNING -v=false
    fi
  # Ignore the \r and jump to a new line
  elif [ "${NEW_LINE}" = "true" ];then
    echo ""
  fi
}
