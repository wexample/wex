#!/usr/bin/env bash

# Return actively running sites list.
sitesRestart() {
  local SITES=$(ls)

  for SITES in ${SITES[@]}
  do
    cd ${SITES}
    wex site/restart
    cd ../
  done

  # Most of sites needs to refresh few times after starting.
  for SITES in ${SITES[@]}
  do
    cd ${SITES}
    wex site/refresh
    cd ../
  done
}
