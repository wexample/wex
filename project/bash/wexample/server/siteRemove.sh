#!/usr/bin/env bash

serverSiteRemove() {
  # Reload file
  wex server/sitesUpdate
  # Rebuild hosts
  wex server/hostsUpdate
}
