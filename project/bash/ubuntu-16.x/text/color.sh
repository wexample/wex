#!/usr/bin/env bash

textColorArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to colorize" true'
    [1]='color c "Color name" true'
  )
}

textColor() {
  local BROWN="\033[0;33m"
  local CYAN="\033[0;36m"
  local LIGHTBLUE="\033[1;34m"
  local LIGHTCYAN="\033[1;36m"
  local LIGHTGRAY="\033[0;37m"
  local LIGHTGREEN="\033[1;32m"
  local LIGHTRED="\033[1;31m"
  local RED="\033[0;31m"
  local GREEN="\033[0;32m"
  local WHITE="\033[1;37m"
  local YELLOW="\033[1;33m"
  local DEFAULT="\033[0m"

  # Uppercase color name
  COLOR=$(wex text/uppercase -t=${COLOR})
  # Find color code
  eval 'COLOR=$'${COLOR}
  # Print
  printf "${COLOR}${TEXT}${DEFAULT}\n"
}
