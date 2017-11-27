#!/usr/bin/env bash

serviceList() {
  # From config.
  SERVICES=$(wex site/config -k=services)
  # Split
  SERVICES=($(wex text/split -t=${SERVICES} -s=","))
  # Return
  echo ${SERVICES[@]}
}
