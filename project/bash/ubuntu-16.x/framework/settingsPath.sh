#!/usr/bin/env bash

frameworkSettingsPathArgs() {
 _ARGUMENTS=(
   [0]='framework_type t "Framework type" true'
 )
}

frameworkSettingsPath() {
  echo ${WEX_FRAMEWORKS_SETTINGS_PATHS[${FRAMEWORK_TYPE}]}
}
