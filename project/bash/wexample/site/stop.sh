#!/usr/bin/env bash

siteStop() {
  wex site/compose -c="down"
  # Add site
  wex server/siteRemove -d="./"
  # Remove config file il exists.
  rm -f ${WEX_WEXAMPLE_SITE_DIR_TMP}config
}
