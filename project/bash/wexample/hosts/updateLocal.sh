#!/usr/bin/env bash

hostsUpdateLocal() {
  case "$(wex system/osName)" in
    "linux")
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
  echo -e "#[ wex ]#" >> ${HOST_FILE}
  cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts >> ${HOST_FILE}
  echo -e "\n#[ endwex ]#" >> ${HOST_FILE}
}
