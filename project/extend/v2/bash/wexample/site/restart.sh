#!/usr/bin/env bash

siteRestartArgs() {
  _ARGUMENTS=(
    [0]='clear_cache cc "Clear all caches" false'
    [1]='if_started is "Restart only if already started" false'
  )
}

siteRestart() {
  # Prevent unwanted restart.
  if [ "${IF_STARTED}" == "true" ] && [[ $(wex site/started) != true ]];then
    return
  fi

  local WEX_ARGUMENTS_BKP=${WEX_ARGUMENTS}
  wex site/stop
  wex site/start ${WEX_ARGUMENTS_BKP}
}
