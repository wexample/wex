#!/usr/bin/env bash

hostsUpdateLocal() {
  case "$(wex system/osName)" in
    "linux" | "mac")
      local HOST_FILE=/etc/hosts
      ;;
    "windows")
      local HOST_FILE='C:\Windows\System32\drivers\etc\hosts'
      ;;
  esac

  # Remove old blocks
  sed -i"${WEX_SED_I_ORIG_EXT}" -e '/\#\[ wex \]\#/,/\#\[ endwex \]\#/d' ${HOST_FILE}
  rm ${HOST_FILE}"${WEX_SED_I_ORIG_EXT}"
  # Add new line if needed.

  # Create new block.
  echo -e "#[ wex ]#" >> ${HOST_FILE}
  cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts >> ${HOST_FILE}
  echo -e "\n#[ endwex ]#" >> ${HOST_FILE}
}
