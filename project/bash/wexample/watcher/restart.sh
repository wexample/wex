#!/usr/bin/env bash

watcherRestart() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  docker restart ${SITE_NAME}_watcher
}
