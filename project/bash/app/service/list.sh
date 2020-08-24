#!/usr/bin/env bash

serviceList() {
  local SERVICES
  # From config.
  SERVICES=$(wex app/config -k=services)
  # Split
  SERVICES=("$(wex string/split -t="${SERVICES}")")
  # Return
  echo "${SERVICES[*]}"
}
