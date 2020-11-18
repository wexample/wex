#!/usr/bin/env bash

webStart() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  local CONTAINER=$(wex site/container -c="")

  docker start ${SITE_NAME_INTERNAL}_${CONTAINER}
}
