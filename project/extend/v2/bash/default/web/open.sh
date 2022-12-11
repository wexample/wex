#!/usr/bin/env bash

webOpenArgs() {
  _ARGUMENTS=(
    [0]='url u "URL to open" true'
  )
}

webOpen() {
  case "$(wex system/os)" in
    "linux")
      # May not exists in production server.
      if [ $(wex package/exists -n=xdg-open) == true ];then
        xdg-open ${URL} &
      fi
      ;;
    "windows")
      start ${URL}
      ;;
  esac
}
