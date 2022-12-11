#!/usr/bin/env bash

coreVersionArgs() {
  _DESCRIPTION='Returns current wex core version'
}

coreVersion() {
  echo ${WEX_CORE_VERSION}
}
