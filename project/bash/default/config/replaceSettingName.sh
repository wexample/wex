#!/usr/bin/env bash

# Replace a variable name into a config file
# TODO Update to last syntax
bashConfigReplaceSettingName() {
  settingName=$1
  settingNewName=$2
  configFile=$3
  sed -i "s/\($settingName *= *\)/$settingNewName = /" ${configFile}
}
