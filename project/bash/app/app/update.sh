#!/usr/bin/env bash

appUpdateArgs() {
  _DESCRIPTION="Update app to last wex scripts"
  _ARGUMENTS=(
    'no_save ns "Do not save new version in .wex file. Useful for dev." false'
  )
}

appUpdate() {
  unset WEX_VERSION

  _wexAppVersion

  wex core/migrate --from $(_wexAppVersion) --to $(wex core/version) --command app

  if [ "${NO_SAVE}" == "" ];then
    # Save new version
    wex config/setValue -f=.wex -k=WEX_VERSION -s="=" -v=$(wex core/version)
  fi
}