#!/usr/bin/env bash

appUpdateArgs() {
  _DESCRIPTION="Update app to last wex scripts"
  _ARGUMENTS=(
    'no_save ns "Do not save new version in .wex file. Useful for dev." false'
  )
}

appUpdate() {
  unset WEX_VERSION

  local VERSION_FROM=$(_wexAppVersion)
  local VERSION_TO=$(wex core/version)
  local STARTED=$(wex app/started)

  wex core::migration/exec --from ${VERSION_FROM} --to ${VERSION_TO} --command app

  if [ "${NO_SAVE}" == "" ];then
    # Save new version
    wex config/setValue -f=.wex -k=WEX_VERSION -s="=" -v=${VERSION_TO}
  fi
}