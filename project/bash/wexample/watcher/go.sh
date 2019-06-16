#!/usr/bin/env bash

watcherGo() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  docker exec -ti ${SITE_NAME}_watcher /bin/bash -c "cd /var/www && gulp"
}