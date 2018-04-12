#!/usr/bin/env bash

webStart() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  CONTAINER=web

  docker start ${SITE_NAME}_${CONTAINER}
}
