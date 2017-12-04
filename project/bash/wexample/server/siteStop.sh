#!/usr/bin/env bash

serverSiteStop() {
  # Reload file
  wex server/sitesUpdate
  # Rebuild hosts
  wex server/hostsUpdate
}
