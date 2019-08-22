#!/usr/bin/env bash

wexVersionArgs() {
  _DESCRIPTION='Returns current wex core version'
}

wexVersion() {
  echo ${WEX_CORE_VERSION}
}
