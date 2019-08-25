#!/usr/bin/env bash

packageUpdateArgs() {
  _DESCRIPTION="Update packages. Use to prevent multiple updates if running chained scripts."
}

packageUpdate() {
  # Prevent multiple calls.
  if [ "${WEX_PACKAGES_UPDATED}" == "" ];then
    WEX_PACKAGES_UPDATED=true
    case "$(wex system/os)" in
      "linux")
        apt-get install git -yq
        ;;
    esac
  fi
}
