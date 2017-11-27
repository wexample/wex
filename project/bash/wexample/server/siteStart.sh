#!/usr/bin/env bash

serverSiteStartArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" true',
  )
}

serverSiteStart() {
  DIR_SITE=$(realpath ${DIR_SITE})"/"
  # Add current site.
  echo -e "\n"${DIR_SITE} >> ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites
  # Reload file to avoid duplicates.
  wex server/sitesUpdate
  # Rebuild hosts
  wex server/hostsUpdate
}
