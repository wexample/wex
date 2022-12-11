#!/usr/bin/env bash

webStart() {
  . ${WEX_APP_CONFIG}
  local CONTAINER=$(wex app/container -c="")

  docker start ${SITE_NAME_INTERNAL}_${CONTAINER}
}
