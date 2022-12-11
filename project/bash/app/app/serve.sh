#!/usr/bin/env bash

appServe() {
  # Update hosts list if IP changed.
  wex hosts/update
  # Update local host file.
  wex hosts/updateLocal
  if [ "$(wex app/started)" = "true" ];then
    # Refresh services (ex apache restart)
    wex hook/exec -c=appServe
  fi
}