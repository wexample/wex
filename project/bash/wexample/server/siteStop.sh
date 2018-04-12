#!/usr/bin/env bash

serverSiteStopArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Root site directory" true',
  )
}

serverSiteStop() {
  # Reload file
  wex server/sitesUpdate
  # Rebuild hosts
  wex hosts/update
}
