#!/usr/bin/env bash

webStart() {
  SITE_NAME=$(wex site/config -k=name)
  CONTAINER=web

  docker start ${SITE_NAME}_${CONTAINER}
}
