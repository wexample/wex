#!/usr/bin/env bash

ftpGo() {
  . ${WEX_APP_CONFIG}
  # USe default container name.
  docker exec -it ${SITE_NAME_INTERNAL}_ftp /bin/bash
}
