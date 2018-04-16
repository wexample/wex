#!/usr/bin/env bash

webOpenArgs() {
  _ARGUMENTS=(
    [0]='url u "URL to open" true'
  )
}

webOpen() {
  case "$(wex system/osName)" in
    "linux")
      xdg-open ${URL} &
      ;;
    "windows")
      start ${URL}
      ;;
  esac
}
