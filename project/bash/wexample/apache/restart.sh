#!/usr/bin/env bash

apacheRestart() {
  SITE_NAME=$(wex site/config -k=name)
  CONTAINER=web
  docker exec ${SITE_NAME}_${CONTAINER} service apache2 restart
}
