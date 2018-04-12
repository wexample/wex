#!/usr/bin/env bash

ftpGo() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  # USe default container name.
  docker exec -it ${SITE_NAME}_ftp /bin/bash
}
