#!/usr/bin/env bash

appUpdateArgs() {
  _DESCRIPTION="Update app to last wex scripts"
  _ARGUMENTS=(
    [0]='no_save ns "Do not save new version in .wex file. Useful for dev." false'
  )
}

appUpdate() {
  unset WEX_VERSION
  . .wex

  # Treat undefined app as v2
  if [ "${WEX_VERSION}" == "" ];then
    WEX_VERSION=2
  fi

  wex core/migrate --from ${WEX_VERSION} --to $(wex core/version) --command app

  if [ "${NO_SAVE}" == "" ];then
    # Save new version
    wex config/setValue -f=.wex -k=WEX_VERSION -s="=" -v=$(wex core/version)
  fi
}