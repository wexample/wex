#!/usr/bin/env bash

siteServe() {
  # Update hosts list if IP changed.
  wex hosts/update
  # Update local host file.
  wex hosts/updateLocal
  if [ $(wex site/started) == "true" ];then
    # Refresh services (ex apache restart)
    wex hook/exec -c=siteServe
  fi
}