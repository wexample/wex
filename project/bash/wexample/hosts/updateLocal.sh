#!/usr/bin/env bash

hostsUpdateLocal() {
  case "$(wex system/osName)" in
    "linux")
      echo 'linux'
      local HOST_FILE=/etc/hosts
      ;;
    "windows")
      local HOST_FILE='C:\Windows\System32\drivers\etc\hosts'
      ;;
  esac

  # Remove old blocks
  sed -i '/\#\[ wex \]\#/,/\#\[ endwex \]\#/d' ${HOST_FILE}
  # Add new line if needed.
  sed -i -e '$a\' ${HOST_FILE}
  # Create new block.
  local HOSTS_TEXT="#[ wex ]#\n"$(wex hosts/info)"\n#[ endwex ]#"
  # Append new hosts
  echo -e ${HOSTS_TEXT} >> ${HOST_FILE}
}
