#!/usr/bin/env bash

serverSiteStartArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" true',
  )
}

serverSiteStart() {
  # Reload sites will clean up list.
  wex server/sitesUpdate
    # Add new site.
  echo -e "\n"${DIR_SITE} >> ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites
  # Rebuild hosts
  wex hosts/update
}
