#!/usr/bin/env bash

serviceList() {
  # From config.
  SERVICES=$(wex site/config -k=services)
  # Split
  SERVICES=($(wex string/split -t="${SERVICES}"))
  # Return
  echo ${SERVICES[@]}
}
