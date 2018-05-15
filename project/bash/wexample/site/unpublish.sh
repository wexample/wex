#!/usr/bin/env bash

siteUnpublish() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  wex repo/delete

  wex remote/exec -q -e=prod -d="/var/www" -s="rm -rf ./"${SITE_NAME}
}