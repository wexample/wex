#!/usr/bin/env bash

watcherRestart() {
  # TODO Test if exists.
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  docker restart ${SITE_NAME_INTERNAL}_watcher
}
