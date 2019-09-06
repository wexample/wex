#!/usr/bin/env bash

siteRestartArgs() {
  _ARGUMENTS=(
    [0]='clear_cache cc "Clear all caches" false'
  )
}

siteRestart() {
  local WEX_ARGUMENTS_BKP=${WEX_ARGUMENTS}
  wex site/stop
  wex site/start ${WEX_ARGUMENTS_BKP}
}
