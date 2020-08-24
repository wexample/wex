#!/usr/bin/env bash

hostsUpdateLocal() {
  case "$(wex system/os)" in
    "linux" | "mac")
      local HOST_FILE=/etc/hosts
      ;;
    "windows")
      local HOST_FILE='C:\Windows\System32\drivers\etc\hosts'
      ;;
  esac

  # Remove old blocks
  sudo sed -i"${WEX_SED_I_ORIG_EXT}" -e '/\#\[ wex \]\#/,/\#\[ endwex \]\#/d' ${HOST_FILE}
  sudo rm ${HOST_FILE}"${WEX_SED_I_ORIG_EXT}"
  # Add new line if needed.

  # Create new block.
  echo -e "#[ wex ]#" | sudo tee -a ${HOST_FILE} > /dev/null
  cat "${WEX_DIR_PROXY_TMP}hosts" | sudo tee -a ${HOST_FILE} > /dev/null
  echo -e "\n#[ endwex ]#" | sudo tee -a ${HOST_FILE} > /dev/null
}
