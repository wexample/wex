#!/usr/bin/env bash

appRestartArgs() {
  _ARGUMENTS=(
    'clear_cache cc "Clear all caches" false'
    'if_started is "Restart only if already started" false'
  )
}

appRestart() {
  # Prevent unwanted restart.
  if [ "${IF_STARTED}" = "true" ] && [ "$(wex app/started -ic)" != true ];then
    return
  fi

  local WEX_ARGUMENTS_BKP=${WEX_ARGUMENTS}

  wex app/stop

  # Remove local config file
  if [ -f ./tmp/config ]; then
      rm ./tmp/config
  fi

  wex app/start ${WEX_ARGUMENTS_BKP}
}
