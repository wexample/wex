#!/usr/bin/env bash

siteOpen() {
  # Open web page
  local DOMAINS=($(wex site/domains))

  for DOMAIN in ${DOMAINS[@]};do
    wex web/open -u=http://${DOMAIN}
  done
}