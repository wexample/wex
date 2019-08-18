#!/usr/bin/env bash

siteRestartArgs() {
  _ARGUMENTS=(
    [0]='clear_cache cc "Clear all caches" false'
  )
}

siteRestart() {
  wex site/stop
  wex site/start ${WEX_ARGUMENTS}
}
